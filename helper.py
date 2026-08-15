from math import pi

import random

from dictionary import nose_cones, materials, fin_shapes


def cost_of_rocket(rmaterial, rocket_mass, ns, fin, bd, bl, cd, cl):

    connections_and_misc = 50
    rocket_cost = (materials[rmaterial]["cost_per_kg"] * rocket_mass) * nose_cones[ns]["complexity"] * fin_shapes[fin]["complexity"] 

    wall_thickness_ratio = 0.074 # I found myself by just meausring the pvp pipe I used
    cost_per_kg_of_pvc = 15.75
    r_outer = bd/2
    r_inner = (bd*wall_thickness_ratio)/2
    barrel_volume = pi * (r_outer**2 - r_inner**2) * bl
    barrel_mass = barrel_volume * 1400
    barrel_cost = barrel_mass *  cost_per_kg_of_pvc


    cr_outer = cd/2
    cr_inner = (cd*wall_thickness_ratio)/2
    chamber_volume = pi * (cr_outer**2 - cr_inner**2) * cl
    chamber_mass = chamber_volume * 1400
    chamber_cost = chamber_mass * cost_per_kg_of_pvc

    cost =  rocket_cost  + connections_and_misc +  chamber_cost +  barrel_cost

    return cost

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Enter a valid number")



def random_number(bd, bl):

    # dimesions are in meters

    rmaterial = random.choice(list(materials.keys()))
    rd = random.uniform(bd/4, bd)  # Rocket diameter between a quarter of the barrel diameter and full barrel diameter   
    rl = random.uniform(rd*5, rd*15)  # Rocket length between 5 and 15 times the rocket diameter
    rt = random.uniform(rd/6, rd/2.01)  # Rocket thickness between a sixth and almost half of the rocket diameter
    
    boat_tail_length = random.uniform(rl/6, rl/2)  # Boat tail length between a sixth and half the rocket length
    boat_tail_diameter = random.uniform(rd/6, rd)  # Boat tail diameter between a sixth and the rocket diameter

    ns = random.choice(list(nose_cones.keys()))  # Random nose cone shape
    ncl = random.uniform(rl/6, rl/2)  # Nose cone length between a sixth and half the rocket length

    fin = random.choice(list(fin_shapes.keys()))  # Random fin shape
    fn = random.randint(2, 4)  # Number of fins between 2 and 4
    fh = random.uniform(0.01, rl/2)  # Fin height between 1 cm and half the rocket length
    fl = random.uniform(0.01, rl/2)  # Fin length/chord between 1 cm and half the rocket length
    ft = random.uniform(0.001, rd/4)  # Fin thickness between 1 mm and half the rocket radius

    return rmaterial, rd, rl, rt, boat_tail_length, boat_tail_diameter, ns, ncl, fin, fn, fh, fl, ft

def rocket_optimizer(elevation, kelvin, psi, bl, bd, cl, cd, efficiency, snug, goal, launch_angle):

    from simulation import simulate
    best_params = None
    best_score = 0
    iteration = 0

    for i in range(1000):  # Run 1000 iterations of random rocket designs
        rmaterial, rd, rl, rt, boat_tail_length, boat_tail_diameter, ns, ncl, fin, fn, fh, fl, ft = random_number(bd, bl)

        x_values, y_values, time_values, a_values, max_speed, stability_margin, rocket_mass, cost = simulate(rmaterial, ncl, rd, rl, ns, fin, fn, fh, fl, ft,
     elevation, kelvin, psi, bl, bd, cl, cd, launch_angle, rt, efficiency, snug, boat_tail_diameter, boat_tail_length)

        if stability_margin < 1.0 or stability_margin > 2.0:
            continue  # Skip unstable designs

        if x_values is None or y_values is None:
            continue  # Skip if simulation failed

        if goal == "range":
            score = max(x_values)
        elif goal == "height":
            score = max(y_values)
        elif goal == "speed":
            score = max_speed
        elif goal == "cheapest":
            rocket_cost = (materials[rmaterial]["cost_per_kg"] * rocket_mass) * nose_cones[ns]["complexity"] * fin_shapes[fin]["complexity"]
            score = max_speed / rocket_cost  # Speed-to-cost ratio

        if score > best_score:
            best_score = score
            best_params = dict(rmaterial=rmaterial, rd=rd, rl=rl, rt=rt, boat_tail_length=boat_tail_length,
                                boat_tail_diameter=boat_tail_diameter, ns=ns, ncl=ncl,
                                fin=fin, fn=fn, fh=fh, fl=fl, ft=ft)
            iteration = i + 1

    return best_params, best_score, iteration
