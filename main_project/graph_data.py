"""
This module provides:
 Graphdata: a special python dataclass for storing data associated with the landpatches on a graph.

Requirements
------------
Package matplotlib https://matplotlib.org/ which can be installed via PIP.
Python 3.7 or higher.

Notes
-----
Module is created as part of the group project for the final exam of DS830 Introduction to programming.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Type
import landpatch_creator as lc

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