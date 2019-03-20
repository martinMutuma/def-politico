from flask import request
from app.v2.models.party_model import Party
from app.v2.models.user_model import User
from app.v2.utils.validator import response, response_error
from app.v2.utils.jwt_utils import not_admin
from app.blueprints import v2 as bp
from flask_jwt_extended import (jwt_required)
from app.v2.utils.jwt_utils import admin_required
from app.v2.utils import validator


@bp.route('/parties', methods=['POST', 'GET', 'PUT'])
@jwt_required
def create_party():
    if request.method == 'POST':
        """ Create party end point """

        restricted = not_admin()
        if restricted:
            return restricted

        data = request.get_json()

        validate=validator.validate_data(data,status="data")
        if validate:
            return validate

        try:
            name = data['name']
            hq_address = data['hq_address']
            logo_url = data['logo_url']
            slogan = data['slogan']
            manifesto = data['manifesto']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        party = Party(name, hq_address, logo_url, slogan, manifesto)

        if not party.validate_object():
            return response_error(party.error_message, party.error_code)

        # append new party to list
        party.save()

        # return added party
        return response("Success", 201, [party.as_json()])

    elif request.method == 'PUT':
        """ Create party end point """

        restricted = not_admin()
        if restricted:
            return restricted
       
        data = request.get_json()
        validate=validator.validate_data(data,status="data")
        if validate:
            return validate

        try:
            name = data['name']
            hq_address = data['hq_address']
            logo_url = data['logo_url']
            slogan = data['slogan']
            manifesto = data['manifesto']
            id = data['id']
        except KeyError as e:
            return response_error(
                "{} field is required".format(e.args[0]), 400)

        party = Party(name, hq_address, logo_url, slogan, manifesto, id)
        data = party.find_by('id', id)

        validate=validator.validate_data(data,status="party")

        if validate:
            return validate
       
        if not party.validate_object():
            return response_error(party.error_message, party.error_code)

        # append new party to list
        party.update()

        # return added party
        return response("Success", 201, [party.as_json()])

    elif request.method == 'GET':
        """ Get all parties end point """
        model = Party()
        return response('Success', 200, model.load_all())


@bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def get_party(id):

    model = Party()
    data = model.find_by('id', id)
    
    validate=validator.validate_data(data,status="party")

    if validate:
        return validate
    elif request.method == 'GET':
        return response('Success', 200, [data])
    else:
        restricted = not_admin()
        if restricted:
            return restricted
        party = model.from_json(data)
        party.delete(party.id)
        return response('Success', 200, [data])


@bp.route('/parties/<int:id>/name', methods=['PATCH'])
@admin_required
def edit_party(id):

    data = request.get_json()

    validate=validator.validate_data(data,status="data")
    if validate:
        return validate

    try:
        name = data['name']
    except KeyError as e:
        return response_error(
            "{} field is required".format(e.args[0]), 400)

    model = Party()
    party_data = model.find_by('id',id)
    validate=validator.validate_data(party_data,status="party")
    if validate:
        return validate

    party = model.from_json(party_data)
    party.name = name

    if not party.validate_object():
        return response_error(party.error_message, party.error_code)

    party.edit(name)

    return response(
        'Success', 200, [party.as_json()])

