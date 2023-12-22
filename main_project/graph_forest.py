import graph_helper as gh
import graph_sim as gs
import os
import sys
import time
import random
from typing import List, Tuple

def main() -> None:
    """Execute main program, get user input, perform simulation and display report"""
    # Show start menu
    # get user input
    edges = get_edges()
    tree_rate = get_tree_rate()
    firefighters = get_firefighters()
    autocombustion_prob = get_autocombustion_prob()
    fire_spread_prob = get_fire_spread_prob()
    rock_respawn_prob = get_rock_respawn_prob()
    sim_limit = get_sim_limit()
    # Show config
    display_config(edges, tree_rate, firefighters, autocombustion_prob, fire_spread_prob, rock_respawn_prob, sim_limit)
    # Ask if config needs updated
    # Run simulation
    # Display report
    # Could ask if user wants to go again or exit? 
    pass

def user_file(fp, fn):
    """This function opens a file using a given file path (fp) and file name (fn), and reads its contents."""

    try:
        with open(os.path.join(fp, fn), 'r') as file:
            file_content = file.read()
            return file_content

    except FileNotFoundError as e:
        return e
    except IOError as e:
        return e

def add_edges_from_lines(lines: str) -> list[tuple]:
    """Read lines, check if line represent an edge of a graph. Return list of edges"""

    # Store edges in a list
    edges_list = []

    # Iterate through the lines and add edges to the graph
    for line in lines:
        # Ignore lines starting with #
        if line.startswith('#'):
            continue

        # Split the line by comma
        nodes = line.split(',')

        # Remove '()' from nodes
        for i in range(len(nodes)):
            nodes[i] = nodes[i].replace('(', '')
            nodes[i] = nodes[i].replace(')', '')

        # Check if both values are valid integers
        if len(nodes) == 2 and nodes[0].strip().isdigit() and nodes[1].strip().isdigit():
            # Convert nodes to integers and add the edge to the graph
            i, j = map(int, nodes)
            # Add the edge as a tuple to the edges_list
            edges_list.append((i, j))
        else:
            print("Invalid input.")

    return edges_list

def create_graph_from_file(filename: str) -> list[tuple]:
    """Reads a file, checks if it's valid, and returns a list of edges for a graph"""

    try:
        with open(filename, 'r') as file:
            # Read lines from the file and remove whitespaces
            lines = [line.strip() for line in file.readlines() if line.strip()]

    except FileNotFoundError as e:
        print("The file could not be found.")
        return []  # Return an empty list

    except IOError as e:
        print("There was an error reading from the file:", str(e))
        return []  # Return an empty list

    # add edges from file to edges_list
    try:
        graph_edges = add_edges_from_lines(lines)
    except UnboundLocalError as e:
        print(e)
        return []

    return graph_edges

# Load the functions
def get_edges() -> List[Tuple]:
    """Return user-defined or pseudorandom edgelist"""
    graph_type = int(input("Enter '1' to load your own graph or '2' to generate a pseudo-random graph: "))

    if graph_type == 1:
        file_path = input("Enter the file path: ")
        file_name = input("Enter the file name: ") + ".dat"

        # Compile file information
        user_file_path = os.path.join(file_path, file_name)

        user_graph = user_file(file_path, file_name)
        graph_edges = create_graph_from_file(user_file_path)

        # Verify that the graph is a planar graph
        if gh.edges_planar(graph_edges):
            print("Your graph is a planar graph. Yahoo!")
        else:
            print("Your graph is not a planar graph.")

    elif graph_type == 2:
        n_random_graph = int(input("Enter the number of patches (vertices) you'd like in your forest (graph): "))
        if n_random_graph > 500:
            print("Your desired number of vertices exceeds the limit.")
        else:
            graph_edges, graph_pos = gh.voronoi_to_edges(n_random_graph)

            # Verify that the graph is a planar graph
            if gh.edges_planar(graph_edges):
                print("Your graph is a planar graph. Yahoo!")
            else:
                print("Your graph is not a planar graph.")
    else:
        print("Invalid choice. Please enter '1' or '2'.")

# Terrain configuration
def get_valid_input(prompt):
    """This function checks to if the user input integer is valid. (To be used in input parameters)"""
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_valid_float_input(prompt):
    """This function checks if the user input float is valid. (To be used in input parameters)"""
    while True:
        try:
            user_input = round(float(input(prompt)), 1)
            return user_input
        except ValueError:
            print("Invalid input. Please enter a valid decimal number.")

