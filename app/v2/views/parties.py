from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v2.models.party_model import Party
from app.v2.models.user_model import User
from app.v2.utils.validator import response, exists, response_error, not_admin
from app.blueprints import v2 as bp
from flask_jwt_extended import (jwt_required)


@bp.route('/parties', methods=['POST', 'GET'])
@jwt_required
def create_party():
    if request.method == 'POST':
        """ Create party end point """

        restricted = not_admin()
        if restricted:
            return restricted

        data = request.get_json()

        if not data:
            return response_error("No data was provided", 400)

        try:
            name = data['name']
            hq_address = data['hq_address']
            logo_url = data['logo_url']
            slogan = data['slogan']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        party = Party(name, hq_address, logo_url, slogan)

        if not party.validate_object():
            return response_error(party.error_message, party.error_code)

        # append new party to list
        party.save()

        # return added party
        return response("Success", 201, [party.as_json()])

    elif request.method == 'GET':
        """ Get all parties end point """
        model = Party()
        return response('Success', 200, model.load_all())


@bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def get_party(id):

    model = Party()
    data = model.find_by('id', id)

    if not data:
        return response_error('Party not found', 404)

    if request.method == 'GET':
        return response('Success', 200, [data])
    else:
        restricted = not_admin()
        if restricted:
            return restricted
        party = model.from_json(data)
        party.delete(party.id)
        return response('Success', 200, [data])


@bp.route('/parties/<int:id>/<string:name>', methods=['PATCH'])
@jwt_required
def edit_party(id, name):

    restricted = not_admin()
    if restricted:
        return restricted

    model = Party()
    data = model.find_by('id', id)

    if not data:
        return response_error('Party not found', 404)

    party = model.from_json(data)
    party.name = name

    if not party.validate_object():
        return response_error(party.error_message, party.error_code)

    party.edit(name)

    return response(
        'Success', 200, [party.as_json()])
