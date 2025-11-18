import unittest
from app import create_app
from app.services import facade


class test_amenities_endpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenities(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenity(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_by_id(self):
        amenity = facade.create_amenity({"name": "Wi-fi"})
        address = f'/api/v1/amenities/{amenity.id}'
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_by_id_invalid_id(self):
        response = self.client.get('/api/v1/amenities/azerty123456')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        amenity = facade.create_amenity({"name": "Balcony"})
        address = f'/api/v1/amenities/{amenity.id}'
        response = self.client.put(address, json={
            "name": "TV"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_invalid_name(self):
        amenity = facade.create_amenity({"name": "Swimming pool"})
        address = f'/api/v1/amenities/{amenity.id}'
        response = self.client.put(address, json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_invalid_id(self):
        address = f'/api/v1/amenities/azerty123456'
        response = self.client.put(address, json={
            "name": "TV"
        })
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
