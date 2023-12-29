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

class Landpatch():
    """This is the base class for representing patches of land as a vertices on a graph. Landpatches in the graph are either of type Tree or type rock. Additionally, the class is used to simulating the evolution of wild fire on the graph on storing data
    associated with the simulation.
    """

    def __init__(
        self,
        edges: List[tuple[int,int]],
        pos_nodes: Optional[dict] = {},
        tree_distribution: float = 30,
        firefighters: int = 3,
        autocombustion: Optional[float] = 0.3,
        fire_spread_prob: Optional[float] = 0.3,
        rock_mutate_prob: Optional[float] = 0.1,
        sim_time: Optional[int] = 10) -> None:
        """
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
        self._edges = edges
        self._pos_nodes = pos_nodes
        self._firefighters = firefighters
        self._autocombustion = autocombustion
        self._tree_distribution = tree_distribution
        self._fire_spread_prob = fire_spread_prob
        self._rock_mutate_prob = rock_mutate_prob
        self._sim_time = sim_time
        self._vertices_list = self._create_vertices_list()
        self._vertices_neighbours = self._create_neighbour_dict() 
        self._patches_map = self._populate_patches()                    # Map patch type to vertex
        self._color_map = {}                                            # Map color to vertex          
        self._firefighters_map = self._deploy_firefighters()            # Map firefighters to vertex
        
        # Initial mapping of landpatches color
        self._update_color_map()
        
        # visualize opening instance of graph
        self._vis_graph = Visualiser(self._edges, vis_labels=True, node_size=50, pos_nodes=self._pos_nodes)
        self._vis_graph.update_node_colours(self._color_map)
        time.sleep(1) # add delay to show initial graph

        # Create data class instance to store graph data
        self._graph_data = Graphdata()
        self._initialize_data()


    # Class methods
    # Basic graph methods
    def _create_vertices_list(self) -> List[Tuple[int,int]]:
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

    def _create_neighbour_dict(self) -> Dict[int, List[int]]:
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

    def update_graph_connection(self) -> None:
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

    # Landpatces specific methods
    def _populate_patches(self) -> None:
        """Populates the vertices of a graph by connecting it to an instance of either Rockpatch or Treepatch class"""
        
        vertices = self._vertices_list
        tree_count = round(len(vertices) * (self._tree_distribution / 100.0))  # Calculate the (rounded) number of tree patches from input tree percentage

        # Randomly select 'tree_count' vertices to be tree patches
        tree_vertices = random.sample(vertices, tree_count)

        # Dictionary mapping vertex to patch class
        patch_map = {}

        for vertex in vertices:
            # Check if the current vertex should be a tree or rock patch
            if vertex in tree_vertices:
                patch_map[vertex] = Treepatch(self._fire_spread_prob) # TODO Add autocombustion
            else:
                patch_map[vertex] = Rockpatch() # TODO add mutate probability
        
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

    def _deploy_firefighters(self) -> dict:
        """Creates fire fighters and maps them to vertices (landpatches) on the graph"""

        vertices = self._vertices_list
        firefighters = self._firefighters

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
        """If treepatch is ignited, randomly spread fire to adjacent Treepatch(es)."""

        # Check for probable fire spread
        if random.random() <= self._patches_map[tree_patch]._fire_spread_prob:
            # Get the neighbors of the current Treepatch
            neighbours = self._neighbours[tree_patch]

            # Ignites adjacents treepatches not already on fire
            for neighbor in neighbours:
                current_neighbour = self._patches_map[neighbor]
                if isinstance(current_neighbour, Treepatch):   # Check if neighbor is tree patch
                    if not current_neighbour._ignited:
                        current_neighbour._ignited = True

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
    
    # Methods for working with data
    def _initialize_data(self):
        """Stores initital data from graph instance creation in dataclass"""

        data = self._graph_data

        data._land_patches = [len(self._vertices_list)]
        data._tree_patches = [round(data._land_patches[0] * (self._tree_distribution / 100.0))]
        data._rock_patches = [data._tree_patches[0] - data._tree_patches[0]]
        data._firefighters = [self._firefighters]
    
    # Base methods overwriting python basic methods.
    def __eq__(self, other) -> bool:
        """Return true if edges of this instance is equal to edges of other instance of same class"""
 
        if (self._edges == other.edges):
            return True
        else:
            return False

    def __str__(self) -> str:
        """Return a textual representation of the attributes of the graph"""

        return f"vertices: {self._vertices_list}. Vertex colors: {self._color_map}. Vertex neighbours: {self._vertices_neighbours}."
    
    def __repr__(self) -> str:
        """Return a Python-like representation of this this instance"""
        return f"GraphCreater({self._edges}, {self._color_pattern})"

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

    def __init__(self, firefighter_skill: Optional[float] = 25) -> None:
        """
        Initialize a Firefighter.

        Parameters
        ----------
        firefighter_skill: Optional[float]
            Represents the instance of a firefighter's ability to extinguish fires on a Treepatch.
        """
        self._firefighter_skill = firefighter_skill
        self._current_patch = None

    def extinguish_fire(self, treepatch) -> None:
        """Based on firefighter_skill, extinguishes fire if toggled on Treepatch."""

        extinguish_probability = self._firefighter_skill
        if random.random() <= extinguish_probability:
            treepatch._ignited = False
            print("Fire extinguished by firefighter.")
        else:
            print("Firefighter failed to extinguish fire.")

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
    #pos_nodes: Optional[dict] = {}
    tree_distribution: float = 30
    firefighters: int = 3
    autocombustion: Optional[float] = 0.3
    fire_spread_prob: Optional[float] = 0.3
    rock_mutate_prob: Optional[float] = 0.1
    sim_time: Optional[int] = 10