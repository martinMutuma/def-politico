from .base_test import Base


class TestParties(Base):
    """ Tests for all parties endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_party = {
            "name": "NARC KENYA",
            "slogan": "Pamoja tujengane",
            "hq_address": "Nairobe",
            "logo_url": "urlkljkj"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST parties
    def test_create_party(self):
        """ Tests that a party was created successfully """

        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_create_party_missing_fields(self):
        """ Tests when some fields are missing e.g name """

        res = self.client.post('/api/v2/parties', json={
            "slogan": "Pamoja tujengane",
            "hq_address": "Nairobe",
            "logo_url": "url"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v2/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_create_party_same_name(self):
        """ Tests when no data is provided """

        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 409)
        self.assertEqual(data['error'], 'Party already exists')
        self.assertEqual(res.status_code, 409)

    def test_create_party_int_name(self):
        """ Tests when integer is provided for name """

        self.new_party['name'] = 3
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Integer types are not allowed for some fields')
        self.assertEqual(res.status_code, 400)

    def test_create_party_short_name(self):
        """ Tests when short name is provided """

        self.new_party['name'] = 'pa'
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'The Party name provided is too short')
        self.assertEqual(res.status_code, 400)

    def test_create_party_not_admin(self):
        """ Tests when short name is provided """

        res = self.client.post('/api/v2/auth/signup', json={
            "firstname": "Andrew",
            "lastname": "Kimani",
            "othername": "Kamau",
            "email": "andrew@gmail.com",
            "phoneNumber": "0700000000",
            "passportUrl": "passport_url",
            "isAdmin": False,
            "password": "jivunie"
        })
        data = res.get_json()
        access_token = data['data'][0]['token']
        headers = {'Authorization': 'Bearer {}'.format(access_token)}

        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=headers)
        data = res.get_json()

        self.assertEqual(data['status'], 401)
        self.assertEqual(
            data['error'], 'This action is reserved to Admins only')
        self.assertEqual(res.status_code, 401)

    # tests for GET parties
    def test_get_all_parties(self):
        """ Tests when get request made to api/v2/parties """

        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        self.new_party['name'] = 'Other name'
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        self.new_party['name'] = 'Other Other name'
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)

        res = self.client.get('/api/v2/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(res.status_code, 200)

    def test_get_all_parties_no_data(self):
        """ Tests when get request made to api/v2/parties """

        res = self.client.get('/api/v2/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    # tests for GET single party
    def test_get_sigle_party(self):
        """ Tests when get reuest made to /parties/<int:id> """

        self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)

        res = self.client.get(
            '/api/v2/parties/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_party_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/v2/parties/14', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)

    # tests for DELETE party
    def test_delete_party(self):
        """ Tests when DELETE reuest made to /parties/<int:id> """

        self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)

        res = self.client.delete('/api/v2/parties/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_party_id_not_found(self):
        """ Tests DELETE request made with id that does not exist """

        res = self.client.delete('/api/v2/parties/14', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)

    # tests for PATCH party
    def test_patch_party(self):
        """ Tests when PATCH reuest made to /parties/<int:id>/name """

        self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)

        res = self.client.patch(
            '/api/v2/parties/1/Rainbow', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'Rainbow')
        self.assertEqual(res.status_code, 200)

    def test_patch_party_id_not_found(self):
        """ Tests PATCH request made with id that does not exist """

        res = self.client.patch(
            '/api/v2/parties/14/Rainbow', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)
