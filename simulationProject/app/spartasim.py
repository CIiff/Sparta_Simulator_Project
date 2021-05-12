import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

class SpartaSimulation:

    def __init__(self, months_to_simulate=12, min_hired_trainees=20, max_hired_trainees=30):
        self.stopping_month = months_to_simulate + 1
        self.current_month = 1
        self.num_waiting_list = 0
        self.min_trainees = min_hired_trainees
        self.max_trainees = max_hired_trainees
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Max capacity','Low att month counter', 'Centre course type','Centre status'])
        self.centre_types = {'Boot camp': 0, 'Hub': 0, 'Tech': {'Java':0,'C#':0,'Data':0,'DevOps':0,'Business':0}}
        self.available_centre_types = ['Boot camp', 'Hub', 'Tech Java']
        self.create_centre()
        #self.simulation_loop()

    def month_inc(self):
        self.current_month += 1

    def trainee_generator(self):
        self.monthly_generated_trainees = random.randint(self.min_trainees, self.max_trainees)

    def create_centre(self):
        tech_centre_type = random.choice(['Java', 'C#', 'Data', 'DevOps', 'Business'])

        hub_template = {'Centre type':'Hub', 'Trainee count':0, 'Max capacity':100, 'Low att month counter':0, 'Centre course type':'N/A', 'Centre status':'open'}
        #boot_camp_template = pd.DataFrame(pd.Series({'Centre type': 'Boot camp', 'Trainee count': 0, 'Max capacity': 500,'Low att month counter':0, 'Centre course type':'N/A', 'Centre status': 'open'}))
        tech_centre_template = pd.DataFrame({'Centre type': 'Tech centre', 'Trainee count': 0, 'Max capacity': 200,'Low att month counter':0, 'Centre course type':f'{tech_centre_type}', 'Centre status': 'open'})
        self.centres_df.append(hub_template,ignore_index=True)

    def count_centres(self):
        [centres_df['Centre type'] for element in self.centres_df]

    def assign_trainees_to_center(self):
        pass

    def simulation_loop(self):
        while self.current_month <= self.stopping_month:
            if self.current_month % 2 == 1 and self.current_month != 1:
                self.add_new_center()
            self.trainee_generator()
            self.month_inc()

a = SpartaSimulation()
print(a.centres_df)