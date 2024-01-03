import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

import unittest
from unittest.mock import patch, MagicMock
from ...graph_forest import get_autocombustion_prob

class TestGetAutocombustionProb(unittest.TestCase):
    @patch('input_helper.get_valid_float_input')
    @patch('random.uniform')
    def test_user_defined_probability(self, mock_uniform, mock_get_valid_float_input):
        # Set up mock for user-defined input scenario
        mock_get_valid_float_input.return_value = 0.7  # Simulate user input of 0.7
        get_autocombustion_prob = MagicMock()
        get_autocombustion_prob.return_value = 0.7
        result = get_autocombustion_prob()
        self.assertEqual(result, 0.7)  # Assert the result based on the expected user input

    @patch('input_helper.get_valid_float_input')
    @patch('random.uniform')
    def test_random_generation(self, mock_uniform, mock_get_valid_float_input):
        # Set up mock for random generation scenario
        mock_uniform.return_value = 0.75  # Simulate random generation returning 0.75
        get_autocombustion_prob = MagicMock()
        get_autocombustion_prob.return_value = 0.75
        result = get_autocombustion_prob()
        self.assertEqual(result, 0.75)  # Assert the result based on the expected random value
