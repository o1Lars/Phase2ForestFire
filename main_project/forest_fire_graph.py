from graph_sim import Firefighter, Landpatch, Treepatch, Rockpatch
import random

class ForestFireGraph:
    def __init__(
        self,
        edges: List[tuple[int,int]],
        pos_nodes: Optional[dict] = {},
        tree_distribution: float = 30,
        number_of_firefighters: int = 3,
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
        self._number_of_firefighters = number_of_firefighters
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
        self._landpatches = self._create_landpatches() # Eksisterer ikke, den skal du lave. Den skal returnere en liste af Landpatches
                                            # LandPatch-klassen som allerede eksisterer skal kun have 2 parametre i dens __init__metode
                                            # Resten af LandPatch's input-argumenter skal i stedet fore ForestFireGraphs.
    #self._vertices = _create_vertices() # EKSISTERER IKKE, den skal du lave. Den skal returnere en liste af ints

        # Initial mapping of landpatches color
        self._update_color_map()
        
        # visualize opening instance of graph
        self._vis_graph = Visualiser(self._edges, vis_labels=True, node_size=50, pos_nodes=self._pos_nodes)
        self._vis_graph.update_node_colours(self._color_map)
        time.sleep(1) # add delay to show initial graph

        # Create data class instance to store graph data
        self._graph_data = Graphdata()
        self._initialize_data()

        self._firefighters_list = None
    """
    Find ud af hvad der skal være i landpatch og hvad der skal være i den her:

    Attributes:
    Edges: List(tuple[int,int])
    Vertices: List[int]
    Landpatches: What is a landpatch?
    Firefighters: What is a landpatch?

    Methods:
    Simulate(Simulation_count: int)
    CreateLandPatches(numberOfLandPatches: int): returns a list of LandPatch
    Landpatch __init__ method should receive ID parameter, and neighbours parameter(list of ID's (int))
    
    """


    def simulate(self): 
        simulation_count = 0
        while simulation_count < self._sim_time:
            # Iterates over patches map
            for vertex, patch in self._patches_map.items():
                # Applies treepatch dynamics
                if isinstance(patch, Treepatch):
                    patch.evolve() #fix evolve method and replace with updateland method ## create autocombustion in updateland
                    if patch._tree_health < 0:
                        patch.mutate()
                    else:
                        patch.updateland()
                
                if isinstance(patch, Rockpatch):
                    # Probability for rocpatches turning into treepatches
                    patch.mutate()

            for vertex, firefighter in self._firefighters_map.items():

                firefighter_patch = self._patches_map[vertex]
                if isinstance(firefighter_patch, Treepatch) and firefighter_patch._ignited:
                    firefighter.extinquish_fire(firefighter_patch)
                else:
                    for id in firefighter_patch.get_neighbour_ids:
                        if(self._patches_map[id]._ignited):
                            firefighter._current_patch = id
                    firefighter._current_patch = random.sample(firefighter_patch.get_neighbour_ids, 1)