from .base_test import Base


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
            "email": "james@gmail.com",
            "phoneNumber": "0700000000",
            "passportUrl": "passport_url",
            "isAdmin": True,
            "password": "jikakamue"
        }
        self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        self.client.post(
            '/api/v2/register', json=self.new_user)
        self.client.post(
            '/api/v2/office/1/register', json=self.new_candidate,
            headers=self.headers)

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST votes
    def test_create_vote(self):
        """ Tests that a vote was created successfully """

        res = self.client.post(
            '/api/v2/votes', json=self.new_vote, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_create_vote_missing_fields(self):
        """ Tests when some fields are missing e.g office """

        res = self.client.post('/api/v2/votes', json={
            "candidate": 1,
            "createdBy": 1
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'office field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_vote_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v2/votes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_create_vote_office_not_exist(self):
        """ Tests when the office does not exist  """

        res = self.client.post('/api/v2/votes', json={
            "office": 28,
            "createdBy": 1,
            "candidate": 1
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected Office does not exist')
        self.assertEqual(res.status_code, 404)

    def test_create_vote_user_not_exist(self):
        """ Tests when the user does not exist  """

        res = self.client.post('/api/v2/votes', json={
            "createdBy": 1,
            "office": 1,
            "candidate": 13
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected Candidate does not exist')
        self.assertEqual(res.status_code, 404)

    def test_create_vote_twice(self):
        """ Tests when user attempts to vote twice for same office """

        self.client.post(
            '/api/v2/votes', json=self.new_vote, headers=self.headers)
        res = self.client.post(
            '/api/v2/votes', json=self.new_vote, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 409)
        self.assertEqual(data['error'], 'You can only vote once per office')
        self.assertEqual(res.status_code, 409)

    def test_create_vote_string_candidate(self):
        """ Tests when string is provided for candidate """

        self.new_vote['candidate'] = 'jack'
        res = self.client.post(
            '/api/v2/votes', json=self.new_vote, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(
            data['error'], 'String types are not allowed for all fields')
        self.assertEqual(res.status_code, 422)

    # tests for GET votes
    def test_get_all_votes(self):
        """ Tests when get request made to api/v2/votes """

        res = self.client.post(
            '/api/v2/votes', json=self.new_vote, headers=self.headers)

        res = self.client.get('/api/v2/votes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)

    def test_get_all_votes_no_data(self):
        """ Tests when get request made to api/v2/votes """

        res = self.client.get('/api/v2/votes', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    # get election results
    def test_election_results(self):
        """ Tests GET request to get election results """

        self.client.post(
            '/api/v2/votes', json=self.new_vote, headers=self.headers)

        res = self.client.get(
            '/api/v2/office/1/result', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['message'], 'Success')
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(res.status_code, 200)
