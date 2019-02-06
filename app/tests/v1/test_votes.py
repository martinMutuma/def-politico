from .base_test import Base
from app.v1.views.votes import votes_list


class TestVotes(Base):
    """ Tests for all votes endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_vote = {
            "createdBy": 1,
            "office": 1,
            "candidate": 1
        }
        self.new_candidate = {
            "party": 1,
            "office": 1,
            "candidate": 1
        }
        self.new_party = {
            "name": "NARC",
            "slogan": "Pamoja tujengane",
            "hq_address": "Nairobe",
            "logo_url": "url"
        }
        self.new_office = {
            "name": "Governor",
            "type": "federal"
        }
        self.new_user = {
            "firstname": "James",
            "lastname": "Kimani",
            "othername": "Kamau",
            "email": "james@mail.com",
            "phoneNumber": "0700000000",
            "passportUrl": "passport_url",
            "isAdmin": True
        }
        self.client.post('/api/v1/offices', json=self.new_office)
        self.client.post('/api/v1/parties', json=self.new_party)
        self.client.post('/api/v1/register', json=self.new_user)
        self.client.post('/api/v1/candidates', json=self.new_candidate)

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        votes_list.clear()

    # tests for POST votes
    def test_create_vote(self):
        """ Tests that a vote was created successfully """

        res = self.client.post('/api/v1/votes', json=self.new_vote)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Vote created successfully')
        self.assertEqual(res.status_code, 201)

    def test_create_vote_missing_fields(self):
        """ Tests when some fields are missing e.g office """

        res = self.client.post('/api/v1/votes', json={
            "candidate": 1,
            "createdBy": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'office field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_vote_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/votes')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_create_vote_office_not_exist(self):
        """ Tests when the office does not exist  """

        res = self.client.post('/api/v1/votes', json={
            "office": 28,
            "createdBy": 1,
            "candidate": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Selected Office does not exist')
        self.assertEqual(res.status_code, 404)

    def test_create_vote_user_not_exist(self):
        """ Tests when the user does not exist  """

        res = self.client.post('/api/v1/votes', json={
            "createdBy": 1,
            "office": 1,
            "candidate": 13
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Selected User does not exist')
        self.assertEqual(res.status_code, 404)

    # tests for GET votes
    def test_get_all_votes(self):
        """ Tests when get request made to api/v1/votes """

        res = self.client.post('/api/v1/votes', json=self.new_vote)

        res = self.client.get('/api/v1/votes')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was sent successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_votes_no_data(self):
        """ Tests when get request made to api/v1/votes """

        res = self.client.get('/api/v1/votes')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was sent successfully')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_all_user_votes(self):
        """ Tests when get request made to api/v1/votes/user/id """

        self.client.post('/api/v1/votes', json=self.new_vote)
        res = self.client.get('/api/v1/votes/user/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request sent successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_candidate_votes(self):
        """ Tests when get request made to api/v1/votes/candidate/id """

        self.client.post('/api/v1/votes', json=self.new_vote)
        res = self.client.get('/api/v1/votes/candidate/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request sent successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_office_votes(self):
        """ Tests when get request made to api/v1/votes/office/id """

        self.client.post('/api/v1/votes', json=self.new_vote)
        res = self.client.get('/api/v1/votes/office/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request sent successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)
