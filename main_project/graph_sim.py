"""
This module holds various classes essential for simulating the evolution of wildfires on a graph.

This module provides:
- Graphdata:    a special python dataclass for storing data associated with the landpatches on a graph.
- Landpatch:    a base class that creates a graph that simulates the evolution of wild fire over tree and rock patches
- Treepatch:    a subclass of landpatch, that doesnt directly inherit most of the functionality of Landpatch, but acts as a dataclass
                The class stores data related to tree patches
- Rockpatch:    a subclass of landpatch, that doesnt directly inherit most of the functionality of Landpatch, but acts as a dataclass
                The class stores data related to rock patches
- Firefighter:  A class that is used in simulating wild fires. Each instance of the firefighter class tries to extinguish 
                fires on tree patches
- ConfigData    A dataclass that stores graph configuration to make previous configurations easily accessible

Requirements
#TODO
------------
Python 3.7 or higher.

Notes
-----
This module is created as material for the phase 2 project for DM857, DS830 (2023). 
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Type
from visualiser_random_forest_graph import Visualiser
import time
import random

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
    _tree_patches: List[int] = field(default_factory=list)
    _rock_patches: List[int] = field(default_factory=list)
    _ignited_tree_patches: List[int] = field(default_factory=list)
    _consumed_tree_patches: int = 0
    _rock_to_tree_counter: int = 0
    _firefighters: List[int] = field(default_factory=list)
    _dead_firefighters_counter: int = 0

    def update_patches(self, patches_map: Dict[str, Type]) -> None:
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
            if isinstance(patch, Rockpatch):
                rockpatches_counter += 1
            else:
                treepatches_counter += 1
                # check if tree patch is ignited
                if patch._ignited:
                    forest_fires_counter += 1
        
        # Append patch count to instance data
        treepatches.append(treepatches_counter) 
        rockpatches.append(rockpatches_counter)
        forest_fires.append(forest_fires_counter) 

    def update_rock_to_tree_counter(self) -> None:
        """Updates number of rock patches that swapped to a tree patch"""

        self._rock_to_tree_counter += 1
    
    def update_firefighter_list(self) -> None:
        """Updates the list of current alive fire fighters"""

        # Compute number of currently alive firefighters
        firefighters = self._firefighters[0] - self._dead_firefighters_counter

        # Append total number of alive firefighters to firefighter list
        self._firefighters.append(firefighters)

    def update_dead_firefighters_counter(self) -> None:
        """Updates counter of dead fire fighters"""
        
        self._dead_firefighters_counter += 1

class Landpatch():
    """This is the base class for representing patches of land as a vertices on a graph. 
    Landpatches in the graph are either of type Tree or type rock. 
    Additionally, the class is used to simulating the evolution of wild fire on the graph on storing data
    associated with the simulation.
    """

    def __init__(
        self,
        id: [int] = None,
        neighbour_ids: [List[int]] = None) -> None:

        # Assign id and neighbour parameters to corresponding attributes
        self._id = id
        self._neighbour_ids = neighbour_ids

        self._firefighters_list = None

    def get_id(self) -> int:
        return self._id

    def get_neighbour_ids(self) -> List[int]:
        return self._neighbour_ids    


        
        # # Change attributes of current Landpatch instance using __dict__
        # if isinstance(self, Treepatch):
        #     self.__dict__ = Rockpatch(id=self._id, neighbours = self._neighbours)
        # if isinstance(self, Rockpatch):
        #     self.__dict__ = Treepatch(id=self._id, neighbours = self._neighbours)
            

        


#    def move_firefighters(self) -> None:
#        """Move firefighter randomly to a neighboring patch based on the specified conditions."""
#
#        firefighter_map = self._firefighters_map
#        new_firefighter_map = {}
#
#        # Iterate over firefighter map
#        for vertex, firefighter in firefighter_map.items():
#            
#            # Check if current patch is on fire
#            if isinstance(self._patches_map[vertex], Treepatch) and self._patches_map[vertex]._ignited:
#                new_firefighter_map[vertex] = firefighter
#            else:
#                # Store neighbours list
#                neighbors = self._neighbours[vertex]
#
#                # Check if there are adjacent Treepatches on fire
#                adjacent_fire_patches = [neighbor for neighbor in neighbors if
#                                        isinstance(self._patches_map[neighbor], Treepatch) and self._patches_map[neighbor]._ignited]
#
#                if adjacent_fire_patches:
#                    # Move to a random adjacent Treepatch on fire
#                    new_location = random.choice(adjacent_fire_patches)
#                else:
#                    # Move to a random adjacent patch
#                    new_location = random.choice(neighbors)
#
#                print(f"Firefighter moved from {vertex} to {new_location}.")
#                new_firefighter_map[new_location] = firefighter
#
#        # add new map to instance attributes
#        self._firefighters_map = new_firefighter_map
    
    #def evolve_patches(self) -> None:
    #    """Evolves the graph 1 simulation step"""
    #    
    #    patches = self._patches_map

    #    # Loop over patch map
    #    for patch in patches:

    #        # Identify if patch is tree or rock
    #        if isinstance(patches[patch], Treepatch):
    #            # Firefighter skills
    #            if patch in self._firefighters_map:
    #                # Check for burning patch
    #                if patches[patch]._ignited:
    #                    # Do fire fighter stuff
    #                    self._firefighters_map[patch].extinguish_fire(patches[patch])   # Try to fight fire
    #                    self._firefighters_map[patch].update_health(patches[patch])     # Update firefighter health
    #                    # Check if firefighter died
    #                    if self._firefighters_map[patch]._heath < 0:
    #                        del self._firefighters_map[patch]
    #                    # Check for spread fire
    #                    self.spread_fire(patch)
    #                    
    #            # Update tree stats
    #            patches[patch].update_treestats

    #            # Check if all trees on patch have died.
    #            if patches[patch]._tree_health < 0:
    #                self.mutate(patch)
    #    
    #        if isinstance(patches[patch], Rockpatch):
    #            if random.randint(0, 100) == patches[patch]._mutate_chance:
    #                self.mutate(patches[patch])
    #    
    #    self.move_firefighters()
    
    # Methods for working with data
   
    # Base methods overwriting python basic methods.
    #def __eq__(self, other) -> bool:
    #    """Return true if edges of this instance is equal to edges of other instance of same class"""
 
    #    if (self._edges == other.edges):
    #        return True
    #    else:
    #        return False

    #def __str__(self) -> str:
    #    """Return a textual representation of the attributes of the graph"""

    #    return f"vertices: {self._vertices_list}. Vertex colors: {self._color_map}. Vertex neighbours: {self._vertices_neighbours}."
    
    #def __repr__(self) -> str:
    #    """Return a Python-like representation of this this instance"""
    #    return f"GraphCreater({self._edges}, {self._color_pattern})"
    
    

class Rockpatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Rockpatch
    Parameters    
    ----------
    _mutate_chance: float, default = 1
        Percentage chance for a rockpatch to mutate into treepatch
    """
    #_mutate_chance: float = 1
    def __init__(self, id: int, neighbour_ids: List[int] = None):
        super().__init__(id, neighbour_ids=neighbour_ids)
        self._mutate_chance = 1

    def mutate(self, fire_spread_prob_input:float) -> Landpatch:
        """Swaps the land patch instance associated with vertex. """
        #patches_map = self._patches_map
        return Treepatch(id=self._id, neighbour_ids = self._neighbour_ids, fire_spread_prob=fire_spread_prob_input)

       # Check if the vertex exists in the patches_map (is problematic - only updates internal map and not current instance of landpatch)
       ## if vertex_id in patches_map:
       ##     if isinstance(patches_map[vertex_id], Treepatch):
       ##         patches_map[vertex_id] = Rockpatch(id=vertex_id, neighbour_ids=patches_map[vertex_id]._neighbours_list)
       ##     elif isinstance(patches_map[vertex_id], Rockpatch):
       ##         patches_map[vertex_id] = Treepatch(id=vertex_id, neighbour_ids=patches_map[vertex_id]._neighbours_list)
       ##     else:
       ##         print("Invalid patch type.")
       ## else:
       ## 
       ##      print("Vertex not found in the graph.")


class Treepatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Treepatch

    Parameters
    ----------
    tree_health: Optional[int]
        Attribute identifies the current health of the treepatch [0-256].
    """
    def __init__(self, id: int, fire_spread_prob: float, neighbour_ids: list[int] = None, autocombustion_prob: float = 0.6):
        super().__init__(id, neighbour_ids = neighbour_ids)
        self._fire_spread_prob = fire_spread_prob
        self._autocombustion_prob = autocombustion_prob
        self._tree_health = 256
        self._ignited = False

    def autocombust(self) -> None:
        """Checks and updates wether instance of tree patch spontaniously catches fire."""
        autocombustion_prob = self._autocombustion_prob

        if random.randint(0,1) <= autocombustion_prob:
            self._ignited = True
            print(f"Treepatch ({self._id}) caught fire.")

    def updateland(self) -> None:
        """Update treestats based on the specified conditions."""
        if not self._ignited:
            self._tree_health += 10
            if self._tree_health > 256:
                self._tree_health = 256
        else:
            self._tree_health -= 20

    def evolve(self) -> None:
        """Perform one evolution step for the Treepatch."""
        self.updateland()
        # Additional logic for the Treepatch's evolution? maybe later not sure

    def mutate(self) -> Landpatch:
        """Swaps the land patch instance associated with vertex. """
        #patches_map = self._patches_map
        return Rockpatch(id=self._id, neighbours = self._neighbours)


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
        self._current_patch: int = None

    def extinguish_fire(self, treepatch) -> None:
        """Based on firefighter_skill, extinguishes fire if toggled on Treepatch."""

        extinguish_probability = self._firefighter_skill/100
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

@dataclass
class ConfigData():
    """This is a dataclass where each instance represents a collection of data from a privious simulation configuration.

    Parameters
    ----------
    edges: List[(int,int)]
        List containing the edges (Tuples of 2 vertices) forming the 2D surface for the graph.
    pos_nodes: Optional[dict], default = {}
        Optional argument. Stores graph position of nodes if provided.
    firefighters: int
        Firefighters for initializing firefighter class
    tree_distribution: int
        The percentage distribution of tree patches on the graph
    autocombustion: float
        Probability for a tree patch to randomly ignite
    fire_spread_probability: int
        Probability for fire to randomly spread to adjacent tree patch neighbours
    rock_mutate_prob: float
        Probability for a rock patch to randomly mutate into a tree patch
    sim_time: int
        The number of simulation steps for the purpose of simulating wildfire evolution.
    """

    edges: List[tuple[int,int]]
    pos_nodes: Optional[dict] = field(default_factory=dict)
    tree_distribution: float = 30
    firefighters: int = 3
    autocombustion: Optional[float] = 0.3
    fire_spread_prob: Optional[float] = 0.3
    rock_mutate_prob: Optional[float] = 0.1
    sim_time: Optional[int] = 10

    def get_config(self) -> Tuple:
        """Return a tuple of all attributes. Used to easility acces attributes from previous configurations
        
        Return: Tuple[edges, pos_nodes, tree_distribution, firefighters, autocombustion, fire_spread_prob, rock_mutate_prob, sim_time]
        ----------
        edges: List[(int,int)]
            List containing the edges (Tuples of 2 vertices) forming the 2D surface for the graph.
        pos_nodes: Optional[dict], default = {}
            Optional argument. Stores graph position of nodes if provided.
        firefighters: int
            Firefighters for initializing firefighter class
        tree_distribution: int
            The percentage distribution of tree patches on the graph
        autocombustion: float
            Probability for a tree patch to randomly ignite
        fire_spread_probability: int
            Probability for fire to randomly spread to adjacent tree patch neighbours
        rock_mutate_prob: float
            Probability for a rock patch to randomly mutate into a tree patch
        sim_time: int
            The number of simulation steps for the purpose of simulating wildfire evolution.
        """

        return self.edges, self.pos_nodes, self.tree_distribution, self.firefighters, \
                self.autocombustion, self.fire_spread_prob, self.rock_mutate_prob, self.sim_time
    