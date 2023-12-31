"""
This module is the main executable and thus is the main module for the random forest simulator program. 
The program utilizes various modules to build a graph and simulate the evolution of wild fires. 

Requirements
------------
Python 3.7 or higher.

Notes
-----
This module is created as material for the phase 2 project for DM857, DS830 (2023). 
"""
import graph_helper as gh
import class_helper as ch
import file_helper as fh
import os
import sys
import time
import random
from sim_forest import ForestFireGraph
from typing import List, Tuple, Optional
from input_helper import get_valid_input, get_valid_float_input, get_valid_string_input, get_valid_file

def main() -> None:
    """Execute function for running Forest Fire Simulator, get user input, perform simulation and display report"""
    # Show start menu
    start_menu()
    program_running = True

    # run program
    while program_running:
        # get user input
        configuration_done = False
        while not configuration_done:
            edges, pos_nodes = get_edges()
            tree_rate = get_tree_rate()
            firefighters = get_firefighters()
            autocombustion_prob = get_autocombustion_prob()
            fire_spread_prob = get_fire_spread_prob()
            rock_mutate_prob = get_rock_mutate_prob()
            sim_limit = get_sim_limit()

            # Show config
            display_config(edges, tree_rate, firefighters, autocombustion_prob, 
                           fire_spread_prob, rock_mutate_prob, sim_limit)

            # Finalize configuration
            if finalize_configuration():
                configuration_done = True

                # Store current config
                configuration_storage.append(ch.ConfigData(edges, pos_nodes, tree_rate, firefighters, autocombustion_prob, 
                                                            fire_spread_prob, rock_mutate_prob, sim_limit))
        
        # Run simulation
        graph = ForestFireGraph(edges, pos_nodes, tree_rate, firefighters, autocombustion_prob, 
                                fire_spread_prob, rock_mutate_prob, sim_limit)
        graph.simulate()

        # Sim done
        print("...Simulation finished. Gathering final results")
        time.sleep(0.4)
        print("...Final results gathered.")

        # Display report
        time.sleep(0.3)
        print("\n============================================================="
              "\nYou have the following options:"
              "\n=> Select '1' to generate and display a report on the evolution of the wildfires"
              "\n=> Select '2' to exit the program")
        choice = get_valid_input("Choice: ", "Option 1 or 2.")

        if choice == 1:
            time.sleep(0.3)
            # Create instance of class
            my_instance = graph._graph_data
            # Call method using created instance
            my_instance.report_forest_evolution(steps=sim_limit)
        elif choice == 2:
            time.sleep(0.3)
            print("Sure, I spent a whole hour configuring the report only for you to be ungrateful and not view the report.")
            quit()
        else:
            print("Invalid choice"
                  "\n...Redirecting")

        # Ask to run simulation again
        time.sleep(0.3)
        print("\n=============================================================\
              \nYou have the following options:\
              \n=> Select '1' to rerun simulation with stored parameters\
              \n=> Select '2' to run simulation with different parameters\
              \n=> Select '3' to quit program (stored configuration is lost).")
        choice = get_valid_input("Choice: ", "Option 1, 2 or 3.")

        graph._vis_graph.close()    # close current sim window

        if choice == 1:
            time.sleep(0.3)
            display_config_storage()
            index = get_config_choice() - 1
            edges, pos_nodes, tree_rate, firefighters, autocombustion_prob, fire_spread_prob, rock_mutate_prob, sim_limit = configuration_storage[index].get_config()
            # Create graph
            graph = ForestFireGraph(edges, pos_nodes, tree_rate, firefighters, autocombustion_prob, fire_spread_prob, rock_mutate_prob, sim_limit)
            # Sim stored data
            time.sleep(0.3)
            graph.simulate()

            # display report
            graph._graph_data.report_forest_evolution(sim_limit)

            # Get next graph
            print("Configure new graph?")
            answer = False
            while not answer:
                answer_choice = get_valid_string_input("(y/n)", "Yes (y) to continue, no (n) to wait", True).lower()
                if answer_choice == "yes" or answer_choice == "y":
                    answer = True
                elif answer_choice == "no" or answer_choice == "n":
                    quit()
            graph._vis_graph.close()
        elif choice == 2:
            time.sleep(0.3)
            print("\n...Redirecting")
        elif choice == 3:
            quit()
        else:
            print("Invalid choice\
                  \n...Redirecting")
        
        time.sleep(0.4)
        print("\n...Redirecting to new graph configuration")
        time.sleep(0.4)

