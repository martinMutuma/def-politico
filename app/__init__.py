'''Creating app'''
import os
from flask import Flask, jsonify, Blueprint, redirect, url_for
from instance.config import app_config
from .v1.views import offices, parties, candidates, votes, users
from .v2.views import offices as v2_offices
from .v2.views import candidates as v2_candidates
from .v2.views import votes as v2_votes
from .v2.views import users as v2_users, parties as v2_parties
from .v2.db.database_config import Database
from app.blueprints import bp, v2
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_name):
    """ create app with specified configs """

    is_prod = os.environ.get('IS_HEROKU', None)
    if is_prod:
        config_name = 'development'

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # create the database
    create_db(config_name)

    # register blueprints
    app.register_blueprint(v2)
    app.register_blueprint(bp)

    CORS(app)
    jwt = JWTManager(app)

    @app.route('/')
    @app.route('/index')
    def index():
        """ THe welcome screen of the api """

        return redirect(url_for('flasgger.apidocs'))

    @app.errorhandler(500)
    def internal_server(error):
        """ Handler for error 500 """

        return jsonify({
            'status': 500, 'message': 'We cannot process your request at this time'
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

        return jsonify({
            'status': 400,
            'message': 'Please review your request and try again'
        })

    @app.errorhandler(415)
    def unsuported_media_type(error):
        """ Handler for error 415 """

        return jsonify({
            'status': 415,
            'message': 'Unsupported Media Type'
        })

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        token_type = expired_token['type']
        return jsonify({
            'status': 401,
            'error': 'The {} token has expired'.format(token_type)
        }), 401

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
