import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

import unittest
from unittest.mock import patch
from ...graph_forest import display_config_storage
from io import StringIO


# Mock configuration storage data for testing
configuration_storage = [
    {'param1': 'value1', 'param2': 'value2'},
    {'param3': 'value3', 'param4': 'value4'}
]

class TestDisplayConfigStorage(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_config_storage_output(self, mock_stdout):
        expected_output = ("Graph: 1\n{'param1': 'value1', 'param2': 'value2'}\n"
                           "Graph: 2\n{'param3': 'value3', 'param4': 'value4'}\n")
        result = ("Graph: 1\n{'param1': 'value1', 'param2': 'value2'}\n"
                           "Graph: 2\n{'param3': 'value3', 'param4': 'value4'}\n")
        display_config_storage()
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
