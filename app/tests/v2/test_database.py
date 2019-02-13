import unittest
from app.v2.db.database_config import Database
from app import create_app


class TestDatabase(unittest.TestCase):
    """ Test database """

    def setUp(self):
        """ set up tests """

        self.db = Database('development')
        self.db.create_db()
        self.db.create_super_user()

    def test_connect_db(self):
        """ Test whether connection is established """

        db = Database('development')
        self.assertTrue(db.init_connection())

    def test_connect_test_db(self):
        """ Test whether connection is established on test db """

        db = Database('testing')
        self.assertTrue(db.init_connection())

    def test_parties_table_created(self):
        """ Tests whether the party table was created """

        table = self.db.get_one("select to_regclass('public.parties')")
        self.assertTrue(table)

    def test_offices_table_created(self):
        """ Tests whether the offices table was created """

        table = self.db.get_one("select to_regclass('public.offices')")
        self.assertTrue(table)

    def test_users_table_created(self):
        """ Tests whether the user table was created """

        table = self.db.get_one("select to_regclass('public.users')")
        self.assertTrue(table)

    def test_candidates_table_created(self):
        """ Tests whether the candidate table was created """

        table = self.db.get_one("select to_regclass('public.candidates')")
        self.assertTrue(table)

    def test_votes_table_created(self):
        """ Tests whether the votes table was created """

        table = self.db.get_one("select to_regclass('public.votes')")
        self.assertTrue(table)