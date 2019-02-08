from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v1.utils.validator import response, exists
from app.v1.models.office_model import Office
from app.v1.blueprints import bp


office_list = Office.offices


@bp.route('/offices', methods=['POST', 'GET'])
def create_office():

    message = 'Request was sent successfully'
    status = 200
    response_data = []

    if request.method == 'POST':
        """ Create office end point """

        data = request.get_json()

        if data:

            try:
                typ = data['type']
                name = data['name']

                office = Office(name, typ)

                if office.validate_object():
                    # append new office to list
                    office.save()

                    # return added office
                    message = "Office created successfully"
                    status = 201
                    response_data = [office.as_json()]
                else:
                    message = office.error_message
                    status = office.error_code

            except KeyError as e:
                message = "{} field is required".format(e.args[0])
                status = 400
        else:
            message = "No data was provided"
            status = 400

    elif request.method == 'GET':
        """ Get all offices end point """
        response_data = office_list

    return response(message, status, response_data)


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
