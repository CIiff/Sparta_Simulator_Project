from app.spartasim import SpartaSimulation
import configparser

# Read local `config.ini` file.
config = configparser.ConfigParser()
config.read('config.ini')
months = config.get('INPUT', 'months')

print(months)

