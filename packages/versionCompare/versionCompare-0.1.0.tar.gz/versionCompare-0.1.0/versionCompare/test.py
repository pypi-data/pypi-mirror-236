import unittest
from versionComparison import compare_versions


class NumberComparatorTester(unittest.TestCase):
    # test cases for geater than
    def test_two_positive_number_for_greater_than(self):
        output = compare_versions("2.1", "1.0")
        self.assertEqual(output, 1)

    def test_two_negative_number_for_greater_than(self):
        output = compare_versions("2.1", "1.1.2")
        self.assertEqual(output, 1)

    def test_two_mixed_numbers_for_greater_than(self):
        output = compare_versions("1.0.7", "1.0.6")
        self.assertEqual(output, 1)

     # test cases for less than

    def test_two_positive_number_for_less_than(self):
        output = compare_versions("2.1.3", "2.2.3")
        self.assertEqual(output, -1)

    def test_two_negative_number_for_less_than(self):
        output = compare_versions("1.1.1", "1.2")
        self.assertEqual(output, -1)

        # test cases for equal to
    def test_two_positive_number_for_equal_to(self):
        output = compare_versions("2.1", "2.1")
        self.assertEqual(output, 0)

    def test_two_negative_number_for_equal_to(self):
        output = compare_versions("3.0", "3.1")
        self.assertEqual(output, -1)

    def test_two_mixed_numbers_for_equal_to(self):
        output = compare_versions("0.1.0", "0.1.1")
        self.assertEqual(output, -1)


unittest.main()
