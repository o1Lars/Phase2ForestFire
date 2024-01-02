import unittest
from unittest.mock import patch
from ...input_helper import get_valid_input


class TestGetValidInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['abc', '5'])
    def test_invalid_input_then_valid(self, mocked_input):
        result = get_valid_input("Enter an integer: ")
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=['2', '10', '15'])
    def test_within_range(self, mocked_input):
        result = get_valid_input("Enter an integer: ", min=5, max=12)
        self.assertEqual(result, 10)

    @patch('builtins.input', side_effect=['15', 'abc', '7'])
    def test_outside_range_then_valid(self, mocked_input):
        result = get_valid_input("Enter an integer: ", min=5, max=12)
        self.assertEqual(result, 7)

    @patch('builtins.input', side_effect=['10', 'abc', '15'])
    def test_valid_then_invalid_input(self, mocked_input):
        result = get_valid_input("Enter an integer: ", max=12)
        self.assertEqual(result, 10)

    @patch('builtins.input', side_effect=KeyboardInterrupt('Ctrl+C'))
    def test_keyboard_interrupt(self, mocked_input):
        with self.assertRaises(SystemExit):
            get_valid_input("Enter an integer: ", max=12)


if __name__ == '__main__':
    unittest.main()