import graph_helper as gh
import graph_sim as gs
import os
import sys
import time
import random
from typing import List, Tuple, Optional

def main() -> None:
    """Execute function for running Forest Fire Simulator, get user input, perform simulation and display report"""
    # Show start menu
    start_menu()
    configuration_done = False       # condition for breaking loop

    # get user input
    while not configuration_done:
        edges = get_edges()
        tree_rate = get_tree_rate()
        firefighters = get_firefighters()
        autocombustion_prob = get_autocombustion_prob()
        fire_spread_prob = get_fire_spread_prob()
        rock_respawn_prob = get_rock_respawn_prob()
        sim_limit = get_sim_limit()

        # Show config
        display_config(edges, tree_rate, firefighters, autocombustion_prob, fire_spread_prob, rock_respawn_prob, sim_limit)

        # Finalize configuration
        print("\nDo you want to run simulation with these configurations?\
              \n=> Select '1' to accept configuration and run simulation\
              \n=> Select '2' to reconfigure parameters\
              \n=> Select '3' to restart program\
              \n=> Select '4' to exit program")
        
        finalize_configuration = get_valid_input("Choice: ")

        if finalize_configuration == 1:
            print("\n Simulation configuration has been accepted")
            time.sleep(0.2)
            print("\n... Initializing simulation.")
            time.sleep(0.5)
            configuration_done = True
        elif finalize_configuration == 2:
            print("...Redirecting")
            time.sleep(0.2)
        elif finalize_configuration == 3:
            restart_program()
        elif finalize_configuration == 4:
            quit()
        else:
            print("Invalid choice.")
            print("...Redirecting")
            time.sleep(0.2)
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

def check_planar_graph(edges: List[Tuple]) -> bool:
    """Return true if edges represent a planar graph.

    Parameters
    ----------
    edges: List[Tuple]
        test utilizes the edges_planar method from the graph_helper module.
    """

    time.sleep(1)
    print(f"\n...Configuring internal test for verifying that edges represent a planar graph. Please wait.")
    time.sleep(0.6)
    print(f"...Finalizing parameter configuration for planar test")
    time.sleep(0.6)
    print(f"...Finalizing test")
    time.sleep(0.6)
    print(f"...Analyzing test data")
    time.sleep(1)
    print("\nTest result:")
    time.sleep(0.3)

    # Get test result
    if gh.edges_planar(edges):
        print("Your graph is a planar graph. Yahoo!")
        return True
    else:
        print("Your graph is not a planar graph.")
        print("Please try again with a new file of edges, or pseudo-randomly generating the edges for the graph.")
        print("\n...Redirecting to graph configuration menu.")
        return False

# Graph edge configuration
def get_edges() -> List[Tuple]:
    """Return a list of user-defined or pseudorandomly generated edges representing a planar graph"""

    graph_edges = None
    getting_param = True

    while getting_param:
        get_input_menu("edges", "graph")
        graph_type = get_valid_input("Choice: ")

        if graph_type == 1:
            print("Generating graph from input file.\
                  \nfile must adhere to the following criteria:\
                  \nEach non-empty line must represent an edge, identified by two integers separated by a comma")
            file_path = input("Enter the file path: ")
            file_name = input("Enter the file name: ") + ".dat"

            # Compile file information
            user_file_path = os.path.join(file_path, file_name)

            # Create edges from provided file
            graph_edges = create_graph_from_file(user_file_path)

            # Verify that the graph is a planar graph
            check_planar_graph(graph_edges)

            # Break loop
            getting_param = False
        elif graph_type == 2:
            print("Generating random graph.")
            
            vertices_num = None

            while vertices_num == None:
                print("Graph must have atleast 4 patches (vertices) of land, and a maximum of 500 patches of land.\
                      \nPlease enter the number of patches  you'd like in your forest (graph):")
                vertices_num = int(input("Number of patches: "))
                if vertices_num > 500:
                    print("Your desired number of vertices exceeds the limit. Please try again!")
                    time.sleep(0.4)
                    print("...Redirecting")
                    time.sleep(0.4)
                    vertices_num = None
                else:
                    graph_edges, graph_pos = gh.voronoi_to_edges(vertices_num)

            # Verify that the graph is a planar graph
            check_planar_graph(graph_edges)

            # Break loop
            getting_param = False
        elif graph_type == 3:
            config_info("edges")
        elif graph_type == 4: 
            quit()
        elif graph_type == 5:
            restart_program()
        else:
            print("Invalid choice.\
                  \n...Redirecting.")


# Terrain configuration
def get_valid_input(prompt: str, valid_input_msg: str = None) -> int:
    """This function checks to if the user input integer is valid. (To be used in input parameters)

    Parameters
    ----------
    prompt: str
        Prompt message for receiving user input. 
    valid_input_msg: Optional[str], default = None
        Will specify to the user, what input will be valid for where function is called
    """
    getting_int = False

    while not getting_int:
        try:
            user_input = input(prompt)
            user_input.isdigit()
            getting_int = True
        except ValueError:
            print("Invalid input. \
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")
        except TypeError:
            print("Invalid operation. \
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")
        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.\
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")

    return user_input

def get_valid_float_input(prompt: str, valid_input_msg: str = None) -> float:
    """This function checks if the user input float is valid. (To be used in input parameters)
    
    Parameters
    ----------
    prompt: str
        Prompt message for receiving user input. 
    valid_input_msg: Optional[str], default = None
        Will specify to the user, what input will be valid for where function is called
    """

    while not getting_float:
        try:
            user_input = round(float(input(prompt)), 1)
            user_input.isdigit()
            getting_float = True
        except ValueError:
            print("Invalid input. \
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")
        except TypeError:
            print("Invalid operation. \
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")
        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.\
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")

    return user_input

def get_valid_string_input(prompt: str, valid_input_msg: str = None) -> str:
    """This function checks if the user input string is valid.
    
    Parameters
    ----------
    prompt: str
        Prompt message for receiving user input. 
    valid_input_msg: Optional[str], default = None
        Will specify to the user, what input will be valid for where function is called
    """
    getting_str = False

    while not getting_str:
        try:
            user_input = input(prompt).strip()
            isinstance(user_input, str)
            getting_str = True
        except ValueError:
            print("Invalid input. \
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")
        except TypeError:
            print("Invalid operation. \
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")
        except KeyboardInterrupt:
            print("\nOperation interrupted by the user.\
                  \nTry again!")
            if valid_input_msg: print(f"Valid input is: {valid_input_msg}")

    
    return user_input

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
            autocombustion_prob = get_valid_float_input("Enter fire ignition probability (0.6-0.8): ", "floating point between 0-1")
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
            spread_prob = get_valid_float_input("Enter the fire spread probability (0.4-0.6): ", "floating point between 0-1")
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
            rock_mutate_prob = get_valid_float_input("Enter the rock mutate probability (0.3-0.5): ", "floating point between 0-1")
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
          \n==>Vertices/land patches<==\
          \n==>Tree to rock rate<==\
          \n==>Firefighters<==\
          \n==>Autocombustion probability<==\
          \n==>Fire spread probability<==\
          \n==>Rock Respawn Probability<==\
          \n==>Simulation limit<==")
    

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
    if config == "edges":
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
