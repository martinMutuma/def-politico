from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp
from app.v1.models.office_model import Office


office_list = Office.offices


@bp.route('/offices', methods=['POST', 'GET'])
def create_office():
    if request.method == 'POST':
        """ Create office end point """

        data = request.get_json()

        if not data:
            return response("No data was provided", 400)

        try:
            typ = data['type']
            name = data['name']
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        office = Office(name, typ)

        if not office.validate_object():
            return response(office.error_message, office.error_code)

        # append new office to list
        office.save()

        # return added office
        return response("Office created successfully", 201, [office.as_json()])

    elif request.method == 'GET':
        """ Get all offices end point """

        return response('Request was sent successfully', 200, office_list)


@bp.route('/offices/<int:id>', methods=['GET', 'DELETE'])
def get_office(id):

    model = Office()
    data = model.find_by_id(id)

    if not data:
        return response('Office not found', 404)

    if request.method == 'GET':
        return response('Request sent successfully', 200, [data])
    else:
        office = model.from_json(data)
        office.delete()
        return response(
            '{} deleted successfully'.format(office.name), 200, [data])
