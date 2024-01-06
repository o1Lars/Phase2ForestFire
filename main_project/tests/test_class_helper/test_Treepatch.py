import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)
import unittest
from ...class_helper import Rockpatch, Treepatch, Landpatch
import random

class TestTreepatch(unittest.TestCase):
    def setUp(self):
        self.treepatch = Treepatch(1, [2, 3], autocombustion_prob=30, tree_health=200)

    def test_initialization(self):
        self.assertEqual(self.treepatch.get_id(), 1)
        self.assertEqual(self.treepatch.get_neighbour_ids(), [2, 3])
        self.assertEqual(self.treepatch._autocombustion_prob, 30)
        self.assertEqual(self.treepatch._tree_health, 200)
        self.assertFalse(self.treepatch._ignited)

    def test_check_autocombust(self):
        random.seed(42)  # Seed for consistent test
        self.treepatch.check_autocombust()
        self.assertTrue(not self.treepatch._ignited)  # Since seed is set, this check will pass

    def test_updateland_ignited(self):
        self.treepatch._ignited = True
        self.treepatch.updateland()
        self.assertEqual(self.treepatch._tree_health, 180)

    def test_updateland_not_ignited(self):
        self.treepatch._ignited = False
        self.treepatch.updateland()
        self.assertEqual(self.treepatch._tree_health, 210)

    def test_updateland_tree_health_limit(self):
        self.treepatch._tree_health = 256
        self.treepatch.updateland()
        self.assertEqual(self.treepatch._tree_health, 256)

    def test_mutate(self):
        mutated_patch = self.treepatch.mutate()
        self.assertIsInstance(mutated_patch, Rockpatch)
        self.assertEqual(mutated_patch.get_id(), 1)
        self.assertEqual(mutated_patch.get_neighbour_ids(), [2, 3])

if __name__ == '__main__':
    unittest.main()
