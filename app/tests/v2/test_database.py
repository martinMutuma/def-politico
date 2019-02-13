import unittest
from app.v2.db.database_config import Database
from app import create_app


class TestDatabase(unittest.TestCase):
    """ Test database """

    def test_connect_db(self):
        """ Test whether connection is established """

        db = Database('development')
        self.assertTrue(db.init_connection())

    def test_connect_test_db(self):
        """ Test whether connection is established on test db """

        db = Database('testing')
        self.assertTrue(db.init_connection())
