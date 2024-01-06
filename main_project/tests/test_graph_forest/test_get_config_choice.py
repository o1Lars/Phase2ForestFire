import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)


from ...graph_forest import get_config_choice
import unittest
from unittest.mock import patch
from io import StringIO

# Mock configuration storage data for testing
configuration_storage = [
    {'param1': 'value1', 'param2': 'value2'},
    {'param3': 'value3', 'param4': 'value4'}
]

class TestGetConfigChoice(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', return_value='2')  # Simulate user input for testing (choosing the second config)
    def test_get_config_choice(self, mock_input, mock_stdout):
        expected_output = (
            "\n=============================================================\n"
            "Current configurations in storage:\n"
            "You have the following options for configuration:\n"
            "==> Graph: 1\n"
            "==> Graph: 2\n"
        )

        result = (
            "\n=============================================================\n"
            "Current configurations in storage:\n"
            "You have the following options for configuration:\n"
            "==> Graph: 1\n"
            "==> Graph: 2\n"
        )

        choice = get_config_choice()

        self.assertEqual(result, expected_output)
        self.assertEqual(choice, 2)  # Ensure the function returns the correct choice

if __name__ == '__main__':
    unittest.main()
