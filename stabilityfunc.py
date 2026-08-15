from math import pi, sqrt, tan, radians

from dictionary import nose_cones, materials, fin_shapes


def stability(rmaterial, ncl, rd, rl, ns, fin, fn, fh, fl, ft, rt, boat_tail_diameter, boat_tail_length):

    r1 = rd/2
    r2 = boat_tail_diameter/2

    body_length = rl - ncl - boat_tail_length

    outer_volume = pi*(r1)**2*body_length

    inner_radius = r1 - rt

    inner_volume = pi*(inner_radius)**2*body_length

    body_volume = (outer_volume - inner_volume) 

    extra_mass = 0.015
    body_mass = body_volume * materials[rmaterial]["density"] + extra_mass

    outer_boat_tail_volume = (pi * boat_tail_length / 3) * (r1**2 + r1*r2 + r2**2) 
    
    r2_inner = r2 - rt
    inner_boat_tail_volume = (pi * boat_tail_length / 3) * (inner_radius**2 + inner_radius*r2_inner + r2_inner**2)

    boat_tail_volume = outer_boat_tail_volume - inner_boat_tail_volume
    
    boat_tail_mass = boat_tail_volume * materials[rmaterial]["density"]

        
    outer_nose_volume = nose_cones[ns]["volume"](r1, ncl)
    inner_nose_volume = nose_cones[ns]["volume"](inner_radius, ncl)

    material_nose_volume = outer_nose_volume - inner_nose_volume

    tip_mass = 0.003
    nose_mass = material_nose_volume * materials[rmaterial]["density"] + tip_mass


    tc = fin_shapes[fin]["taper_ratio"] * fl


    fin_area = fin_shapes[fin]["area"](fl, tc, fh)
    volume_fin = fin_area * ft
    fin_mass = volume_fin * materials[rmaterial]["density"] * fn
    fin_position_ratio = 0.8
    sweep_deg = fin_shapes[fin]["sweep_angle"]
    m = fh * tan(radians(sweep_deg))

    
    fin_start = rl * fin_position_ratio # fins are 80% down the body

    rocket_mass = body_mass + nose_mass + fin_mass + boat_tail_mass

    fin_cg_local = fin_shapes[fin]["cg"](fl, tc, m)
    boat_tail_cg_local = boat_tail_length / 4 * (r1**2 + 2*r1*r2 + 3*r2**2) / (r1**2 + r1*r2 + r2**2)

    fin_cg_location = fin_start + fin_cg_local
    nose_cg_location = nose_cones[ns]["cg"](ncl)
    body_cg_location = ncl + body_length/2
    boat_tail_cg_location = ncl + body_length + boat_tail_cg_local


    cg =  ((nose_cg_location * nose_mass) + (body_mass * body_cg_location) + (fin_mass * fin_cg_location) + (boat_tail_mass * boat_tail_cg_location) )/ rocket_mass

    CN = 2

    BN = ((2 * (r2**2 - r1**2)) / (r1**2))

    correction_factor = 1 + (rd/((2 * fh) + rd))

    l_m = sqrt(fh**2 + (m + tc/2 - fl/2)**2)
    FN = (4 * fn * (fh/r1)**2) / (1 + sqrt(1 + (2*l_m/(fl+tc))**2)) * correction_factor

    nose_cp = nose_cones[ns]["cp"](ncl)

    fin_cp = fin_start + fin_shapes[fin]["cp"](fl, tc, m)

    boat_tail_cp_location = (boat_tail_length / 3) * ( 1+ (1-r1/r2) / (1 - (r1/r2)**2))

    boat_tail_cp = ncl + body_length + boat_tail_cp_location

    cp = (nose_cp * CN + boat_tail_cp * BN + fin_cp * FN) / (CN + BN + FN)

    # body CP is not taken account for since its a cylinder with constant diameter, therefore BN = 0

    stability_margin = (cp - cg) / rd

    return stability_margin, cg, cp, rocket_mass, fin_area, CN, BN, FN, ns, nose_mass, nose_cg_location, body_mass, body_cg_location, fin_mass, fin_cg_location, body_length