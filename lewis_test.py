import unittest
#from simulationProject.app.spartasim import SpartaSimulation
from Kathryn_test_file import SpartaSimulation

class GetTests(unittest.TestCase):

    sim = SpartaSimulation(4)

    def test_get_num_open_centres(self):
        self.assertEqual(self.sim.get_num_open_centres(), 0)

    def test_get_num_full_centres(self):
        self.assertEqual(self.sim.get_num_full_centres(), 0)

    def test_get_num_current_trainees(self):
        self.assertEqual(self.sim.get_num_current_trainees(), 0)

    def test_get_num_waiting_list(self):
        self.assertEqual(self.sim.get_num_waiting_list(), 0)


