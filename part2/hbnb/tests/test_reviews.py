import unittest
import uuid
from app import create_app
from app.services import facade


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

        # Create user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Password123"
            })
        self.user_id = user_response.get_json()["id"]

        # Create place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Studio",
            "description": "Nice place",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.place_id = place_response.get_json()["id"]

    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": self.place_id,
            "comment": "Very nice",
            "rating": 5
        })

        self.assertEqual(response.status_code, 201)

    def test_create_review_duplicate(self):
        self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": self.place_id,
            "comment": "Very nice",
            "rating": 5
        })

        response = self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": self.place_id,
            "comment": "Very nice",
            "rating": 5
        })

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": self.place_id,
            "comment": "Bad rating",
            "rating": 6
        })

        self.assertEqual(response.status_code, 400)

    def test_delete_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": self.place_id,
            "comment": "To delete",
            "rating": 5
        })

        review_id = response.get_json()["id"]

        delete_response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 200)

    def test_get_review_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/reviews/{fake_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()