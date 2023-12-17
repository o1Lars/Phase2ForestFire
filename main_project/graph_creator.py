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
import landpatch_creator as lc
import visualiser_random_forest_graph as vis_rfg
import graph_helper
import matplotlib.pyplot as plt
from typing import List, Optional, Dict
import random as random
import math as math
from time import sleep


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
        """Populates the vertices of a graph with either Rockpatches or Treepatches"""
        
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

# Import doctest module
if __name__ == "__main__":
    import doctest
    doctest.testmod()
