""" File to run the server """
import os
from app import create_app

config_name = os.getenv("APP_SETTINGS")
"""Gets the app settings defined in the .env file"""


app = create_app(config_name)
"""defining the configuration to be used"""


if __name__ == '__main__':
    app.run()
