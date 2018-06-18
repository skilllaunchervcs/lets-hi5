import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database
MONGO_DBNAME='hi5'
MONGO_URI='mongodb://admin:mongo123@ds263460.mlab.com:63460/hi5'
