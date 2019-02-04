from flask import Blueprint
from flask import request
from flask import jsonify

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/parties', methods=('POST'))
def create_party():
    if request.method == 'POST':
        name = request.form