# Main program functions
def start_menu() -> None:
    """Print start menu (containing program info and required setup to user"""

    print("\
          \n======================================\
          \n=========Forest Fire Simulator========\
          \n======================================")
    
    print("\nThis is the Forest Fire Simulator program.\
          \nThis program uses a graph to simulate the evolution of a wildfire over patches of land.\
          \nEach patch of land is considered either a rock patch or a tree patch.\
          \nWhile simulating the evolution, a set number of firefighters will try to extinguish fires on tree patches.\
          \nThe tree patches have a (small) probability of catching fire (autcombustion) and, once lit, fire can propagate\
          \nto neighbouring tree patches. A tree patch that is devoured by the fire will turn into a rock patch.\
          \nThe rock patches will not propagate fire, however, over time, they have a small probability of turning into a tree patch.")
    
    print("\nThe simulation needs the following parameters for the configuration\
          \n and can be defined by the user or randomly generated:\
          \n==> Vertices/land patches\
          \n==> Tree to rock rate\
          \n==> Firefighters\
          \n==> Autocombustion probability\
          \n==> Fire spread probability\
          \n==> Rock Respawn Probability\
          \n==> Simulation limit")
# Graph edge configuration
def get_edges() -> List[Tuple]:
    """Return a list of user-defined or pseudorandomly generated edges representing a planar graph"""

    graph_edges = None
    graph_pos = {}
    getting_param = True

    while getting_param:
        get_input_menu("landpatches", "graph")
        graph_type = get_valid_input("Choice: ", max=6)

        if graph_type == 1:
            time.sleep(0.3)
            print("\n=============================================================")
            time.sleep(0.3)
            print(f"Generating graph from input file.\
                  \nfile must adhere to the following criteria:\
                  \nFile must contain edges which have a planar representation for simulation purposes.\
                  \nEach non-empty line must represent an edge, identified by two integers separated by a comma\
                  \nFilepath example: /Users/JohnDoe/examplePath/filename.dat ")
            
            # Get valid file
            validating_file = True
            while validating_file:
                file_path = get_valid_file("Enter the file path: ", "Each non-empty line must represent an edge,\
                                           identified by two integers separated by a comma")

                # Create edges from provided file
                graph_edges = fh.create_graph_from_file(file_path)

                # Verify that the graph is a planar graph
                if fh.check_planar_graph(graph_edges):
                    validating_file = False
                else:
                    # Redirecting to file input
                    pass

            # Break loop
            getting_param = False
        elif graph_type == 2:
            time.sleep(0.3)
            print("\n=============================================================\
                  \nGenerating random graph.")
            time.sleep(0.3)
            vertices_num = None

            while vertices_num == None:
                print("Graph must have atleast 4 patches (vertices) of land, and a maximum of 500 patches of land.\
                      \nPlease enter the number of patches  you'd like in your forest (graph):")
                vertices_num = get_valid_input("Number of patches: ", "atleast 4, maximum is 500", 4, 500)

                graph_edges, graph_pos = gh.voronoi_to_edges(vertices_num)

            # Verify that the graph is a planar graph
            fh.check_planar_graph(graph_edges)

            # Break loop
            getting_param = False
        elif graph_type == 3:
            config_info("landpatches")
        elif graph_type == 4: 
            quit()
        elif graph_type == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")

    return graph_edges, graph_pos

