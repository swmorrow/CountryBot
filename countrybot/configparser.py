import os, configparser, sys

config = configparser.ConfigParser()
config.read('config.ini')

db = config['Data Management']['Database']
if 'unittest' in sys.modules.keys():
    db = config['Data Management']['Test database']

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__)).removesuffix('\\countrybot') # may not work on linux, untested
DATA_DIRECTORY =  os.path.join(ABSOLUTE_PATH, os.path.dirname(config['Data Management']['Data directory'] + '\\'))
DATABASE = os.path.join(DATA_DIRECTORY, db)

ICON = config['Graphics']['Icon']

LOG_LEVEL = config['Logging']['Log level']
LOG_FILE = config['Logging']['Log file']

print('unittest' in sys.modules.keys())
