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

    def test_create_party(self):
        """ Tests that a party was created successfully """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Party created successfully')
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
        self.assertEqual(data['message'], 'name field is required')
        self.assertEqual(res.status_code, 400)

    def test_create_party_no_data(self):
        """ Tests when no data is provided """

        res = self.client.post('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data was provided')
        self.assertEqual(res.status_code, 400)
