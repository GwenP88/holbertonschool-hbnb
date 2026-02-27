import unittest
import uuid
from app import create_app
from app.services import facade


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

        # Create required user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Password123"
        })
        
        self.user_id = user_response.get_json()["id"]

        # Create required amenity
        amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "wifi"
        })
        self.amenity_id = amenity_response.get_json()["id"]

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Studio",
            "description": "Nice place",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": self.user_id,
            "amenities": []
        })

        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid lat",
            "description": "bad",
            "price": 50,
            "latitude": 200,
            "longitude": 6,
            "owner_id": self.user_id,
            "amenities": []
        })

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid owner",
            "description": "bad",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": str(uuid.uuid4()),
            "amenities": []
        })

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_amenity(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid amenity",
            "description": "bad",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": self.user_id,
            "amenities": [str(uuid.uuid4())]
        })

        self.assertEqual(response.status_code, 400)

    def test_get_place_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/places/{fake_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()