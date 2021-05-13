import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import csv
from tabulate import tabulate


class SpartaSimulation:

    def __init__(self, months_to_simulate=120, min_hired_trainees=20, max_hired_trainees=30):
        self.stopping_month = months_to_simulate + 1
        self.current_month = 1
        self.num_waiting_list = 0
        self.min_trainees = min_hired_trainees
        self.max_trainees = max_hired_trainees
        self.trainee_df = pd.DataFrame(columns=["Assigned centre ID", "Course type", "Start month", "Stop month","Status"])
        self.courses = ["Data", "DevOps", "C#", "Java", "Business"]
        self.status_list = ["Waiting", "Training", "Benched"]
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Max capacity','Low att month counter', 'Centre course type','Centre status'])
        self.available_centre_types = ['Boot camp', 'Hub', 'Tech centre']
        self.simulation_loop()

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

        self.monthly_generated_trainees = random.randint(self.min_trainees, self.max_trainees)

    def create_centre(self):
        self.count_centres()
        chosen_centre_type = random.choice(self.available_centre_types)
        tech_centre_type = random.choice(self.courses)

        hub_template = [{'Centre type': 'Hub', 'Trainee count': 0, 'Max capacity': 100, 'Low att month counter': 0,'Centre course type': 'None', 'Centre status': 'Open'}]
        boot_camp_template = [{'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500, 'Low att month counter': 0,'Centre course type': 'None', 'Centre status': 'Open'}]
        tech_centre_template = [{'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200, 'Low att month counter': 0,'Centre course type': f'{tech_centre_type}', 'Centre status': 'Open'}]

        if chosen_centre_type == 'Hub':
            self.centres_df = self.centres_df.append(hub_template, ignore_index=True)
        elif chosen_centre_type == 'Boot camp':
            self.centres_df = self.centres_df.append(boot_camp_template, ignore_index=True)
        elif chosen_centre_type == 'Tech centre':
            self.centres_df = self.centres_df.append(tech_centre_template, ignore_index=True)

        self.centre_debug_prints(chosen_centre_type)

    def count_centres(self):
        bootcamp = self.centres_df.loc[
            (self.centres_df['Centre status'] == "Open") &
            (self.centres_df['Centre type'] == 'Boot camp')].count()[0]

        hub = self.centres_df.loc[
            (self.centres_df['Centre status'] == "Open") &
            (self.centres_df['Centre type'] == 'Hub')].count()[0]

        # pop hub from available centre types
        if 'Hub' in self.available_centre_types:
            if hub >= 3:
                self.available_centre_types.remove('Hub')
        if 'Hub' not in self.available_centre_types and hub < 3:
            self.available_centre_types.append('Hub')

        #pop boot camp from available centre types
        if 'Boot camp' in self.available_centre_types:
            if bootcamp >= 2:
                self.available_centre_types.remove('Boot camp')
        if 'Boot camp' not in self.available_centre_types and bootcamp < 2:
            self.available_centre_types.append('Boot camp')

        #prioritise filling centres with less than 25 and tech centres, the fill hub and boot camp

    def centre_debug_prints(self, chosen_centre_type):
        print('MONTH:', self.current_month, '/ ', self.available_centre_types)
        print('CHOSEN: ', chosen_centre_type)
        print(tabulate(self.centres_df))
        print('////////////////////')

    def simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1:
                self.create_centre()
            self.trainee_generator()
            self.month_inc()


    def assign_trainee_to_course(self):
        num_new_trainees = self.trainee_generator()
        for trainee in range(num_new_trainees):
            row_data = {"Course type": random.choice(self.courses), "Assigned centre ID": "None",
                        "Start month": 0, "Stop month": 0, "Status": "Waiting"}
            self.trainee_df = self.trainee_df.append(row_data, ignore_index=True)

a = SpartaSimulation()

