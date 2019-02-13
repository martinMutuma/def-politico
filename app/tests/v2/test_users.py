from .base_test import Base


class TestUsers(Base):
    """ Tests for all user endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.new_user = {
            "firstname": "Bedan",
            "lastname": "Kimani",
            "othername": "Kamau",
            "email": "bedank6@gmail.com",
            "phoneNumber": "0700000000",
            "passportUrl": "passport_url",
            "isAdmin": True,
            "password": "jivunie"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()

    # tests for POST register
    def test_register_user(self):
        """ Tests that a user was registered successfully """

        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(data['data'][0]['user']['firstname'], 'Bedan')
        self.assertIn('token', data['data'][0])
        self.assertEqual(res.status_code, 201)

    def test_register_user_duplicate(self):
        """ Tests that a user is not created twice with same email """

        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'A User with that email already exists')
        self.assertEqual(res.status_code, 400)

    def test_register_user_missing_fields(self):
        """ Tests when some fields are missing e.g firstname """

        res = self.client.post('/api/v2/auth/signup', json={
            "lastname": "Pamo"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'firstname field is required')
        self.assertEqual(res.status_code, 400)

    def test_register_user_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v2/auth/signup')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'No data was provided')
        self.assertEqual(res.status_code, 400)

    def test_register_short_password(self):
        """ Tests when a short password is provided """

        self.new_user['password'] = 'can'
        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 422)
        self.assertEqual(data['error'], 'Password must be at least 6 characters long')
        self.assertEqual(res.status_code, 422)

    def test_register_user_int_name(self):
        """ Tests when integer is provided for firstname """

        self.new_user['firstname'] = 3
        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Integer types are not allowed for some fields')
        self.assertEqual(res.status_code, 400)

    def test_register_user_string_bool(self):
        """ Tests when bool is not provided for isAdmin """

        self.new_user['isAdmin'] = "true"
        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'isAdmin is supposed to be a boolean value')
        self.assertEqual(res.status_code, 400)

    def test_register_user_ivalid_email(self):
        """ Tests when invalid email is provided """

        self.new_user['email'] = 'bedank6'
        res = self.client.post('/api/v2/auth/signup', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'Invalid email')
        self.assertEqual(res.status_code, 400)

    # tests for login
    def test_login_user(self):
        """ Tests that a user was loged in successfully """

        res = self.client.post('/api/v2/auth/login', json=self.new_user)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(data['data'][0]['user']['firstname'], 'Bedan')
        self.assertIn('token', data['data'][0])
        self.assertEqual(res.status_code, 201)

    def test_login_missing_email(self):
        """ Tests when some fields are missing e.g email """

        res = self.client.post('/api/v2/auth/login', json={
            "password": "jivunie"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'email field is required')
        self.assertEqual(res.status_code, 400)

    def test_login_missing_password(self):
        """ Tests when some fields are missing e.g password """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "jivunie@gmail.com"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], 'password field is required')
        self.assertEqual(res.status_code, 400)

    def test_login_no_user(self):
        """ Tests when user is not registered """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "jivunie@gmail.com",
            "password": "some_screte"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'User not registered')
        self.assertEqual(res.status_code, 404)

    def test_login_incorrect_password(self):
        """ Tests when user is not registered """

        res = self.client.post('/api/v2/auth/login', json={
            "email": "bedank6@gmail.com",
            "password": "some_screte"
        })
        data = res.get_json()

        self.assertEqual(data['status'], 401)
        self.assertEqual(data['error'], 'Incorrect password')
        self.assertEqual(res.status_code, 401)

    # tests for GET single user
    def test_get_sigle_user_profile(self):
        """ Tests when get reuest made to /users/<int:id> """

        self.client.post('/api/v2/auth/signup', json=self.new_user)

        res = self.client.get('/api/v2/users/1')
        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Success')
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['id'], 1)
        self.assertEqual(res.status_code, 200)

    def test_get_single_user_id_not_found(self):
        """ Tests request made with id that does not exist """

        res = self.client.get('/api/v2/users/14')
        data = res.get_json()

        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'User not found')
        self.assertEqual(res.status_code, 404)
