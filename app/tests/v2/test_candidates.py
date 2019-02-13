from .base_test import Base


class TestCandidate(Base):
    """ Tests for all candidates endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

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
            "isAdmin": True
        }
        self.client.post('/api/v2/offices', json=self.new_office)
        self.client.post('/api/v2/parties', json=self.new_party)
        self.client.post('/api/v2/register', json=self.new_user)
        self.new_user['email'] = 'some@gmail.com'
        self.client.post('/api/v2/register', json=self.new_user)
        self.new_user['email'] = 'some2@gmail.com'
        self.client.post('/api/v2/register', json=self.new_user)
        self.new_user['email'] = 'some3@gmail.com'
        self.client.post('/api/v2/register', json=self.new_user)

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST candidates
    def test_register_candidate(self):
        """ Tests that a candidate was created successfully """

        res = self.client.post('/api/v2/office/1/register', json=self.new_candidate)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_register_candidate_twice(self):
        """ Tests when attempt to create candidate twice """

        self.client.post('/api/v2/office/1/register', json=self.new_candidate)
        res = self.client.post('/api/v2/office/1/register', json=self.new_candidate)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Candidate already exists')
        self.assertEqual(res.status_code, 400)

    def test_register_candidate_missing_fields(self):
        """ Tests when some fields are missing e.g name """

        res = self.client.post('/api/v2/office/1/register', json={
            "office": 1,
            "candidate": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'party field is required')
        self.assertEqual(res.status_code, 400)

    def test_register_candidate_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v2/office/1/register')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_register_candidate_party_not_exist(self):
        """ Tests when the party does not exist  """

        res = self.client.post('/api/v2/office/1/register', json={
            "party": 28,
            "office": 1,
            "candidate": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected Party does not exist')
        self.assertEqual(res.status_code, 404)

    def test_register_candidate_office_not_exist(self):
        """ Tests when the office does not exist  """

        res = self.client.post('/api/v2/office/19/register', json={
            "party": 1,
            "office": 13,
            "candidate": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected Office does not exist')
        self.assertEqual(res.status_code, 404)

    def test_register_candidate_office_not_exist(self):
        """ Tests when the office does not exist  """

        res = self.client.post('/api/v2/office/19/register', json={
            "party": 1,
            "office": 13,
            "candidate": 1
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected Office does not exist')
        self.assertEqual(res.status_code, 404)

    def test_register_candidate_user_not_exist(self):
        """ Tests when the candidate does not exist  """

        res = self.client.post('/api/v2/office/1/register', json={
            "party": 1,
            "office": 1,
            "candidate": 11
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Selected User does not exist')
        self.assertEqual(res.status_code, 404)

    def test_create_candidate_string_candidate(self):
        """ Tests when string is provided for candidate """

        self.new_candidate['candidate'] = 'jack'
        res = self.client.post('/api/v2/office/1/register', json=self.new_candidate)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'String types are not allowed for all fields')
        self.assertEqual(res.status_code, 400)

    # tests for GET candidates
    def test_get_all_candidates(self):
        """ Tests when get request made to api/v2/candidates """

        res = self.client.post('/api/v2/candidates', json=self.new_candidate)
        self.new_candidate['candidate'] = 2
        res = self.client.post('/api/v2/candidates', json=self.new_candidate)
        self.new_candidate['candidate'] = 3
        res = self.client.post('/api/v2/candidates', json=self.new_candidate)

        res = self.client.get('/api/v2/candidates')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(res.status_code, 200)

    def test_get_all_candidates_no_data(self):
        """ Tests when get request made to api/v2/candidates """

        res = self.client.get('/api/v2/candidates')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    # tests for GET single candidate
    def test_get_sigle_candidate(self):
        """ Tests when get reuest made to /candidates/<int:id> """

        self.client.post('/api/v2/candidates', json=self.new_candidate)

        res = self.client.get('/api/v2/candidates/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_candidate_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/v2/candidates/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Candidate not found')
        self.assertEqual(res.status_code, 404)
