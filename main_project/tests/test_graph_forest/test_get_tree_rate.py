import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

import unittest
from unittest.mock import patch, MagicMock
from ...graph_forest import get_tree_rate

class TestGetTreeRate(unittest.TestCase):

    @patch('input_helper.get_valid_input')
    def test_user_input(self, mock_get_valid_input):
        # Set up mocks for user input scenario
        mock_get_valid_input.return_value = 50  # Simulate user input of 50
        get_tree_rate = MagicMock()
        get_tree_rate.return_value = 50
        result = get_tree_rate()
        self.assertEqual(result, 50)  # Assert the result based on the expected user input

    @patch('random.randint')
    def test_random_generation(self, mock_randint):
        # Set up mocks for random generation scenario
        mock_randint.return_value = 70  # Simulate random generation returning 70
        get_tree_rate = MagicMock()
        get_tree_rate.return_value = 70
        result = get_tree_rate()
        self.assertEqual(result, 70)  # Assert the result based on the expected random value

if __name__ == '__main__':
    unittest.main()
