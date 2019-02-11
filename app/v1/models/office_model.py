from app.v1.utils.validator import generate_id, exists, validate_ints
from app.v1.utils.validator import validate_strings
from .base_model import BaseModel


class Office(BaseModel):
    """ model for political office """

    offices = []

    def __init__(self, name=None, type=None):
        super().__init__('Office', self.offices)

        self.name = name
        self.type = type

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type
        }

    def from_json(self, json):
        self.__init__(json['name'], json['type'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.name, self.type):
            self.error_message = "Integer types are not allowed for some fields"
            self.error_code = 400
            return False

        if len(self.name) < 3:
            self.error_message = "The {} name provided is too short".format(self.object_name)
            self.error_code = 400
            return False

        if exists('name', self.name, self.table):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()
