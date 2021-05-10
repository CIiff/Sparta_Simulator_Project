import random
import matplotlib.pyplot as plt
import csv

class SpartaSimulation:

    centre_max_capacity = 100

    def __init__(self, month):
        self.month = month
        self.current_month = 1
        self.num_open_centres = 1
        self.num_full_centres = 0
        self.num_current_trainees = 0
        self.num_waiting_list = 0
        self.centers = {1:0}

    def month_inc(self):
        self.current_month += 1

    def trainee_generator(self):
        self.num_current_trainees = random.randint(20, 30)

    def get_num_open_centres(self):
        return self.num_open_centres

    def get_num_full_centres(self):
        return self.num_full_centres

    def get_num_current_trainees(self):
        return self.num_current_trainees

    def get_num_waiting_list(self):
        return self.num_waiting_list

    def add_new_center(self):
        newcenter_id = len(self.centers.keys()) + 1
        self.centers.update({newcenter_id: 0})

    def plot_location_distributions(self):
        fig, ax = plt.subplots()
        ax.set_xlabel('Centre number')
        ax.set_ylabel('Trainees in centre')
        # add legend - wait for new init parameter to keep count of total trainees
        for i in sorted(self.centers.keys()):
            ax.bar(i, self.centers[i])
        ax.bar('waiting list', self.num_waiting_list, color='r')
        fig.savefig('filled_centres_bar.pdf')

    def csv_write(self, csv_file_name):
        with open(csv_file_name, 'w') as out_csv:
            fieldnames = ['trainee location', 'number of trainees']
            writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
            for i in sorted(self.centers.keys()):
                writer.writerow({'Centre '+str(i): self.centers[i]})
            writer.writerow({'waiting list': self.num_waiting_list})
