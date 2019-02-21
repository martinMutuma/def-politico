from app.v2.utils.validator import validate_ints
from app.v2.utils.validator import validate_strings
from .base_model import BaseModel


class Party(BaseModel):
    """ model for political party """

    def __init__(
            self, name=None, hq_address=None, logo_url=None, slogan=None,
            manifesto=None, id=None):
        super().__init__('Party', 'parties')

        self.name = name
        self.hq_address = hq_address
        self.logo_url = logo_url
        self.slogan = slogan
        self.id = id
        self.manifesto = manifesto

    def as_json(self):
        # get the object as a json
        return {
            "id": self.id,
            "name": self.name,
            "hq_address": self.hq_address,
            "logo_url": self.logo_url,
            "slogan": self.slogan,
            "manifesto": self.manifesto
        }

    def save(self):
        """save party to db  """

        data = super().save(
            'name, hq_address, logo_url, slogan, manifesto', self.name,
            self.hq_address, self.logo_url, self.slogan, self.manifesto)

        self.id = data.get('id')
        return data

    def from_json(self, json):
        self.__init__(
            json['name'], json['hq_address'], json['logo_url'], json['slogan'],
            json['manifesto'])
        self.id = json['id']
        return self

    def edit(self, new_name):
        """ Edit party name """
        self.name = new_name
        return super().edit('name', new_name, self.id)

    def validate_object(self):
        """ validates the object """

        ok = True

        if not validate_strings(
                self.name, self.hq_address, self.logo_url, self.slogan,
                self.manifesto):
            self.error_message = (
                "Invalid or empty string")
            self.error_code = 400
            ok = False

        elif len(self.name) < 3:
            self.error_message = "The {} name provided is too short".format(
                self.object_name)
            self.error_code = 400
            ok = False

        elif len(self.slogan) > 30:
            self.error_message = (
                "Slogan should not exceed 30 characters")
            self.error_code = 400
            ok = False

        elif len(self.manifesto) > 230:
            self.error_message = (
                "Manifesto should not exceed 230 characters")
            self.error_code = 400
            ok = False

        elif self.find_by('name', self.name):
            self.error_message = "{} already exists".format(self.object_name)
            self.error_code = 409
            ok = False

        return ok
