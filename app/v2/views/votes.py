from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v2.models.office_model import Office
from app.v2.models.user_model import User
from app.v2.models.vote_model import Vote
from app.v2.utils.validator import response, exists, response_error
from app.blueprints import v2 as bp
from flask_jwt_extended import (jwt_required)


@bp.route('/votes', methods=['POST', 'GET'])
@jwt_required
def vote():
    if request.method == 'POST':
        """ Create vote end point """

        data = request.get_json()

        if not data:
            return response_error("No data was provided", 400)

        try:
            created_by = data['createdBy']
            office = data['office']
            candidate = data['candidate']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        vote = Vote(created_by, office, candidate)

        if not vote.validate_object():
            return response_error(vote.error_message, vote.error_code)

        if not Office().find_by('id', office):
            return response_error('Selected Office does not exist', 404)
        if not User().find_by('id', candidate):
            return response_error('Selected User does not exist', 404)

        # append new vote to list
        vote.save()

        # return added vote
        return response("Success", 201, [vote.as_json()])

    elif request.method == 'GET':
        """ Get all votes end point """

        return response('Success', 200, Vote().load_all())


@bp.route('/office/<int:office_id>/result', methods=['GET'])
@jwt_required
def get_results(office_id):
    """ Gets results """

    filtered = Vote().get_all(
        "SELECT office, candidate, COUNT(*) as result FROM votes WHERE office = '{}'\
             GROUP BY candidate, office".format(office_id))

    return response('Success', 200, filtered)
