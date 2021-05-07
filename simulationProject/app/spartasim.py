import random

class SpartaSimulation:

    centre_max_capacity = 100

    def __init__(self, month):
        self.month = month
        self.current_month = 1
        self.num_open_centres = 0
        self.num_full_centres = 0
        self.num_current_trainees = self.trainee_generator()
        self.num_waiting_list = 0
        self.centers = self.create_center()

    def month_inc(self):
        self.current_month += 1

    def trainee_generator(self):
        total_trainees = 0
        for month in range(self.month):
            new_trainees = random.randint(20, 30)
            total_trainees += new_trainees
        return total_trainees

    def get_num_open_centres(self):
        return self.num_open_centres

    def get_num_full_centres(self):
        return self.num_full_centres

    def get_num_current_trainees(self):
        return self.num_current_trainees

    def get_num_waiting_list(self):
        return self.num_waiting_list

    def create_center(self):
        return {1:0}

    def add_new_center(self):
        newcenter_id = len(self.centers.keys()) + 1
        self.centers.update({newcenter_id: 0})









