"""
This module holds various classes essential for simulating the evolution of wildfires on a graph.

This module provides:
- Graphdata:    a special python dataclass for storing data associated with the landpatches on a graph.
- Landpatch:    a base class that creates patches of land as vertices on a graph
- Treepatch:    a subclass of landpatch, that specifies patches of land with trees on them. Tree patches have special attributes
- Rockpatch:    a subclass of landpatch, that specifies patches of land with rock on them. Rock patches can mutate into tree patches
- Firefighter:  A class that is used in simulating wild fires. Each instance of the firefighter class tries to extinguish 
                fires on tree patches and can move around a graph of landpatches.
- ConfigData    A dataclass that stores graph configuration to make previous configurations easily accessible

Requirements
------------
Python 3.7 or higher.

Notes
-----
This module is created as material for the phase 2 project for DM857, DS830 (2023). 
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Type
import matplotlib.pyplot as plt
import random
import time


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
        """Updates number of tree patches, rock patches and forest fires
        
        Parameter
        ---------
        patches_map: Dict[str, Type]
            A dictionary containing a vertex as the key, and a landpatch as its value. patches_map is used to identify
            whether a vertex is a treepatch (ignited or not) or a rockpatch.
        """

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
      
      
    def report_forest_evolution(self, steps: int) -> None:
        """Displays a plot of evolution of tree patches, rock patches, and wildfires over a specified number of steps"""

        # Retrieve data for visualisation
        tree_patches = self._tree_patches
        rock_patches = self._rock_patches
        wildfires = self._ignited_tree_patches
        print("tree: ", len(tree_patches))
        print("rock: ", len(rock_patches))
        print("fire: ", len(wildfires))
        # Create a list of steps for the x-axis
        step_list = list(range(steps + 1))
    
        # Create a figure and axis for the plot
        plt.figure(figsize=(10, 6))
    
        # Plot individual lines for each metric
        plt.plot(step_list, tree_patches, color='r', label='Trees Population')
        plt.plot(step_list, rock_patches, color='b', label='Non-combustible Land')
        plt.plot(step_list, wildfires, color='g', label='Wildfires')
    
        # Labels, title, legend, and grid
        plt.xlabel("Simulation Steps")
        plt.ylabel("Count")
        plt.title("Evolution of Wildfire")
        plt.legend(loc="upper right")
        plt.grid(True)
    
        # Show the plot
        plt.show()

    
class Landpatch():
    """This is the base class for representing patches of land as vertices on a graph. 
    Landpatches in the graph are either of type Tree or type rock."""
    def __init__(
        self,
        id: [int] = None,
        neighbour_ids: [List[int]] = None) -> None:
        """
        Parameter
        ---------
        id: [int] = None
            Represents a unique identifier for each unique instance of the class
        neighbour_ids: [List[int]] = None
            List of ids from neighbouring vertices. Necessary to properly identify neighbours of each instance
        """
        # Assign id and neighbour parameters to corresponding attributes
        self._id = id
        self._neighbour_ids = neighbour_ids

        self._firefighters_list = None

    def get_id(self) -> int:
        return self._id

    def get_neighbour_ids(self) -> List[int]:
        return self._neighbour_ids
        


class Rockpatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Rockpatch"""
    def __init__(self, 
                 id: int, 
                 neighbour_ids: List[int]=None, 
                 mutate_chance: Optional[float]=1)->None:
        super().__init__(id, neighbour_ids=neighbour_ids)
        self._mutate_chance = mutate_chance
        """
        Parameters    
        ----------
        id: [int] = None
            Represents a unique identifier for each unique instance of the class
        neighbour_ids: [List[int]] = None
            List of ids from neighbouring vertices. Necessary to properly identify neighbours of each instance
        mutate_chance: float, default = 1
            Percentage chance for a rockpatch to mutate into treepatch
        """

    def mutate(self, autocombustion_prob:float, tree_health: Optional[int]=256) -> Landpatch:
        """Swaps the land patch instance associated with vertex. """
        #patches_map = self._patches_map
        #return Treepatch(id=self._id, neighbour_ids = self._neighbour_ids, self_combustion_prob=autocombustion_prob)

        return Treepatch(id=self._id, neighbour_ids = self._neighbour_ids, 
                         autocombustion_prob=autocombustion_prob, tree_health=tree_health)


