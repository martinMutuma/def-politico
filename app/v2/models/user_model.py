from app.v2.utils.validator import validate_ints, valid_email, valid_string
from app.v2.utils.validator import validate_strings, validate_links
from app.v2.utils.validator import validate_bool
from .base_model import BaseModel
import datetime
import jwt
import re
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required)
from flask_jwt_extended import (get_jwt_identity, get_raw_jwt)


class User(BaseModel):
    """ model for political party """

    def __init__(
            self, first_name=None, last_name=None, other_name=None, email=None,
            phone_number=None, passport_url=None, is_admin=False,
            password=None, id=None):

        super().__init__('User', 'users')

        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.email = email
        self.phone_number = phone_number
        self.passport_url = passport_url
        self.is_admin = is_admin
        self.password = password
        self.id = id

    def save(self):
        """save user to db and generate tokens """

        data = super().save(
            'firstname, lastname, othername, email, phonenumber, password, \
            admin', self.first_name, self.last_name,
            self.other_name, self.email, self.phone_number,
            generate_password_hash(self.password), self.is_admin)

        self.id = data.get('id')
        self.create_tokens()
        return data

    def create_tokens(self):
        expires = datetime.timedelta(days=60)
        self.access_token = create_access_token(
            identity=self.id, expires_delta=expires)
        self.refresh_token = create_refresh_token(identity=self.id)

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
        self.__init__(
            json['firstname'], json['lastname'], json['othername'],
            json['email'], json['phoneNumber'], json['passportUrl'],
            json['isAdmin'])
        self.id = json['id']
        return self

    def validate_object(self):
        """ validates the object """

        ok = True

        validate_strings(
            self.as_json(), 'firstname', 'lastname', 'othername', 'email',
            'phoneNumber')

        validate_links(
            self.as_json(), 'passportUrl')

        if not valid_email(self.email):
            self.error_message = "Invalid email"
            self.error_code = 422
            ok = False

        elif not valid_string(self.password):
            self.error_message = "Invalid or empty string for password"
            self.error_code = 422
            ok = False

        elif not validate_bool(self.is_admin):
            self.error_message = "isAdmin is supposed to be a boolean value"
            self.error_code = 422
            ok = False

        elif self.find_by('email', self.email):
            self.error_message = "A {} with that email already exists".format(
                self.object_name)
            self.error_code = 409
            ok = False

        elif not re.match('^[0-9]*$', self.phone_number):
            self.error_message = "Invalid phone number"
            self.error_code = 422
            ok = False

        elif len(self.password) < 6:
            self.error_message = "Password must be at least 6 characters long"
            self.error_code = 422
            ok = False

        return ok
