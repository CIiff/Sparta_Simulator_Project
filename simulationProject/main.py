from app.spartasim import SpartaSimulation
import configparser
import logging

# Read local `config.ini` file.
config = configparser.ConfigParser()
config.read('config.ini')
months = int(config.get('INPUT', 'months'))
min_new_monthly_trainees = float(config.get('INPUT', 'min_new_trainees_per_month'))
max_new_monthly_trainees = float(config.get('INPUT', 'max_new_trainees_per_month'))
login_type = config.get('INPUT', 'login_type')


def main(months, min_new_monthly_trainees, max_new_monthly_trainees, login_type):

    if login_type == "INFO":
        logging.basicConfig(format='%(message)s', level=20)
    elif login_type == "DEBUG":
        logging.basicConfig(format='%(message)s', level=10)

    print(f"This simulation is running for {months} months")
    SpartaSimulation_object = SpartaSimulation(months, min_new_monthly_trainees, max_new_monthly_trainees)
    print(SpartaSimulation_object.client_orders_df.to_string())

if __name__ == '__main__':
    main(months, min_new_monthly_trainees, max_new_monthly_trainees, login_type)
