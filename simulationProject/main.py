from app.spartasim import SpartaSimulation
import configparser

# Read local `config.ini` file.
config = configparser.ConfigParser()
config.read('config.ini')
post_code = config.get('INPUT', 'months')

