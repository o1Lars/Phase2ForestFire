import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)
import unittest
from ...class_helper import Landpatch

class TestLandpatch(unittest.TestCase):
    def setUp(self):
        self.landpatch = Landpatch(1, [2, 3])

    def test_get_id(self):
        self.assertEqual(self.landpatch.get_id(), 1)

    def test_get_neighbour_ids(self):
        self.assertEqual(self.landpatch.get_neighbour_ids(), [2, 3])

if __name__ == '__main__':
    unittest.main()