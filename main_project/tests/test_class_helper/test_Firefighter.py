import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

from ...class_helper import Firefighter
import unittest
from typing import Optional, Type
import random

# Mock Treepatch class
class Treepatch:
    def __init__(self, id: int, ignited: bool = False):
        self._id = id
        self._ignited = ignited

class TestFirefighter(unittest.TestCase):
    def setUp(self):
        self.firefighter = Firefighter(firefighter_skill=50, health=80)

    def test_initialization(self):
        self.assertEqual(self.firefighter._firefighter_skill, 50)
        self.assertEqual(self.firefighter._health, 80)
        self.assertIsNone(self.firefighter._current_patch)
        self.assertTrue(self.firefighter.isAlive)

    def test_extinguish_fire_success(self):
        treepatch = Treepatch(1, ignited=True)
        random.seed(51)  # Seed for consistent test
        self.firefighter.extinguish_fire(treepatch)
        self.assertFalse(treepatch._ignited)  # Since seed is set, fire should be extinguished

    def test_extinguish_fire_failure(self):
        treepatch = Treepatch(1, ignited=True)
        random.seed(10)  # Seed for consistent test
        self.firefighter.extinguish_fire(treepatch)
        self.assertTrue(treepatch._ignited)  # Since seed is set, fire shouldn't be extinguished

    def test_update_health_ignited(self):
        self.firefighter._current_patch = Treepatch(1, ignited=True)
        self.firefighter.update_health()
        self.assertEqual(self.firefighter._health, 70)

    def test_update_health_not_ignited(self):
        self.firefighter._current_patch = Treepatch(1, ignited=False)
        self.firefighter.update_health()
        self.assertEqual(self.firefighter._health, 85)

    def test_check_death_saved(self):
        random.seed(42)  # Seed for consistent test
        self.firefighter._firefighter_skill = 50  # Makes the save_check 0.5
        self.firefighter.check_death()
        self.assertTrue(self.firefighter.isAlive)  # Since seed is set, firefighter should survive

    def test_check_death_not_saved(self):
        random.seed(10)  # Seed for consistent test
        self.firefighter._firefighter_skill = 50  # Makes the save_check 0.5
        self.firefighter.check_death()
        self.assertFalse(not self.firefighter.isAlive)  # Since seed is set, firefighter should not survive

if __name__ == '__main__':
    unittest.main()
