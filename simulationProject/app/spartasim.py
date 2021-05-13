import random
import pandas as pd
import scipy.stats as stats
import logging


class SpartaSimulation:

    def __init__(self, months_to_simulate, min_hired_trainees, max_hired_trainees):
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
        fillable_centres = self.centres_df[
            (self.centres_df['Trainee count'] < self.centres_df['Max capacity']) &
            (self.centres_df['Centre status'] == 'Open')]

        for centre_index, centre_row in fillable_centres.iterrows():
            spaces = centre_row['Max capacity'] - centre_row['Trainee count']
            if centre_row['Centre type'] == 'Hub' or centre_row['Centre type'] == 'Boot camp':
                for i in range(spaces):
                    if self.trainee_df.loc[self.trainee_df['Status'] == 'Waiting'].count()[0] == 0:
                        break
                    else:
                        trainee = self.trainee_df[self.trainee_df['Status'] == 'Waiting'].index.to_list()[0]
                        self.trainee_df.loc[trainee, ['Assigned centre ID']] = centre_index
                        self.trainee_df.loc[trainee, ['Status']] = 'Training'
                        self.trainee_df.loc[trainee, ["Start month"]] = self.current_month
                        self.trainee_df.loc[trainee, ["Stop month"]] = self.current_month + 12
                        self.centres_df.loc[centre_index, ['Trainee count']] += 1

            elif centre_row['Centre type'] == 'Tech centre':
                for i in range(spaces):
                    if self.trainee_df.loc[(self.trainee_df['Status'] == 'Waiting') & (
                            self.trainee_df['Course type'] == centre_row['Centre course type'])].count()[0] == 0:
                        break
                    else:
                        trainee = self.trainee_df[(self.trainee_df['Status'] == 'Waiting') &
                                                  (self.trainee_df['Course type'] == centre_row[
                                                      'Centre course type'])].index.to_list()[0]
                        self.trainee_df.loc[trainee, ['Assigned centre ID']] = centre_index
                        self.trainee_df.loc[trainee, ['Status']] = 'Training'
                        self.trainee_df.loc[trainee, ["Start month"]] = self.current_month
                        self.trainee_df.loc[trainee, ["Stop month"]] = self.current_month + 12
                        self.centres_df.loc[centre_index, ['Trainee count']] += 1

    def create_centre(self):
        self.count_centres()
        chosen_centre_type = random.choice(self.available_centre_types)
        tech_centre_type = random.choice(self.courses)

        hub_template = [{'Centre type': 'Hub', 'Trainee count': 0, 'Max capacity': 100,
                         'Low att month counter': 0, 'Centre course type': 'None', 'Centre status': 'Open'}]
        boot_camp_template = [{'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500,
                               'Low att month counter': 0, 'Centre course type': 'None', 'Centre status': 'Open'}]
        tech_centre_template = [{'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,
                                 'Low att month counter': 0, 'Centre course type': f'{tech_centre_type}',
                                 'Centre status': 'Open'}]

        if chosen_centre_type == 'Hub':
            self.centres_df = self.centres_df.append(hub_template, ignore_index=True)
        elif chosen_centre_type == 'Boot camp':
            self.centres_df = self.centres_df.append(boot_camp_template, ignore_index=True)
        elif chosen_centre_type == 'Tech centre':
            self.centres_df = self.centres_df.append(tech_centre_template, ignore_index=True)

    def count_centres(self):
        bootcamp = self.centres_df.loc[(self.centres_df['Centre status'] == "Open") &
                                       (self.centres_df['Centre type'] == 'Boot camp')].count()[0]
        hub = self.centres_df.loc[(self.centres_df['Centre status'] == "Open") &
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
            new_order = {'Client ID': 1,
                         'Month advert placed': self.current_month, 'Month advert removed': self.current_month + 12,
                         'Course requested': client_course, 'Spartans requested': spartans_needed_rand,
                         'Spartans obtained': 0, 'Happy? (T/F)': "Neutral"}

            # append new_order to the dataframe
            self.client_orders_df = self.client_orders_df.append(new_order, ignore_index=True)

    def add_repeat_client_order(self):
        happy_client_index_list = self.client_orders_df.index[self.client_orders_df['Happy? (T/F)'] == "Happy"].tolist()
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
                                        'Spartans obtained': 0, 'Happy? (T/F)': "Neutral"}
                self.client_orders_df = self.client_orders_df.append(old_client_new_order, ignore_index=True)

    def end_of_client_order_resolve(self):
        # END-OF-ORDER CODE
        # fulfilled_index_list = []
        # time_up_index_list = []
        # for i, row in self.client_orders_df.iterrows():
        #     if int(row['Spartans requested']) == int(row['Spartans obtained']):
        #         fulfilled_index_list.append(i)
        #     elif int(self.current_month) == int(row['Month advert removed']):
        #         time_up_index_list.append(i)

        #fulfilled_index_list =list( self.client_orders_df.loc[(self.client_orders_df['Spartans requested']) ==self.client_orders_df['Spartans obtained']].index)
        #fulfilled_index_list = self.client_orders_df.index[self.client_orders_df['Spartans requested'] ==
           #                                                self.client_orders_df['Spartans obtained']].tolist()

        #time_up_index_list = list(self.client_orders_df.loc[self.current_month ==
        #                                                 self.client_orders_df['Month advert removed']] )
        # time_up_index_list = self.client_orders_df.index[self.current_month ==
        #                                                  self.client_orders_df['Month advert removed']].tolist()
        for index, i_row in self.client_orders_df.iterrows():  # i = index, i_row = all row info at index i
            # if successful: right part of 'and' statement prevents assignments for old orders in DF
            print(self.current_month)
            print(i_row)
            if (int(i_row['Spartans requested']) == int(i_row['Spartans obtained'])) and (int(self.current_month) <= int(i_row['Month advert removed'])):
                print("Yes")
                i_row['Month advert removed'] = self.current_month
                i_row['Happy? (T/F)'] = "Happy"
            # else: not enough spartans recruited
            elif int(self.current_month) == int(i_row['Month advert removed']):
                print("No")
                i_row['Happy? (T/F)'] = "Unhappy"

    def assign_new_trainees_to_data_frame(self):
        num_new_trainees = self.trainee_generator()
        for trainee in range(num_new_trainees):
            row_data = {"Assigned centre ID": "None", "Course type": random.choice(self.courses), "Start month": 0,
                        "Stop month": 0, "Status": "Waiting"}
            self.trainee_df = self.trainee_df.append(row_data, ignore_index=True)

    def graduating_trainees(self):
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
                    if self.trainee_df.loc[trainee]['Assigned centre ID'] == centreID:

                        self.trainee_df.loc[trainee]['Start month'] = 0
                        self.trainee_df.loc[trainee]['Stop month'] = 0
                        self.trainee_df.loc[trainee]['Status'] = 'Waiting'
                        self.trainee_df.loc[trainee]['Assigned centre ID'] = 'None'

            if self.centres_df.loc[centreID]['Trainee count'] < 25 and \
                    self.centres_df.loc[centreID]['Centre status'] == 'Open':
                self.centres_df.loc[centreID]['Low att month counter'] += 1
            else:
                self.centres_df.loc[centreID]['Low att month counter'] = 0

            if self.centres_df.loc[centreID]['Centre type'] == 'Boot camp' and \
                    self.centres_df.loc[centreID]['Low att month counter'] >= 3 and \
                    self.centres_df.loc[centreID]['Centre status'] == 'Open':
                update_centre()
                update_trainee()

            elif self.centres_df.loc[centreID]['Centre type'] == 'Hub' and \
                    self.centres_df.loc[centreID]['Low att month counter'] >= 1 and \
                    self.centres_df.loc[centreID]['Centre status'] == 'Open':
                update_centre()
                update_trainee()

            elif self.centres_df.loc[centreID]['Centre type'] == 'Tech centre' and \
                    self.centres_df.loc[centreID]['Low att month counter'] >= 1 and \
                    self.centres_df.loc[centreID]['Centre status'] == 'Open':
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

            self.graduating_trainees()

            self.assign_new_trainees_to_data_frame()

            self.assign_trainees_to_center()
            self.update_full_center_status()

            self.close_centre()

            self.add_new_client_order()
            self.add_repeat_client_order()
            self.orders_index_priority_and_assign()
            self.end_of_client_order_resolve()

            self.print_centre_information()
            self.print_trainee_information()

            self.month_inc()

    def update_full_center_status(self):
        for center in self.centres_df.loc[self.centres_df["Centre status"] == "Open"].index:
            if int(self.centres_df.loc[center, ["Trainee count"]]) == int(
                    self.centres_df.loc[center, ["Max capacity"]]):
                self.centres_df.loc[center, ["Centre status"]] = "Full"

    def orders_index_priority_and_assign(self):
        # rank the orders by earliest (lowest index) to latest (highest index)
        # should be done automatically via autoincrement in client_orders_df
        order_index_list = self.client_orders_df.index.to_list()
        for i in order_index_list:
            # order_assign_grads changes client_orders_df: no need for return
            self.order_assign_grads(i)

    def order_assign_grads(self, order_index):
        # use order_index to assign trainee graduates to clients
        # order_row = the client order's row in client_orders_df
        order_row = self.client_orders_df.iloc[order_index]
        client_course = order_row['Course requested']
        # Get trainees whose course matches the client order's need
        wanted_trainees_index_list = self.trainee_df[(self.trainee_df["Course type"] == client_course) &
                                                     (self.trainee_df["Status"] == "Benched")].index.to_list()
        for wanted_trainee_index in wanted_trainees_index_list:
            perm_trainee_record = self.trainee_df.iloc[wanted_trainee_index]
            if int(self.client_orders_df.loc[order_index, ['Spartans requested']]) > int(self.client_orders_df.loc[order_index, ['Spartans obtained']]):
                # assign trainee to the order
                self.client_orders_df.loc[order_index, ['Spartans obtained']] += 1
                #order_row['Spartans obtained'] += 1
                # Once trainee has been assigned, change the trainee's status in the (permanent) self.trainee_df
                self.trainee_df.loc[wanted_trainee_index, ["Status"]] = "Working"
                #perm_trainee_record["Status"] = "Working"
