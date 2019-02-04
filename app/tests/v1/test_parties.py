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

    def test_create_party_no_data(self):
        """ Tests that a party was created successfully """

        res = self.client.post('/api/v1/parties', json=self.new_party)
        data = res.get_json()

        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Party created successfully')
        self.assertEqual(res.status_code, 201)
