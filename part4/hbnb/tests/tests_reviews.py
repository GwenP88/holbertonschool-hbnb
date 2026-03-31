import unittest
from tests.test_helpers import TestBase


class TestReviewEndpoints(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.john_id, self.john_token = self._create_user(
            "John", "Doe", "johndoe@email.com"
        )
        self.jane_id, self.jane_token = self._create_user(
            "Jane", "Doe", "janedoe@email.com"
        )
        self.gwen_id, self.gwen_token = self._create_user(
            "Gwen", "Aelle", "gwenaelle@email.com"
        )
        # John's place — Jane and Gwen will review it
        self.john_place_id = self._create_place(
            self.john_token,
            title="Sunny Loft in the City Center",
            price=95,
            latitude=48.8566,
            longitude=2.3522,
            description="A bright and modern loft."
        )

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_review_success(self):
        """Authenticated user can leave a review on someone else's place."""
        response = self._create_review(
            self.jane_token,
            self.john_place_id,
            comment="Absolutely loved the loft! The location was unbeatable.",
            rating=5
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 5)

    def test_create_review_rating_min(self):
        """Rating of 1 must be accepted."""
        response = self._create_review(self.jane_token, self.john_place_id, rating=1)

        self.assertEqual(response.status_code, 201)

    def test_create_review_rating_max(self):
        """Rating of 5 must be accepted."""
        response = self._create_review(self.jane_token, self.john_place_id, rating=5)

        self.assertEqual(response.status_code, 201)

    # =========================================================
    # CREATE — Forbidden / Invalid
    # =========================================================

    def test_create_review_without_token_forbidden(self):
        """Creating a review without a token must return 401."""
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "No token",
            "rating": 4,
            "place_id": self.john_place_id
        })

        self.assertEqual(response.status_code, 401)

    def test_create_review_on_own_place_forbidden(self):
        """Owner cannot review their own place."""
        response = self._create_review(
            self.john_token,
            self.john_place_id,
            comment="Mon propre loft est super",
            rating=5
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_duplicate_forbidden(self):
        """A user cannot leave a second review on the same place."""
        self._create_review(self.jane_token, self.john_place_id)
        response = self._create_review(
            self.jane_token,
            self.john_place_id,
            comment="Deuxième review",
            rating=3
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_high(self):
        """Rating above 5 must be rejected."""
        response = self._create_review(self.jane_token, self.john_place_id, rating=10)

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_low(self):
        """Rating of 0 must be rejected."""
        response = self._create_review(self.jane_token, self.john_place_id, rating=0)

        self.assertEqual(response.status_code, 400)

    def test_create_review_nonexistent_place(self):
        """Review on a non-existent place must return 404."""
        response = self._create_review(
            self.jane_token,
            "00000000-0000-0000-0000-000000000000"
        )

        self.assertIn(response.status_code, [400, 404])

    # =========================================================
    # GET — Success (public)
    # =========================================================

    def test_list_reviews(self):
        """GET /reviews/ returns a list of all reviews."""
        self._create_review(self.jane_token, self.john_place_id)
        response = self.client.get('/api/v1/reviews/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_review_by_id(self):
        """GET /reviews/<id> returns the correct review."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.get(f'/api/v1/reviews/{review_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], review_id)

    def test_get_review_not_found(self):
        response = self.client.get(
            '/api/v1/reviews/00000000-0000-0000-0000-000000000000'
        )

        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        """GET /places/<id>/reviews returns all reviews for that place."""
        self._create_review(self.jane_token, self.john_place_id)
        self._create_review(self.gwen_token, self.john_place_id)
        response = self.client.get(
            f'/api/v1/places/{self.john_place_id}/reviews'
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_reviews_by_nonexistent_place(self):
        """GET /places/<bad_id>/reviews must return 404."""
        response = self.client.get(
            '/api/v1/places/00000000-0000-0000-0000-000000000000/reviews'
        )

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Own review
    # =========================================================

    def test_author_can_update_own_review(self):
        """Review author can update their comment and rating."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"comment": "Appartement encore mieux que prévu !", "rating": 5},
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()["comment"],
            "Appartement encore mieux que prévu !"
        )

    def test_update_review_preserves_rating(self):
        """Updating only the comment must leave the rating intact."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id, rating=4
        ).get_json()["id"]
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"comment": "Updated comment only"},
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["rating"], 4)

    # =========================================================
    # UPDATE — Forbidden
    # =========================================================

    def test_non_author_cannot_update_review(self):
        """A user who is not the author cannot update the review."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"comment": "Review hackée"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_update_review_without_token_forbidden(self):
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"comment": "No token"}
        )

        self.assertEqual(response.status_code, 401)

    # =========================================================
    # UPDATE — Admin override
    # =========================================================

    def test_admin_can_update_any_review(self):
        """Admin can update a review they did not write."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"comment": "Review updated by admin", "rating": 4},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_review_on_any_place(self):
        """Admin can leave a review on any place."""
        response = self._create_review(
            self.admin_token,
            self.john_place_id,
            comment="Admin review test on John's loft",
            rating=4
        )

        self.assertEqual(response.status_code, 201)

    # =========================================================
    # DELETE — Own review
    # =========================================================

    def test_author_can_delete_own_review(self):
        """Review author can delete their own review."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_review_then_404(self):
        """After deletion, GET on the deleted review must return 404."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.jane_token)
        )

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)

    # =========================================================
    # DELETE — Forbidden
    # =========================================================

    def test_non_author_cannot_delete_review(self):
        """A user who is not the author cannot delete the review."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_review_without_token_forbidden(self):
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.delete(f'/api/v1/reviews/{review_id}')

        self.assertEqual(response.status_code, 401)

    def test_delete_nonexistent_review(self):
        """Deleting a non-existent review must return 404."""
        response = self.client.delete(
            '/api/v1/reviews/00000000-0000-0000-0000-000000000000',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # DELETE — Admin override
    # =========================================================

    def test_admin_can_delete_any_review(self):
        """Admin can delete a review they did not write."""
        review_id = self._create_review(
            self.jane_token, self.john_place_id
        ).get_json()["id"]
        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()