import graph_helper as gh
import graph_sim as gs
import os
import sys
import random

def main() -> None:
    """Execute main program, get user input, perform simulation and display report"""
    # Show start menu
    # get user input
    edges = get_edges()
    tree_rate = get_tree_rate()
    firefighters = get_firefighters()
    autocombustion_prob = get_autocombustion_prob
    fire_spread_prob = get_fire_spread_prob()
    rock_respawn_prob = get_rock_respawn_prob()
    sim_limit = get_sim_limit()
    # Show config
    display_config()
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
def get_edges() -> List[(int, int)]:
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
    """Return the trees to rockpatches rate"""

    tree_rate = None

    assign_tree_percent = get_valid_input("Enter '1' for user-defined tree percentage or '2' for random assignment: ")

    if assign_tree_percent == 1:
        tree_rate = get_valid_input("Enter percentage of tree patches in the forest (1-99): ")
    else:
        tree_rate = random.randint(1, 99)

    return tree_rate

# Simulation parameter
def get_firefighters() -> int:
    """Return user-defined or randomly generated number of firefighters between 2-50"""

    firefighters = None

    assign_firefighters = get_valid_input("Enter '1' for user-defined number of firefighters or '2' for random assignment: ")

    if assign_firefighters == 1:
        firefighters = get_valid_input("Enter the number of firefighters in the forest (2-50): ")
    else:
        firefighters = random.randint(2, 50)
    
    return firefighters

# Set of probabilities
def get_autocombustion_prob() -> float:
    """Return user-defined or random probability for tree patch to randomly catch fire"""

    autocombustion_prob = None

    assign_fire_ignition_prob = get_valid_input("Enter '1' for user-defined fire ignition probability or '2' for random assignment: ")

    if assign_fire_ignition_prob == 1:
        autocombustion_prob = get_valid_float_input("Enter fire ignition probability (0.6-0.8): ")
    else:
        autocombustion_prob = round(random.uniform(0.6, 0.8), 1)
    
    return autocombustion_prob

def get_fire_spread_prob() -> float:
    """Return user-defined or random probability for fire to spread to adjacent non-ignited tree patches"""

    spread_prob = None

    assign_fire_spread_prob = get_valid_input("Enter '1' for user-defined fire spread probability or '2' for random assignment: ")

    if assign_fire_spread_prob == 1:
        spread_prob = get_valid_float_input("Enter the fire spread probability (0.4-0.6): ")
    else:
        spread_prob = round(random.uniform(0.4, 0.6), 1)
    
    return spread_prob

def get_rock_respawn_prob() -> float:
    """Return user-defined or random respawn probability for rockpatch to mutate to treepatch"""

    rock_mutate_prob = 0

    # get user input
    assign_respawn_prob = get_valid_input("Enter '1' for user-defined respawn probability (likelihood of a rock patch turning into a tree patch over time) or '2' for random assignment: ")

    if assign_respawn_prob == 1:
        rock_mutate_prob = get_valid_float_input("Enter the fire spread probability (0.3-0.5): ")
    else:
        rock_mutate_prob = round(random.uniform(0.3, 0.5), 1)
    
    return rock_mutate_prob

# Similation time limit
def get_sim_limit() -> int:
    """Return the user defined simulation limit for the simulation"""

    sim_time = None

    # get user input
    assign_sim_time_limit = get_valid_input("Enter '1' for user-defined simulation time limit or '2' for random assignment: ")
    if assign_sim_time_limit == 1:
        sim_time = get_valid_input("Enter a time limit, between 2 and 50 years, for the simulation: ")
    else:
        sim_time = round(random.randint(2, 50))
    
    return sim_time

def quit() -> None:
    """Exits the current program execution"""
    sys.exit()

# Printing Terrain configuration
def display_config() -> None:
    """Displays current simulation configuration to the user"""

    print(f"The ratio of trees to rocks is {user_tree_percent} : {user_rock_percent}.")
    print(f"You have employed {user_firefighters} number of firefighters.")
    print(f"The probability of fire ignition is {random_fire_ignition_prob}, the probability of fire spread is {fire_spread_prob}, and the probability of respawn is {random_respawn_prob}.")
    print(f"The time limit set for this simulation is {sim_time_limit} years.")
    print(graph_edges)

# Execute random forest fire simulation
if __name__ == "__main__":
    main()
