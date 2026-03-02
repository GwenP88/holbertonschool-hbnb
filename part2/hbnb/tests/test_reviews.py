"""Unit tests for Review API endpoints (create, retrieve, update, and delete behaviors)."""
import unittest
import uuid
from app import create_app
from app.services import facade


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """Create a test client, reset storage, and seed a user and a place."""
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

    # -------------------------
    # Helper
    # -------------------------

    def _create_review(self, comment="Very nice", rating=5):
        """Helper to create a review and return the response."""
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": self.place_id,
            "comment": comment,
            "rating": rating
        })
        return response

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_review_success(self):
        """POST /reviews creates a review and returns 201 with expected fields."""
        response = self._create_review()
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["comment"], "Very nice")

    def test_create_review_rating_min(self):
        """POST /reviews accepts the minimum rating value (1) and returns 201."""
        response = self._create_review(rating=1)
        self.assertEqual(response.status_code, 201)

    # =========================================================
    # CREATE — Invalid
    # =========================================================

    def test_create_review_duplicate(self):
        """POST /reviews rejects duplicate reviews for the same author and place and returns 400."""
        self._create_review()
        response = self._create_review()
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_high(self):
        """POST /reviews rejects a rating above 5 and returns 400."""
        response = self._create_review(rating=6)
        self.assertEqual(response.status_code, 400)

    def test_create_review_rating_too_low(self):
        """POST /reviews rejects a rating below 1 and returns 400."""
        response = self._create_review(rating=0)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_author(self):
        """POST /reviews rejects an unknown author_id and returns an error status."""
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": str(uuid.uuid4()),
            "place_id": self.place_id,
            "comment": "Test",
            "rating": 4
        })
        self.assertIn(response.status_code, [400, 404])

    def test_create_review_invalid_place(self):
        """POST /reviews rejects an unknown place_id and returns an error status."""
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": self.user_id,
            "place_id": str(uuid.uuid4()),
            "comment": "Test",
            "rating": 4
        })
        self.assertIn(response.status_code, [400, 404])

    # =========================================================
    # GET — Success
    # =========================================================

    def test_get_review_success(self):
        """GET /reviews/<id> returns 200 and the correct review id."""
        review_id = self._create_review().get_json()["id"]
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], review_id)

    # =========================================================
    # GET — Not found
    # =========================================================

    def test_get_review_not_found(self):
        """GET /reviews/<id> returns 404 when the review does not exist."""
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/reviews/{fake_id}')
        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Success
    # =========================================================

    def test_update_review_success(self):
        """PUT /reviews/<id> updates the comment and returns 200."""
        review_id = self._create_review().get_json()["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "comment": "Updated comment"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["comment"], "Updated comment")

    def test_update_review_rating_unchanged(self):
        """PUT /reviews/<id> keeps rating unchanged when only updating comment."""
        review_id = self._create_review(rating=4).get_json()["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "comment": "New comment"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["rating"], 4)

    # =========================================================
    # DELETE — Success + 404 after
    # =========================================================

    def test_delete_review(self):
        """DELETE /reviews/<id> removes the review and returns 200."""
        review_id = self._create_review().get_json()["id"]
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_then_get(self):
        """DELETE then GET on the same review returns 404."""
        review_id = self._create_review().get_json()["id"]
        self.client.delete(f'/api/v1/reviews/{review_id}')
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
