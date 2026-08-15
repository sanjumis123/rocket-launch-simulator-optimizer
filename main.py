from dictionary import nose_cones, materials, fin_shapes, snugness

from helper import get_number, rocket_optimizer

from simulation import simulate, plot_trajectory



def main():

    # plot the trajectory on a graph
    # monte carlo anaylsis
    # manufacturing tolerance analysis

    bd = get_number("Enter the barrel diameter (in inches): ")
    bd = bd * 0.0254  # Convert inches to meters

    bl = get_number("Enter the barrel length (in feet): ")
    bl = bl * 0.3048  # Convert feet to meters

    cd = get_number("Enter the chamber diameter (in inches): ")
    cd = cd * 0.0254  # Convert inches to meters

    cl = get_number("Enter the chamber length (in feet): ") 
    cl = cl * 0.3048  # Convert feet to meters

    psi = get_number("Enter the pressure (in psi): ")
    launch_angle = get_number("Enter the launch angle (in degrees): ")
    e = get_number("Enter the elevation (in feet): ")
    elevation = e * 0.3048  # Convert feet to meters
    temperature = get_number("Enter the temperature (in celcius): ")
    kelvin = temperature + 273.15  # Convert Celsius to Kelvin
    E = get_number("Enter the efficiency rate of the launcher (%): ")
    efficiency = E / 100

  



    while True:
        snug = input("How tight do you want the rocket seal to be (loose, snug, tight): ").lower()
    
        if snug in snugness:
            break
        else:
             print("Invalid input. Try again:", )

    choice = input("Do you want to choose your own rocket dimensions or not?: ").lower()
    

    if choice == "yes" or choice == "y":

        
        while True:
            rmaterial = input("Enter the rocket material (pool noodle, foam, cardboard, plastic): ").lower()
        
            if rmaterial in materials:
                    break
            else:
                    print("Invalid material. Try again:", )
        
        rd = get_number("Enter the rocket diameter (in inches): ")
        rd = rd * 0.0254  # Convert inches to meters

        
        if rd > bd:
            print("The rocket diameter cannot be larger than the barrel diameter.")
                  
        rl = get_number("Enter the rocket length (in inches): ")
        rl = rl * 0.0254  # Convert inches to meters

        if rl > bl:
            print("The rocket length cannot be larger than the barrel length.")

        rt = get_number("Enter the rocket thickness (in cm): ")
        rt = rt / 100  # Convert cm to meters

        if rt > rd * 25.4 / 2:
            print("The rocket thickness cannot be larger than the rocket radius.")

        boat_tail_length = get_number("Enter the boat tail length (in inches): ")
        boat_tail_length = boat_tail_length *  0.0254   # Convert inches to meters

        boat_tail_diameter = get_number("Enter the boat tail diameter (in inches): ")
        boat_tail_diameter = boat_tail_diameter * 0.0254  # Convert inches to meters

        if boat_tail_diameter > rd:
            print("The boat tail diameter cannot be larger than the rocket diameter.")
        

       
        while True:
            ns = input("Enter the nose cone shape (conical, ogive, elliptical, parabolic): ").lower()
        
            if ns in nose_cones:
                 break
            else:
                print("Invalid Shape. Try again:", )

        ncl = get_number("Enter the nose cone length (in cm): ")
        ncl = ncl / 100  # Convert cm to meters


        while True:
            fin = input("Enter the fin shape (trapezoidal, rectangular, elliptical, swept): ").lower()
                
            if fin in fin_shapes:
                break
            else:
                print("Invalid Shape. Try again:", )

        fn = get_number("Enter the number of fins: ")

        fh = get_number("Enter the fin height (in cm): ")
        fh = fh / 100  # Convert cm to meters

        fl = get_number("Enter the fin length/chord (in cm): ")
        fl = fl / 100  # Convert cm to meters

        ft = get_number("Enter the fin thickness (in cm): ")
        ft = ft / 100  # Convert cm to meters

        x_values, y_values, time_values, a_values, max_speed, stability_margin, rocket_mass, cost = simulate(
        rmaterial=rmaterial,
        ncl=ncl,
        rd=rd,
        rl=rl,
        ns=ns,
        fin=fin,
        fn=fn,
        fh=fh,
        fl=fl,
        ft=ft,
        elevation=elevation,
        kelvin=kelvin,
        psi=psi,
        bl=bl,
        bd=bd,
        cl=cl,
        cd=cd,
        launch_angle=launch_angle,
        rt=rt,
        efficiency=efficiency,
        snug=snug,
        boat_tail_diameter=boat_tail_diameter, 
        boat_tail_length=boat_tail_length
    )
        plot_trajectory(x_values, y_values, time_values, a_values)

    elif choice == "no" or choice == "n":

        while True:
            goal = input("What is your goal for the rocket? (range, height, speed, cheapest: ").lower()
                
            if goal == "range" or goal == "height" or goal == "speed" or goal == "cheapest":
                break
            else:
                print("Invalid goal. Try again:", )
        
    
    
        best_params, best_score, iteration = rocket_optimizer(elevation, kelvin, psi, bl, bd, cl, cd, efficiency, snug, goal, launch_angle)
    
    
        if best_params is None:
                print("No stable design was found in 1000 trials — try again.")
                return
    
            
        print("Best Parameters:", best_params)
        print("Best Score:", best_score)
        print("Found in iteration:", iteration)
    
        rd = best_params["rd"]
        rl = best_params["rl"]
        rt = best_params["rt"]
        boat_tail_length = best_params["boat_tail_length"]
        boat_tail_diameter = best_params["boat_tail_diameter"]
        ns = best_params["ns"]
        ncl = best_params["ncl"]
        fin = best_params["fin"]
        fn = best_params["fn"]
        fh = best_params["fh"]
        fl = best_params["fl"]
        ft = best_params["ft"]
        rmaterial = best_params["rmaterial"]


        x_values, y_values, time_values, a_values, max_speed, stability_margin, rocket_mass, cost= simulate(
                rmaterial=rmaterial,
                ncl=ncl,
                rd=rd,
                rl=rl,
                ns=ns,
                fin=fin,
                fn=fn,
                fh=fh,
                fl=fl,
                ft=ft,
                launch_angle=launch_angle,
                elevation=elevation,
                kelvin=kelvin,
                psi=psi,
                bl=bl,
                bd=bd,
                cl=cl,
                cd=cd,
                rt=rt,
                efficiency=efficiency,
                snug=snug,
                boat_tail_diameter=boat_tail_diameter, 
                boat_tail_length=boat_tail_length
            )
        plot_trajectory(x_values, y_values, time_values, a_values)

main()