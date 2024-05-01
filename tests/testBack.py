import unittest
from back import (
    first_row,
    second_row,
    third_row,
    four_row,
    five_row,
    coordinates_counting,
    remainder,
    skan_codes,
    value_code,
    place_statistic_name,
    size_button,
    return_shift_key,
take_text
)

class TestYourModule(unittest.TestCase):
    def test_first_row(self):
        self.assertEqual(first_row(1), (0, 350))
        self.assertEqual(first_row(41), (0, 350))
        self.assertEqual(first_row(58), (897, 350))

    def test_second_row(self):
        self.assertEqual(second_row(14), (933, 400))
        self.assertEqual(second_row(59), (0, 400))

    def test_third_row(self):
        self.assertEqual(third_row(28), (1977, 450))
        self.assertEqual(third_row(43), (933, 400))
        self.assertEqual(third_row(61), (880, 450))

    def test_four_row(self):
        self.assertEqual(four_row(44), (144, 500))
        self.assertEqual(four_row(62), (0, 500))
        self.assertEqual(four_row(63), (850, 500))

    def test_five_row(self):
        self.assertEqual(five_row(57), (297, 550))
        self.assertEqual(five_row(64), (0, 550))
        self.assertEqual(five_row(68), (4981, 550))

    def test_coordinates_counting(self):
        self.assertEqual(coordinates_counting(2), (69, 350))
        self.assertEqual(coordinates_counting(12), (759, 350))

    def test_remainder(self):
        self.assertEqual(remainder(5, 3), 2)
        self.assertEqual(remainder(10, 3), 1)

    def test_skan_codes(self):
        self.assertEqual(skan_codes('\t'), 59)
        self.assertEqual(skan_codes('ё'), 41)
        self.assertEqual(skan_codes('ъ'), 27)

    def test_value_code(self):
        self.assertEqual(value_code(7), '6')
        self.assertEqual(value_code(58), 'delete')

    def test_place_statistic_name(self):
        self.assertEqual(place_statistic_name(3), (3, 0))
        self.assertEqual(place_statistic_name(9), (2, 3))
        self.assertEqual(place_statistic_name(15), (None, None))

    def test_size_button(self):
        self.assertEqual(size_button(1), (60, 50))
        self.assertEqual(size_button(58), (95, 50))
        self.assertEqual(size_button(67), (85, 50))
        self.assertEqual(size_button(71), (60, 25))

    def test_return_shift_key(self):
        self.assertEqual(return_shift_key(5), ';')
        self.assertEqual(return_shift_key(7), ':')

    def test_take_text(self):
        self.assertIsNotNone(take_text())
