from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp, exists
from .parties import party_list
from .offices import office_list
from .users import users_list
from datetime import datetime


votes_list = []


@bp.route('/votes', methods=['POST', 'GET'])
def vote():
    if request.method == 'POST':
        """ Create vote end point """

        data = request.get_json()

        if not data:
            return response("No data was provided", 400)

        try:
            created_by = data['createdBy']
            office = data['office']
            candidate = data['candidate']
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        vote = {
            "id": generate_id(votes_list),
            "office": office,
            "createdBy": created_by,
            "candidate": candidate,
            "createdOn": datetime.now()
        }

        if not exists(office, office_list):
            return response('Selected Office does not exist', 404)
        if not exists(candidate, users_list):
            return response('Selected User does not exist', 404)
        if voted_for(created_by, office):
            return response('You can only vote once per office', 400)

        # append new vote to list
        votes_list.append(vote)

        # return added vote
        return response("Vote created successfully", 201, [vote])

    elif request.method == 'GET':
        """ Get all votes end point """

        return response('Request was sent successfully', 200, votes_list)


@bp.route('/votes/user/<int:id>', methods=['GET'])
def get_user_votes(id):
    """ Gets all votes a user has cast """

    filtered = filter(lambda c: c['createdBy'] == id, votes_list)
    filtered = list(filtered)

    return vote_response(
        'Request sent successfully', 200, len(filtered), filtered)


@bp.route('/votes/candidate/<int:id>', methods=['GET'])
def get_candidate_votes(id):
    """ Gets all votes for a specific candidate """

    filtered = filter(lambda c: c['candidate'] == id, votes_list)
    filtered = list(filtered)

    return vote_response(
        'Request sent successfully', 200, len(filtered), filtered)


@bp.route('/votes/office/<int:id>', methods=['GET'])
def get_office_votes(id):
    """ Gets all votes for a specific office """

    filtered = filter(lambda c: c['office'] == id, votes_list)
    filtered = list(filtered)

    return vote_response(
        'Request sent successfully', 200, len(filtered), filtered)


def voted_for(uid, office):
    filtered = filter(lambda item: item['createdBy'] == uid and item['office'] == office, votes_list)
    filtered = list(filtered)
    return len(filtered) > 0


def vote_response(message, code, count, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data,
        "count": count
    }
    return make_response(jsonify(response), code)
