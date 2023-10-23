import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join("..", "src")))
from multiply.multiply_by_three import multiply_by_three

class TestMultiplyByThree(unittest.TestCase):
    def test_multiply_by_three(self):
        self.assertEqual(multiply_by_three(12), 36)

unittest.main()