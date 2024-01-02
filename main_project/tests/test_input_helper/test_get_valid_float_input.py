import unittest
from unittest.mock import patch
from ...input_helper import get_valid_float_input


class TestGetValidFloatInput(unittest.TestCase):

    @patch('builtins.input', side_effect=['abc', '5.0'])
    def test_invalid_input_then_valid(self, mocked_input):
        result = get_valid_float_input("Enter an integer: ")
        self.assertEqual(result, 5.0)

    @patch('builtins.input', side_effect=['0.1', '0.2', '0.4'])
    def test_within_range(self, mocked_input):
        result = get_valid_float_input("Enter an integer: ", min=0.2, max=0.5)
        self.assertEqual(result, 0.2)

    @patch('builtins.input', side_effect=['1', 'abc', '0.3'])
    def test_outside_range_then_valid(self, mocked_input):
        result = get_valid_float_input("Enter an integer: ", min=0.3, max=0.5)
        self.assertEqual(result, 0.3)

    @patch('builtins.input', side_effect=['0.1', 'abc', '15'])
    def test_valid_then_invalid_input(self, mocked_input):
        result = get_valid_float_input("Enter an integer: ", max=0.8)
        self.assertEqual(result, 0.1)

    @patch('builtins.input', side_effect=KeyboardInterrupt('Ctrl+C'))
    def test_keyboard_interrupt(self, mocked_input):
        with self.assertRaises(SystemExit):
            get_valid_float_input("Enter an integer: ", max=12)


if __name__ == '__main__':
    unittest.main()