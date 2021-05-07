class SpartaSimulation:

    def __init__(self, month):
        self.month = month
        self.current_month = 1
        self.num_open_centres = 0
        self.num_full_centres = 0
        self.num_current_trainees = 0
        self.num_waiting_list = 0

    def month_inc(self):
        self.current_month += 1

    def get_num_open_centres(self):
        return self.num_open_centres

    def get_num_full_centres(self):
        return self.num_full_centres

    def get_num_current_trainees(self):
        return self.num_current_trainees

    def get_num_waiting_list(self):
        return self.num_waiting_list








