from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import verify_jwt_in_request_optional
from flask_jwt_extended import verify_jwt_in_request
from app.v2.models.user_model import User
from functools import wraps
from flask import jsonify
from app.v2.utils.validator import response_error


def admin_optional(fn):
    """ The below function checks if an admin token exists in the request """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request_optional()
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    """ The below function checks if an admin token exists in the request """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity:
            admin = User().find_by('id', identity)
            if admin and admin['admin']:
                return fn(*args, **kwargs)
            return response_error(
                "This action is reserved to Admins only", 401)
    return wrapper
