from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp


office_list = []


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

        office = {
            "id": generate_id(office_list),
            "name": name,
            "type": typ
        }

        validate_object(office, office_list, 'Office')

        # append new office to list
        office_list.append(office)

        # return added office
        return response("Office created successfully", 201, [office])

    elif request.method == 'GET':
        """ Get all offices end point """

        return response('Request was sent successfully', 200, office_list)


@bp.route('/offices/<int:id>', methods=['GET', 'DELETE'])
def get_office(id):

    filtered = filter(lambda office: office['id'] == id, office_list)
    filtered = list(filtered)

    if len(filtered) == 0:
        return response('Office not found', 404, [])

    if request.method == 'GET':
        return response('Request sent successfully', 200, filtered)
    else:
        for i in range(len(office_list)):
            if office_list[i]['id'] == id:
                office = office_list.pop(i)
                break
        return response(
            '{} deleted successfully'.format(office['name']), 200, [office])
