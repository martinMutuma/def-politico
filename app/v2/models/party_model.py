from app.v2.utils.validator import generate_id, exists, validate_ints
from app.v2.utils.validator import validate_strings
from .base_model import BaseModel


class Party(BaseModel):
    """ model for political party """

    def __init__(self, name=None, hq_address=None, logo_url=None, slogan=None, id=None):
        super().__init__('Party', 'parties')

        self.name = name
        self.hq_address = hq_address
        self.logo_url = logo_url
        self.slogan = slogan
        self.id = id

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
        """save party to db  """

        data = super().save('name, hq_address, logo_url, slogan', self.name, self.hq_address, self.logo_url, self.slogan)

        self.id = data.get('id')
        return data

    def from_json(self, json):
        self.__init__(json['name'], json['hq_address'], json['logo_url'], json['slogan'])
        self.id = json['id']
        return self

    def edit(self, new_name):
        """ Edit party name """
        self.name = new_name
        return super().edit('name', new_name, self.id)

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

        if self.find_by('name', self.name):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            return False

        return super().validate_object()
