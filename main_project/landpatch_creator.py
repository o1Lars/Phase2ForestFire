"""
This module provides classes for representing different landpatches. Landpatch is the base class and extends to the subclasses Rockpatch and Treepatch

Furthermore, this module provides the Firefighter class. 

Requirements
#TODO
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Package networkx https://networkx.org/ which can be installed via PIP.
Python 3.7 or higher.



Notes
-----
This module is created as material for the phase 2 project for DM857, DS830 (2023). 
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import random


class Landpatch():
    """This is the base class for representing a patch of land as a vertex of a graph"""

    def __init__(
        self, 
        vertices: List[int],
        neighbours: Dict[str, int],
        firefighters: int,
        tree_distribution: int) -> None:
        """
        Parameters
        ----------
        vertices: List[(int,int)]
            List of vertices for mapping patches of land
        neighbours: Dict[str, int]
            List of neighbours for tracking neighbouring patches of land
        firefighters: int
            Firefighters for initializing firefighter class
        tree_distribution: int
            The percentage distribution of tree patches on the graph
        # TODO
        """
        self._vertices_list = vertices
        self._neighbours = neighbours
        self.firefighters = firefighters
        self._tree_distribution = tree_distribution 
        self._patches_map = self._populate_patches()                            # Map patch type to vertex
        self._color_map = self._create_color_map()                              # Map color to vertex          
        self._firefighters_map = self._deploy_firefighters(firefighters)        # Map firefighters to vertex

    # Class methods
    def _populate_patches(self):
        """Populates the vertices of a graph by connecting it to an instance of either Rockpatch or Treepatch class"""
        
        vertices = self._vertices_list
        tree_count = round(len(vertices) * (self._tree_distribution / 100.0))  # Calculate the (rounded) number of tree patches

        # Randomly select 'tree_count' vertices to be tree patches
        tree_vertices = random.sample(vertices, tree_count)

        # Dictionary mapping vertex to patch class
        patch_map = {}

        for vertex in vertices:
            # Check if the current vertex should be a tree or rock patch
            if vertex in tree_vertices:
                patch_map[vertex] = Treepatch()
            else:
                patch_map[vertex] = Rockpatch()
        
        return patch_map
    
    def _create_color_map(self) -> dict:
        """Return dictionary with color mapped to vertex"""

        patches = self._patches_map

        color_map = {}

        # Iterate over patches dictionary
        for vertex, patch_type in patches.items():
            color_code = 0

            # Identify if patch is tree or rock
            if isinstance(patch_type, Treepatch):
                # Check if tree patch is ignited
                if patch_type._ignited:
                    color_code = patch_type._tree_health - 256
                else:
                    color_code = patch_type._tree_health
            
            color_map[vertex] = color_code
        
        return color_map
    
    def mutate_landpatch(self, vertex_id: int) -> None:
        """Swaps the land patch instance associated with vertex. 
        If vertex was populated by rock, becomes populated by tree and vice versa"""

        patches_map = self._patches_map

        # Check if the vertex exists in the patches_map
        if vertex_id in patches_map:
            if isinstance(patches_map[vertex_id], Treepatch):
                patches_map[vertex_id] = Rockpatch()
            elif isinstance(patches_map[vertex_id], Rockpatch):
                patches_map[vertex_id] = Treepatch()
            else:
                print("Invalid patch type.")
        else:
            print("Vertex not found in the graph.")
    
    def _deploy_firefighters(self, firefighters) -> dict:
        """Creates fire fighters and maps them to vertices (landpatches) on the graph"""

        vertices = self._vertices_list

        # Randomly select vertices for firefighters to be deployed
        firefighters_vertices = random.sample(vertices, firefighters)

        # Dictionary for mapping fire fighters to vertex
        firefighter_map = {}

        for vertex in vertices:
            # Check if the current vertex should be a tree or rock patch
            if vertex in firefighters_vertices:
                firefighter_map[vertex] = Firefighter()
        
        return firefighter_map
    

    def next_neighbours_ID(self):
        """Return the ID of the next neighbors to the present patch"""
        # TODO
        print("This returns the next neighbors to the present patch")

@dataclass
class Rockpatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Rockpatch
    Parameters    
    ----------
    _mutate_chance: float, default = 1
    Percentage chance for a rockpatch to mutate into treepatch
    """
    _mutate_chance: float = 1
    
    def mutate(self):
        """Allows swapping a Rockpatch with a Treepatch without losing connections to neighbors and associations with firefighters."""
        ## Each Rockpatch has a possibility of becoming a Treepatch at each step (default 1%).
        if random.random() < 0.01:
            self.mutate_landpatch(Treepatch)
            print("The Rockpatch has mutated into a Treepatch.")

