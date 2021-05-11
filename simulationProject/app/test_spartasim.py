import unittest
from spartasim import SpartaSimulation


class SpartaSimulationTests(unittest.TestCase):

    def setUp(self):
        self.months_to_simulate = 10
        self.sim = SpartaSimulation(self.months_to_simulate)

    def test_month_inc(self):
        initial_value = self.sim.current_month
        self.sim.month_inc()
        self.assertIs(type(self.sim.current_month), int)
        self.assertEqual(self.sim.current_month, initial_value + 1)
        self.sim.current_month = initial_value

    # tests get functions:
    def test_get_num_open_centres(self):
        self.assertEqual(self.sim.get_num_open_centres(), 6)

    def test_get_num_full_centres(self):
        self.assertEqual(self.sim.get_num_full_centres(), 2)

    def test_get_num_current_trainees(self):
        self.assertGreaterEqual(self.sim.trainees_in_training, self.months_to_simulate*20)
        self.assertLessEqual(self.sim.trainees_in_training, self.months_to_simulate*30)

    def test_get_num_waiting_list(self):
        self.assertEqual(self.sim.get_num_waiting_list(), 0)

    def test_trainee_generator(self):
        self.sim.trainee_generator()
        self.assertGreaterEqual(self.sim.num_monthly_trainees, 20)
        self.assertLessEqual(self.sim.num_monthly_trainees, 30)

    def test_center_dict_keys(self):
        no_of_locs = self.months_to_simulate // 2
        self.assertEqual(list(self.sim.centers.keys()), [i for i in range(1, no_of_locs + 2)])

    def test_assign_trainee_to_center(self):

        for v in self.sim.centers.values():
            self.assertLessEqual(v, 100)

        self.sim.num_monthly_trainees = 0

        self.sim.centers = {1: 50}
        self.sim.num_waiting_list = 150
        self.sim.assign_trainees_to_center()
        self.assertEqual(self.sim.centers[1], 100)
        self.assertEqual(self.sim.num_waiting_list, 100)

        self.sim.centers = {1: 50}
        self.sim.num_waiting_list = 30
        self.sim.assign_trainees_to_center()
        self.assertEqual(self.sim.centers[1], 80)
        self.assertEqual(self.sim.num_waiting_list, 0)

        self.sim.centers = {1: 100, 2: 50}
        self.sim.num_waiting_list = 20
        self.sim.assign_trainees_to_center()
        self.assertEqual(self.sim.centers[1], 100)
        self.assertEqual(self.sim.centers[2], 70)
        self.assertEqual(self.sim.num_waiting_list, 0)

        self.sim.centers = {1: 0, 2: 0}
        self.sim.num_waiting_list = 150
        self.sim.assign_trainees_to_center()
        self.assertEqual(self.sim.centers[1], 100)
        self.assertEqual(self.sim.centers[2], 50)
        self.assertEqual(self.sim.num_waiting_list, 0)

        self.sim.centers = {1: 100, 2: 90}
        self.sim.num_waiting_list = 20
        self.sim.assign_trainees_to_center()
        self.assertEqual(self.sim.centers[1], 100)
        self.assertEqual(self.sim.centers[2], 100)
        self.assertEqual(self.sim.num_waiting_list, 10)

        self.sim = SpartaSimulation(self.months_to_simulate)