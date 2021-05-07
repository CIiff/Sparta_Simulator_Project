# AS A user I WANT a get function SO THAT I can return the sim output

# number of open centres
# number of full centres
# number of trainees currently training
# number of trainees on the waiting list

def get_num_open_centres(self):
    return self.num_open_centres


def get_num_full_centres(self):
    return self.num_full_centres


def get_num_current_trainees(self):
    return self.num_current_trainees


def get_num_waiting_list(self):
    return self.num_waiting_list
