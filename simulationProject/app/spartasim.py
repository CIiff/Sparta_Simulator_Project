import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import csv
import pandas as pd
import scipy.stats as stats


class SpartaSimulation:

    def __init__(self, months_to_simulate, min_hired_trainees, max_hired_trainees, centre_size=100):
        self.stopping_month = months_to_simulate + 1
        self.current_month = 1
        self.num_waiting_list = 0
        self.min_trainees = min_hired_trainees
        self.max_trainees = max_hired_trainees
        self.trainee_df = pd.DataFrame(columns=["Assigned centre ID", "Course type", "Start month", "Stop month","Status"])
        self.courses = ["Data", "DevOps", "C#", "Java", "Business"]
        self.status_list = ["Waiting", "Training", "Benched"]
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Max capacity','Low att month counter', 'Centre course type','Centre status'])
        #self.centre_types = {'Boot camp': 0, 'Hub': 0, 'Tech': {'Java':0,'C#':0,'Data':0,'DevOps':0,'Business':0}}
        self.available_centre_types = ['Boot camp', 'Hub', 'Tech centre']
        self.available_tech_centre_types = ['Java','C#','Data','DevOps','Business']
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
        tech_centre_type = random.choice(self.available_tech_centre_types)

        hub_template = [{'Centre type': 'Hub', 'Trainee count': 0, 'Max capacity': 100, 'Low att month counter': 0,'Centre course type': 'None', 'Centre status': 'open'}]
        boot_camp_template = [{'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500, 'Low att month counter': 0,'Centre course type': 'None', 'Centre status': 'open'}]
        tech_centre_template = [{'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200, 'Low att month counter': 0,'Centre course type': f'{tech_centre_type}', 'Centre status': 'open'}]

        if chosen_centre_type == 'Hub':
            self.centres_df = self.centres_df.append(hub_template, ignore_index=True)
        if chosen_centre_type == 'Boot camp':
            self.centres_df = self.centres_df.append(boot_camp_template, ignore_index=True)
        if chosen_centre_type == 'Tech centre':
            self.centres_df = self.centres_df.append(tech_centre_template, ignore_index=True)


    def count_centres(self):
        hub_template = {'Centre type': 'Hub', 'Trainee count': 0, 'Max capacity': 100, 'Low att month counter': 0,'Centre course type': 'None', 'Centre status': 'open'}
        boot_camp_template = {'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500,'Low att month counter': 0, 'Centre course type': 'None', 'Centre status': 'open'}
        tech_centre_template_Java = {'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,'Low att month counter': 0, 'Centre course type': 'Java', 'Centre status': 'open'}
        tech_centre_template_Business = {'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,'Low att month counter': 0, 'Centre course type': 'Business','Centre status': 'open'}
        tech_centre_template_Data = {'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,'Low att month counter': 0, 'Centre course type': 'Data', 'Centre status': 'open'}
        rows = [hub_template, boot_camp_template, hub_template, boot_camp_template, tech_centre_template_Java,tech_centre_template_Business, tech_centre_template_Data]

        df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Max capacity', 'Low att month counter', 'Centre course type','Centre status'])
        df = df.append(rows, ignore_index=True)

        counted_tech_centre_types = dict(Counter(df['Centre course type']))
        for k, v in counted_tech_centre_types.items():
            if v >= 1:
                self.available_tech_centre_types.remove(k)

        counted_centre_types = dict(Counter(df['Centre type']))
        if counted_centre_types['Hub'] >= 3:
            self.available_centre_types.remove('Hub')
        #functionality to add back onto list
        #if 'hub' not in list and counted hubs < 3:
            #add 'hub' back to list
        if counted_centre_types['Boot camp'] >= 2:
            self.available_centre_types.remove('Boot camp')
        if self.available_tech_centre_types == []:
            self.available_centre_types.remove('Tech centre')

        print(self.available_centre_types, self.available_tech_centre_types)

    def simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1 and self.current_month != 1:
                self.add_new_center()
            self.trainee_generator()
            self.month_inc()


    def assign_trainee_to_course(self):
        num_new_trainees = self.trainee_generator()
        for trainee in range(num_new_trainees):
            row_data = {"Course type": random.choice(self.courses), "Assigned centre ID": "None",
                        "Start month": 0, "Stop month": 0, "Status": "Waiting"}
            self.trainee_df = self.trainee_df.append(row_data, ignore_index=True)

a = SpartaSimulation()

