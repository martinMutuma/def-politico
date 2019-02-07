from app.v1.views.base_view import generate_id, exists, validate_ints
from app.v1.views.base_view import validate_strings
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

    def edit(self, new_name):
        """ Edit office name """
        self.name = new_name
        for i in range(len(self.table)):
            if self.table[i]['id'] == self.id:
                office = self.table[i]
                office['name'] = new_name
                self.table[i] = office
                break

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
