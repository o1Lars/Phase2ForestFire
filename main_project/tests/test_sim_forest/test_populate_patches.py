import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

import unittest
from ...sim_forest import ForestFireGraph
from ...class_helper import Landpatch, Rockpatch, Treepatch


# test class GraphSimulator and methods
class TestGraphSimulator(unittest.TestCase):
    
    def setUp_test_graph(self):
        """Create instance of ForestFireGraph for testing"""
        custom_edges = [(0, 1), (1, 2), (2, 0)]
        custom_pos_nodes = {0: (0, 0), 1: (1, 1), 2: (2, 2)}
        custom_tree_distribution = 60
        custom_firefighters = 5
        custom_autocombustion = 1
        custom_fire_spread_prob = 30
        custom_rock_mutate_prob = 1
        custom_sim_time = 15
        custom_firefighter_average_skill = 20

        test_graph = ForestFireGraph(
            edges=custom_edges,
            pos_nodes=custom_pos_nodes,
            tree_distribution=custom_tree_distribution,
            firefighters=custom_firefighters,
            autocombustion=custom_autocombustion,
            fire_spread_prob=custom_fire_spread_prob,
            rock_mutate_prob=custom_rock_mutate_prob,
            sim_time=custom_sim_time,
            firefighter_average_skill=custom_firefighter_average_skill,
        )
        
        return test_graph
    
    # Test for _populate_patches method on ForestFireGraph
    def test_populate_patches(self):
        test = self.setUp_test_graph()

        # Get the patches map
        patches_map = test._patches_map
        print("patches: ", patches_map)

        # Check the count of tree and rock patches against the expected values
        expected_tree_count = 2
        expected_rock_count = 1

        # Check initial storing in graph data for tree and rock patches
        tree_count = test._graph_data._tree_patches[0]
        rock_count = test._graph_data._rock_patches[0]

        # Check if the count matches the expected values
        self.assertEqual(tree_count, expected_tree_count, 'Mismatch in tree patch count')
        self.assertEqual(rock_count, expected_rock_count, 'Mismatch in rock patch count')



if __name__ == '__main__':
    unittest.main()