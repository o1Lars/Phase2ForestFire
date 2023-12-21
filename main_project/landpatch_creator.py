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
        tree_distribution: int,
        fire_spread_prob: int) -> None:
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
        fire_spread_probability: int
            Probability for fire to randomly spread to adjacent tree patch neighbours
        # TODO
        """
        self._vertices_list = vertices
        self._neighbours = neighbours
        self.firefighters = firefighters
        self._tree_distribution = tree_distribution
        self._fire_spread_prob = fire_spread_prob
        self._patches_map = self._populate_patches()                           # Map patch type to vertex
        self._color_map = {}                                                   # Map color to vertex          
        self._firefighters_map = self._deploy_firefighters(firefighters)       # Map firefighters to vertex

        self._update_color_map()   

    # Class methods
    def _populate_patches(self) -> None:
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
                patch_map[vertex] = Treepatch(self._fire_spread_prob)
            else:
                patch_map[vertex] = Rockpatch()
        
        return patch_map
    
    def _update_color_map(self) -> dict:
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
        
        self._color_map = color_map

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

    def spread_fire(self, tree_patch: int) -> None:
        """If treepatch is ignited, spread fire to adjacent Treepatch(es)."""

        # Check for probable fire spread
        if random.random() <= self._patches_map[tree_patch]._fire_spread_prob:
            # Get the neighbors of the current Treepatch
            neighbors = self._neighbours[tree_patch]

            # Ignites adjacents treepatches not already on fire
            for neighbor in neighbors:
                current_neighbor = self._patches_map[neighbor]
                if isinstance(current_neighbor, Treepatch):   # Check if neighbor is tree patch
                    if not current_neighbor._ignited:
                        current_neighbor._ignited = True

    def move_firefighters(self) -> None:
        """Move firefighter randomly to a neighboring patch based on the specified conditions."""

        firefighter_map = self._firefighters_map
        new_firefighter_map = {}

        # Iterate over firefighter map
        for vertex, firefighter in firefighter_map.items():
            
            # Check if current patch is on fire
            if isinstance(self._patches_map[vertex], Treepatch) and self._patches_map[vertex]._ignited:
                new_firefighter_map[vertex] = firefighter
            else:
                # Store neighbours list
                neighbors = self._neighbours[vertex]

                # Check if there are adjacent Treepatches on fire
                adjacent_fire_patches = [neighbor for neighbor in neighbors if
                                        isinstance(self._patches_map[neighbor], Treepatch) and self._patches_map[neighbor]._ignited]

                if adjacent_fire_patches:
                    # Move to a random adjacent Treepatch on fire
                    new_location = random.choice(adjacent_fire_patches)
                else:
                    # Move to a random adjacent patch
                    new_location = random.choice(neighbors)

                print(f"Firefighter moved from {vertex} to {new_location}.")
                new_firefighter_map[new_location] = firefighter

        # add new map to instance attributes
        self._firefighters_map = new_firefighter_map
    
    def evolve_patches(self) -> None:
        """Evolves the graph 1 simulation step"""
        
        patches = self._patches_map

        # Loop over patch map
        for patch in patches:

            # Identify if patch is tree or rock
            if isinstance(patches[patch], Treepatch):
                # Firefighter skills
                if patch in self._firefighters_map:
                    # Check for burning patch
                    if patches[patch]._ignited:
                        # Do fire fighter stuff
                        self._firefighters_map[patch].extinguish_fire(patches[patch])   # Try to fight fire
                        self._firefighters_map[patch].update_health(patches[patch])     # Update firefighter health
                        # Check if firefighter died
                        if self._firefighters_map[patch]._heath < 0:
                            del self._firefighters_map[patch]
                        # Check for spread fire
                        self.spread_fire(patch)
                        
                # Update tree stats
                patches[patch].update_treestats

                # Check if all trees on patch have died.
                if patches[patch]._tree_health < 0:
                    self.mutate_landpatch(patch)
        
            if isinstance(patches[patch], Rockpatch):
                if random.randint(0, 100) == patches[patch]._mutate_chance:
                    self.mutate_landpatch(patches[patch])
        
        self.move_firefighters()


@dataclass
class Rockpatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Rockpatch
    Parameters    
    ----------
    _mutate_chance: float, default = 1
        Percentage chance for a rockpatch to mutate into treepatch
    """
    _mutate_chance: float = 1


@dataclass
class Treepatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Treepatch

    Parameters
    ----------
    tree_health: Optional[int]
        Attribute identifies the current health of the treepatch [0-256].
    """
    _fire_spread_prob: float
    _tree_health: Optional[int] = 256
    _ignited: bool = False

    def update_treestats(self) -> None:
        """Update treestats based on the specified conditions."""
        if not self._ignited:
            self._tree_health += 10
        else:
            self._tree_health -= 20


    def evolve(self) -> None:
        """Perform one evolution step for the Treepatch."""
        self.update_treestats()
        self.spread_fire()
        # Additional logic for the Treepatch's evolution? maybe later not sure

class Firefighter:
    """Each instance of this class creates a firefighter for extinguishing fires in a graph of landpatches"""

    def __init__(self, firefighter_skill: Optional[float] = 25, health: Optional[float] = 100) -> None:
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

        extinguish_probability = self._firefighter_skill
        if random.random() <= extinguish_probability:
            treepatch._ignited = False
            print("Fire extinguished by firefighter.")
        else:
            print("Firefighter failed to extinguish fire.")

    def update_health(self, current_patch) -> None:
        """Updates the current instance of a firefighter's health."""
        if current_patch._ignited:
            self._health -= 10
        else:
            self._health += 5
        print(f"Firefighter health updated to {self._health}.")

    def evolve(self) -> None:
        """Perform one evolution step for the firefighter."""
        self.move_firefighter()
        # Additional logic for the firefighter's evolution, if needed.
