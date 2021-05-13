import random
import numpy as np
from collections import Counter
import pandas as pd
import scipy.stats as stats
import logging




class SpartaSimulation:

    def __init__(self, months_to_simulate, min_hired_trainees, max_hired_trainees, centre_size=100):
        self.stopping_month = months_to_simulate + 1
        self.current_month = 1
        self.num_waiting_list = 0
        self.min_trainees = min_hired_trainees
        self.max_trainees = max_hired_trainees
        self.trainee_df = pd.DataFrame(columns=["Assigned centre ID", "Course type", "Start month", "Stop month",
                                                "Status"])
        self.courses = ["Data", "DevOps", "C#", "Java", "Business"]
        self.status_list = ["Waiting", "Training", "Benched"]
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Max capacity', 'Low att month counter',
                                                'Centre course type', 'Centre status'])
        # self.centre_types = {'Boot camp': 0, 'Hub': 0, 'Tech': {'Java':0,'C#':0,'Data':0,'DevOps':0,'Business':0}}
        self.available_centre_types = ['Boot camp', 'Hub', 'Tech centre']
        self.available_tech_centre_types = ['Java', 'C#', 'Data', 'DevOps', 'Business']
        # self.simulation_loop()

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

<<<<<<< HEAD
        # self.monthly_generated_trainees = random.randint(self.min_trainees, self.max_trainees)
=======
    def assign_trainees_to_center(self):
        self.num_waiting_list += self.num_monthly_trainees
        for key in self.centers.keys():
            trainees = min(self.centre_max_capacity - self.centers[key], self.num_waiting_list)
            self.centers[key] += trainees
            self.trainees_in_training += trainees
            self.num_waiting_list -= trainees
        self.monthly_generated_trainees = random.randint(self.min_trainees, self.max_trainees)
>>>>>>> alex

    def create_centre(self):
        self.count_centres()
        chosen_centre_type = random.choice(self.available_centre_types)
        tech_centre_type = random.choice(self.available_tech_centre_types)

        hub_template = [{'Centre type': 'Hub', 'Trainee count': 0, 'Max capacity': 100, 'Low att month counter': 0,
                         'Centre course type': 'None', 'Centre status': 'open'}]
        boot_camp_template = [{'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500,
                               'Low att month counter': 0, 'Centre course type': 'None', 'Centre status': 'open'}]
        tech_centre_template = [{'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,
                                 'Low att month counter': 0, 'Centre course type': f'{tech_centre_type}',
                                 'Centre status': 'open'}]

        if chosen_centre_type == 'Hub':
            self.centres_df = self.centres_df.append(hub_template, ignore_index=True)
        if chosen_centre_type == 'Boot camp':
            self.centres_df = self.centres_df.append(boot_camp_template, ignore_index=True)
        if chosen_centre_type == 'Tech centre':
            self.centres_df = self.centres_df.append(tech_centre_template, ignore_index=True)

    def count_centres(self):
        counted_tech_centre_types = dict(Counter(self.centres_df['Centre course type']))
        print(counted_tech_centre_types.items())

        for k, v in counted_tech_centre_types.items():
            if k in self.available_tech_centre_types and v >= 1:
                self.available_tech_centre_types.remove(k)

        counted_centre_types = dict(Counter(self.centres_df['Centre type']))

        # pop hub from available centre types
        if counted_centre_types['Hub'] >= 3:
            self.available_centre_types.remove('Hub')
        if 'Hub' not in self.available_centre_types and counted_centre_types['Hub'] < 3:
            self.available_centre_types.append('Hub')

        # pop boot camp from available centre types
        if counted_centre_types['Boot camp'] >= 2:
            self.available_centre_types.remove('Boot camp')
<<<<<<< HEAD

        if 'Boot camp' not in self.available_centre_types and counted_centre_types['Boot camp'] < 2:
            self.available_centre_types.append('Boot camp')

        # pop tech centre from available centre types
