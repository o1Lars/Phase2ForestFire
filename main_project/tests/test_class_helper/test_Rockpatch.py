import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)
import unittest
from ...class_helper import Rockpatch, Treepatch, Landpatch

class TestRockpatch(unittest.TestCase):
    def setUp(self):
        self.rockpatch = Rockpatch(1, [2, 3], mutate_chance=5)

    def test_initialization(self):
        self.assertEqual(self.rockpatch.get_id(), 1)
        self.assertEqual(self.rockpatch.get_neighbour_ids(), [2, 3])
        self.assertEqual(self.rockpatch._mutate_chance, 5)

    def test_mutate(self):
        new_treepatch = self.rockpatch.mutate(0.5, tree_health=300)
        self.assertIsInstance(new_treepatch, Treepatch)
        self.assertEqual(new_treepatch.get_id(), 1)
        self.assertEqual(new_treepatch.get_neighbour_ids(), [2, 3])

if __name__ == '__main__':
    unittest.main()