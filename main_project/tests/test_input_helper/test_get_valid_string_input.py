import unittest
from unittest.mock import patch
from ...input_helper import get_valid_string_input

class TestGetValidStringInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['hello', 'world'])
    def test_valid_string_input(self, mocked_input):
        result = get_valid_string_input("Enter a string: ")
        self.assertEqual(result, "hello")

    @patch('builtins.input', side_effect=['123', 'abc'])
    def test_invalid_string_input_then_valid(self, mocked_input):
        result = get_valid_string_input("Enter a string: ", "Should be a string")
        self.assertEqual(result, "abc")

    @patch('builtins.input', side_effect=['y', 'yes', 'n', 'no'])
    def test_yes_no_input(self, mocked_input):
        result = get_valid_string_input("Yes or no (y/n): ", yes_no=True)
        self.assertIn(result, ["y", "yes", "n", "no"])

    @patch('builtins.input', side_effect=['abc', '1', 'yes', '2', 'n'])
    def test_mixed_input(self, mocked_input):
        result = get_valid_string_input("Enter a string or yes/no (y/n): ", yes_no=True)
        self.assertIn(result, ["abc", "yes", "no"])

    @patch('builtins.input', side_effect=KeyboardInterrupt('Ctrl+C'))
    def test_keyboard_interrupt(self, mocked_input):
        with self.assertRaises(SystemExit):
            get_valid_string_input("Enter a string: ")

if __name__ == '__main__':
    unittest.main()