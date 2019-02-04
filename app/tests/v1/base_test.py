from app import create_app
import unittest


class Base(unittest.TestCase):
    """ This is the super class for all tests """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
  
    def tearDown(self):
        self.app = None
