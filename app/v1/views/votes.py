from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v1.models.vote_model import Vote
from app.v1.utils.validator import response, exists
from app.v1.blueprints import bp


votes_list = Vote.votes


@bp.route('/votes', methods=['POST', 'GET'])
def vote():

    message = 'Request was sent successfully'
    status = 200
    response_data = []
    
    if request.method == 'POST':
        """ Create vote end point """

        data = request.get_json()

        if data:
            try:
                created_by = data['createdBy']
                office = data['office']
                candidate = data['candidate']

                vote = Vote(created_by, office, candidate)

                if vote.validate_object():
                    # append new vote to list
                    vote.save()

                    # return added vote
                    message = "Vote created successfully"
                    response_data = [vote.as_json()]
                    status = 201
                else:
                    message = vote.error_message
                    status = vote.error_code

            except KeyError as e:
                message = "{} field is required".format(e.args[0])
                status = 400
        else:
            message = "No data was provided"
            status = 400

    elif request.method == 'GET':
        """ Get all votes end point """
        response_data = votes_list

    return response(message, status, response_data)


@bp.route('/votes/user/<int:id>', methods=['GET'])
def get_user_votes(id):
    """ Gets all votes a user has cast """

    filtered = [vote for vote in votes_list if vote['createdBy'] == id]

    return vote_response(
        'Request sent successfully', 200, len(filtered), filtered)


@bp.route('/votes/candidate/<int:id>', methods=['GET'])
def get_candidate_votes(id):
    """ Gets all votes for a specific candidate """

    filtered = [vote for vote in votes_list if vote['candidate'] == id]

    return vote_response(
        'Request sent successfully', 200, len(filtered), filtered)


@bp.route('/votes/office/<int:id>', methods=['GET'])
def get_office_votes(id):
    """ Gets all votes for a specific office """

    filtered = [vote for vote in votes_list if vote['office'] == id]

    return vote_response(
        'Request sent successfully', 200, len(filtered), filtered)


def vote_response(message, code, count, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data,
        "count": count
    }
    return make_response(jsonify(response), code)