# Terrain configuration


# Terrain configuration input parameters
def get_tree_rate() -> int:
    """Return the trees to rockpatches rate (1-99), from either user-specified input or randomly generated."""

    tree_rate = None
    getting_param = True

    while getting_param:
        get_input_menu("tree_rate", "terrain")
        assign_tree_percent = get_valid_input("Choice: ")

        if assign_tree_percent == 1:
            tree_rate = get_valid_input("Enter percentage of tree patches in the forest (1-99): ", "an integer between 1-99", 1, 99)
            getting_param = False
        elif assign_tree_percent == 2:
            tree_rate = random.randint(1, 99)
            getting_param = False
        elif assign_tree_percent == 3:
            config_info("tree rate")
        elif assign_tree_percent == 4: 
            quit()
        elif assign_tree_percent == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")

    return tree_rate

# Simulation parameter
def get_firefighters() -> int:
    """Return user-defined or randomly generated number of firefighters between 2-15"""

    firefighters = None
    getting_param = True

    while getting_param:
        get_input_menu("firefighters", "simulation parameter")
        assign_firefighters = get_valid_input("Choice: ")

        if assign_firefighters == 1:
            firefighters = get_valid_input("Enter the number of firefighters in the forest (2-15): ", "least 2 and at most 15 firefighters", 2, 15)
            getting_param = False # break loop
        elif assign_firefighters == 2:
            firefighters = random.randint(2, 15)
            getting_param = False # break loop
        elif assign_firefighters == 3:
            config_info("firefighters")
        elif assign_firefighters == 4: 
            quit()
        elif assign_firefighters == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")
    
    return firefighters

# Set of probabilities
def get_autocombustion_prob() -> int:
    """Return user-defined or random probability for tree patch to randomly catch fire"""

    autocombustion_prob = None
    getting_param = True

    while getting_param:
        get_input_menu("autocombustion", "probability")
        assign_fire_ignition_prob = get_valid_input("Choice: ")

        if assign_fire_ignition_prob == 1:
            autocombustion_prob = get_valid_input("Enter fire ignition probability (1-10): ", 
                                                        "Integer between 1-10", 1, 10)
            getting_param = False # break loop
        elif assign_fire_ignition_prob == 2:
            autocombustion_prob = random.randint(1, 10)
            getting_param = False # break loop
        elif assign_fire_ignition_prob == 3:
            config_info("autocombustion probability")
        elif assign_fire_ignition_prob == 4: 
            quit()
        elif assign_fire_ignition_prob == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")
    
    return autocombustion_prob

def get_fire_spread_prob() -> int:
    """Return user-defined or random probability for fire to spread to adjacent non-ignited tree patches"""

    spread_prob = None
    getting_param = True

    while getting_param:
        get_input_menu("fire spread", "probability")
        assign_fire_spread_prob = get_valid_input("Choice: ")

        if assign_fire_spread_prob == 1:
            spread_prob = get_valid_input("Enter fire spread probability (30-60): ", 
                                                        "Integer between 30-60", 30, 60)
            getting_param = False # break loop
        elif assign_fire_spread_prob == 2:
            spread_prob = random.randint(30, 60)
            getting_param = False # break loop
        elif assign_fire_spread_prob == 3:
            config_info("fire spread probability")
        elif assign_fire_spread_prob == 4: 
            quit()
        elif assign_fire_spread_prob == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")

    return spread_prob

def get_rock_mutate_prob() -> int:
    """Return user-defined or random respawn probability for rockpatch to mutate to treepatch"""

    rock_mutate_prob = 0
    getting_param = True

    while getting_param:
        get_input_menu("rockpatch mutation", "probability")
        assign_respawn_prob = get_valid_input("Choice: ")

        if assign_respawn_prob == 1:
            rock_mutate_prob = get_valid_input("Enter rock mutate probability (1-10): ", 
                                                        "Integer between 1-10", 1, 10)
            getting_param = False # break loop
        elif assign_respawn_prob == 2:
            rock_mutate_prob = random.randint(1, 10)
            getting_param = False # break loop
        elif assign_respawn_prob == 3:
            config_info("rock respawn probability")
        elif assign_respawn_prob == 4: 
            quit()
        elif assign_respawn_prob == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")
    
    return rock_mutate_prob

