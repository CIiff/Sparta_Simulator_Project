import random

# ignore proxy class
class Sim:

    def __init__(self, max_months):
        self.max_months = max_months
        self.centers = self.create_center()
        self.current_month = 1

    def month_inc(self):
        self.current_month += 1

    def simulation_loop(self):
        while self.current_month <= self.max_months and self.current_month != 1:

            if self.current_month % 2 == 1:
                self.add_new_center()

            self.trainee_generator()

            # updating centers



