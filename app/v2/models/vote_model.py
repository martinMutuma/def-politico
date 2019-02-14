from app.v1.utils.validator import generate_id, exists, validate_ints
from app.v1.utils.validator import validate_strings
from .base_model import BaseModel
from datetime import datetime


class Vote(BaseModel):
    """ model for political vote """

    votes = []

    def __init__(self, created_by=None, office=None, candidate=None):
        super().__init__('Vote', self.votes)

        self.created_by = created_by
        self.office = office
        self.candidate = candidate
        self.created_on = datetime.now()

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "createdBy": self.created_by,
            "office": self.office,
            "candidate": self.candidate,
            "createdOn": self.created_on
        }

    def from_json(self, json):
        self.__init__(json['createdBy'], json['office'], json['candidate'])
        self.id = json['id']
        self.created_on = json['createdOn']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_ints(self.created_by, self.candidate, self.office):
            self.error_message = "String types are not allowed for all fields"
            self.error_code = 400
            return False

        filtered = filter(lambda item: item['createdBy'] == self.created_by and item['office'] == self.office, self.votes)
        filtered = list(filtered)
        if len(filtered) > 0:
            self.error_message = "You can only vote once per office"
            self.error_code = 400
            return False

        return super().validate_object()
