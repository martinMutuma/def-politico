from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v2.models.office_model import Office
from app.v2.models.user_model import User
from app.v2.models.vote_model import Vote
from app.v2.utils.validator import response, response_error
from app.blueprints import v2 as bp
from flask_jwt_extended import (jwt_required, get_jwt_identity)


@bp.route('/votes', methods=['POST', 'GET'])
@jwt_required
def vote():
    if request.method == 'POST':
        """ Create vote end point """

        data = request.get_json()
        current_user = get_jwt_identity()

        if not data:
            return response_error("No data was provided", 400)

        try:
            created_by = current_user
            office = data['office']
            candidate = data['candidate']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        vote = Vote(created_by, office, candidate)

        if not vote.validate_object():
            return response_error(vote.error_message, vote.error_code)

        # append new vote to list
        vote.save()

        # return added vote
        return response("Success", 201, [vote.as_json()])

    elif request.method == 'GET':
        """ Get all votes end point """

        return response('Success', 200, Vote().load_all())


@bp.route('/office/<int:office_id>/result', methods=['GET'])
@jwt_required
def get_results(office_id):
    """ Gets results """

    filtered = Vote().get_all(
        """
        SELECT concat_ws(' ', users.firstname, users.lastname) AS candidate,
        offices.name as office,
         (SELECT COUNT(*)
            FROM votes AS p
            WHERE p.candidate = e.candidate
            GROUP BY p.candidate
         ) AS results,
         (
             SELECT parties.name FROM candidates as h
             INNER JOIN parties ON parties.id = h.party
             WHERE h.id = e.candidate
         ) as party, passport_url
         FROM votes AS e
         INNER JOIN users ON users.id = e.candidate
         INNER JOIN offices ON offices.id = e.office
         WHERE office = '{}'
         GROUP BY e.candidate, users.firstname, users.lastname, offices.name, users.passport_url
         ORDER BY results DESC
        """.format(office_id)
    )

    return response('Success', 200, filtered)


@bp.route('/results', methods=['GET'])
@jwt_required
def get_all_results():
    """ Gets results """

    filtered = Vote().get_all(
        """
        SELECT concat_ws(' ', users.firstname, users.lastname) AS candidate,
         (SELECT COUNT(*)
            FROM votes AS p
            WHERE p.candidate = e.candidate
            GROUP BY p.candidate
         ) AS results,
         offices.name as office,
         (
             SELECT parties.name FROM candidates as h
             INNER JOIN parties ON parties.id = h.party
             WHERE h.id = e.candidate
         ) as party, passport_url
         FROM votes AS e
         INNER JOIN users ON users.id = e.candidate
         INNER JOIN offices ON offices.id = e.office
         GROUP BY e.candidate, users.firstname, users.lastname, offices.name, users.passport_url
         ORDER BY results DESC
        """
    )

    return response('Success', 200, filtered)
