from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response

bp = Blueprint('api', __name__, url_prefix='/api/v1')

party_list = []


@bp.route('/parties', methods=['POST'])
def create_party():
    try:
        data = request.get_json()
        name = data['name']
        hq_address = data['hq_address']
        logo_url = data['logo_url']
        slogan = data['slogan']
    except KeyError as e:
        return response(
            "Failed", "{} field is required".format(e.args[0]), 400)

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
    return response("OK", "Party created successfully", 201, party)


def validate_party(party):
    """This function validates a party and rejects or accepts it"""
    for key, value in party.items():
        if not value:
            return "Please provide a {} for the party".format(key)
        if key == "name":
            if len(value) < 3:
                return "The party name provided is too short"


def generate_id(list):
    """ Creates a unique ID for a new item to be added to the list"""

    return len(list) + 1


def response(status, message, code, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": status,
        "message": message,
    }
    if data:
        response["data"] = data
    return make_response(jsonify(response), code)