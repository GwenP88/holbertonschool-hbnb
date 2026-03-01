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

    # -------------------------
    # Helper
    # -------------------------
    def _create_review(self, comment="Very nice", rating=5):
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
        response = self._create_review()
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["comment"], "Very nice")

    def test_create_review_rating_min(self):
        """Rating of 1 (minimum) must be accepted."""
        response = self._create_review(rating=1)
        self.assertEqual(response.status_code, 201)

    # =========================================================
    # CREATE — Invalid
    # =========================================================

    def test_create_review_duplicate(self):
        self._create_review()
        response = self._create_review()
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_high(self):
        response = self._create_review(rating=6)
        self.assertEqual(response.status_code, 400)

    def test_create_review_rating_too_low(self):
        """Rating of 0 (below minimum) must be rejected."""
        response = self._create_review(rating=0)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_author(self):
        """Unknown author_id must be rejected (API returns 404)."""
        response = self.client.post('/api/v1/reviews/', json={
            "author_id": str(uuid.uuid4()),
            "place_id": self.place_id,
            "comment": "Test",
            "rating": 4
        })
        self.assertIn(response.status_code, [400, 404])

    def test_create_review_invalid_place(self):
        """Unknown place_id must be rejected (API returns 404)."""
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
        review_id = self._create_review().get_json()["id"]
        response = self.client.get(f'/api/v1/reviews/{review_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], review_id)

    # =========================================================
    # GET — Not found
    # =========================================================

    def test_get_review_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/reviews/{fake_id}')
        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Success
    # =========================================================

    def test_update_review_success(self):
        """PUT on an existing review must update the comment and return 200."""
        review_id = self._create_review().get_json()["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "comment": "Updated comment"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["comment"], "Updated comment")

    def test_update_review_rating_unchanged(self):
        """Updating only the comment must leave the rating intact."""
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
        review_id = self._create_review().get_json()["id"]
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_then_get(self):
        """After deletion, GET on the same review must return 404."""
        review_id = self._create_review().get_json()["id"]

        self.client.delete(f'/api/v1/reviews/{review_id}')

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()