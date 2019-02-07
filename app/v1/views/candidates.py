from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v1.utils.validator import response, exists
from app.v1.models.party_model import Party
from app.v1.models.office_model import Office
from app.v1.models.user_model import User
from app.v1.models.candidate_model import Candidate
from app.v1.blueprints import bp


candidate_list = Candidate.candidates


@bp.route('/candidates', methods=['POST', 'GET'])
def post_candidate():
    if request.method == 'POST':
        """ Create candidate end point """

        data = request.get_json()

        if not data:
            return response("No data was provided", 400)

        try:
            office = data['office']
            party = data['party']
            candidate = data['candidate']
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        item = Candidate(party, office, candidate)

        if not exists('id', office, Office.offices):
            return response('Selected Office does not exist', 404)
        if not exists('id', party, Party.parties):
            return response('Selected Party does not exist', 404)
        if not exists('id', candidate, User.users):
            return response('Selected User does not exist', 404)

        if not item.validate_object():
            return response(item.error_message, item.error_code)

        # append new candidate to list
        item.save()

        # return added candidate
        return response(
            "Candidate created successfully", 201, [item.as_json()])

    elif request.method == 'GET':
        """ Get all candidates end point """

        return response('Request was sent successfully', 200, candidate_list)


@bp.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):

    model = Candidate()
    data = model.find_by_id(id)

    if not data:
        return response('Candidate not found', 404)

    return response('Request sent successfully', 200, [data])
