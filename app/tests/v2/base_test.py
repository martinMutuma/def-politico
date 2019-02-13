from app import create_app
import unittest
from app.v2.db.database_config import Database


class Base(unittest.TestCase):
    """ This is the super class for all tests """

    def setUp(self):
        """ Setup the common stuff """

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['JWT_SECRET_KEY'] = 'mysecret'
        self.client = self.app.test_client()

        # login as a super user
        # res = self.client.post('/api/v2/auth/login', json={
        #     'email': 'bedank6@gmail.com', 'password': 'jivunie'})

        # self.access_token = res.get_json()['data'][0]['token']
        # self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def tearDown(self):
        self.app = None
        # clear the database here
        db = Database('testing')
        db.init_connection()
        db.truncate()
