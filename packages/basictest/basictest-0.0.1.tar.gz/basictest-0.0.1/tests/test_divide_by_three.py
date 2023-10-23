import unittest
import sys, os

sys.path.append(os.path.abspath(os.path.join("..", "src")))
from divide.divide_by_three import divide_by_three

class TestDivideByThree(unittest.TestCase):
    def test_divide_by_three(self):
        self.assertEqual(divide_by_three(12), 4)

unittest.main()