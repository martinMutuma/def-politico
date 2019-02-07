""" model that defines all models """


class BaseModel():

    def __init__(self, object_name):
        self.object_name = object_name
        self.error_message = ""
        self.error_code = 200

    def as_json(self):
        return {}

    def validate_object(self):
        """This function validates an object and rejects or accepts it"""

        item = self.as_json()
        for key, value in item.items():
            if not value:
                self.error_message = "Please provide a {} for the {}".format(key, self.object_name)
                self.error_code = 400
                return False
        return True
