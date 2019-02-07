from flask import Flask, jsonify
from app.v1.views.base_view import generate_id, exists, validate_ints
from app.v1.views.base_view import validate_strings
from .db import Database
from .base_model import BaseModel

parties = Database('parties').get_items()


class Party(BaseModel):
    """ model for political party """

    def __init__(self, name, hq_address, logo_url, slogan):
        super().__init__('Party')

        self.name = name
        self.hq_address = hq_address
        self.logo_url = logo_url
        self.slogan = slogan
        self.id = generate_id(parties)

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "hq_address": self.hq_address,
            "logo_url": self.logo_url,
            "slogan": self.slogan
        }

    def save(self):
        """ save the party to parties """
        parties.append(self.as_json())

    def edit(self, new_name):
        """ Edit party name """
        self.name = new_name
        for i in range(len(parties)):
            if parties[i]['id'] == self.id:
                party = parties[i]
                party['name'] = new_name
                parties[i] = party
                break

    def delete(self):
        """ Remove party from list and return instance """
        for i in range(len(parties)):
            if parties[i]['id'] == self.id:
                return parties.pop(i)

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.name, self.hq_address, self.logo_url, self.slogan):
            self.error_message = "Integer types are not allowed for some fields"
            self.error_code = 400
            return False

        if len(self.name) < 3:
            self.error_message = "The {} name provided is too short".format(self.object_name)
            self.error_code = 400
            return False

        if exists('name', self.name, parties):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()
