from math import pi, sqrt, log10

from dictionary import nose_cones, materials, fin_shapes, snugness, snugness_airleakage

def drag_force(rmaterial, rd, ns, fin, fn, velocity, kelvin, reference_area, fin_area, fl, ft, air_density, mu, boat_tail_diameter, boat_tail_length, body_length, ncl):

    velocity = max(velocity, 0.01) # avoids dividing by zero


    # Reynolds number for different components of the rocket

    Re_body = (air_density * velocity * body_length) / mu
    Re_fin  = (air_density * velocity * fl) / mu
    Re_nose = (air_density * velocity * ncl) / mu
    Re_boat_tail = (air_density * velocity * boat_tail_length) / mu


     # Skin friction

    Cf_fin = 0.455 / log10(Re_fin)**2.58
    Cf_body = 0.455 / log10(Re_body)**2.58
    Cf_nose = 0.455 / log10(Re_nose)**2.58  
    Cf_boat_tail = 0.455 / log10(Re_boat_tail)**2.58 


# Nose
    body_surface_area_nose = pi * (rd/2) * sqrt(ncl**2 + (rd/2)**2) # surface area of the nose cone exluding the base area
    cd_nose = (Cf_nose * (body_surface_area_nose / reference_area) + nose_cones[ns]["nose_drag"]) * materials[rmaterial]["surface_multiplier"]


# Body

    body_surface_area = pi * rd * body_length

    body_pressure = 0.125 # empircal value

    body_friction = Cf_body * (body_surface_area / reference_area)

    cd_body = (body_pressure + body_friction) * materials[rmaterial]["surface_multiplier"]

# Boat Tail?

    slant_height = sqrt(boat_tail_length**2 + (rd/2 - boat_tail_diameter/2)**2)
    boat_tail_surface_area = pi * (rd/2 + boat_tail_diameter/2) * slant_height

    cd_boat_tail = (Cf_boat_tail * (boat_tail_surface_area / reference_area))* materials[rmaterial]["surface_multiplier"]

# Fins

    # include other factors that affect the drag of the fin

    interference_drag = 0.3 # # empirical estimate, fin-body junction drag; not derived from a specific source

    base_fin_drag = Cf_fin * (1 + 2*(ft/fl) + 60*(ft/fl)**4) # models the affects the fin thickness has on the drag

    cd_fin_single = (base_fin_drag * fin_shapes[fin]["drag_factor"] * (1 + interference_drag) * materials[rmaterial]["surface_multiplier"])

    cd_fins = (cd_fin_single* (fin_area/reference_area)) * fn


# Total
    a = 331.4 + 0.606 * (kelvin - 273.15) # speed of sound in m/s

    mach = velocity / a

    diameter_ratio = boat_tail_diameter / rd

    boundary_value = 0.18 + 0.12*0.8 
    peak_value = boundary_value + 0.30*(1.2-0.8)**2 

    if mach < 0.8:
        cd_base_flat = 0.18 + 0.12*mach
    elif mach < 1.2:
    # anchor at mach=0.8 using the subsonic value there, then rise to a peak
        cd_base_flat = boundary_value + 0.30*(mach - 0.8)**2
    else:
        cd_base_flat = peak_value - 0.1*(mach - 1.2)  # now decreasing, matching real supersonic behavior

    # models how base drag changes with mach number and the ratio of the boat tail diameter to the body diameter

    cd_base = cd_base_flat * diameter_ratio

    cd_total = cd_nose + cd_body + cd_fins + cd_boat_tail + cd_base

    fd = 0.5 * air_density * velocity**2 * cd_total * reference_area

    return fd, cd_total


def exit_velocity(rocket_mass, psi, bl, bd, cl, cd, rd, efficiency, air_density, mu, rmaterial, snug):

    # Initial conditions
    x = 0
    velocity = 0
    
    time = 0
    dt = 0.0001

    # Convert PSI to Pascals
    pressure_initial = psi * 6894.76 + 101325

    # Volumes
    chamber_volume = pi * (cd/2)**2 * cl

    # Areas
    rocket_area = pi * (rd/2)**2
    barrel_area = pi * (bd/2)**2

    # Before rocket moves

    initial_volume = chamber_volume

    air_gap_volume = barrel_area * (0.8 * bl)

    expanded_volume = initial_volume + air_gap_volume

    pressure_after_valve = pressure_initial * (initial_volume / expanded_volume)**1.4


# Rocket movement

    while x < 0.2*bl and time < 10:  


        velocity = max(velocity, 0.01) # avoids dividing by zero

        Re_barrel = (air_density * velocity * bd) / mu

        f = 0.184 * (Re_barrel**-0.2)

        P_friction = f * (((0.8 * bl) + x) / bd) * (0.5 * air_density * velocity**2) 
        # friction between the air and the barrel

        base_seal_friction = snugness[snug] 
        seal_friction = base_seal_friction * materials[rmaterial]["surface_multiplier"]

        current_volume = expanded_volume + barrel_area*x

        pressure = ((pressure_after_valve * (expanded_volume/current_volume)**1.4) * snugness_airleakage[snug]) - P_friction

        force = (((pressure - 101325) * rocket_area) * efficiency) - seal_friction

        acceleration = force / rocket_mass

        velocity += acceleration * dt
        velocity = max(velocity, 0)
        x += velocity * dt

        time += dt

    if x < 0.2*bl:
        print("Rocket did not clear the barrel — seal friction may be too high.")
        return 

    return velocity
   
  
