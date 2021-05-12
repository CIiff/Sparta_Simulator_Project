import random
import matplotlib.pyplot as plt
import csv
import pandas as pd
import scipy.stats as stats


class SpartaSimulation:

    def __init__(self, months_to_simulate, min_hired_trainees, max_hired_trainees, centre_size=100):
        self.course_types = ['Data', 'Java', 'C#', 'DevOps', 'Business']
        self.centre_types = ['Boot Camp', 'Tech', 'Hub']
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
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Low att month counter',
                                                'Centre course type', 'Max centre capacity', 'Centre status'])

    def month_inc(self):
        self.current_month += 1

    def trainee_generator(self):
        new_train_mean = (self.min_trainees + self.max_trainees)/2.0
        new_train_stdev = (new_train_mean - self.min_trainees)/3.0
        num_new_trainees = float(stats.truncnorm.rvs(
                  (self.min_trainees-new_train_mean)/new_train_stdev,
                  (self.max_trainees-new_train_mean)/new_train_stdev,
                  loc=new_train_mean, scale=new_train_stdev, size=1))
        return round(num_new_trainees)

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
            #self.count_full_centers()
            self.month_inc()

    def assign_trainee_to_course(self):
        num_new_trainees = self.trainee_generator()
        for trainee in range(num_new_trainees):
            row_data = {"Course type": random.choice(self.courses), "Assigned centre ID": "None",
                        "Start month": 0, "Stop month": 0, "Status": "Waiting"}
            self.trainee_df = self.trainee_df.append(row_data, ignore_index=True)

    def complete_trainees(self):
        self.assign_trainee_to_course()
        for index in self.trainee_df.loc[self.trainee_df["Stop month"] == self.current_month].index:
            self.trainee_df.loc[index, "Assigned centre ID"] = "None"
            self.trainee_df.loc[index, "Status"] = "Benched"
            self.centres_df["Trainee count"] -= 1
        return self.trainee_df
