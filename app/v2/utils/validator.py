from flask import make_response, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.v2.models.user_model import User


def not_admin():
    current_user = User().find_by('id', get_jwt_identity())

    if not current_user['admin']:
        return response_error(
            "This action is reserved to Admins only", 401)
    return None


def generate_id(list):
    """ Creates a unique ID for a new item to be added to the list"""

    return len(list) + 1


def response(message, code, data=[]):
    """ Creates a basic reposnse """

    response = {
        "status": code,
        "message": message,
        "data": data
    }
    return make_response(jsonify(response), code)


def response_error(message, code):
    """ Creates a basic error reposnse """

    response = {
        "status": code,
        "error": message
    }
    return make_response(jsonify(response), code)


def exists(key, value, collection):
    """ Checks if list contains certain item based on certain key """

    filtered = [item for item in collection if item[key] == value]
    return len(filtered) > 0


def validate_strings(*args):
    """ validates that inputs are strings only """

    for value in args:
        if not isinstance(value, str):
            return False
    return True


def validate_bool(*args):
    """ validates that inputs are boolean only """

    for value in args:
        if not isinstance(value, bool):
            return False
    return True


def validate_ints(*args):
    """ validates that inputs are ints only """

    for value in args:
        if not isinstance(value, int):
            return False
    return True