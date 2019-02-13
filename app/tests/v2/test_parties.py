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

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST parties
    def test_create_party(self):
        """ Tests that a party was created successfully """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
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
        self.assertEqual(data['error'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_create_party_same_name(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Party already exists')
        self.assertEqual(res.status_code, 400)

    def test_create_party_int_name(self):
        """ Tests when integer is provided for name """

        self.new_party['name'] = 3
        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Integer types are not allowed for some fields')
        self.assertEqual(res.status_code, 400)

    def test_create_party_short_name(self):
        """ Tests when short name is provided """

        self.new_party['name'] = 'pa'
        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'The Party name provided is too short')
        self.assertEqual(res.status_code, 400)

    # tests for GET parties
    def test_get_all_parties(self):
        """ Tests when get request made to api/v1/parties """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        self.new_party['name'] = 'Other name'
        res = self.client.post('/api/v1/parties', json=self.new_party)
        self.new_party['name'] = 'Other Other name'
        res = self.client.post('/api/v1/parties', json=self.new_party)

        res = self.client.get('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(res.status_code, 200)

    def test_get_all_parties_no_data(self):
        """ Tests when get request made to api/v1/parties """

        res = self.client.get('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    # tests for GET single party
    def test_get_sigle_party(self):
        """ Tests when get reuest made to /parties/<int:id> """

        self.client.post('/api/v1/parties', json=self.new_party)

        res = self.client.get('/api/v1/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_party_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/v1/parties/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)

    # tests for DELETE party
    def test_delete_party(self):
        """ Tests when DELETE reuest made to /parties/<int:id> """

        self.client.post('/api/v1/parties', json=self.new_party)

        res = self.client.delete('/api/v1/parties/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_party_id_not_found(self):
        """ Tests DELETE request made with id that does not exist """

        res = self.client.delete('/api/v1/parties/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)

    # tests for PATCH party
    def test_patch_party(self):
        """ Tests when PATCH reuest made to /parties/<int:id>/name """

        self.client.post('/api/v1/parties', json=self.new_party)

        res = self.client.patch('/api/v1/parties/1/Rainbow')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'Rainbow')
        self.assertEqual(res.status_code, 200)

    def test_patch_party_id_not_found(self):
        """ Tests PATCH request made with id that does not exist """

        res = self.client.patch('/api/v1/parties/14/Rainbow')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)
