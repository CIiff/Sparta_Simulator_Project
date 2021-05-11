import random


class SpartaSimulation:

    def __init__(self, month):
        self.month = month
        self.current_month = 1
        self.num_open_centres = 1
        self.num_full_centres = 0
        self.num_current_trainees = 0
        self.num_waiting_list = 0
        self.centers = {1: 0}
        self.centre_max_capacity = 100

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
        new_center_id = len(self.centers.keys()) + 1
        self.centers.update({new_center_id: 0})

    def assign_trainees_to_center(self):
        self.num_waiting_list += self.num_current_trainees
        for key in self.centers.keys():
            trainees = min(self.centre_max_capacity - self.centers[key], self.num_waiting_list)
            self.centers[key] += trainees
            self.num_waiting_list -= trainees

    def simulation_loop(self):
        while self.current_month <= self.month:
            if self.current_month % 2 == 1 and self.current_month != 1:
                self.add_new_center()
            self.trainee_generator()
            self.assign_trainees_to_center()
            self.count_full_centers()
            self.month_inc()

    def count_full_centers(self):
        # Checks for each center if they're at max capacity yet.
        self.num_full_centres = sum(value == self.centre_max_capacity for value in self.centers.values())
