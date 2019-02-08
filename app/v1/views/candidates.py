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
    message = 'Request was sent successfully'
    status = 200
    response_data = []
    if request.method == 'POST':
        """ Create candidate end point """

        data = request.get_json()

        if data:
            try:
                office = data['office']
                party = data['party']
                candidate = data['candidate']

                item = Candidate(party, office, candidate)

                if item.validate_object():
                    # append new candidate to list
                    item.save()

                    # return added candidate
                    message = "Candidate created successfully"
                    response_data = [item.as_json()]
                    status = 201
                else:
                    message = item.error_message
                    status = item.error_code

            except KeyError as e:
                message = "{} field is required".format(e.args[0])
                status = 400
        else:
            message = "No data was provided"
            status = 400

    elif request.method == 'GET':
        """ Get all candidates end point """
        response_data = candidate_list

    return response(message, status, response_data)


@bp.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):

    model = Candidate()
    data = model.find_by_id(id)

    if not data:
        return response('Candidate not found', 404)

    return response('Request sent successfully', 200, [data])
