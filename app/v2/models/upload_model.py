from .base_model import BaseModel


class UploadImage(BaseModel):
    """ contains methods for uploading an image """

    def __init__(self, user_id, new_url):
        
        super().__init__('User', 'users')
        self.user_id = user_id
        self.new_url = new_url

    def updateimage(self):
        """ update image url """

        return super().edit('passport_url', self.new_url, self.user_id)