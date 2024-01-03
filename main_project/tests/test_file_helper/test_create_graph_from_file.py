import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

from ...file_helper import create_graph_from_file
import unittest


class TestCreateGraphFromFile(unittest.TestCase):

    def test_valid_file(self):
        filename = "/Users/chrisvandborg/Documents/sdu_2023/Phase2ForestFire/test_files/graph1.dat"
        result = create_graph_from_file(filename)
        # Add assertions based on the expected output from a valid file
        self.assertEqual(result, [(0, 1), (1, 2), (2, 3), (3, 0)])

    def test_invalid_file(self):
        filename = "/Users/chrisvandborg/Documents/sdu_2023/Phase2ForestFire/test_files/graph7.dat"
        result = create_graph_from_file(filename)
        # Add assertions based on the expected output from an invalid file
        self.assertEqual(result, [])

    def test_nonexistent_file(self):
        filename = "/Users/chrisvandborg/Documents/sdu_2023/Phase2ForestFire/test_files/graph7.dat"
        result = create_graph_from_file(filename)
        # Add assertions based on the expected output from a non-existent file
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
