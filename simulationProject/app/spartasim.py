import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import csv

class SpartaSimulation:

    def __init__(self, months_to_simulate=12, min_hired_trainees=20, max_hired_trainees=30):
        self.stopping_month = months_to_simulate + 1
        self.current_month = 1
        self.num_waiting_list = 0
        self.min_trainees = min_hired_trainees
        self.max_trainees = max_hired_trainees
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Max capacity','Low att month counter', 'Centre course type','Centre status'])
        #self.centre_types = {'Boot camp': 0, 'Hub': 0, 'Tech': {'Java':0,'C#':0,'Data':0,'DevOps':0,'Business':0}}
        self.available_centre_types = ['Boot camp', 'Hub', 'Tech centre']
        self.available_tech_centre_types = ['Java','C#','Data','DevOps','Business']
        #self.create_centre()
        self.count_centres()
        #self.simulation_loop()

    def month_inc(self):
        self.current_month += 1

    def trainee_generator(self):
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

        #pop boot camp from available centre types
        if counted_centre_types['Boot camp'] >= 2:
            self.available_centre_types.remove('Boot camp')
        if 'Boot camp' not in self.available_centre_types and counted_centre_types['Boot camp'] < 2:
            self.available_centre_types.append('Boot camp')

        # pop tech centre from available centre types
        if self.available_tech_centre_types == []:
            self.available_centre_types.remove('Tech centre')
        if not self.available_tech_centre_types == []:
            self.available_centre_types.append('Tech centre')

        #prioritise filling centres with less than 25 and tech centres, the fill hub and boot camp

    def assign_trainees_to_center(self):
        pass

    def simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1 and self.current_month != 1:
                self.add_new_center()
            self.trainee_generator()
            self.month_inc()

a = SpartaSimulation()