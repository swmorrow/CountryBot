import os

# Data storage config (may need to change gitignore)
DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), os.path.dirname('data\\'))
PICKLE_PATH = os.path.join(DATA_DIRECTORY, 'RPDate.pickle')
DB_PATH = os.path.join(DATA_DIRECTORY, 'country_database.db')

# Date config
LOCALE = 'en_CA' # Note: If changing this, make sure to change command description in date.py to fit the set locale.
