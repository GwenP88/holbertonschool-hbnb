import unittest
from app import create_app, db


class TestReviewEndpointsPart3(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        # Create admin
        r_admin = self.client.post('/api/v1/users/', json={
            "first_name": "Admin",
            "last_name": "HBnB",
            "email": "admin@hbnb.io",
            "password": "admin1234",
            "is_admin": True
        })
        self.admin_id = r_admin.get_json()["id"]
        self.admin_token = self._login("admin@hbnb.io", "admin1234")

        # Create John (place owner)
        r_john = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "password": "string123"
        })
        self.john_id = r_john.get_json()["id"]
        self.john_token = self._login("johndoe@email.com", "string123")

        # Create Jane (reviewer)
        r_jane = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@email.com",
            "password": "string123"
        })
        self.jane_id = r_jane.get_json()["id"]
        self.jane_token = self._login("janedoe@email.com", "string123")

        # Create Gwen (third reviewer)
        r_gwen = self.client.post('/api/v1/users/', json={
            "first_name": "Gwen",
            "last_name": "Aelle",
            "email": "gwenaelle@email.com",
            "password": "string123"
        })
        self.gwen_id = r_gwen.get_json()["id"]
        self.gwen_token = self._login("gwenaelle@email.com", "string123")

        # Create John's place
        r_place = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Sunny Loft in the City Center",
                "description": "A bright and modern loft.",
                "price": 95,
                "latitude": 48.8566,
                "longitude": 2.3522,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )
        self.john_place_id = r_place.get_json()["id"]

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # -------------------------
    # Helpers
    # -------------------------
    def _login(self, email, password):
        response = self.client.post('/api/v1/auth/login', json={
            "email": email,
            "password": password
        })
        return response.get_json().get("access_token")

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def _create_review(self, token, place_id=None, comment="Very nice", rating=5):
        return self.client.post(
            '/api/v1/reviews/',
            json={
                "comment": comment,
                "rating": rating,
                "place_id": place_id or self.john_place_id
            },
            headers=self._auth(token)
        )

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_review_success(self):
        """Authenticated user can leave a review on someone else's place."""
        response = self._create_review(
            self.jane_token,
            comment="Absolutely loved the loft! The location was unbeatable.",
            rating=5
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 5)

    def test_create_review_rating_min(self):
        """Rating of 1 must be accepted."""
        response = self._create_review(self.jane_token, rating=1)

        self.assertEqual(response.status_code, 201)

    def test_create_review_rating_max(self):
        """Rating of 5 must be accepted."""
        response = self._create_review(self.jane_token, rating=5)

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
            comment="Mon propre loft est super",
            rating=5
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_duplicate_forbidden(self):
        """A user cannot leave a second review on the same place."""
        self._create_review(self.jane_token)
        response = self._create_review(
            self.jane_token,
            comment="Deuxième review",
            rating=3
        )

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_high(self):
        """Rating above 5 must be rejected."""
        response = self._create_review(self.jane_token, rating=10)

        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_too_low(self):
        """Rating of 0 must be rejected."""
        response = self._create_review(self.jane_token, rating=0)

        self.assertEqual(response.status_code, 400)

    def test_create_review_nonexistent_place(self):
        """Review on a non-existent place must return 404."""
        response = self._create_review(
            self.jane_token,
            place_id="00000000-0000-0000-0000-000000000000"
        )

        self.assertIn(response.status_code, [400, 404])

    # =========================================================
    # GET — Success (public)
    # =========================================================

    def test_list_reviews(self):
        """GET /reviews/ returns a list of all reviews."""
        self._create_review(self.jane_token)

        response = self.client.get('/api/v1/reviews/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertGreaterEqual(len(response.get_json()), 1)

    def test_get_review_by_id(self):
        """GET /reviews/<id> returns the correct review."""
        review_id = self._create_review(self.jane_token).get_json()["id"]
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
        self._create_review(self.jane_token)
        self._create_review(self.gwen_token)

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
        review_id = self._create_review(self.jane_token).get_json()["id"]

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
        review_id = self._create_review(self.jane_token, rating=4).get_json()["id"]

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
        review_id = self._create_review(self.jane_token).get_json()["id"]

        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"comment": "Review hackée"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_update_review_without_token_forbidden(self):
        review_id = self._create_review(self.jane_token).get_json()["id"]

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
        review_id = self._create_review(self.jane_token).get_json()["id"]

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
            comment="Admin review test on John's loft",
            rating=4
        )

        self.assertEqual(response.status_code, 201)

    # =========================================================
    # DELETE — Own review
    # =========================================================

    def test_author_can_delete_own_review(self):
        """Review author can delete their own review."""
        review_id = self._create_review(self.jane_token).get_json()["id"]

        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_review_then_404(self):
        """After deletion, GET on the deleted review must return 404."""
        review_id = self._create_review(self.jane_token).get_json()["id"]

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
        review_id = self._create_review(self.jane_token).get_json()["id"]

        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_review_without_token_forbidden(self):
        review_id = self._create_review(self.jane_token).get_json()["id"]

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
        review_id = self._create_review(self.jane_token).get_json()["id"]

        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()