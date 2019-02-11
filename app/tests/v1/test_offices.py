from .base_test import Base
from app.v1.models.db import Database


class TestOffices(Base):
    """ Tests for all office endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.office_list = Database().get_table(Database.OFFICES)

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

        res = self.client.post('/api/v1/offices', json=self.new_office)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)

    def test_create_office_same_name(self):
        """ Tests when same name is given twice """

        self.client.post('/api/v1/offices', json=self.new_office)
        res = self.client.post('/api/v1/offices', json=self.new_office)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Office already exists')
        self.assertEqual(res.status_code, 400)

    def test_create_office_missing_fields(self):
        """ Tests when some fields are missing e.g name """

        res = self.client.post('/api/v1/offices', json={
            "type": "Pamoja tujengane"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_office_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    # tests for GET offices
    def test_get_all_offices(self):
        """ Tests when get request made to api/v1/offices """

        res = self.client.post('/api/v1/offices', json=self.new_office)
        self.new_office['name'] = 'Other name'
        res = self.client.post('/api/v1/offices', json=self.new_office)
        self.new_office['name'] = 'Other Other name'
        res = self.client.post('/api/v1/offices', json=self.new_office)

        res = self.client.get('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(res.status_code, 200)

    def test_get_all_offices_no_data(self):
        """ Tests when get request made to api/v1/offices """

        res = self.client.get('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)

    # tests for GET single office
    def test_get_sigle_office(self):
        """ Tests when get reuest made to /offices/<int:id> """

        self.client.post('/api/v1/offices', json=self.new_office)

        res = self.client.get('/api/v1/offices/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_office_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/v1/offices/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Office not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)

    # tests for DELETE office
    def test_delete_office(self):
        """ Tests when DELETE reuest made to /offices/<int:id> """

        self.client.post('/api/v1/offices', json=self.new_office)

        res = self.client.delete('/api/v1/offices/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_delete_office_id_not_found(self):
        """ Tests DELETE request made with id that does not exist """

        res = self.client.delete('/api/v1/offices/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Office not found')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 404)
