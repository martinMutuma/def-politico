from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from .base_view import response, generate_id, validate_object, bp
from app.v1.models.user_model import User


users_list = User.users


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

    user = User(first_name, last_name, other_name, email, phone_number, passport_url, is_admin)

    if not user.validate_object():
            return response(user.error_message, user.error_code)

    # append new user to list
    user.save()

    # return registered user
    return response("User registered successfully", 201, [user.as_json()])


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):

    model = User()
    data = model.find_by_id(id)

    if not data:
        return response('User not found', 404)

    return response('Request sent successfully', 200, [data])
