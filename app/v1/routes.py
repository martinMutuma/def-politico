from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response

bp = Blueprint('api', __name__, url_prefix='/api/v1')

party_list = []


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

        party = {
            "id": generate_id(party_list),
            "name": name,
            "hq_address": hq_address,
            "logo_url": logo_url,
            "slogan": slogan
        }

        validate_party(party)

        # append new party to list
        party_list.append(party)

        # return list of parties to display added party
        return response("Party created successfully", 201, [party])

    elif request.method == 'GET':
        """ Get all parties end point """

        return response('Request was sent successfully', 200, party_list)


@bp.route('/parties/<int:id>', methods=['GET'])
def get_party(id):

    filtered = filter(lambda party: party['id'] == id, party_list)
    filtered = list(filtered)

    if len(filtered) == 0:
        return response('Party not found', 404)

    return response('Request sent successfully', 200, filtered)


def validate_party(party):
    """This function validates a party and rejects or accepts it"""
    for key, value in party.items():
        if not value:
            return response(
                "Please provide a {} for the party".format(key), 400)
        if key == "name":
            if len(value) < 3:
                return response(
                    "The party name provided is too short", 400)


def generate_id(list):
    """ Creates a unique ID for a new item to be added to the list"""

    return len(list) + 1


def response(message, code, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data
    }
    return make_response(jsonify(response), code)