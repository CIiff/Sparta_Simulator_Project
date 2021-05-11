import unittest
from spartasim import SpartaSimulation


class SpartaSimulationTests(unittest.TestCase):
    sim = SpartaSimulation(4)

    def test_month_inc(self):
        initial_value = self.sim.current_month
        self.sim.month_inc()
        self.assertIs(type(self.sim.current_month), int)
        self.assertEqual(self.sim.current_month, initial_value + 1)
        self.sim.current_month = initial_value

    # tests get functions:
    def test_get_num_open_centres(self):
        self.assertEqual(self.sim.get_num_open_centres(), 0)

    def test_get_num_full_centres(self):
        self.assertEqual(self.sim.get_num_full_centres(), 0)

    def test_get_num_current_trainees(self):
        self.assertEqual(self.sim.get_num_current_trainees(), 0)

    def test_get_num_waiting_list(self):
        self.assertEqual(self.sim.get_num_waiting_list(), 0)

    def test_trainee_generator(self):
        self.assertGreaterEqual(self.sim.trainee_generator(), 20)
        self.assertLessEqual(self.sim.trainee_generator(), 30)

    def test_center_dict_keys(self):
        no_of_locs = self.sim.months // 2
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

    def test_count_full_centers(self):

        self.sim.centers = {1: 100, 2: 100, 3: 50}
        self.sim.count_full_centers()
        self.assertEqual(self.sim.num_full_centres, 2)

        self.sim.centers = {1: 0, 2: 0, 3: 50}
        self.sim.count_full_centers()
        self.assertEqual(self.sim.num_full_centres, 0)

        self.sim.centers = {1: 100, 2: 100, 3: 100}
        self.sim.count_full_centers()
        self.assertEqual(self.sim.num_full_centres, 3)

        self.sim.centers = {1: 100, 2: 100, 3: 50, 4: 30, 5: 100}
        self.sim.count_full_centers()
        self.assertEqual(self.sim.num_full_centres, 3)
