from luke_test import Sim
import unittest


class PostcodeTests(unittest.TestCase):

    # function setup:
    function = Sim(3)

    def test_month_inc(self):
        self.function.month_inc()
        self.assertIs(type(self.function.current_month), int)
        self.assertEqual(self.function.current_month, 2)
