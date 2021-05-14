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


def main(months_to_run, min_trainees, max_trainees, login):

    if login == "INFO":
        logging.basicConfig(format='%(message)s', level=20)
    elif login == "DEBUG":
        logging.basicConfig(format='%(message)s', level=10)

    print(f"This simulation is running for {months} months")

    SpartaSimulation(months_to_run, min_trainees, max_trainees)


if __name__ == '__main__':
    main(months, min_new_monthly_trainees, max_new_monthly_trainees, login_type)
