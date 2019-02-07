from app.v1.views.base_view import generate_id, exists, validate_ints
from app.v1.views.base_view import validate_strings
from .base_model import BaseModel


class Candidate(BaseModel):
    """ model for political candidate """

    candidates = []

    def __init__(self, party=None, office=None, candidate=None):
        super().__init__('Candidate', self.candidates)

        self.party = party
        self.office = office
        self.candidate = candidate

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "party": self.party,
            "office": self.office,
            "candidate": self.candidate
        }

    def from_json(self, json):
        self.__init__(json['party'], json['office'], json['candidate'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_ints(self.party, self.candidate, self.office):
            self.error_message = "String types are not allowed for all fields"
            self.error_code = 400
            return False

        if exists('candidate', self.candidate, self.table):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()
