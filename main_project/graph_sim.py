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
from dataclasses import dataclass, field
import landpatch_creator as lc
import visualiser_random_forest_graph as vis_rfg
import graph_helper as gh
import matplotlib.pyplot as plt
from typing import List, Optional, Dict, Type
import random as random
import math as math
from time import sleep
import os
import sys

class Graph():
    """Each instance of this class creates a Graph with edges and vertices populated with landpatches (either rock or tree) and a coloring pattern. """

    def __init__(
        self,
        edges: list,
        tree_distribution: float,
        firefighters: int,
        fire_spread_prob: int,
        sim_time: int) -> None:
        """
        Parameters
        ----------
        edges: List[(int,int)]
            List containing the edges (Tuples of 2 vertices) forming the 2D surface for the graph.
        tree_distribution: float
            Percentage distribution of tree to rock patches ratio
        firefighters: int, default = 0
            firefighters at instance creation
        """

        self._edges = edges
        self._tree_distribution = tree_distribution
        self.fire_spread_prob = fire_spread_prob
        self.sim_time = sim_time
        self._vertices_list = self._create_vertices_list()
        self._vertices_neighbours = self._create_neighbour_dict()
        self._is_connected = False

        # Create instance of class landpatch for landpatches data
        self._patches = lc.Landpatch(self._vertices_list, self._vertices_neighbours, firefighters, tree_distribution, fire_spread_prob)      

        # visualize opening instance of graph
        self._vis_graph = vis_rfg.Visualiser(self._edges, vis_labels=True, node_size=50)
        self._vis_graph.update_node_colours(self._patches._color_map)
        sleep(1) # add delay to show initial graph


    # class methods

    def _create_vertices_list(self) -> list:
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

    def _create_neighbour_dict(self):
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

        return f"vertices: {self._vertices_list}. Vertex colors: {self._patches._color_map}. Vertex neighbours: {self._vertices_neighbours}."
    
    def __repr__(self):
        """Return a Python-like representation of this this instance"""
        return f"GraphCreater({self._edges}, {self._color_pattern})"

# Import doctest module
if __name__ == "__main__":
    import doctest
    doctest.testmod()
