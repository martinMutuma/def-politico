from app import create_app
import unittest


class Base(unittest.TestCase):
    """ This is the super class for all tests """

    def setUp(self):
        """ Setup the common stuff """

        self.app = create_app('testing')
        self.client = self.app.test_client()

        # login as a super user
        # res = self.client.post('/api/v2/auth/login', json={
        #     'email': 'bedank6@gmail.com', 'password': 'jivunie'})

        # self.access_token = res.get_json()[0]['access_token']
        # self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def tearDown(self):
        self.app = None
        # clear the database here
