import unittest
from spartasim import SpartaSimulation


class TestSpartaSim (unittest.TestCase):

    sim = SpartaSimulation(4)

    def test_month_inc(self):
        initial_value = self.sim.current_month
        self.sim.month_inc()
        self.assertIs(type(self.sim.current_month), int)
        self.assertEqual(self.sim.current_month, initial_value+1)
        self.sim.current_month = initial_value
