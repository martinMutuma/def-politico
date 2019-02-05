from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp


users_list = []


@bp.route('/register', methods=['POST'])
def register_user():
    """ Register user end point """

    data = request.get_json()

    if not data:
        return response("No data was provided", 400)

    try:
        first_name = data['firstname']
        last_name = data['lastname']
        other_name = data['othername']
        email = data['email']
        phone_number = data['phoneNumber']
        passport_url = data['passportUrl']
        is_admin = data['isAdmin']
    except KeyError as e:
        return response("{} field is required".format(e.args[0]), 400)

    user = {
        "id": generate_id(users_list),
        "firstname": first_name,
        "lastname": last_name,
        "othername": other_name,
        "email": email,
        "phoneNumber": phone_number,
        "passportUrl": passport_url,
        "isAdmin": is_admin
    }

    validate_object(user, users_list, 'User')

    # append new user to list
    users_list.append(user)

    # return registered user
    return response("User registered successfully", 201, [user])


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):

    filtered = filter(lambda user: user['id'] == id, users_list)
    filtered = list(filtered)

    if len(filtered) == 0:
        return response('User not found', 404, [])

    if request.method == 'GET':
        return response('Request sent successfully', 200, filtered)
