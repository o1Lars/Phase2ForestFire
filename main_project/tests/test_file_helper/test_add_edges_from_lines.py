import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

from ...file_helper import add_edges_from_lines
import unittest

class TestAddEdgesFromLines(unittest.TestCase):

    def test_valid_edges(self):
        lines = ["(1, 2)\n", "(3, 4)\n", "(5, 6)\n"]
        result = add_edges_from_lines(lines)
        self.assertEqual(result, [(1, 2), (3, 4), (5, 6)])

    def test_invalid_edges(self):
        lines = ["(1, a)\n", "(3, 4, 5)\n", "# Comment line\n"]
        result = add_edges_from_lines(lines)
        self.assertEqual(result, [])

    def test_mixed_valid_invalid_edges(self):
        lines = ["(1, 2)\n", "(3, a)\n", "# Comment line\n", "(5, 6)\n"]
        result = add_edges_from_lines(lines)
        self.assertEqual(result, [(1, 2), (5, 6)])

    def test_empty_lines(self):
        lines = ["\n", "\n", "\n"]
        result = add_edges_from_lines(lines)
        self.assertEqual(result, [])

    def test_edge_cases(self):
        lines = ["(1, 2)\n", "(3, 4)\n", "(5, 6)\n"]
        lines.append(f"({2 ** 31 - 1}, {2 ** 31})\n")  # Testing edge case for large integers
        result = add_edges_from_lines(lines)
        self.assertEqual(result, [(1, 2), (3, 4), (5, 6), (2147483647, 2147483648)])  # Ensure it still handles valid input

if __name__ == '__main__':
    unittest.main()