=======
>>>>>>> alex
        if self.available_tech_centre_types == []:
            self.available_centre_types.remove('Tech centre')
        if not self.available_tech_centre_types == []:
            self.available_centre_types.append('Tech centre')

        # prioritise filling centres with less than 25 and tech centres, the fill hub and boot camp

    def simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1 and self.current_month != 1:
                self.add_new_center()
            self.trainee_generator()
            self.month_inc()

    def assign_trainee_to_course(self):
        num_new_trainees = self.trainee_generator()
        for trainee in range(num_new_trainees):
            row_data = {"Assigned centre ID": "None", "Course type": random.choice(self.courses), "Start month": 0,
                        "Stop month": 0, "Status": "Waiting"}
            self.trainee_df = self.trainee_df.append(row_data, ignore_index=True)

    def complete_trainees(self):
        self.assign_trainee_to_course()
        for index in self.trainee_df.loc[self.trainee_df["Stop month"] == self.current_month].index:
            self.trainee_df.loc[index, "Assigned centre ID"] = "None"
            self.trainee_df.loc[index, "Status"] = "Benched"
            self.centres_df["Trainee count"] -= 1
        return self.trainee_df

    def print_centre_information(self):
        if self.current_month == self.stopping_month:
            log_type = 20
        else:
            log_type = 10

        logging.log(log_type, f"Centre Information for month {self.current_month}:")

        centre_status = ["Open", "Full", "Closed"]
        for status in centre_status:
            total = self.centres_df.loc[self.centres_df['Centre status'] == status].count()[0]
            bootcamp = self.centres_df.loc[
                (self.centres_df['Centre status'] == status) & (self.centres_df['Centre type'] == 'Boot camp')].count()[
                0]
            hub = self.centres_df.loc[
                (self.centres_df['Centre status'] == status) & (self.centres_df['Centre type'] == 'Hub')].count()[0]
            tech_centre = self.centres_df.loc[(self.centres_df['Centre status'] == status) & (
                        self.centres_df['Centre type'] == 'Tech centre')].count()[0]

            logging.log(log_type, f"Number of Centres which are {status.lower()}: {total}")
            logging.log(log_type, f"    Boot camps   : {bootcamp}")
            logging.log(log_type, f"    Hubs         : {hub}")
            logging.log(log_type, f"    Tech Centres : {tech_centre}\n")

        logging.log(log_type, f"\n")

    def print_trainee_information(self):
        if self.current_month == self.stopping_month:
            log_type = 20
        else:
            log_type = 10

        logging.log(log_type, f"Trainee Information for month {self.current_month}:")

        status_list = ["Waiting", "Training", "Benched"]
        for status in status_list:

            total = self.trainee_df.loc[self.trainee_df['Status'] == status].count()[0]
            data = self.trainee_df.loc[
                (self.trainee_df['Status'] == status) & (self.trainee_df['Course type'] == "Data")].count()[0]
            devops = self.trainee_df.loc[
                (self.trainee_df['Status'] == status) & (self.trainee_df['Course type'] == "DevOps")].count()[0]
            java = self.trainee_df.loc[
                (self.trainee_df['Status'] == status) & (self.trainee_df['Course type'] == "Java")].count()[0]
            c_sharp = self.trainee_df.loc[
                (self.trainee_df['Status'] == status) & (self.trainee_df['Course type'] == "C#")].count()[0]
            business = self.trainee_df.loc[
                (self.trainee_df['Status'] == status) & (self.trainee_df['Course type'] == "Business")].count()[0]

            logging.log(log_type, f"Number of trainees which are {status.lower()}: {total}")
            logging.log(log_type, f"    Data     : {data}")
            logging.log(log_type, f"    DevOps   : {devops}")
            logging.log(log_type, f"    Java     : {java}")
            logging.log(log_type, f"    C#       : {c_sharp}")
            logging.log(log_type, f"    Business : {business}\n")

        logging.log(log_type, f"\n")
