from app.spartasim import SpartaSimulation
import configparser

# Read local `config.ini` file.
config = configparser.ConfigParser()
config.read('config.ini')
months = int(config.get('INPUT', 'months'))
min_new_monthly_trainees = float(config.get('INPUT', 'min_new_trainees_per_month'))
max_new_monthly_trainees = float(config.get('INPUT', 'max_new_trainees_per_month'))

new_train_mean = (min_new_monthly_trainees + max_new_monthly_trainees)/2.0
new_train_stdev = (new_train_mean - min_new_monthly_trainees)/3.0
N = 100

samples = stats.truncnorm.rvs(
          (min_new_monthly_trainees-new_train_mean)/new_train_stdev,
          (max_new_monthly_trainees-new_train_mean)/new_train_stdev,
          loc=new_train_mean, scale=new_train_stdev, size=months)
print(samples)
print(f"This simulation is running for {months} months")

SpartaSimulation_object = SpartaSimulation(months)
SpartaSimulation_object.plot_location_distributions()

print("Number of current trainees enrolled : " + str(SpartaSimulation_object.get_num_current_trainees()))

print("Number of open centres : " + str(SpartaSimulation_object.get_num_open_centres()))

print("Number of trainees in the waiting list : " + str(SpartaSimulation_object.get_num_waiting_list()))

print("Number of full centers : " + str(SpartaSimulation_object.get_num_full_centres()))
