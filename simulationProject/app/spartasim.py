import random
import matplotlib.pyplot as plt
import csv
import pandas as pd


class SpartaSimulation:

    def __init__(self, months_to_simulate=12, centre_size=100, min_hired_trainees=20, max_hired_trainees=30):

        self.stopping_month = months_to_simulate + 1
        self.current_month = 1
        self.num_open_centres = 1
        self.num_full_centres = 0
        self.num_monthly_trainees = 0
        self.num_waiting_list = 0
        self.centers = {1: 0}
        self.centre_max_capacity = centre_size
        self.trainees_in_training = 0
        self.min_trainees = min_hired_trainees
        self.max_trainees = max_hired_trainees
        self.simulation_loop()
        self.trainee_df = pd.DataFrame(columns=["Assigned centre ID", "Course type", "Start month", "Stop month",
                                                "Status"])
        self.courses = ["Data", "DevOps", "C#", "Java", "Business"]
        self.status_list = ["Waiting", "Training", "Benched"]

    def month_inc(self):
        self.current_month += 1

    def trainee_generator(self):
        self.num_monthly_trainees = random.randint(self.min_trainees, self.max_trainees)

    def get_num_open_centres(self):
        return self.num_open_centres

    def get_num_full_centres(self):
        return self.num_full_centres

    def get_num_current_trainees(self):
        return self.trainees_in_training

    def get_num_waiting_list(self):
        return self.num_waiting_list

    def add_new_center(self):
        new_center_id = len(self.centers.keys()) + 1
        self.num_open_centres += 1
        self.centers.update({new_center_id: 0})

    def assign_trainees_to_center(self):
        self.num_waiting_list += self.num_monthly_trainees
        for key in self.centers.keys():
            trainees = min(self.centre_max_capacity - self.centers[key], self.num_waiting_list)
            self.centers[key] += trainees
            self.trainees_in_training += trainees
            self.num_waiting_list -= trainees

    def simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1 and self.current_month != 1:
                self.add_new_center()
            self.trainee_generator()
            self.assign_trainees_to_center()
            self.count_full_centers()
            self.month_inc()

    def count_full_centers(self):
        # Checks for each center if they're at max capacity yet.
        self.num_full_centres = sum(value == self.centre_max_capacity for value in self.centers.values())

# Trainee data frame
# index trainee id
# assigned centre id, course type, start month, stop month, status (benched/training/waiting)

# self.trainee_df = pd.DataFrame(columns=["Assigned centre ID", "Course type", "Start month", "Stop month",
#                                                 "Status"])
    def assign_trainee_to_course(self):
        num_new_trainees =
        for trainee in self.centers.values():
            row_data = {}
            row_data["Course type"] = random.choice(self.courses)
            row_data["Assigned centre ID"] = "None"
            row_data["Start month"] = 0
            row_data["Stop month"] = 0
            row_data["Status"] = "Waiting"
            self.trainee_df = self.trainee_df.append(row_data, ignore_index=True)
