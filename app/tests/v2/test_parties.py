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
            "logo_url": "https://kurayangu.herokuapp.com",
            "manifesto": "We will bring change"
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
            "logo_url": "https://kurayangu.herokuapp.com"
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

        self.assertEqual(data['status'], 422)
        self.assertEqual(data['error'], "Invalid or empty string for name")
        self.assertEqual(res.status_code, 422)

    def test_create_party_long_slogan(self):
        """ Tests when slogan exceeds limit """

        self.new_party['slogan'] = """
        To change the world we need to change ourselves first and 
        to change ourselfve we need to change some other stuff
        """
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'], "Slogan should not exceed 30 characters")
        self.assertEqual(res.status_code, 400)

    def test_create_party_invalid_link(self):
        """ Tests when an invalid link is provided """

        self.new_party['logo_url'] = 'cansd'
        res = self.client.post('/api/v2/parties', json=self.new_party,
            headers=self.headers)
        data = res.get_json()
        print(data)
        self.assertEqual(data['status'], 422)
        self.assertEqual(
            data['error'], 'Invalid link for logo_url')
        self.assertEqual(res.status_code, 422)

    def test_create_party_long_manifesto(self):
        """ Tests when slogan exceeds limit """

        self.new_party['manifesto'] = """
        The Manifesto Project provides the scientific community
        with parties’ policy positions derived from a content
        analysis of parties’ electoral manifestos. It covers over
        1000 parties from 1945 until today in over 50 countries on
         five continents. The DFG-funded MARPOR project continues th
          work of the Manifesto Research Group (MRG) and the
          Comparative Manifestos Project (CMP). On this website
          you find the Manifesto Project Dataset containing the
          parties' policy preferences generated by the project. You
          also find coded and uncoded election manifestos of the parties
        """
        res = self.client.post(
            '/api/v2/parties', json=self.new_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(
            data['error'], "Manifesto should not exceed 230 characters")
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
            "passportUrl": "https://kurayangu.herokuapp.com",
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
            '/api/v2/parties/1/name', json={
                "name": "New name"
            }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'New name')
        self.assertEqual(res.status_code, 200)

    def test_patch_party_id_not_found(self):
        """ Tests PATCH request made with id that does not exist """

        res = self.client.patch(
            '/api/v2/parties/14/name', json={
                "name": "New name"
            }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Party not found')
        self.assertEqual(res.status_code, 404)