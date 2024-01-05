import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

import unittest
from ...sim_forest import ForestFireGraph


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
    
    # Test for _initialize_data method on ForestFireGraph
    def test_initialize_data(self):
        test = self.setUp_test_graph()

        # Ensure the initial data matches the expected values
        expected_land_patches = len(test._vertices_list)
        expected_tree_patches = round(expected_land_patches * (test._tree_distribution / 100.0))
        expected_rock_patches = expected_land_patches - expected_tree_patches
        expected_firefighters = test._number_of_firefighters
        expected_ignited_tree_patches = 0

        # Get the initialized data from the instance
        graph_data = test._graph_data

        # Check if the initialized data matches the expected values
        self.assertEqual(graph_data._land_patches, [expected_land_patches], 'Mismatch in land patches')
        self.assertEqual(graph_data._tree_patches, [expected_tree_patches], 'Mismatch in tree patches')
        self.assertEqual(graph_data._rock_patches, [expected_rock_patches], 'Mismatch in rock patches')
        self.assertEqual(graph_data._firefighters, [expected_firefighters], 'Mismatch in firefighters')
        self.assertEqual(graph_data._ignited_tree_patches, [expected_ignited_tree_patches], 'Mismatch in ignited tree patches')



if __name__ == '__main__':
    unittest.main()