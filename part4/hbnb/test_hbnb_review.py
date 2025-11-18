import unittest
from app import create_app
from app.services import facade


class test_review_endpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Lemon",
            "email": "lemon@gmail.com",
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
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user.id,
            "place_id": place.id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_review_text(self):
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Lemon",
            "email": "lemon@gmail.com",
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
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": user.id,
            "place_id": place.id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_review_rating(self):
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Lemon",
            "email": "lemon@gmail.com",
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
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 9,
            "user_id": user.id,
            "place_id": place.id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_review_user(self):
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Lemon",
            "email": "lemon@gmail.com",
            "is_admin": False
        })
        place = facade.create_place({
            "title": "Nice Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.8749,
            "longitude": -122.4124,
            "owner_id": user.id
        })
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "azerty123456",
            "place_id": place.id
        })
        self.assertEqual(response.status_code, 404)

    def test_create_invalide_review_place(self):
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Lemon",
            "email": "lemon@gmail.com",
            "is_admin": False
        })
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user.id,
            "place_id": "azerty123456"
        })
        self.assertEqual(response.status_code, 404)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id(self):
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "azertyujikl"
        })
        review = facade.create_review({
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": place.id
        })
        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_invalid_id(self):
        response = self.client.get(f'/api/v1/reviews/azerty123456')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "azertyujikl"
        })
        review = facade.create_review({
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": place.id
        })
        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)

    def test_update_review_invalid_text(self):
        place = facade.create_place({
            "title": "Great Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "azertyujikl"
        })
        review = facade.create_review({
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": place.id
        })
        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "",
            "rating": 4
        })
        self.assertEqual(response.status_code, 400)

    def test_update_review_invalid_rating(self):
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "azertyujikl"
        })
        review = facade.create_review({
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": place.id
        })
        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "Amazing stay!",
            "rating": 10
        })
        self.assertEqual(response.status_code, 400)

    def test_update_review_invalid_id(self):
        response = self.client.put(f'/api/v1/reviews/azerty123456', json={
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_review(self):
        place = facade.create_place({
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "azertyujikl"
        })
        review = facade.create_review({
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": place.id
        })
        response = self.client.delete(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_invalid_id(self):
        response = self.client.delete('/api/v1/reviews/azerty123456')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        user = facade.create_user({
            "first_name": "John",
            "last_name": "Lemon",
            "email": "lemon@gmail.com",
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
        response = self.client.get(
            f'/api/v1/reviews/places/{place.id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_reviews_by_place_invalid_id(self):
        response = self.client.get(
            '/api/v1/reviews/places/azerty12346/reviews')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
