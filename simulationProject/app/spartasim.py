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
        self.client_orders_df = pd.DataFrame(columns=['Client ID', 'Month advert placed', 'Month advert removed',
                                                      'Course requested', 'Spartans requested', 'Spartans obtained',
                                                      'Happy? (T/F)'])
        # self.centre_types = {'Boot camp': 0, 'Hub': 0, 'Tech': {'Java':0,'C#':0,'Data':0,'DevOps':0,'Business':0}}
        self.available_centre_types = ['Boot camp', 'Hub', 'Tech centre']
        self.new_simulation_loop()

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

    def assign_trainees_to_center(self):
        self.num_waiting_list += self.num_monthly_trainees
        for key in self.centers.keys():
            trainees = min(self.centre_max_capacity -
                           self.centers[key], self.num_waiting_list)
            self.centers[key] += trainees
            self.trainees_in_training += trainees
            self.num_waiting_list -= trainees
        self.monthly_generated_trainees = random.randint(
            self.min_trainees, self.max_trainees)

    def create_centre(self):
        self.count_centres()
        chosen_centre_type = random.choice(self.available_centre_types)
        tech_centre_type = random.choice(self.available_tech_centre_types)

        hub_template = [{'Centre type': 'Hub', 'Trainee count': 0, 'Max capacity': 100,
                         'Low att month counter': 0, 'Centre course type': 'None', 'Centre status': 'Open'}]
        boot_camp_template = [{'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500,
                               'Low att month counter': 0, 'Centre course type': 'None', 'Centre status': 'Open'}]
        tech_centre_template = [{'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,
                                 'Low att month counter': 0, 'Centre course type': f'{tech_centre_type}', 'Centre status': 'Open'}]

        if chosen_centre_type == 'Hub':
            self.centres_df = self.centres_df.append(
                hub_template, ignore_index=True)
        elif chosen_centre_type == 'Boot camp':
            self.centres_df = self.centres_df.append(
                boot_camp_template, ignore_index=True)
        elif chosen_centre_type == 'Tech centre':
            self.centres_df = self.centres_df.append(
                tech_centre_template, ignore_index=True)

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

        # pop boot camp from available centre types
        if 'Boot camp' in self.available_centre_types:
            if bootcamp >= 2:
                self.available_centre_types.remove('Boot camp')
        if 'Boot camp' not in self.available_centre_types and bootcamp < 2:
            self.available_centre_types.append('Boot camp')

    def add_new_client_order(self):
        if self.current_month >= 13:
            # variables below apply for returning AND new clients
            client_course = random.choice(self.courses)
            spartans_needed_rand = random.choice(range(15, 51))
            if len(self.client_orders_df) == 0:  # should only occur for first DF entry
                new_client_id = 1
            else:
                new_client_id = int(max(self.client_orders_df['Client ID']) + 1)
            new_order = {'Client ID': new_client_id,
                         'Month advert placed': self.current_month, 'Month advert removed': self.current_month + 12,
                         'Course requested': client_course, 'Spartans requested': spartans_needed_rand,
                         'Spartans obtained': 0, 'Happy? (T/F)': True}

            # append new_order to the dataframe
            self.client_orders_df.append(new_order, ignore_index=True)

    def add_repeat_client_order(self):
        happy_client_index_list = self.client_orders_df.index[self.client_orders_df['Happy? (T/F)']].tolist()
        # if DF empty, should be no happy clients
        for happy_index in happy_client_index_list:
            # get row info for each index with a 'happy' client - so unhappy clients never place new orders.
            retrieval_row = self.client_orders_df.iloc[happy_index, :]
            if retrieval_row['Month advert removed'] == (self.current_month - 12):
                # only take new orders from existing happy clients 12 months after their previous order was
                # successfully completed
                client_course = random.choice(self.courses)
                spartans_needed_rand = random.choice(range(15, 51))
                old_client_new_order = {'Client ID': retrieval_row['Client ID'],
                                        'Month advert placed': self.current_month,
                                        'Month advert removed': self.current_month + 12,
                                        'Course requested': client_course, 'Spartans requested': spartans_needed_rand,
                                        'Spartans obtained': 0, 'Happy? (T/F)': True}
                self.client_orders_df.append(old_client_new_order, ignore_index=True)

    def end_of_client_order_resolve(self):
        # END-OF-ORDER CODE
        fulfilled_index_list = self.client_orders_df.index[self.client_orders_df['Spartans requested'] ==
                                                           self.client_orders_df['Spartans obtained']].tolist()
        time_up_index_list = self.client_orders_df.index[self.current_month ==
                                                         self.client_orders_df['Month advert removed']].tolist()
        for index, i_row in self.client_orders_df.iterrows():  # i = index, i_row = all row info at index i
            # if successful: right part of 'and' statement prevents assignments for old orders in DF
            if (index in fulfilled_index_list) and (self.current_month <= i_row['Month advert removed']):
                i_row['Month advert removed'] = self.current_month
            # else: not enough spartans recruited
            elif index in time_up_index_list:
                i_row['Happy? (T/F)'] = False

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
            self.trainee_df = self.trainee_df.append(
                row_data, ignore_index=True)

    def graduating_trainees(self):
        # checks that if trainees are due to graduate, reassigns centre to 'none' and status to 'benched'
        self.assign_trainee_to_course()
        for index in self.trainee_df.loc[self.trainee_df["Stop month"] == self.current_month].index:
            x = self.trainee_df.loc[index, "Assigned centre ID"]
            self.trainee_df.loc[index, "Assigned centre ID"] = "None"
            self.trainee_df.loc[index, "Status"] = "Benched"
            self.centres_df.loc[x, ["Trainee count"]] -= 1

    def close_centre(self):

        def update_centre():
            self.centres_df.loc[centreID]['Centre status'] = 'Closed'
            self.centres_df.loc[centreID]['Trainee count'] = 0

        for centreID in self.centres_df.index:

            def update_trainee():
                for trainee in self.trainee_df.index:
                    if self.trainee_df.loc[trainee]['CentreID_FK'] == centreID:

                        self.trainee_df.loc[trainee]['Start month'] = 0
                        self.trainee_df.loc[trainee]['Stop month'] = 0
                        self.trainee_df.loc[trainee]['Status'] = 'Waiting'
                        self.trainee_df.loc[trainee]['Assigned centre ID'] = 'None'

            if self.centres_df.loc[centreID]['Trainee count'] < 25 and self.centres_df.loc[centreID]['Centre status'] == 'Open':
                self.centres_df.loc[centreID]['Low att month counter'] += 1
            else:
                self.centres_df.loc[centreID]['Low att month counter'] = 0

            if self.centres_df.loc[centreID]['Centre_type'] == 'Boot camp' and self.centres_df.loc[centreID]['Low att month counter'] >= 3 and self.centres_df.loc[centreID]['Centre status'] == 'Open':
                update_centre()
                update_trainee()

            elif self.centres_df.loc[centreID]['Centre_type'] == 'Hub' and self.centres_df.loc[centreID]['Low att month counter'] >= 1 and self.centres_df.loc[centreID]['Centre status'] == 'Open':
                update_centre()
                update_trainee()

            elif self.centres_df.loc[centreID]['Centre_type'] == 'Tech centre' and self.centres_df.loc[centreID]['Low att month counter'] >= 1 and self.centres_df.loc[centreID]['Centre status'] == 'Open':
                update_centre()
                update_trainee()

    def print_centre_information(self):
        if self.current_month == self.stopping_month:
            log_type = 20
        else:
            log_type = 10

        logging.log(
            log_type, f"Centre Information for month {self.current_month}:")

        centre_status = ["Open", "Full", "Closed"]
        for status in centre_status:
            total = self.centres_df.loc[self.centres_df['Centre status'] == status].count()[
                0]
            bootcamp = self.centres_df.loc[
                (self.centres_df['Centre status'] == status) & (self.centres_df['Centre type'] == 'Boot camp')].count()[
                0]
            hub = self.centres_df.loc[
                (self.centres_df['Centre status'] == status) & (self.centres_df['Centre type'] == 'Hub')].count()[0]
            tech_centre = self.centres_df.loc[(self.centres_df['Centre status'] == status) & (
                self.centres_df['Centre type'] == 'Tech centre')].count()[0]

            logging.log(
                log_type, f"Number of Centres which are {status.lower()}: {total}")
            logging.log(log_type, f"    Boot camps   : {bootcamp}")
            logging.log(log_type, f"    Hubs         : {hub}")
            logging.log(log_type, f"    Tech Centres : {tech_centre}\n")

        logging.log(log_type, f"\n")

    def print_trainee_information(self):
        if self.current_month == self.stopping_month:
            log_type = 20
        else:
            log_type = 10

        logging.log(
            log_type, f"Trainee Information for month {self.current_month}:")

        status_list = ["Waiting", "Training", "Benched", "Working"]
        for status in status_list:

            total = self.trainee_df.loc[self.trainee_df['Status'] == status].count()[
                0]
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

            logging.log(
                log_type, f"Number of trainees which are {status.lower()}: {total}")
            logging.log(log_type, f"    Data     : {data}")
            logging.log(log_type, f"    DevOps   : {devops}")
            logging.log(log_type, f"    Java     : {java}")
            logging.log(log_type, f"    C#       : {c_sharp}")
            logging.log(log_type, f"    Business : {business}\n")

        logging.log(log_type, f"\n")


    def new_simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1:
                self.create_centre()
            self.trainee_generator()
            self.graduating_trainees()
            self.assign_trainee_to_course()
            # assign trainee to centre method
            # close centres method
            # client methods
            self.add_new_client_order()
            self.add_repeat_client_order()
            self.end_of_client_order_resolve()
            # end of client methods
            self.print_centre_information()
            self.print_trainee_information()
            self.month_inc()
