from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp, exists
from .parties import party_list
from .offices import office_list
from .users import users_list


candidate_list = []


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

        item = {
            "id": generate_id(candidate_list),
            "office": office,
            "party": party,
            "candidate": candidate
        }

        if not exists(office, office_list):
            return response('Selected Office does not exist', 404)
        if not exists(party, party_list):
            return response('Selected Party does not exist', 404)
        if not exists(candidate, users_list):
            return response('Selected User does not exist', 404)

        validate_object(item, candidate_list, 'Candidate')

        # append new candidate to list
        candidate_list.append(item)

        # return added candidate
        return response("Candidate created successfully", 201, [item])

    elif request.method == 'GET':
        """ Get all candidates end point """

        return response('Request was sent successfully', 200, candidate_list)


@bp.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):

    filtered = filter(lambda c: c['id'] == id, candidate_list)
    filtered = list(filtered)

    if len(filtered) == 0:
        return response('Candidate not found', 404, [])

    if request.method == 'GET':
        return response('Request sent successfully', 200, filtered)
