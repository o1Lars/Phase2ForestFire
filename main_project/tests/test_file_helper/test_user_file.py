import sys
import os

# Ensure other modules can be opened while perfoming tests.
# Get the absolute path of the directory containing your modules
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Add the module directory to the Python path
sys.path.insert(0, main_project_dir)

from ...file_helper import user_file
import unittest
from unittest.mock import patch

class TestUserFile(unittest.TestCase):

    @patch('builtins.open', create=True)
    def test_successful_file_read(self, mock_open):
        mock_file = mock_open.return_value
        mock_file.__enter__.return_value.read.return_value = "File content"
        result = user_file("path/to/folder", "file.txt")
        self.assertEqual(result, "File content")

    @patch('builtins.open', side_effect=FileNotFoundError("File not found"))
    def test_file_not_found(self, mock_open):
        result = user_file("path/to/folder", "nonexistent_file.txt")
        self.assertIsInstance(result, FileNotFoundError)
        self.assertEqual(str(result), "File not found")

    @patch('builtins.open', side_effect=IOError("IO error"))
    def test_io_error(self, mock_open):
        result = user_file("path/to/folder", "file.txt")
        self.assertIsInstance(result, IOError)
        self.assertEqual(str(result), "IO error")

    @patch('builtins.open', side_effect=KeyboardInterrupt("Ctrl+C"))
    def test_keyboard_interrupt(self, mock_open):
        with self.assertRaises(SystemExit):
            user_file("path/to/folder", "file.txt")

if __name__ == '__main__':
    unittest.main()
