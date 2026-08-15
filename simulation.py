from math import atan2, pi, sin, sqrt, cos, radians

from stabilityfunc import stability

from physics import exit_velocity, drag_force

from helper import cost_of_rocket

import matplotlib.pyplot as plt

from math import atan2, pi, sin, sqrt, cos, radians, degrees


def simulate(rmaterial, ncl, rd, rl, ns, fin, fn, fh, fl, ft,
             elevation, kelvin, psi, bl, bd, cl, cd, launch_angle, rt, efficiency, snug, boat_tail_diameter, boat_tail_length):

    # Calculate rocket stability and mass
    stability_margin, cg, cp, rocket_mass, fin_area, CN, BN, FN, ns, nose_mass, nose_cg_location, body_mass, body_cg_location, fin_mass, fin_cg_location, body_length = stability(
        rmaterial, ncl, rd, rl, ns, fin, fn, fh, fl, ft, rt, boat_tail_diameter, boat_tail_length
    )

    P = 101325 * (1 - (0.0000225577 * elevation)) ** 5.25588
    air_density = P / (287.05 * kelvin)
    mu = 1.716e-5 * (kelvin/273.15)**1.5 * (273.15 + 110.4) / (kelvin + 110.4)
    reference_area = pi * (rd / 2) ** 2

    # Calculate exit velocity
    velocity = exit_velocity(
        rocket_mass,
        psi,
        bl,
        bd,
        cl,
        cd,
        rd, 
        efficiency,
        air_density, 
        mu,
        rmaterial,
        snug
    )

    # Simulate flight
    x_values, y_values, time_values, max_speed, a_values = trajectory(rmaterial,
        rocket_mass,
        rd,
        rl,
        ns,
        fin,
        fn,
        velocity,
        launch_angle,
        elevation,
        kelvin,
        reference_area,
        fin_area,
        fl,
        ft,
        air_density, 
        mu,
        CN, 
        BN,
        FN,
        cg,
        cp,
        nose_mass,
        nose_cg_location, 
        body_mass, 
        body_cg_location, 
        fin_mass, 
        fin_cg_location,
        boat_tail_diameter,
        boat_tail_length,
        body_length, 
        ncl
    )
    

    fd, cd_total = drag_force(rmaterial, rd, ns, fin, fn, velocity, kelvin, reference_area, fin_area, fl, ft, air_density, mu, boat_tail_diameter, boat_tail_length, body_length, ncl) 

    cost = cost_of_rocket(rmaterial, rocket_mass, ns, fin, bd, bl, cd, cl)

    print(f"Max Range: {max(x_values)}")
    print(f"Max Height: {max(y_values)}")
    print(f"Time Elapsed: {max(time_values)}")
    print(f"Max Speed: {max_speed}")
    print(f"Exit Velocity: {velocity}")
    print(f"Stability Margin: {stability_margin}")
    print("Mass:",rocket_mass)
    print("CG:",cg)
    print("CP:",cp)
    print(f"Max Angle of Attack: {max(a_values)}")
    print(f"cd: {cd_total}") 
    print(f"Cost: {cost}")


    return x_values, y_values, time_values, a_values, max_speed, stability_margin, rocket_mass, cost

    

def trajectory(rmaterial, rocket_mass, rd, rl, ns, fin,fn,velocity,launch_angle,elevation,kelvin,reference_area,fin_area,fl,ft,
               air_density, mu,CN, BN,FN,cg,cp,nose_mass,nose_cg_location, body_mass, body_cg_location, fin_mass, 
               fin_cg_location,boat_tail_diameter,boat_tail_length, body_length, ncl):

    x = 0
    y = elevation 
    dt = 0.001  # time step in seconds
    time = 0
    ev = velocity  # exit velocity from the barrel

    vx = ev*cos(radians(launch_angle))
    vy = ev*sin(radians(launch_angle))

    theta = radians(launch_angle) # pitch angle of the body axis
    angular_velocity = 0.05 # small initial angular velocity to simulate minor perturbations in flight

    x_values = []
    y_values = []
    time_values = []
    max_speed = 0
    a_values = []

     # Initialize maximum speed with the exit velocity

    while y >= 0 and time < 60:  # simulate until the rocket hits the ground or 1 minute has passed

        

        velocity = sqrt(vx**2 + vy**2)
        fd, cd_total = drag_force(rmaterial, rd, ns, fin, fn, velocity, kelvin, reference_area, fin_area, fl, ft, air_density, mu, boat_tail_diameter, boat_tail_length, body_length, ncl) # maybe i dont have to call function and i can js call fd
        fda = fd / rocket_mass

        if velocity == 0 or velocity > ev * 1.001:
            break  # Avoid division by zero and overflow integer

        flight_path_angle = atan2(vy, vx)
        a = theta - flight_path_angle
        q = 0.5 * air_density * velocity**2 # dynamic pressure (kinetic energy of moving air)
        
        N = (CN + BN + FN) * q * reference_area * a
        
        NX = -N * sin(theta)
        NY = N * cos(theta)


        ax = -fda * (vx / velocity) - (NX/ rocket_mass) # have to convert it from force to acceleration
        ay = -fda * (vy / velocity) - 9.81 - (NY/ rocket_mass) # gravity acts downward

        vx += ax * dt
        vy += ay * dt

        C_damp = 0.5 # empirical scale factor for damping torque, can be adjusted based on experimental data

        damping_torque = -C_damp * angular_velocity * q * (fin_area * (fin_cg_location - cg)**2 + CN * reference_area 
                                                           * (nose_cg_location - cg)**2 + BN * reference_area * (body_cg_location - cg)**2)

        
        torque = -N * (cp - cg) + damping_torque

        I = (nose_mass * (nose_cg_location - cg) ** 2) + (body_mass * (body_cg_location - cg) ** 2) + (fin_mass * (fin_cg_location - cg) ** 2)

        angular_acceleration = torque / I

        angular_velocity += angular_acceleration * dt
        theta += angular_velocity * dt

        

        speed = sqrt(vx**2 + vy**2)
        if speed > max_speed:
            max_speed = speed

        x += vx * dt
        y += vy * dt

        time += dt

        x_values.append(x)
        y_values.append(y)
        time_values.append(time)
        a_values.append(a)

    return x_values, y_values, time_values, max_speed, a_values



def plot_trajectory(x_values, y_values, time_values, a_values):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Trajectory: range vs height
    ax1.plot(x_values, y_values)
    ax1.set_xlabel("Range (m)")
    ax1.set_ylabel("Height (m)")
    ax1.set_title("Rocket Trajectory")
    ax1.grid(True)

    # Angle of attack over time
    ax2.plot(time_values, [degrees(a) for a in a_values])
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Angle of Attack (degrees)")
    ax2.set_title("Angle of Attack vs Time")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()