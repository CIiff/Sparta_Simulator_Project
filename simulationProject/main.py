from app.spartasim import SpartaSimulation
import configparser

# Read local `config.ini` file.
config = configparser.ConfigParser()
config.read('config.ini')
months = int(config.get('INPUT', 'months'))

print(f"This simulation is running for {months} months")

SpartaSimulation_object = SpartaSimulation(months)
SpartaSimulation_object.plot_location_distributions()

print("Number of current trainees enrolled : " + str(SpartaSimulation_object.get_num_current_trainees()))

print("Number of open centres : " + str(SpartaSimulation_object.get_num_open_centres()))

print("Number of trainees in the waiting list : " + str(SpartaSimulation_object.get_num_waiting_list()))

print("Number of full centers : " + str(SpartaSimulation_object.get_num_full_centres()))
