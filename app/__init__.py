'''Creating app'''
import os
from flask import Flask, jsonify, Blueprint, redirect
from instance.config import app_config
from .v1.views import offices, parties, candidates, votes, users
from .v2.views import offices as v2_offices
from .v2.views import candidates as v2_candidates
from .v2.views import votes as v2_votes
from .v2.views import users as v2_users, parties as v2_parties
from .v2.db.database_config import Database
from app.blueprints import bp, v2
from flask_jwt_extended import JWTManager


def create_app(config_name):
    """ create app with specified configs """

    is_prod = os.environ.get('IS_HEROKU', None)
    if is_prod:
        config_name = 'development'
        os.environ["DATABASE_URL"] = "dbname='politico_db' host='127.0.0.1' port='5432' user='politico' password='politica'"

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # create the database
    create_db(config_name)

    # register blueprints
    app.register_blueprint(v2)
    app.register_blueprint(bp)

    jwt = JWTManager(app)

    @app.route('/docs')
    def docs():
        """ Documentation"""

        return redirect('https://app.swaggerhub.com/apis-docs/Bedan/kura-yangu/2.0')

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


def create_db(config_name):
    """ Create all db tables """

    try:
        db = Database(config_name)
        db.init_connection()
        db.create_db()
        db.create_super_user()

    except Exception as error:
        print('Error creating the database: {}'.format(str(error)))
