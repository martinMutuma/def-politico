from app import create_app
import unittest
from app.v1.models.db import Database
from app.v1.models.party_model import Party
from app.v1.models.office_model import Office
from app.v1.models.user_model import User
from app.v1.models.candidate_model import Candidate
from app.v1.models.vote_model import Vote


class Base(unittest.TestCase):
    """ This is the super class for all tests """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.item_list = []

    def tearDown(self):
        self.app = None
        self.item_list.clear()
        User.users.clear()
        Office.offices.clear()
        Candidate.candidates.clear()
        Vote.votes.clear()
        Party.parties.clear()
