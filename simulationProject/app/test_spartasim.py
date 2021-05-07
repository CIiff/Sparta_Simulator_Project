import unittest
from spartasim import SpartaSimulation


class SpartaSimulationTests (unittest.TestCase):

    sim = SpartaSimulation(4)

    def test_month_inc(self):
        initial_value = self.sim.current_month
        self.sim.month_inc()
        self.assertIs(type(self.sim.current_month), int)
        self.assertEqual(self.sim.current_month, initial_value+1)
        self.sim.current_month = initial_value

    #tests get functions:
    def test_get_num_open_centres(self):
        self.assertEqual(self.sim.get_num_open_centres(), 0)
    def test_get_num_full_centres(self):
        self.assertEqual(self.sim.get_num_full_centres(), 0)
    def test_get_num_current_trainees(self):
        self.assertEqual(self.sim.get_num_current_trainees(), 0)
    def test_get_num_waiting_list(self):
        self.assertEqual(self.sim.get_num_waiting_list(), 0)
