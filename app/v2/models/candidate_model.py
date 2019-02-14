from app.v2.utils.validator import validate_ints
from .base_model import BaseModel
from .office_model import Office
from .party_model import Party
from .user_model import User


class Candidate(BaseModel):
    """ model for political candidate """

    def __init__(self, party=None, office=None, candidate=None, id=None):
        super().__init__('Candidate', 'candidates')

        self.party = party
        self.office = office
        self.candidate = candidate
        self.id = id

    def save(self):
        """save candidate to db """

        data = super().save(
            'party, office, candidate', self.party, self.office,
            self.candidate)

        self.id = data.get('id')
        return data

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

        if self.find_by('candidate', self.candidate):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            return False

        if not Office().find_by('id', self.office):
            self.error_message = 'Selected Office does not exist'
            self.error_code = 404
            return False

        if not Party().find_by('id', self.party):
            self.error_message = 'Selected Party does not exist'
            self.error_code = 404
            return False

        if not User().find_by('id', self.candidate):
            self.error_message = 'Selected User does not exist'
            self.error_code = 404
            return False

        return super().validate_object()