# Terrain configuration input parameters
def get_tree_rate() -> int:
    """Return the trees to rockpatches rate (1-99), from either user-specified input or randomly generated."""

    tree_rate = None
    getting_param = True

    while getting_param:
        get_input_menu("tree_rate", "terrain")
        assign_tree_percent = get_valid_input("Choice: ")

        if assign_tree_percent == 1:
            tree_rate = get_valid_input("Enter percentage of tree patches in the forest (1-99): ")
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
    """Return user-defined or randomly generated number of firefighters between 2-50"""

    firefighters = None
    getting_param = True

    while getting_param:
        get_input_menu("firefighters", "simulation parameter")
        assign_firefighters = get_valid_input("Choice: ")

        if assign_firefighters == 1:
            firefighters = get_valid_input("Enter the number of firefighters in the forest (2-50): ")
            getting_param = False # break loop
        elif assign_firefighters == 2:
            firefighters = random.randint(2, 50)
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
def get_autocombustion_prob() -> float:
    """Return user-defined or random probability for tree patch to randomly catch fire"""

    autocombustion_prob = None
    getting_param = True

    while getting_param:
        get_input_menu("autocombustion", "probability")
        assign_fire_ignition_prob = get_valid_input("Choice: ")

        if assign_fire_ignition_prob == 1:
            autocombustion_prob = get_valid_float_input("Enter fire ignition probability (0.6-0.8): ")
            getting_param = False # break loop
        elif assign_fire_ignition_prob == 2:
            autocombustion_prob = round(random.uniform(0.6, 0.8), 1)
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

def get_fire_spread_prob() -> float:
    """Return user-defined or random probability for fire to spread to adjacent non-ignited tree patches"""

    spread_prob = None
    getting_param = True

    while getting_param:
        get_input_menu("fire spread", "probability")
        assign_fire_spread_prob = get_valid_input("Choice: ")

        if assign_fire_spread_prob == 1:
            spread_prob = get_valid_float_input("Enter the fire spread probability (0.4-0.6): ")
            getting_param = False # break loop
        elif assign_fire_spread_prob == 2:
            spread_prob = round(random.uniform(0.4, 0.6), 1)
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

def get_rock_respawn_prob() -> float:
    """Return user-defined or random respawn probability for rockpatch to mutate to treepatch"""

    rock_mutate_prob = 0
    getting_param = True

    while getting_param:
        get_input_menu("rockpatch mutation", "probability")
        assign_respawn_prob = get_valid_input("Choice: ")

        if assign_respawn_prob == 1:
            rock_mutate_prob = get_valid_float_input("Enter the rock mutate probability (0.3-0.5): ")
            getting_param = False # break loop
        elif assign_respawn_prob == 2:
            rock_mutate_prob = round(random.uniform(0.3, 0.5), 1)
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
            sim_time = get_valid_input("Enter a time limit, between 2 and 50 years, for the simulation: ")
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

def quit() -> None:
    """Exits the current program execution"""
    print("\n...Exiting program. Have a great day!")
    sys.exit()

def restart_program() -> None:
    """Exits current program execution and returns to main menu"""
    print("\n...Restarting program." )
    python = sys.executable
    os.execl(python, python, *sys.argv)

def start_menu() -> None:
    """Present start menu (containing program info and required setup to user"""

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
          \nConfiguring {input} {config_type} parameter.\
          \nYou have the following options:\
          \n=> Enter '1' for user-defined {input}\
          \n=> Enter '2' for random assignment\
          \n=> Enter '3' for info regarding the {input} configuration parameter\
          \n=> Enter '4' to exit program\
          \n=> Enter '5' to restart program")

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
    if config == "tree rate":
        print(f"Info for configuring tree rate:\
              \n# This parameter sets the configuration for the ratio of tree patches to rock patches in the graph. \
              \n# This parameter can be set either by the user or by randomly generating a percentage.\
              \n# If you wish to specify the rate, Please enter an integer value beteween 1-99.")
    elif config == "firefighters":
        print(f"Info for configuring firefighters:\
              \n# This parameter sets the configuration for the number of firefighters used in simulating the graph.\
              \n# This parameter can be set either by the user or by randomly generating a number of firefighters.\
              \n# If you wish to specify the number, please enter an integer value beteween 2-50.")
    elif config == "autocombustion probability":
        print(f"Info for configuring autocombustion probability on tree patches:\
              \n# This parameter sets the probability for tree patches to autocombust (min 60%, max 80%).\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter a floating point number between 0.6-0.8.")
    elif config == "fire spread probability":
        print(f"Info for configuring fire spread probability:\
              \n# This parameter sets the probability that fire spreads from ignited tree patches.\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter a floating point number between 0-1.")
    elif config == "rock respawn probability":
        print(f"Info for configuring forest on rockpatches repawn probability:\
              \n# This parameter sets the probability that a treepatch grows on a rockpatch.\
              \n# This parameter can be set either by the user or by randomly generating the probability.\
              \n# If you wish to specify the number, please enter a floating point number between 0-1.")
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
                   autocombustion_prob: float, fire_spread_prob: float, rock_respawn_prob: float, sim_limit: int) -> None:
    """Displays current simulation configuration to the user"""

    time.sleep(1)
    print(f"...Completing calculations.")
    time.sleep(0.5)
    print(f"...Finalizing configuration.")
    time.sleep(0.5)

    print("Your current configuration for the simulation:")
    print(f"The ratio of trees to rocks is {tree_rate} : {100 - tree_rate}.")
    print(f"You have employed {firefighters} firefighters.")
    print(f"The probability of fire ignition is {autocombustion_prob}, the probability of fire spread is {fire_spread_prob}, and the probability of tree patch respawn is {rock_respawn_prob}.")
    print(f"The time limit set for this simulation is {sim_limit} years.")

# Execute random forest fire simulation
if __name__ == "__main__":
    main()
