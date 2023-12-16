"""
This module provides Graph, a class for creating a graph of edges and sites forming a graph

Requirements
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Python 3.7 or higher.

Notes
-----
Module is created as part of the group project for the final exam of DS830 Introduction to programming.
"""

# Import dependencies
import visualiser_rndgraph as vrg
import matplotlib.pyplot as plt
from typing import List, Optional, Dict
import random as random
import math as math
from time import sleep


class Graph():
    """Each instance of this class creates a Graph with edges, vertices and a coloring pattern. """

    def __init__(
        self,
        edges: list,
        color_pattern: int) -> None:

        """
        Parameters
        ----------
        edges: List[(int,int)]
            List containing the edges (Tuples of 2 vertices) forming the 2D surface for the graph.
        color_pattern:
            Color of the vertices
        vertices_dict: Optional[dict], default = {}
            dictionary with vertices as key and values for each vertex: color, frustration, neighbours
        total_frustration: Optional[float], default = 0
            The graphs total frustration over numbers of iterations/simulation
        is_connected: Optional[Boolean], default = False
            Is true if all graph vertices has at least one neighbour
        """

        self.edges = edges
        self.color_pattern = color_pattern
        self.vertices_list = self.create_vertices_list()
        self.val_map = self.create_val_map()
        self.vertices_neighbours = self.create_neighbour_dict()
        self.vertices_frustration = {}
        self.total_frustration = []
        self.is_connected = False
        self.vis_graph = vrg.Visualiser(self.edges, val_map=self.val_map, vis_labels=True, node_size=200)

        # add delay to show initial graph
        sleep(0.6)

        # calculate initial vertex frustration / local metric
        self.update_vertex_frustration()
        # calculate initial total frustration at instance construction
        self.total_frustration.append(self.global_metric())

    # class methods

    def create_vertices_list(self) -> list:
        """Return a list of vertices from tuple of edges"""

        edges = self.edges

        # Create vertices list
        graph_vertices = []

        # Iterate over edges_list and append vertex
        for edge_tuple in edges:
            x, y = edge_tuple  # Unpack the tuple into x and y
            # check if vertices already in graph_dict
            if x not in graph_vertices:
                graph_vertices.append(x)
            if y not in graph_vertices:
                graph_vertices.append(y)

        return graph_vertices

    def create_val_map(self) -> dict:
        """Return dictionary with color mapped to vertex"""

        color_pattern = 0
        # set color pattern
        if self.color_pattern == 'All 0':
            color_pattern = 0
        elif self.color_pattern == 'All 1':
            color_pattern = 1
        else:
            color_pattern = 2
        
        color_dict = {}
        vertices_list = self.vertices_list

        # Add color pattern to vertex
        for vertex in vertices_list:
            # add color pattern to vertex
            if color_pattern == 0 or color_pattern == 1:
                color_dict[vertex] = color_pattern
            else:  # if color pattern not 0 or 1, randomly assign color value
                color = random.randint(0, 1)
                color_dict[vertex] = color

        return color_dict

    def create_neighbour_dict(self):
        """Return dictionary of vertices as key and neighbours (if any) as value"""

        vertices_list = self.vertices_list
        edges = self.edges
        vertices_neighbours = {}

        # add neighbours to dictionary
        # Iterate over dictionary
        for vertex in vertices_list:
            # Store list of neighbours
            neighbours_list = []

            # Iterate over edges
            for edge_tuple in edges:
                x, y = edge_tuple  # split tuple into two values

                # If neighbour not already added, append to neighbours list
                if x not in neighbours_list and x != vertex and y == vertex:
                    neighbours_list.append(x)
                if y not in neighbours_list and x == vertex and y != vertex:
                    neighbours_list.append(y)

                # add neighbour list to dictionary
                vertices_neighbours[vertex] = neighbours_list

        return vertices_neighbours

    def local_metric(self, c_i: int, n_j: int) -> float:
        """Return  the frustration of a site"""

        # Store local metric total
        total_frustration = 0.0

        for c_j in n_j:
            total_frustration += (1 - 2 * c_i) * (1 - 2 * c_j)
        return total_frustration

    def global_metric(self) -> float:
        """Return the sum of the local_metric over every single vertex of the graph.
        The global metric is the measure of the frustration of the graph simulated by the program.
        """
        vertices_frustration = self.vertices_frustration

        # Store total frustration
        total_frustration = 0.0

        # iterate over dictionary of vertices
        for vertex in vertices_frustration:
            # add all vertex frustrations to total
            total_frustration += vertices_frustration[vertex]

        # Multiply total_frustration by 1/2 as per the provided formula.
        total_frustration *= 0.5

        return total_frustration

    def update_vertex_frustration(self):
        """Updates frustration for each vertex"""

        vertices_list = self.vertices_list
        vertices_neighbours = self.vertices_neighbours
        vertices_color = self.val_map

        for vertex in vertices_list:
            c_i = vertices_color[vertex]
            n_J = [vertices_color[neighbour] for neighbour in vertices_neighbours[vertex]]
            frustration = self.local_metric(c_i, n_J)
            self.vertices_frustration[vertex] = frustration

    def update_graph_connection(self):
        # Return True if graph is connected, otherwise return False
        visited = set()
        self.is_connected = False

        for start_vertex in self.vertices_list:
            if start_vertex not in visited:
                stack = [start_vertex]

                while stack:
                    vertex = stack.pop()
                    if vertex not in visited:
                        visited.add(vertex)
                        stack.extend(
                            neighbour for neighbour in self.vertices_neighbours[vertex] if neighbour not in visited)

                # If all vertices are visited, the graph is connected
                self.is_connected = (len(visited) == len(self.vertices_list))
                if self.is_connected:
                    return True
                else:
                    return False
                    break # Finish the loop if an unconnected section has been found
    def update_ordered(self) -> None:
        """Visit each site of the graph and change (swap) the colour if the local action of the site is positive"""
        vertices_list = self.vertices_list
        vertices_frustration = self.vertices_frustration
        val_map = self.val_map

        # iterate over vertices in vertices_dictionary
        for vertex in vertices_list:
            # set local action for each vertex
            local_action = vertices_frustration[vertex]
            if local_action > 0:
                current_color = val_map[vertex]                     # set current color
                new_color = 1.0 if current_color != 1.0 else 0.0    # swap current color
                val_map[vertex] = new_color
                self.update_vertex_frustration()                    # update vertices frustration

    def update_max_violation(self) -> None:
        """Identify the site with the largest value of local action and swap its colour."""

        vertices_list = self.vertices_list
        vertices_frustration = self.vertices_frustration
        val_map = self.val_map

        # store vertix with largest local action
        largest_action = None
        largest_vertex = None

        # iterate over dictionary
        for vertex in vertices_list:
            # set current local action
            current_action = vertices_frustration[vertex]

            # check if local action of current vertex > largest
            if largest_action is None or current_action > largest_action:
                largest_action = current_action                             # set new largest action value
                largest_vertex = vertex                                     # track vertex with largest action value

        # swap the color of vertex with largest local action
        if val_map[largest_vertex] == 1.0:
            val_map[largest_vertex] = 0.0
        else:
            val_map[largest_vertex] = 1.0

        # calculate new frustration for each vertex
        self.update_vertex_frustration()

    def update_monte_carlo(self) -> None:
        """Visit each site of the graph and swap colour if the exponential of the local action > a random float between 0,1."""

        vertices_list = self.vertices_list
        vertices_frustration = self.vertices_frustration
        val_map = self.val_map

        # iterate over vertices in vertices_dictionary
        for vertex in vertices_list:
            # set local action for each vertex
            local_action = vertices_frustration[vertex]
            if local_action > 0:
                current_color = val_map[vertex]  # set current color
                random_number = random.uniform(0, 1)  # generate random float between 0 and 1
                exp_local_action = math.exp(local_action)

                if exp_local_action > random_number: #compare exponent to random number
                    new_color = 1.0 if current_color != 1.0 else 0.0 # swap current colour
                    val_map[vertex] = new_color
                    self.update_vertex_frustration()  # update vertices frustration

    def run_simulation(self, update_procedure, iterations):
        """Simulate update of graph accourding to update_procedure for number of iterations"""

        for iteration in range(iterations):
            # small delay 
            sleep(0.6)
            if update_procedure.lower() == "ordered":
                self.update_ordered()
            elif update_procedure.lower() == "maxviolation":
                self.update_max_violation()
            else:
                self.update_monte_carlo()
            # update coloring in visual representation of the graph instance
            self.vis_graph.update(val_map=self.val_map)

            # compute new global metric and add to total_frustration
            self.total_frustration.append(self.global_metric())

    def report_frustration_history(self, steps: int) -> None:
        """ Display plot of the evolution of total frustration over a specified number of steps"""

        step_list = list(range(0, steps + 1))
        frustration = self.total_frustration

        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        ax.plot(step_list, frustration)  # Plot some data on the axes

        # Set labels
        ax.set_ylabel("Frustration of the graph")
        ax.set_xlabel("Number of update steps")

        # Set the title directly on the axes
        ax.set_title("Evolution of Total Frustration")

        # Display
        plt.show()
        
    def __eq__(self, other):
        """Return true if edges of this instance is equal to edges of other instance of same class"""
 
        if (self.edges == other.edges):
            return True
        else:
            return False


    def __str__(self):
        """Return a textual representation of the attributes of the graph"""

        return f"vertices: {self.vertices_list}. Vertex colors: {self.val_map}. Vertex neighbours: {self.vertices_neighbours}.\
            vertex frustration: {self.vertices_frustration}. Total graph frustration: {self.total_frustration}"
    
    def __repr__(self):
        """Return a Python-like representation of this this instance"""
        return f"GraphCreater({self.edges}, {self.color_pattern})"

