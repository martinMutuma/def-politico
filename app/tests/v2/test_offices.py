from .base_test import Base


class TestOffices(Base):
    """ Tests for all office endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_office = {
            "name": "Governor",
            "type": "federal"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST offices
    def test_create_office(self):
        """ Tests that a office was created successfully """

        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Successfully created office')
        self.assertEqual(res.status_code, 201)

    def test_create_office_same_name_different_type(self):
        """ Tests when same name is given twice """

        self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)

        self.new_office['type'] = 'local'

        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Successfully created office')
        self.assertEqual(res.status_code, 201)

    def test_create_office_same_name_same_type(self):
        """ Tests when same name is given twice """

        self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['error'], 'Office already exists')
        self.assertEqual(data['status'], 409)
        self.assertEqual(res.status_code, 409)

    def test_create_office_missing_fields(self):
        """ Tests when some fields are missing e.g name """

        res = self.client.post('/api/v2/offices', json={
            "type": "Pamoja tujengane"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_office_incorrect_type(self):
        """ Tests when incorrect type is provided """

        res = self.client.post('/api/v2/offices', json={
            "name": "Governor",
            "type": "random"
        }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(
            data['error'], "'random' is not a supported office type")
        self.assertEqual(res.status_code, 422)

    def test_create_office_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post(
            '/api/v2/offices', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_create_office_int_name(self):
        """ Tests when integer is provided for name """

        self.new_office['name'] = 3
        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(
            data['error'], "Invalid or empty string for name")
        self.assertEqual(res.status_code, 422)

    def test_create_office_short_name(self):
        """ Tests when short name is provided """

        self.new_office['name'] = 'of'
        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(
            data['error'], 'The Office name provided is too short')
        self.assertEqual(res.status_code, 422)

    # tests for GET offices
    def test_get_all_offices(self):
        """ Tests when get request made to api/v2/offices """

        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        self.new_office['name'] = 'Other name'
        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)
        self.new_office['name'] = 'Other Other name'
        res = self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)

        res = self.client.get('/api/v2/offices', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Successfully retreived all offices')
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(res.status_code, 200)

    def test_get_all_offices_no_data(self):
        """ Tests when get request made to api/v2/offices """

        res = self.client.get(
            '/api/v2/offices', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(
            data['message'], 'Successfully retreived all offices')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    # tests for GET single office
    def test_get_sigle_office(self):
        """ Tests when get reuest made to /offices/<int:id> """

        self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)

        res = self.client.get(
            '/api/v2/offices/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(
            data['message'], 'Successfully retreived single office')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_office_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get(
            '/api/v2/offices/14', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Office not found')
        self.assertEqual(res.status_code, 404)

    # tests for DELETE office
    def test_delete_office(self):
        """ Tests when DELETE reuest made to /offices/<int:id> """

        self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)

        res = self.client.delete(
            '/api/v2/offices/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Successfully deleted office')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_office_id_not_found(self):
        """Tests DELETE request made with id that does not exist"""

        res = self.client.delete(
            '/api/v2/offices/14', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Office not found')
        self.assertEqual(res.status_code, 404)

    # tests for PATCH office
    def test_patch_office(self):
        """ Tests when PATCH request made to /offices/<int:id>/name """

        self.client.post(
            '/api/v2/offices', json=self.new_office, headers=self.headers)

        res = self.client.patch(
            '/api/v2/offices/1/name', json={
                "name": "New name"
            }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Successfully updated office name')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(data['data'][0]['name'], 'New name')
        self.assertEqual(res.status_code, 200)

    def test_patch_office_id_not_found(self):
        """ Tests PATCH request made with id that does not exist """

        res = self.client.patch(
            '/api/v2/offices/14/name', json={
                "name": "New name"
            }, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Office not found')
        self.assertEqual(res.status_code, 404)
