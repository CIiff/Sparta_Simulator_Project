import unittest
from import SpartaSimulation

class GetTests(unittest.TestCase):

    calc = SpartaSimulation()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 4), 6)

    def test_sub(self):
        self.assertEqual(self.calc.sub(4, 2), 2)

    def test_mult(self):
        self.assertEqual(self.calc.mult(2, 2), 4)
        self.assertEqual(self.calc.mult(3, 5), 15)
#this needs to be run in terminal



def test_get_num_open_centres(self):
    self.assertEqual(self.calc.add(2), 6)


def test_get_num_full_centres(self):
    pass


def test_get_num_current_trainees(self):
    pass


def test_get_num_waiting_list(self):
    pass