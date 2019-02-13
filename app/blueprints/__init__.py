from flask import Blueprint


# init blueprints
bp = Blueprint('api_version1', __name__, url_prefix='/api/v1')
v2 = Blueprint('api_version2', __name__, url_prefix='/api/v2')
