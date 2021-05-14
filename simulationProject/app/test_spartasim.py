import unittest
import math
from spartasim import SpartaSimulation


class SpartaSimulationTests(unittest.TestCase, SpartaSimulation):

    def setUp(self):
        self.months_to_simulate = 20
        self.min_trainees = 20
        self.max_trainees = 30
        self.sim = SpartaSimulation(self.months_to_simulate, self.min_trainees, self.max_trainees)

    def test_month_inc(self):
        initial_value = self.sim.current_month
        self.sim.month_inc()
        self.assertIs(type(self.sim.current_month), int)
        self.assertEqual(self.sim.current_month, initial_value + 1)
        self.sim.current_month = initial_value

    def test_trainee_generator(self):
        random_number = self.sim.trainee_generator()
        self.assertIs(type(self.sim.current_month), int)
        self.assertGreaterEqual(random_number, self.sim.min_trainees)
        self.assertLessEqual(random_number, self.sim.max_trainees)

    def test_trainee_df(self):
        self.assertEqual(
            sum((type(value) != int and value != "None") for value in self.sim.trainee_df["Assigned centre ID"]), 0)
        self.assertEqual(sum(value not in self.sim.courses for value in self.sim.trainee_df["Course type"]), 0)
        self.assertEqual(sum(value < 1 for value in self.sim.trainee_df["Start month"]), 0)
        self.assertEqual(sum(value < 13 for value in self.sim.trainee_df["Stop month"]), 0)
        self.assertEqual(sum(value not in ["Waiting", "Training", "Benched", "Working"] for value in self.sim.trainee_df["Status"]), 0)

    def test_centre_df(self):
        self.assertEqual(
            sum(value not in ['Boot camp', 'Hub', 'Tech centre'] for value in self.sim.centres_df["Centre type"]), 0)
        self.assertEqual(sum(type(value) != int for value in self.sim.centres_df["Trainee count"]), 0)
        self.assertEqual(sum(value not in ["Open", "Closed", "Full"] for value in self.sim.centres_df["Centre status"]),
                         0)

        for value in range(0, len(self.sim.centres_df)):
            if self.sim.centres_df["Centre type"][value] == "Hub":
                self.assertEqual(self.sim.centres_df["Max capacity"][value], 100)
                self.assertEqual(self.sim.centres_df["Centre course type"][value], "None")

            if self.sim.centres_df["Centre type"][value] == "Boot camp":
                self.assertEqual(self.sim.centres_df["Max capacity"][value], 500)
                self.assertEqual(self.sim.centres_df["Centre course type"][value], "None")

            if self.sim.centres_df["Centre type"][value] == "Tech centre":
                self.assertEqual(self.sim.centres_df["Max capacity"][value], 200)
                self.assertNotEqual(self.sim.centres_df["Centre course type"][value], "None")

    # def test_client_orders_df(self):
    #     self.assertEqual(sum(value != "None" for value in self.sim.client_orders_df["Client ID"]), 0)
    #     self.assertEqual(sum(value not in self.sim.courses for value in self.sim.client_orders_df["Month advert placed"]), 0)
    #     self.assertEqual(sum(value != 0 for value in self.sim.client_orders_df["Month advert removed"]), 0)
    #     self.assertEqual(sum(value != 0 for value in self.sim.client_orders_df["Course requested"]), 0)
    #     self.assertEqual(sum(value != "Waiting" for value in self.sim.client_orders_df["Spartans requested"]), 0)
    #     self.assertEqual(sum(value != "Waiting" for value in self.sim.client_orders_df["Spartans obtained"]), 0)
    #     self.assertEqual(sum(value != "Waiting" for value in self.sim.client_orders_df["Happy? (T/F)"]), 0)

    def test_count_dfs(self):
        self.assertGreaterEqual(len(self.sim.trainee_df), self.sim.min_trainees * self.months_to_simulate)
        self.assertLessEqual(len(self.sim.trainee_df), self.sim.max_trainees * self.months_to_simulate)

        self.assertEqual(len(self.sim.centres_df), math.ceil(1 / 2 * (self.months_to_simulate + 1)))

        self.assertEqual(len(self.sim.client_orders_df), self.months_to_simulate - 11)

    def test_centre_type(self):
        for value in range(0, len(self.sim.trainee_df)):
            if self.months_to_simulate < 13:
                self.assertIn(self.sim.trainee_df["Status"][value], ["Waiting", "Training"])
            else:
                self.assertIn(self.sim.trainee_df["Status"][value], ["Waiting", "Training", "Benched", "Working"])

        self.assertLessEqual(len(self.sim.centres_df[(self.sim.centres_df['Centre type'] == "Hub") & (
                self.sim.centres_df["Centre status"] == "Open")]), 3)
        self.assertLessEqual(len(self.sim.centres_df[(self.sim.centres_df['Centre type'] == "Boot camp") & (
                self.sim.centres_df["Centre status"] == "Open")]), 2)

        for value in range(0, len(self.sim.centres_df)):
            if (self.sim.centres_df["Centre type"][value] != "Boot camp" and
                    self.sim.centres_df["Trainee count"][value] < 25):

                # print(self.sim.centres_df.iloc[value:value + 1])
                # print(self.sim.centres_df["Centre type"][value] != "Boot camp", self.sim.centres_df["Trainee count"][value] < 25)
                # print(self.sim.centres_df["Centre type"][value] == "Boot camp", self.sim.centres_df["Low att month counter"][value] >= 3)
                self.assertEqual(self.sim.centres_df["Centre status"][value], "Closed")

            elif (self.sim.centres_df["Centre type"][value] == "Boot camp" and
                  self.sim.centres_df["Low att month counter"][value] >= 3):

                # print(self.sim.centres_df.iloc[value:value + 1])
                # print(self.sim.centres_df["Centre type"][value] != "Boot camp", self.sim.centres_df["Trainee count"][value] < 25)
                # print(self.sim.centres_df["Centre type"][value] == "Boot camp", self.sim.centres_df["Low att month counter"][value] >= 3)
                self.assertEqual(self.sim.centres_df["Centre status"][value], "Closed")

            else:
                # print(self.sim.centres_df.iloc[value:value + 1])
                # print(self.sim.centres_df["Centre type"][value] != "Boot camp", self.sim.centres_df["Trainee count"][value] < 25)
                # print(self.sim.centres_df["Centre type"][value] == "Boot camp", self.sim.centres_df["Low att month counter"][value] >= 3)
                self.assertIn(self.sim.centres_df["Centre status"][value], ["Open", "Full"])
