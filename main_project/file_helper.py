"""
This module provides a set of helper functions, to:
- user_file:                opens a file using a given file path (fp) and file name (fn), and reads its contents
- add_edges_from_lines:     Read lines, check if line represent an edge of a graph. Return list of edges
- create_graph_from_file:   Reads a file, checks if it's valid, and returns a list of edges for a graph
- check_planar_graph:       Checks if a list of edges on a graph can be represented planar

Requirements
------------
Python 3.7 or higher.

Notes
-----
This module created as material for the phase 2 project for DM857, DS830 (2023). 
"""
import time
import os
from typing import List, Tuple
import graph_helper as gh

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
    except KeyboardInterrupt as e:
        print(e)
        quit()

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