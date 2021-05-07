import unittest
#from simulationProject.app.spartasim import SpartaSimulation
from Kathryn_test_file import SpartaSimulation

class GetTests(unittest.TestCase):

    sim = SpartaSimulation(4)

    #tests get functions:
    def test_get_num_open_centres(self):
        self.assertEqual(self.sim.get_num_open_centres(), 0)
    def test_get_num_full_centres(self):
        self.assertEqual(self.sim.get_num_full_centres(), 0)
    def test_get_num_current_trainees(self):
        self.assertEqual(self.sim.get_num_current_trainees(), 0)
    def test_get_num_waiting_list(self):
        self.assertEqual(self.sim.get_num_waiting_list(), 0)

    def test_trainee_generator(self):
        self.assertGreaterEqual(self.sim.trainee_generator(), 20*self.sim.month)
        self.assertLessEqual(self.sim.trainee_generator(), 30*self.sim.month)

    def test_get_num_trainees(self):
        self.assertGreaterEqual(self.sim.get_num_trainees(), 20*self.sim.month)
        self.assertLessEqual(self.sim.get_num_trainees(), 30*self.sim.month)


