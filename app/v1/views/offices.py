from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v1.utils.validator import response, exists, response_error
from app.v1.models.office_model import Office
from app.v1.blueprints import bp


office_list = Office.offices


@bp.route('/offices', methods=['POST', 'GET'])
def create_office():
    if request.method == 'POST':
        """ Create office end point """

        data = request.get_json()

        if not data:
            return response_error("No data was provided", 400)

        try:
            typ = data['type']
            name = data['name']
        except KeyError as e:
            return response_error("{} field is required".format(e.args[0]), 400)

        office = Office(name, typ)

        if not office.validate_object():
            return response_error(office.error_message, office.error_code)

        # append new office to list
        office.save()

        # return added office
        return response("Success", 201, [office.as_json()])

    elif request.method == 'GET':
        """ Get all offices end point """

        return response('Success', 200, office_list)


@bp.route('/offices/<int:id>', methods=['GET', 'DELETE'])
def get_office(id):

    model = Office()
    data = model.find_by_id(id)

    if not data:
        return response_error('Office not found', 404)

    if request.method == 'GET':
        return response('Success', 200, [data])
    else:
        office = model.from_json(data)
        office.delete()
        return response(
            'Success', 200, [data])
