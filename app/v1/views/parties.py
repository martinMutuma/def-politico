from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp
from app.v1.models.db import Database
from app.v1.models.party_model import Party


party_list = Database('parties').get_items()


@bp.route('/parties', methods=['POST', 'GET'])
def create_party():
    if request.method == 'POST':
        """ Create party end point """

        data = request.get_json()

        if not data:
            return response("No data was provided", 400)

        try:
            name = data['name']
            hq_address = data['hq_address']
            logo_url = data['logo_url']
            slogan = data['slogan']
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        party = Party(name, hq_address, logo_url, slogan)

        if not party.validate_object():
            return response(party.error_message, party.error_code)

        # append new party to list
        party.save()

        # return added party
        return response("Party created successfully", 201, [party.as_json()])

    elif request.method == 'GET':
        """ Get all parties end point """

        return response('Request was sent successfully', 200, party_list)


@bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
def get_party(id):

    filtered = filter(lambda party: party['id'] == id, party_list)
    filtered = list(filtered)

    if len(filtered) == 0:
        return response('Party not found', 404, [])

    if request.method == 'GET':
        return response('Request sent successfully', 200, filtered)
    else:
        for i in range(len(party_list)):
            if party_list[i]['id'] == id:
                party = party_list.pop(i)
                break
        return response(
            '{} deleted successfully'.format(party['name']), 200, [party])


@bp.route('/parties/<int:id>/<string:name>', methods=['PATCH'])
def edit_party(id, name):

    filtered = filter(lambda party: party['id'] == id, party_list)
    filtered = list(filtered)

    if len(filtered) == 0:
        return response('Party not found', 404, [])

    if len(name) < 4:
        return response('The name provided is too short', 400, [])

    for i in range(len(party_list)):
        if party_list[i]['id'] == id:
            party = party_list[i]
            party['name'] = name
            party_list[i] = party
            break
    return response(
        '{} updated successfully'.format(party['name']), 200, [party])
