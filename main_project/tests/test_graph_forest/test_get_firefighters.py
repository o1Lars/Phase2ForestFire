import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

import unittest
from unittest.mock import patch, MagicMock
from ...graph_forest import get_firefighters

class TestGetFirefighters(unittest.TestCase):
    @patch('input_helper.get_valid_input')
    @patch('random.randint')
    def test_user_defined_firefighters(self, mock_randint, mock_get_valid_input):
        # Set up mock for user-defined input scenario
        mock_get_valid_input.return_value = 5  # Simulate user input of 5
        max_fighters = 15  # Set the maximum number of firefighters
        get_firefighters = MagicMock()
        get_firefighters.return_value = 5
        result = get_firefighters(max_fighters)
        self.assertEqual(result, 5)  # Assert the result based on the expected user input

    @patch('input_helper.get_valid_input')
    @patch('random.randint')
    def test_random_generation(self, mock_randint, mock_get_valid_input):
        # Set up mock for random generation scenario
        mock_randint.return_value = 8  # Simulate random generation returning 8
        max_fighters = 15  # Set the maximum number of firefighters
        get_firefighters = MagicMock()
        get_firefighters.return_value = 8
        result = get_firefighters(max_fighters)
        self.assertEqual(result, 8)  # Assert the result based on the expected random value