# Similation time limit
def get_sim_limit() -> int:
    """Return the user defined simulation limit for the simulation"""

    sim_time = None
    getting_param = True

    while getting_param:
        get_input_menu("simulation limit", "configuration")
        assign_sim_time_limit = get_valid_input("Choice: ")

        if assign_sim_time_limit == 1:
            sim_time = get_valid_input("Enter a time limit, between 2 and 50 years, for the simulation: ", "2-50", 2, 50)
            getting_param = False # break loop
        elif assign_sim_time_limit == 2:
            sim_time = round(random.randint(2, 50))
            getting_param = False # break loop
        elif assign_sim_time_limit == 3:
            config_info("simulation limit")
        elif assign_sim_time_limit == 4: 
            quit()
        elif assign_sim_time_limit == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")
    
    return sim_time

def get_input_menu(input: str, config_type: str) -> print:
    """Print the menu options for input configuration.

    Parameters
    ----------
    input: str
        Name of input for graph configuration
    config_type: str
        Type of configuration argument, eg. graph, terrain, probability, simulation. 
    """
    time.sleep(1)
    print(f"\n...Opening {input} configuraton menu")
    time.sleep(1)

    print(f"\n=============================================================\
          \nConfiguring the {input} {config_type} parameter.\
          \nYou have the following options:\
          \n=> Enter '1' for user-defined {input}\
          \n=> Enter '2' for random assignment\
          \n=> Enter '3' for info regarding the {input} configuration parameter\
          \n=> Enter '4' to exit program\
          \n=> Enter '5' to restart program")

def quit() -> None:
    """Exits the current program execution"""
    print("\n...Exiting program. Have a great day!")
    sys.exit()

def restart_program() -> None:
    """Exits current program execution and returns to main menu"""
    print("\n...Restarting program." )
    python = sys.executable
    os.execl(python, python, *sys.argv)

def config_info(config: str) -> None:
    """Display configuration information to user

    Parameters
    ----------
    config: str
        configuration parameter, the user is requesting info on: tree rate, firefighters, autocombustion probability, 
        fire spread probability, rock respawn probability & simulation limit.
    """

    time.sleep(1)
    print(f"\n...Opening {config} information.")
    time.sleep(1)

    print('\n=============================================================')
    # Display configuration information to user
    if config == "landpatches":
        print(f"Info for configuring land patches:\
              \n# This parameter sets the configuration for the number of landpatches and how they are connected on the graph. \
              \n# This parameter can be set either by the user or by randomly generating a percentage.\
              \n# If you choose option 1 and generate the vertices from a file, the file must adhere to:\
              \n# Each non-empty line represents an edge, identified by two integers separated by a comma.\
              \n# The edges from the file must configure a graph, that can have a planar representation.\
              \n# If you choose option 2, the graph will be pseudo-randomly generated and have a planar representation")
    elif config == "tree rate":
        print(f"Info for configuring tree rate:\
              \n# This parameter sets the configuration for the ratio of tree patches to rock patches in the graph. \
              \n# This parameter can be set either by the user or by randomly generating a percentage.\
              \n# If you wish to specify the rate, Please enter an integer value beteween 1-99.")
    elif config == "firefighters":
        print(f"Info for configuring firefighters:\
              \n# This parameter sets the configuration for the number of firefighters used in simulating the graph.\
              \n# This parameter can be set either by the user or by randomly generating a number of firefighters.\
              \n# If you wish to specify the number, please enter an integer value beteween 2-and num of patches.")
    elif config == "autocombustion probability":
        print(f"Info for configuring autocombustion probability on tree patches:\
              \n# This parameter sets the probability for tree patches to autocombust (min 1%, max 10%).\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter an integer number between 1-10 (1-10%).")
    elif config == "fire spread probability":
        print(f"Info for configuring fire spread probability:\
              \n# This parameter sets the probability that fire spreads from ignited tree patches.\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter  an integer number between 30-60 (30-60%)")
    elif config == "rock respawn probability":
        print(f"Info for configuring forest on rockpatches repawn probability:\
              \n# This parameter sets the probability that a treepatch grows on a rockpatch.\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter  an integer number between 1-10 (1-10%)")
    elif config == "simulation limit":
        print(f"Info for configuring simulation limit:\
              \n# This parameter sets the limit for the simulation.\
              \n# This determines for how many evolution steps, the simulation will run.\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter an integer between 2-50.")

    # redirect to called configuration
    time.sleep(2)
    print(f"\n...Redirecting to {config} configuration.")
    time.sleep(2)

