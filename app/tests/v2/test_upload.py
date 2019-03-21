from .base_test import Base

class TestUpload(Base):
    """ Tests for uploading profile picture """

    def setUp(self):
        """ setup objects required for test """

        super().setUp()

        self.new_pic = {
            "url": "http://thisisanewpic.com"
        }

    def tearDown(self):
        super().tearDown()

    
    #test for PATCH profile image
    def test_upload_image(self):
        """ Test if user can update a profile image """
        msg = "Profile image was updated successfully"

        res = self.client.patch(
            'api/v2/user/update_image', json=self.new_pic, headers=self.headers
        )

        data = res.get_json()

        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], msg)