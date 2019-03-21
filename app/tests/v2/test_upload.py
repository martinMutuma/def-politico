from .base_test import Base


class TestUpload(Base):
    """ Tests for uploading profile picture """

    def setUp(self):
        """ setup objects required for test """

        super().setUp()

        self.new_pic = {
            "url": "http://thisisanewpic.com"
        }

        self.no_data = {}

        self.no_url = {
            "url": ""
        }

    def tearDown(self):
        super().tearDown()

    # test for PATCH profile image
    def test_upload_image(self):
        """ Test if user can update a profile image """
        msg = "Profile image was updated successfully"

        res = self.client.patch(
            'api/v2/user/update_image', json=self.new_pic, headers=self.headers
        )

        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], msg)

    def test_no_data(self):
        """ Test if no data was provided """

        res = self.client.patch(
            'api/v2/user/update_image', json=self.no_data, headers=self.headers
        )

        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], "No data was provided")

    def test_no_url(self):
        """ Test if no url was provided """

        res = self.client.patch(
            'api/v2/user/update_image', json=self.no_url, headers=self.headers
        )

        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['error'], "url field is required")
