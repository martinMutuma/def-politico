from .base_test import Base


class TestParties(Base):
    """ Tests for all parties endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_party = {
            "name": "NARC",
            "slogan": "Pamoja tujengane",
            "hq_address": "Nairobe",
            "logo_url": "url"
        }

    # tests for POST parties
    def test_create_party(self):
        """ Tests that a party was created successfully """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Party created successfully')
        self.assertEqual(res.status_code, 201)

    def test_create_party_missing_fields(self):
        """ Tests when some fields are missing e.g name """

        res = self.client.post('/api/v1/parties', json={
            "slogan": "Pamoja tujengane",
            "hq_address": "Nairobe",
            "logo_url": "url"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    # tests for GET parties
    def test_get_all_parties(self):
        """ Tests when get request made to api/v1/parties """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        res = self.client.post('/api/v1/parties', json=self.new_party)
        res = self.client.post('/api/v1/parties', json=self.new_party)

        res = self.client.get('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was sent successfully')
        self.assertEqual(len(data['data']), 4)
        self.assertEqual(res.status_code, 200)

    def test_get_all_parties_no_data(self):
        """ Tests when get request made to api/v1/parties """

        res = self.client.get('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was sent successfully')
        self.assertEqual(len(data['data']), 4)
        self.assertEqual(res.status_code, 200)

    # tests for GET single party
    def test_get_sigle_party(self):
        """ Tests when get reuest made to /parties/<int:id> """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        res = self.client.get('/api/vi/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request sent successfully')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_party_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/vi/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Party not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)
