import unittest
from unittest.mock import patch
import os
from ...input_helper import get_valid_file

class TestGetValidFile(unittest.TestCase):

    @patch('builtins.input', side_effect=['nonexistent_file.txt', 'existing_file.txt'])
    def test_invalid_then_valid_file(self, mocked_input):
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.side_effect = [False, True]
            result = get_valid_file("Enter a file path: ")
            self.assertEqual(result, 'existing_file.txt')

    @patch('builtins.input', side_effect=['file1.txt', 'file2.txt', 'file3.txt'])
    def test_invalid_files_then_valid(self, mocked_input):
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.side_effect = [False, False, True]
            result = get_valid_file("Enter a file path: ", "File must exist")
            self.assertEqual(result, 'file3.txt')

    @patch('builtins.input', side_effect=['dir/', 'file4.txt'])
    def test_directory_input_then_valid_file(self, mocked_input):
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.side_effect = [False, True]
            result = get_valid_file("Enter a file path: ", "File must exist")
            self.assertEqual(result, 'file4.txt')

    @patch('builtins.input', side_effect=KeyboardInterrupt('Ctrl+C'))
    def test_keyboard_interrupt(self, mocked_input):
        with self.assertRaises(SystemExit):
            get_valid_file("Enter a file path: ")

if __name__ == '__main__':
    unittest.main()