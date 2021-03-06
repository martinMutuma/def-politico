from .base_test import Base


class TestUsers(Base):
    """ Tests for all user endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_user = {
            "firstname": "James",
            "lastname": "Kimani",
            "othername": "Kamau",
            "email": "james@mail.com",
            "phoneNumber": "0700000000",
            "passportUrl": "passport_url",
            "isAdmin": True
        }

    # clear all lists after tests
    def tearDown(self):
        self.new_user['firstname'] = 'James'
        super().tearDown()

    # tests for POST register
    def test_register_user(self):
        """ Tests that a user was registered successfully """

        res = self.client.post('/api/v1/register', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(res.status_code, 201)
    
    def test_register_user_duplicate(self):
        """ Tests that a user is not created twice with same email """

        res = self.client.post('/api/v1/register', json=self.new_user)
        res = self.client.post('/api/v1/register', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'A User with that email already exists')
        self.assertEqual(res.status_code, 400)

    def test_register_user_missing_fields(self):
        """ Tests when some fields are missing e.g firstname """

        res = self.client.post('/api/v1/register', json={
            "lastname": "Pamo"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'firstname field is required')
        self.assertEqual(res.status_code, 400)

    def test_register_user_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/register')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_register_user_int_name(self):
        """ Tests when integer is provided for firstname """

        self.new_user['firstname'] = 3
        res = self.client.post('/api/v1/register', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Integer types are not allowed for some fields')
        self.assertEqual(res.status_code, 400)

    def test_register_user_string_bool(self):
        """ Tests when bool is not provided for isAdmin """

        self.new_user['isAdmin'] = "true"
        res = self.client.post('/api/v1/register', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'isAdmin is supposed to be a boolean value')
        self.assertEqual(res.status_code, 400)

    # tests for GET single office
    def test_get_sigle_user(self):
        """ Tests when get reuest made to /users/<int:id> """

        self.client.post('/api/v1/register', json=self.new_user)

        res = self.client.get('/api/v1/users/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_user_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/v1/users/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'User not found')
        self.assertEqual(res.status_code, 404)
