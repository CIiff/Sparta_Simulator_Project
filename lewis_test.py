import unittest
from simulationProject.app.spartasim import SpartaSimulation

class GetTests(unittest.TestCase):

    test_sim_instance = SpartaSimulation()

    def test_get_num_open_centres(self):
        self.assertEqual(self.test_sim_instance.get_num_open_centres(), )

    def test_get_num_full_centres(self):
        self.assertEqual(self.test_sim_instance.get_num_full_centres(), )

    def test_get_num_current_trainees(self):
        self.assertEqual(self.test_sim_instance.get_num_current_trainees(), )

    def test_get_num_waiting_list(self):
        self.assertEqual(self.test_sim_instance.get_num_waiting_list(), )


