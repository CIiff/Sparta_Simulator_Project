import random

class SpartaSimulation:

    def __init__(self, month):
        self.month = month
        self.num_open_centres = 0
        self.num_full_centres = 0
        self.num_current_trainees = self.trainee_generator()
        self.num_waiting_list = 0

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

# AS A user
# I WANT a method to add a training centre
# SO THAT trainees can be enrolled in the centres

sim = SpartaSimulation(4)
print(sim.get_num_current_trainees())
