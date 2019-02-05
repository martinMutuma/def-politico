from .base_test import Base
from app.v1.routes import office_list


class TestParties(Base):
    """ Tests for all office endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_office = {
            "name": "NARC",
            "type": "federal"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        office_list.clear()

    # tests for POST offices
    def test_create_office(self):
        """ Tests that a office was created successfully """

        res = self.client.post('/api/v1/offices', json=self.new_office)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Office created successfully')
        self.assertEqual(res.status_code, 201)

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
        res = self.client.post('/api/v1/offices', json=self.new_office)
        res = self.client.post('/api/v1/offices', json=self.new_office)

        res = self.client.get('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was sent successfully')
        self.assertEqual(len(data['data']), 3)
        self.assertEqual(res.status_code, 200)

    def test_get_all_offices_no_data(self):
        """ Tests when get request made to api/v1/offices """

        res = self.client.get('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Request was sent successfully')
        self.assertEqual(len(data['data']), 0)
        self.assertEqual(res.status_code, 200)
