import time
from graph_sim import Firefighter, Treepatch, Rockpatch, Graphdata
from visualiser_random_forest_graph import Visualiser
import random
from typing import List, Dict, Optional, Tuple

class ForestFireGraph:
    """This is the base class for representing patches of land as a vertices on a graph. 
    Landpatches in the graph are either of type Tree or type rock. 
    Additionally, the class is used to simulating the evolution of wild fire on the graph on storing data
    associated with the simulation.
    """

    def __init__(
        self,
        edges: List[Tuple[int,int]],
        pos_nodes: Optional[Dict] = {},
        tree_distribution: Optional[float] = 30,
        firefighters: Optional[int] = 3,
        autocombustion: Optional[float] = 0.3,
        fire_spread_prob: Optional[float] = 0.3,
        rock_mutate_prob: Optional[float] = 0.1,
        sim_time: Optional[int] = 10,
        firefighter_average_skill: Optional[int] = 25
        ):
        """
        Parameters
        ----------
        edges: List[(int,int)]
            List containing the edges (Tuples of 2 vertices) forming the 2D surface for the graph.
        pos_nodes: Optional[dict], default = {}
            Optional argument. Stores graph position of nodes if provided.
        firefighters: Optional[int], default = 3
            Firefighters for initializing firefighter class
        tree_distribution: Optional[int], default = 30
            The percentage distribution of tree patches on the graph
        autocombustion: Optional[float], default = 0.3
            Probability for a tree patch to randomly ignite
        fire_spread_probability: Optional[int], default = 0.3
            Probability for fire to randomly spread to adjacent tree patch neighbours
        rock_mutate_prob: Optional[float], default = 0.1
            Probability for a rock patch to randomly mutate into a tree patch
        sim_time: Optional[int], default = 10
            The number of simulation steps for the purpose of simulating wildfire evolution.
        firefighter_average_skill: Optional[int], default = 25
            The average skill of instances of class firefighter
        """

        self._edges = edges
        self._pos_nodes = pos_nodes
        self._number_of_firefighters = firefighters
        self._autocombustion = autocombustion
        self._tree_distribution = tree_distribution
        self._fire_spread_prob = fire_spread_prob
        self._rock_mutate_prob = rock_mutate_prob
        self._sim_time = sim_time
        self._vertices_list = self._create_vertices_list()
        self._vertices_neighbours = self._create_neighbour_dict() 
        self._patches_map = self._populate_patches()                    # Map patch type to vertex
        self._color_map = {}                                            # Map color to vertex          
        self._firefighters_list = []
        self._firefighter_average_skill = firefighter_average_skill     #skill level is probability (in percentage) of extinguishing fire
        self._deploy_firefighters()            # Map firefighters to vertex
        
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
    def _create_vertices_list(self) -> List[int]:
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
        # TODO "(if any)" should probably be removed, since vertices of our planar graph always have at least 1 neighbour?

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
    def _populate_patches(self) -> Dict:
        """Populates the vertices of a graph by connecting it to an instance of either Rockpatch or Treepatch class"""
        
        vertices = self._vertices_list
        tree_count = round(len(vertices) * (self._tree_distribution / 100.0))  # Calculate the (rounded) number of tree patches from input tree percentage

        # Randomly select 'tree_count' vertices to be tree patches
        tree_vertices = random.sample(vertices, tree_count)

        # Dictionary mapping vertex to patch class
        patch_map = {}

        for vertex in vertices:
            # Get list of neighbours
            neighbours = self._vertices_neighbours[vertex]
            # Check if the current vertex should be a tree or rock patch
            if vertex in tree_vertices:
                patch_map[vertex] = Treepatch(id = vertex, fire_spread_prob=self._fire_spread_prob, autocombustion_prob=self._autocombustion, neighbour_ids=neighbours)
            else:
                patch_map[vertex] = Rockpatch(id = vertex, neighbour_ids=neighbours, mutate_chance=self._rock_mutate_prob)
        
        return patch_map
    
    def _update_color_map(self) -> Dict:
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

    def _deploy_firefighters(self) -> None:
        """Instantiates firefighters, and adds them to list """

        for i in range(0, self._number_of_firefighters):
            my_firefighter = Firefighter(firefighter_skill=self._firefighter_average_skill)
            my_firefighter._current_patch = random.sample(self._vertices_list, 1)[0]
            self._firefighters_list.append(my_firefighter)
            i+= 1

    # Methods for working with data
    def _initialize_data(self):
        """Stores initital data from graph instance creation in dataclass"""

        data = self._graph_data

        data._land_patches = [len(self._vertices_list)]
        data._tree_patches = [round(data._land_patches[0] * (self._tree_distribution / 100.0))]
        data._rock_patches = [data._land_patches - data._tree_patches[0]]
        data._firefighters = [self._number_of_firefighters]

    def simulate(self): 
        simulation_count = 0
        while simulation_count < self._sim_time:

            # Iterates over patches map
            for vertex, patch in self._patches_map.items():
                # Applies treepatch dynamics
                if isinstance(patch, Treepatch):
                    patch.evolve()
                    if patch._ignited:
                        patch.spread_fire(patch.get_id)
                    if patch._tree_health < 0:
                        self._patches_map[vertex] = patch.mutate()
                # Applies rockpatch dynamics
                if isinstance(patch, Rockpatch):
                    # Probability for rocpatches turning into treepatches
                    if random.random() <= patch._mutate_chance:
                        self._patches_map[vertex] = patch.mutate(fire_spread_prob_input = self._fire_spread_prob, 
                                                                 autocombustion_prob=self._autocombustion, 
                                                                 tree_health=random.randint(1,256))

            for firefighter in self._firefighters_list:
                firefighter_patch = self._patches_map[firefighter._current_patch]
                if isinstance(firefighter_patch, Treepatch) and firefighter_patch._ignited:
                    firefighter.extinguish_fire(firefighter_patch)
                else:
                    for id in firefighter_patch.get_neighbour_ids():
                        if(isinstance(self._patches_map[id], Treepatch) and self._patches_map[id]._ignited):
                            firefighter._current_patch = id
                        else:
                            #change firefighters _current_patch attribute
                            firefighter._current_patch = random.sample(firefighter_patch.get_neighbour_ids(), 1)[0]
            print(self._patches_map)
            for firefighter in self._firefighters_list:
                print(firefighter)
                    ### remove old placement of firefighter in firefighter_map
                    ##del self._firefighters_map[vertex]
                    ##self._firefighters_map[vertex] = firefighter
            
            #TODO Er det rigtig anvendelse af graph data???
            self._graph_data.update_patches(self._patches_map)

            # visualize instance of graph
            self._update_color_map()
            #self._vis_graph = Visualiser(self._edges, vis_labels=True, node_size=50, pos_nodes=self._pos_nodes)
            self._vis_graph.update_node_colours(self._color_map)
            time.sleep(0.5) # add delay to show graph between steps
            print("Simulation count is currently" + str(simulation_count))

            simulation_count += 1

    def spread_fire(self, id: int) -> None:
        """If treepatch is ignited, spread fire to adjacent Treepatch(es)."""

        # Get the neighbors of the current Treepatch
        neighbours = self._patches_map._neighbours_list

        # Ignites adjacents treepatches not already on fire
        for neighbor_id in neighbours:
            current_neighbour = self._patches_map[neighbor_id]

            # Check if neighbor is tree patch AND simulate chance of igniting
            if isinstance(current_neighbour, Treepatch) and random.random() <= self._patches_map[id]._fire_spread_prob:   
                current_neighbour._ignited = True
        # Check for probable fire spread