@dataclass
class Treepatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Treepatch

    Parameters
    ----------
    tree_health: Optional[int]
        Attribute identifies the current health of the treepatch [0-256].
    """
    
    tree_health: Optional[int] = 100
    ignited: bool = False

    def update_treestats(self) -> None:
        """Update treestats based on the specified conditions."""
        if not self._ignited:
            self._tree_health += 10
        else:
            self._tree_health -= 20

        if self._tree_health < 0:
            self.mutate_landpatch(Rockpatch)
        print("Treestats has been updated.")

    def spread_fire(self) -> None:
        """With probability 30%, spread fire to adjacent Treepatch."""
        if random.random() <= 0.3:
            # Get the neighbors of the current Treepatch
            neighbors = self.next_neighbours_ID()

            # Ignites adjacents treepatches not already on fire
            for neighbor in neighbors:
                if not neighbor._ignited:
                    neighbor._ignited = True

            print("Fire has spread to adjacent Treepatch")

    def evolve(self) -> None:
        """Perform one evolution step for the Treepatch."""
        self.update_treestats()
        self.spread_fire()
        # Additional logic for the Treepatch's evolution? maybe later not sure

class Firefighter:
    """Each instance of this class creates a firefighter for extinguishing fires in a graph of landpatches"""

    def __init__(self, firefighter_skill: Optional[float] = 1, health: Optional[float] = 100) -> None:
        """
        Initialize a Firefighter.

        Parameters
        ----------
        firefighter_skill: Optional[float]
            Represents the instance of a firefighter's ability to extinguish fires on a Treepatch.
        health: Optional[float], default=100
            Represents the instance of a firefighter's current health.
        """
        self._firefighter_skill = firefighter_skill
        self._health = health
        self._current_patch = None

    def extinguish_fire(self, treepatch) -> None:
        """Based on firefighter_skill, extinguishes fire if toggled on Treepatch."""
        if treepatch._ignited:
            extinguish_probability = self._firefighter_skill
            if random.random() < extinguish_probability:
                treepatch._ignited = False
                print("Fire extinguished by firefighter.")
            else:
                print("Firefighter failed to extinguish fire.")

    def move_firefighter(self) -> None:
        """Move firefighter randomly to a neighboring patch based on the specified conditions."""
        if self._current_patch is not None:
            neighbors = self._current_patch.next_neighbours_ID()

            # Check if there are adjacent Treepatches on fire
            adjacent_fire_patches = [neighbor for neighbor in neighbors if
                                     isinstance(neighbor, Treepatch) and neighbor._ignited]

            if adjacent_fire_patches:
                # Move to a random adjacent Treepatch on fire
                new_location = random.choice(adjacent_fire_patches)
            else:
                # Move to a random adjacent patch
                new_location = random.choice(neighbors)

            print(f"Firefighter moved from {self._current_patch} to {new_location}.")
            self._current_patch = new_location
        else:
            print("Firefighter has no current location.")

    def update_health(self) -> None:
        """Updates the current instance of a firefighter's health."""
        if self._current_patch and self._current_patch._ignited:
            self._health -= 10
        else:
            self._health += 5
        print(f"Firefighter health updated to {self._health}.")

    def evolve(self) -> None:
        """Perform one evolution step for the firefighter."""
        self.move_firefighter()
        # Additional logic for the firefighter's evolution, if needed.
