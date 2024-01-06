import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)


from ...graph_forest import get_sim_limit
import unittest
from unittest.mock import patch

# Mocking get_input_menu, get_valid_input, config_info, quit, restart_program functions for testing
def get_input_menu(menu_type, parameter):
    pass

def get_valid_input(prompt, valid_range=None, min_val=None, max_val=None):
    pass

def config_info(parameter):
    pass

def quit():
    pass

def restart_program():
    pass

def random():
    return MockRandom()

class MockRandom:
    def randint(self, a, b):
        return 5  # Fixed value for testing

class TestGetRockMutateProb(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '10'])  # Simulate user input for testing (choosing option 1 and entering 42)
    def test_get_fire_spread_prob_user_defined(self, mock_input):
        spread_prob = get_sim_limit()
        self.assertEqual(spread_prob, 10)  # Ensure the function returns the user-defined spread probability

    @patch('builtins.input', side_effect=['2'])
    def test_get_fire_spread_prob_random(self, mock_input):
        sim_limit = get_sim_limit()
        self.assertTrue(2 <= sim_limit <= 50)  # Ensure the function returns a random value within the specified range

if __name__ == '__main__':
    unittest.main()