'''Creating app'''
import os
from flask import Flask
from instance.config import app_config
from .v1.views.base_view import bp
from .v1.views import offices, parties, candidates, votes, users


def create_app(config_name):
    """ create app with specified configs """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(bp)

    return app
