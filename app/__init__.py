'''Creating app'''
import os
from flask import Flask, jsonify
from instance.config import app_config
from .v1.views.base_view import bp
from .v1.views import offices, parties, candidates, votes, users


def create_app(config_name):
    """ create app with specified configs """

    is_prod = os.environ.get('IS_HEROKU', None)
    if is_prod:
        config_name = 'development'

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(bp)

    @app.route('/')
    @app.route('/index')
    def index():
        """ THe welcome screen of the api """

        return jsonify({
            'status': 200, 'message': 'Welcome to the Politico API'
            })

    @app.errorhandler(404)
    def page_not_found(error):
        """ Handler for error 404 """

        return jsonify({
            'status': 404, 'message': 'The requested resource was not found'
            })

    @app.errorhandler(405)
    def method_not_allowed(error):
        """ Handler for error 405 """

        return jsonify({'status': 405, 'message': 'Method not allowed'})

    @app.errorhandler(400)
    def bad_request(error):
        """ Handler for error 400 """

        return jsonify({'status': 400, 'message': 'Please review your request and try again'})

    return app
