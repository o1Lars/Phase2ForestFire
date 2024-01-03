import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

from ...file_helper import check_planar_graph
import unittest
from unittest.mock import patch, MagicMock

class TestCheckPlanarGraph(unittest.TestCase):

    @patch('file_helper.gh.edges_planar')
    @patch('file_helper.time.sleep')
    @patch('builtins.print')
    def test_planar_graph(self, mock_print, mock_sleep, mock_edges_planar):
        mock_edges_planar.return_value = True
        result = check_planar_graph([(1, 2), (2, 3), (3, 1)])
        self.assertTrue(result)
        mock_print.assert_called()  # Add appropriate assert for print calls

    @patch('file_helper.gh.edges_planar')
    @patch('file_helper.time.sleep')
    @patch('builtins.print')
    def test_non_planar_graph(self, mock_print, mock_sleep, mock_edges_planar):
        mock_edges_planar.return_value = False
        result = check_planar_graph([(1, 2), (2, 3), (3, 4), (4, 1)])
        self.assertFalse(result)
        mock_print.assert_called()  # Add appropriate assert for print calls



if __name__ == '__main__':
    unittest.main()






