import os
import config

config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(config.__file__))
config.DATA_DIRECTORY =  os.path.join(config.ABSOLUTE_PATH, os.path.dirname(config.DATA_DIRECTORY + '\\'))
config.DATABASE = os.path.join(config.DATA_DIRECTORY, 'country_database.db')