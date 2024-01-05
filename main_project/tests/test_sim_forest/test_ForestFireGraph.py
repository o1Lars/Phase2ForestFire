import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)
import unittest
from ...sim_forest import ForestFireGraph


class TestForestFireGraphInitialization(unittest.TestCase):
    def test_default_initialization(self):
        graph = ForestFireGraph(edges=[(0, 1), (1, 2)])
        
        self.assertEqual(graph._edges, [(0, 1), (1, 2)])
        self.assertEqual(graph._pos_nodes, {})
        self.assertEqual(graph._tree_distribution, 80)
        self.assertEqual(graph._number_of_firefighters, 3)
        self.assertEqual(graph._autocombustion, 1)
        self.assertEqual(graph._fire_spread_prob, 30)
        self.assertEqual(graph._rock_mutate_prob, 1)
        self.assertEqual(graph._sim_time, 10)
        self.assertEqual(graph._firefighter_average_skill, 25)

    def test_custom_initialization(self):
        custom_edges = [(0, 1), (1, 2), (2, 0)]
        custom_pos_nodes = {0: (0, 0), 1: (1, 1), 2: (2, 2)}
        custom_tree_distribution = 60
        custom_firefighters = 5
        custom_autocombustion = 1
        custom_fire_spread_prob = 30
        custom_rock_mutate_prob = 1
        custom_sim_time = 15
        custom_firefighter_average_skill = 20

        graph = ForestFireGraph(
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

        # Kill graph visualiser
        graph._vis_graph = None

        self.assertEqual(graph._edges, custom_edges)
        self.assertEqual(graph._pos_nodes, custom_pos_nodes)
        self.assertEqual(graph._tree_distribution, custom_tree_distribution)
        self.assertEqual(graph._number_of_firefighters, custom_firefighters)
        self.assertEqual(graph._autocombustion, custom_autocombustion)
        self.assertEqual(graph._fire_spread_prob, custom_fire_spread_prob)
        self.assertEqual(graph._rock_mutate_prob, custom_rock_mutate_prob)
        self.assertEqual(graph._sim_time, custom_sim_time)
        self.assertEqual(graph._firefighter_average_skill, custom_firefighter_average_skill)

if __name__ == '__main__':
    unittest.main()
