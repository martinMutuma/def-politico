from app.v1.models.office_model import Office
from app.v1.models.user_model import User
from app.v1.models.vote_model import Vote
from app.v1.models.candidate_model import Candidate
from app.v1.models.party_model import Party


class Database:
    """ The database model """
    USERS = 'users'
    PARTIES = 'parties'
    OFFICES = 'offices'
    CANDIDATES = 'candidates'
    VOTES = 'votes'

    def __init__(self):
        self.tables = {
            self.USERS: User.users,
            self.PARTIES: Party.parties,
            self.OFFICES: Office.offices,
            self.CANDIDATES: Candidate.candidates,
            self.VOTES: Vote.votes
        }

    def get_table(self, table_name):
        return self.tables[table_name]

    def clear(self, table_name=None):
        # clears the entire database or single table
        if table_name:
            self.tables[table_name] = []
        else:
            for key in self.tables.items:
                self.tables[key] = []
