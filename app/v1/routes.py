from flask import Blueprint
from flask import request
from flask import jsonify

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/parties', methods=('POST'))
def create_party():
    if request.method == 'POST':
        party_name = request.form['name']


def validate_party(party):
    """This function validates a party and rejects or accepts it"""
    for key, value in party.items():
        if not value:
            return "Please provide a {} for the party".format(key)
        if key == "name":
            if len(value) < 3:
                return "The party name provided is too short"
