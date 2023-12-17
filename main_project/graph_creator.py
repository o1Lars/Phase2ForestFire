"""
This module provides:
 - Graph: a class for creating a graph of edges and sites forming a graph
 - Graphdata: a special python dataclass for storing data associated with the graph, eg. evolution of landpatches

Requirements
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Python 3.7 or higher.

Notes
-----
Module is created as part of the group project for the final exam of DS830 Introduction to programming.
"""

# Import dependencies
from dataclasses import dataclass
import landpatch_creator as lc
import visualiser_random_forest_graph as vis_rfg
import graph_helper as gh
import matplotlib.pyplot as plt
from typing import List, Optional, Dict
import random as random
import math as math
from time import sleep
import os


class Graph():
    """Each instance of this class creates a Graph with edges and vertices populated with landpatches (either rock or tree) and a coloring pattern. """

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

        self._edges = edges
        self._color_pattern = color_pattern
        self._vertices_list = self.create_vertices_list()
        self._val_map = self.create_val_map()
        self._vertices_neighbours = self.create_neighbour_dict()
        self._patches_map = self.populate_patches() 
        self._is_connected = False
        self._vis_graph = vis_rfg.Visualiser(self._edges, val_map=self.val_map, vis_labels=True, node_size=200)

        # add delay to show initial graph
        sleep(0.6)



    # class methods
    
    def populate_patches(self):
        """Populates the vertices of a graph by connecting it to an instance of either Rockpatch or Treepatch class"""
        
        vertices = self._vertices_list

        #TODO

        print("Populating vertices with patches...")

    def create_vertices_list(self) -> list:
        """Return a list of vertices from tuple of edges"""

        edges = self._edges

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
        if self._color_pattern == 'All 0':
            color_pattern = 0
        elif self._color_pattern == 'All 1':
            color_pattern = 1
        else:
            color_pattern = 2
        
        color_dict = {}
        vertices_list = self._vertices_list

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

        vertices_list = self._vertices_list
        edges = self._edges
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

    def update_graph_connection(self):
        # Return True if graph is connected, otherwise return False
        visited = set()
        self._is_connected = False

        for start_vertex in self._vertices_list:
            if start_vertex not in visited:
                stack = [start_vertex]

                while stack:
                    vertex = stack.pop()
                    if vertex not in visited:
                        visited.add(vertex)
                        stack.extend(
                            neighbour for neighbour in self._vertices_neighbours[vertex] if neighbour not in visited)

                # If all vertices are visited, the graph is connected
                self._is_connected = (len(visited) == len(self._vertices_list))
                if self._is_connected:
                    return True
                else:
                    return False
                    break # Finish the loop if an unconnected section has been found
        
    def __eq__(self, other):
        """Return true if edges of this instance is equal to edges of other instance of same class"""
 
        if (self._edges == other.edges):
            return True
        else:
            return False


    def __str__(self):
        """Return a textual representation of the attributes of the graph"""

        return f"vertices: {self._vertices_list}. Vertex colors: {self.val_map}. Vertex neighbours: {self._vertices_neighbours}.\
            vertex frustration: {self.vertices_frustration}. Total graph frustration: {self.total_frustration}"
    
    def __repr__(self):
        """Return a Python-like representation of this this instance"""
        return f"GraphCreater({self._edges}, {self._color_pattern})"


@dataclass
class Graphdata:
    """Each instance of this class creates a dataclass that stores various information related to simulating the evolution of patches of land

    Parameters
    ----------
    _land_patches: int, default = 0
        Stores total number of landpatches on the graph (coresponds to total number of vertices)
    _tree_patches: List[int], default = []
        Stores current number of tree patches on the graph
    _rock_patches: List[int], default = []
        Stores current number of rock patches on the graph
    _ignited_tree_patches: List[int], default = []
        Stores current number of ignited tree patches
    _consumed_tree_patches: int, default = 0
        Stores total number of tree patches consumed by fire
    _rock_to_tree_counter: int, default = 0
        Stores number of rock patches that, during the course of simulation, have turned into tree patches
    _firefighters: List[int] = []
        Stores current number of firefighters
    _dead_firefighters: int = 0
        Stores number of firefighters, who have perished
    """
    _land_patches: int = 0
    _tree_patches: List[int] = []
    _rock_patches: List[int] = []
    _ignited_tree_patches: List[int] = []
    _consumed_tree_patches: int = 0
    _rock_to_tree_counter: int = 0
    _firefighters: List[int] = []
    _dead_firefighters_counter: int = 0

    def update_patches(self, patches_map: Dict[str]) -> None:
        """Updates number of tree patches, rock patches and forest fires"""

        # Store variables for updating patches of instance
        treepatches = self._tree_patches
        rockpatches = self._rock_patches
        forest_fires = self._ignited_tree_patches

        # Initialize counters
        treepatches_counter = 0
        rockpatches_counter = 0
        forest_fires_counter = 0

        # Iterate over patches_map
        for vertex, patch in patches_map.items():
            # check if patch mapped to vertex is rock or tree
            if isinstance(patch, lc.Rockpatch):
                rockpatches_counter += 1
            else:
                treepatches_counter += 1
                # check if tree patch is ignited
                if patch.is_ignited:
                    forest_fires_counter += 1
        
        # Append patch count to instance data
        treepatches.append(treepatches_counter) 
        rockpatches.append(rockpatches_counter)
        forest_fires.append(forest_fires_counter) 

    def update_rock_to_tree_counter(self) -> None:
        """Updates number of rock patches that swapped to a tree patch"""
        # TODO

        self._rock_to_tree_counter += 1
    
    def update_firefighter_list(self) -> None:
        """Updates the list of current alive fire fighters"""

        # Compute number of currently alive firefighters
        firefighters = self._firefighters[0] - self._dead_firefighters_counter

        # Append total number of alive firefighters to firefighter list
        self._firefighters.append(firefighters)

    def update_dead_firefighters_counter(self):
        """Updates counter of dead fire fighters"""
        
        self._dead_firefighters_counter += 1

# function for generating af g
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
    """Read a file, checks if its valid and return a list of edges for a graph"""

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
        # Generate a random graph
        graph_edges = gh.voronoi_to_edges(n_random_graph)

        # Verify that the graph is a planar graph
        if gh.edges_planar(graph_edges[0]):
            print("Your graph is a planar graph. Yahoo!")
        else:
            print("Your graph is not a planar graph.")
else:
    print("Invalid choice. Please enter '1' or '2'.")

print(graph_edges)


# Import doctest module
if __name__ == "__main__":
    import doctest
    doctest.testmod()
