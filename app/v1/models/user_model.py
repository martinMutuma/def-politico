from app.v1.utils.validator import generate_id, exists, validate_ints, validate_bool
from app.v1.utils.validator import validate_strings
from .base_model import BaseModel


class User(BaseModel):
    """ model for political party """

    users = []

    def __init__(self, first_name=None, last_name=None, other_name=None, email=None, phone_number=None, passport_url=None, is_admin=False):
        super().__init__('User', self.users)

        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.email = email
        self.phone_number = phone_number
        self.passport_url = passport_url
        self.is_admin = is_admin

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "othername": self.other_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "passportUrl": self.passport_url,
            "isAdmin": self.is_admin
        }

    def from_json(self, json):
        self.__init__(json['firstname'], json['lastname'], json['othername'], json['email'], json['phoneNumber'], json['passportUrl'], json['isAdmin'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        if not validate_strings(self.first_name, self.last_name, self.email, self.passport_url):
            self.error_message = "Integer types are not allowed for some fields"
            self.error_code = 400
            return False

        if not validate_bool(self.is_admin):
            self.error_message = "isAdmin is supposed to be a boolean value"
            self.error_code = 400
            return False

        if exists('email', self.email, self.table):
            self.error_message = "A {} with that email already exists".format(self.object_name)
            self.error_code = 400
            return False

        return super().validate_object()
