from flask import Flask, jsonify
from app.v1.views.base_view import generate_id

party_list = []


class Party():
    """ model for political party """

    def __init__(self, name, hq_address, logo_url, slogan):
        # save the object as a json

        self.name = name
        self.hq_address = hq_address
        self.logo_url = logo_url
        self.slogan = slogan
        self.id = generate_id(party_list)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "hq_address": self.hq_address,
            "logo_url": self.logo_url,
            "slogan": self.slogan
        }

    def save(self):
        # save the party to parties
