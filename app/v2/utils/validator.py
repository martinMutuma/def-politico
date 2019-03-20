from flask import make_response, jsonify, abort
from flask_jwt_extended import (jwt_required, get_jwt_identity)
import re


error_value = None


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


def validate_ints(data, *args):
    """ validates that inputs are ints only """

    for key, value in data.items():
        if key in args and not valid_int(value):
            abort(response_error('Invalid integer for {}'.format(key), 422))
    return True


def valid_int(value):
    if not isinstance(value, int):
        return False
    return True


def validate_strings(data, *args):
    """ validates that inputs are strings only """

    for key, value in data.items():
        if key in args and not valid_string(value):
            abort(response_error(
                    'Invalid or empty string for {}'.format(key), 422))
    return True


def valid_string(value):
    if not isinstance(value, str) or not value or not value.split():
        return False
    return True


def validate_bool(*args):
    """ validates that inputs are boolean only """

    for value in args:
        if not isinstance(value, bool):
            return False
    return True


def valid_email(email):
    return re.match(
                r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                email)


def validate_links(data, *args):
    """ validates that inputs are links only """

    for key, value in data.items():
        if key in args and not valid_link(value):
            abort(response_error(
                    'Invalid link for {}'.format(key), 422))
    return True


def valid_link(value):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, value)

def validate_data(data,status):
    if not data:
        if status =="party":
            return response_error('Party not found', 404)
        if status =="data":
            return response_error("No data was provided", 400)

