from flask import request
from flask import jsonify
from flask import make_response
from app.v2.utils.validator import response, response_error, not_admin
from app.v2.models.party_model import Party
from app.v2.models.office_model import Office
from app.v2.models.user_model import User
from app.v2.models.candidate_model import Candidate
from app.blueprints import v2 as bp
from flask_jwt_extended import (jwt_required)


@bp.route('/office/<int:id>/register', methods=['POST'])
@jwt_required
def post_candidate(id):
    message = 'Success'
    status = 200
    response_data = []
    error = True
    """ Create candidate end point """

    restricted = not_admin()
    if restricted:
        return restricted

    data = request.get_json()

    if data:
        try:
            office = id
            party = data['party']
            candidate = data['candidate']

            item = Candidate(party, office, candidate)

            if item.validate_object():
                # append new candidate to list
                item.save()

                # return added candidate
                message = "Success"
                response_data = [item.as_json()]
                status = 201
                error = False
            else:
                message = item.error_message
                status = item.error_code

        except KeyError as e:
            message = "{} field is required".format(e.args[0])
            status = 400
    else:
        message = "No data was provided"
        status = 400

    if error:
        return response_error(message, status)
    else:
        return response(message, status, response_data)


@bp.route('/candidates', methods=['GET'])
@jwt_required
def get_candidates():
    """ Get all candidates end point """

    return response('Success', 200, Candidate().load_all())


@bp.route('/candidates/<int:id>', methods=['GET'])
@jwt_required
def get_candidate(id):
    """ Get single candidate end point """

    model = Candidate()
    data = model.find_by('id', id)

    if not data:
        return response_error('Candidate not found', 404)

    return response('Success', 200, [data])