# function for generating af g
def generate_random_graph(n, p=0.6):
    """Return a list of edges in tuples by generating a random graph from n vertices with p 0.6"""

    # Randomly assign connection between vertices
    graph = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph[i][j] = graph[j][i] = 1

    # Create list of edges
    edges = []

    for i in range(len(graph)):
        for j in range(i + 1, len(graph[i])):
            if graph[i][j] == 1:
                edges.append((i, j))

    return edges

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
            u, v = map(int, nodes)
            # Add the edge as a tuple to the edges_list
            edges_list.append((u, v))
        else:
            print("Invalid input.")

    return edges_list

# functions for creating list of edges from a file

def create_graph_from_file(file_path: str) -> list[tuple]:
    """Read a file, checks if its valid and return a list of edges for a graph"""
    # Open the text file in read mode
    try:
        with open(file_path, 'r') as file:
            # Read lines from the file and remove whitespaces
            lines = [line.strip() for line in file.readlines() if line.strip()]
    # Handle errors
    except FileNotFoundError:
        print("Error: The file could not be found.")
    except IOError:
        print("There was an error reading from the file.")

    # add edges from file to edges_list
    try:
        graph_edges = add_edges_from_lines(lines)
    except UnboundLocalError as e:
        print(e)
        return []

    return graph_edges

""" graph_color_test1 = GraphCreater([(1,2), (1, 3), (2, 3)], 0)
graph_color_test2 = GraphCreater([(1,2), (1, 3), (2, 3)], 0)
print(graph_color_test1.val_map)
print(graph_color_test2.val_map) """

# Import doctest module
if __name__ == "__main__":
    import doctest
    doctest.testmod()
