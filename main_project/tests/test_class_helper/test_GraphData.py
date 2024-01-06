import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)
import unittest
from unittest.mock import patch, MagicMock
from ...class_helper import Graphdata


# Mock classes for testing purposes
class Landpatch:
    def __init__(self, ignited: bool = False):
        self._ignited = ignited

class Rockpatch:
    def __init__(self, ignited: bool = False):
        self._ignited = ignited
    pass

class TestGraphdata(unittest.TestCase):
    def setUp(self):
        self.graph_data = Graphdata()

    def test_update_patches(self):
        patches_map = {
            "vertex1": Landpatch(),
            "vertex2": Landpatch(ignited=True),
            "vertex3": Rockpatch()
        }

        self.graph_data.update_patches(patches_map)

        self.assertEqual(self.graph_data._tree_patches, [3])
        self.assertEqual(self.graph_data._rock_patches, [0])
        self.assertEqual(self.graph_data._ignited_tree_patches, [1])

    def test_update_rock_to_tree_counter(self):
        self.graph_data.update_rock_to_tree_counter()
        self.assertEqual(self.graph_data._rock_to_tree_counter, 1)

    def test_update_firefighter_list(self):
        self.graph_data._firefighters = [5]
        self.graph_data._dead_firefighters_counter = 2

        self.graph_data.update_firefighter_list()
        self.assertEqual(self.graph_data._firefighters, [5, 3])

    def test_update_dead_firefighters_counter(self):
        self.graph_data.update_dead_firefighters_counter()
        self.assertEqual(self.graph_data._dead_firefighters_counter, 1)

    @patch('builtins.print')
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.close')
    def test_report_forest_evolution(self, mock_close, mock_show, mock_print):
        steps = 10
        self.graph_data._tree_patches = [5, 8, 12, 15, 10, 8, 5, 2, 1, 0, 0]
        self.graph_data._rock_patches = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.graph_data._ignited_tree_patches = [0, 0, 1, 3, 5, 7, 9, 10, 8, 4, 0]

        self.graph_data.report_forest_evolution(steps)

        mock_print.assert_called()
        mock_show.assert_called()
        mock_close.assert_called()

if __name__ == '__main__':
    unittest.main()
