import random
import matplotlib.pyplot as plt
import csv
import pandas as pd


class SpartaSimulation:

    def __init__(self, months_to_simulate=12, centre_size=100, min_hired_trainees=20, max_hired_trainees=30):
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
        self.centres_df = pd.DataFrame(columns=['Centre type', 'Trainee count', 'Low att month counter',
                                                'Centre course type', 'Max centre capacity', 'Centre status'])

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

    def plot_location_distributions(self):
        fig, ax = plt.subplots()
        ax.set_xlabel('Centre number')
        ax.set_ylabel('Trainees in centre')

        num_trainee_labels = []
        for i in sorted(self.centers.keys()):
            ax.bar(str(i), self.centers[i])
            num_trainee_labels.append(self.centers[i])
        ax.bar('waiting list', self.num_waiting_list, color='r')
        num_trainee_labels.append(self.num_waiting_list)
        for index, value in enumerate(num_trainee_labels):
            ax.text(index, (value + 2), str(value), ha='center', va='center')

        fig.savefig('filled_centres_bar.pdf')

    def csv_write(self, csv_file_name):
        with open(csv_file_name, 'w') as out_csv:
            fieldnames = ['trainee location', 'number of trainees']
            writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
            for i in sorted(self.centers.keys()):
                writer.writerow({'Centre '+str(i): self.centers[i]})
            writer.writerow({'waiting list': self.num_waiting_list})
        new_center_id = len(self.centers.keys()) + 1
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