# Printing Terrain configuration
def display_config(edges: List[Tuple], tree_rate: int, firefighters: int, 
                   autocombustion_prob: float, fire_spread_prob: float, rock_mutate_prob: float, sim_limit: int) -> None:
    """Displays current simulation configuration to the user"""

    time.sleep(1)
    print(f"...Completing calculations.")
    time.sleep(0.5)
    print(f"...Finalizing configuration.")
    time.sleep(0.5)

    print("Your current configuration for the simulation:")
    print(f"The ratio of trees to rocks is {tree_rate} : {100 - tree_rate}.")
    print(f"You have employed {firefighters} firefighters.")
    print(f"The probability of fire ignition is {autocombustion_prob}, the probability of fire spread is {fire_spread_prob}, and the probability of tree patch respawn is {rock_mutate_prob}.")
    print(f"The time limit set for this simulation is {sim_limit} years.")

def finalize_configuration() -> bool:
    """Return true if final configuration parameters are accepted, false otherwise"""

    # Menu
    print("\nDo you want to run simulation with these configurations?\
              \n=> Select '1' to accept configuration and run simulation\
              \n=> Select '2' to reconfigure parameters\
              \n=> Select '3' to restart program\
              \n=> Select '4' to exit program")
    
    # Get choice
    choice = get_valid_input("Choice: ")

    if choice == 1:
        print("\n Simulation configuration has been accepted")
        time.sleep(0.2)
        print("\n... Initializing simulation.")
        time.sleep(0.5)
        return True
    elif choice == 2:
        print("...Redirecting")
        time.sleep(0.2)
    elif choice == 3:
        restart_program()
    elif choice == 4:
        quit()
    else:
        print("Invalid choice.")
        print("...Redirecting")
        time.sleep(0.2)
    
    return False

configuration_storage = []

def display_config_storage() -> None:
    """Display previous configurations from storage"""

    time.sleep(0.5)
    print("...Retrieving previous configurations")
    time.sleep(0.5)
    print("\n=============================================================\
          \nCurrent configurations in storage:")

    # Iterate over configuration storage
    for index, config in enumerate(configuration_storage):
        print(f"\nGraph: {index + 1}")
        print(config)
        time.sleep(0.2)

def get_config_choice() -> int:
    """Return user-specified choice of configuration from configuration storage"""
    
    print("\n=============================================================\
          \nCurrent configurations in storage:")
    print("You have the following options for configuration:")
    
    # Display list of choices
    for index, config in enumerate(configuration_storage):
        print(f"==> Graph: {index + 1}")

    # Get user choice
    config_choice = get_valid_input("Choice: ", f"Numbers: 1-{len(configuration_storage)}.", 1, len(configuration_storage))

    return config_choice

# Execute random forest fire simulation
if __name__ == "__main__":
    main()
