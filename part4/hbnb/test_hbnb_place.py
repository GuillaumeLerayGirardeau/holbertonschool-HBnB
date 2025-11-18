import unittest
from app import create_app
from app.services import facade


class test_place_endpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_places(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_place_title(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_place_description(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_place_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -52.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_place_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 237.7749,
            "longitude": -122.4194,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_place_longitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -5122.4194,
            "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_place_owner(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner_id(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "azerty123456"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_place(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_get_place_by_id(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        address = f'/api/v1/places/{place.id}'
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)

    def test_get_place_by_id_invalid_id(self):
        response = self.client.get('/api/v1/places/azerty123456')
        self.assertEqual(response.status_code, 404)

    def test_update_place(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Apartment",
            "description": "Nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        address = f'/api/v1/places/{place.id}'
        response = self.client.put(address, json={
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(response.status_code, 200)

    def test_update_place_invalid_title(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        address = f'/api/v1/places/{place.id}'
        response = self.client.put(address, json={
            "title": "",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_invalid_description(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        address = f'/api/v1/places/{place.id}'
        response = self.client.put(address, json={
            "title": "Luxury Condo",
            "description": "",
            "price": 200.0
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_invalid_price(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        address = f'/api/v1/places/{place.id}'
        response = self.client.put(address, json={
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": -200.0
        })
        self.assertEqual(response.status_code, 400)

    def test_update_place_invalid_id(self):
        response = self.client.put('/api/v1/places/azerty123456', json={
            "title": "Great House",
            "description": "A great place to stay",
            "price": 100.0
        })
        self.assertEqual(response.status_code, 404)

    def test_add_new_amenity(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        facade.create_amenity({"name": "Pool"})
        address = f'/api/v1/places/{place.id}'
        response = self.client.post(address, json={"name": "Pool"})
        self.assertEqual(response.status_code, 200)

    def test_add_new_amenity_invalid_amenity_name(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        address = f'/api/v1/places/{place.id}'
        response = self.client.post(address, json={"name": "Garden"})
        self.assertEqual(response.status_code, 404)

    def test_add_new_amenity_invalid_input(self):
        user = facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janoe@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user.id
        })
        facade.create_amenity({"name": "Pool"})
        address = f'/api/v1/places/{place.id}'
        response = self.client.post(address, json={"data": "Pool"})
        self.assertEqual(response.status_code, 400)

    def test_add_new_amenity_invalid_place_id(self):
        facade.create_amenity({"name": "Free Wi-fi"})
        address = f'/api/v1/places/azerty123456'
        response = self.client.post(address, json={"name": "Free Wi-fi"})
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
