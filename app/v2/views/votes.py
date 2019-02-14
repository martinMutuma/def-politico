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


@bp.route('/votes/user/<int:id>', methods=['GET'])
@jwt_required
def get_user_votes(id):
    """ Gets all votes a user has cast """

    filtered = Vote().find_all_by('createdby', id)

    return vote_response('Success', 200, len(filtered), filtered)


@bp.route('/votes/candidate/<int:id>', methods=['GET'])
@jwt_required
def get_candidate_votes(id):
    """ Gets all votes for a specific candidate """

    filtered = Vote().find_all_by('candidate', id)

    return vote_response(
        'Success', 200, len(filtered), filtered)


@bp.route('/votes/office/<int:id>', methods=['GET'])
@jwt_required
def get_office_votes(id):
    """ Gets all votes for a specific office """

    filtered = Vote().find_all_by('office', id)

    return vote_response(
        'Success', 200, len(filtered), filtered)


def vote_response(message, code, count, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data,
        "count": count
    }
    return make_response(jsonify(response), code)