class Treepatch(Landpatch):
    """This class extends Landpatch and creates an instance of subclass Treepatch"""
    def __init__(self, 
                 id: int, 
                 neighbour_ids: list[int] = None, 
                 autocombustion_prob: Optional[float] = 0.6, 
                 tree_health: Optional[int] = 256)->None:
        super().__init__(id, 
                         neighbour_ids = neighbour_ids)
        """
        Parameters
        ----------
        id: [int] = None
            Represents a unique identifier for each unique instance of the class
        fire_spread_prob: Optional[float], default = 0.3
            Represents the probability for an ignited tree patch to spread fire to neighbouring tree patches
        neighbour_ids: [List[int]] = None
            List of ids from neighbouring vertices. Necessary to properly identify neighbours of each instance
        autocombustion_prob: Optional[float], default = 0.6
            Represents the probability for each instance of tree patch to self-ignite
        tree_health: Optional[int], default = 256
            Attribute identifies the current health of the treepatch [0-256].
        """
        self._autocombustion_prob = autocombustion_prob
        self._tree_health = tree_health
        self._ignited = False

    def check_autocombust(self) -> None:
        """Checks and updates wether instance of tree patch spontaniously catches fire."""

        autocombustion_prob = self._autocombustion_prob

        if random.randint(0,100) <= autocombustion_prob:
            self._ignited = True
            print(f"Treepatch ({self._id}) caught fire.")

    def updateland(self) -> None:
        """Update treestats based on the specified conditions."""
        if self._ignited:
            self._tree_health -= 20
        else:
            self._tree_health += 10

            # Check health doesn't exceed 256
            if self._tree_health > 256:
                self._tree_health = 256

            # Check for autocombustion
            self.check_autocombust()

    def mutate(self) -> Landpatch:
        """Swaps the land patch instance associated with vertex. """
        return Rockpatch(id=self._id, neighbour_ids=self._neighbour_ids)


class Firefighter:
    """Each instance of this class creates a firefighter for extinguishing fires in a graph of landpatches"""
    def __init__(self, 
                 firefighter_skill: Optional[float] = 25, 
                 health: Optional[float] = 100) -> None:
        """
        Parameters
        ----------
        firefighter_skill: Optional[float]
            Represents the instance of a firefighter's ability to extinguish fires on a Treepatch.
        health: Optional[float], default=100
            Represents the instance of a firefighter's current health."""
        self._firefighter_skill = firefighter_skill
        self._health = health
        self._current_patch: int = None
        self.isAlive = True

    def extinguish_fire(self, treepatch: Type) -> None:
        """Based on firefighter_skill, extinguishes fire if toggled on Treepatch. 
        If fail, small chance for firefighter to die

        Parameters
        ----------
        treepatch: Class
            A patch of land of type tree, created as an instance of class Treepatch
        """

        extinguish_probability = self._firefighter_skill/100
        if random.random() <= extinguish_probability:
            treepatch._ignited = False
            print("Fire extinguished by firefighter.")
        else:
            print("Firefighter failed to extinguish fire.")
            self.check_death()

    def update_health(self) -> None:
        """Updates the current instance of a firefighter's health."""

        current_patch = self._current_patch

        if current_patch._ignited:
            self._health -= 10
        else:
            self._health += 5
        print(f"Firefighter health updated to {self._health}.")

    def evolve(self) -> None:
        """Perform one evolution step for the firefighter."""
        self.move_firefighter()
    
    def check_death(self) -> None:
        """Checks if firefighter is killed by forestfire"""

        save_check = 3 - (self._firefighter_skill/100)
        death_roll = random.randint(0, 100)

        # check for death
        if death_roll <= save_check:
            self.isAlive = False


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
        """Return a tuple of all attributes. Used to easily access attributes from previous configurations
        
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
    