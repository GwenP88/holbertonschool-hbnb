"""Unit tests for Review endpoints with author/admin permissions."""

import unittest
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

        # admin
        admin = self.client.post('/api/v1/users/', json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@test.com",
            "password": "Password123"
        })

        self.admin_id = admin.get_json()["id"]
        facade.user_repo.get(self.admin_id)._is_admin = True

        # owner
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@test.com",
            "password": "Password123"
        })

        self.owner_id = owner.get_json()["id"]

        # reviewer
        reviewer = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "review@test.com",
            "password": "Password123"
        })

        self.reviewer_id = reviewer.get_json()["id"]

        self.admin_token = self._login("admin@test.com")
        self.reviewer_token = self._login("review@test.com")
        self.owner_token = self._login("owner@test.com")

        # create place
        place = self.client.post('/api/v1/places/', headers=self._auth(self.owner_token), json={
            "title": "Studio",
            "description": "Nice place",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": self.owner_id,
            "amenities": []
        })

        data = place.get_json()

        if place.status_code != 201:
            raise Exception(f"Place creation failed: {data}")

        self.place_id = data["id"]

        # create review
        review = self.client.post('/api/v1/reviews/', headers=self._auth(self.reviewer_token), json={
            "author_id": self.reviewer_id,
            "place_id": self.place_id,
            "comment": "Nice",
            "rating": 5
        })

        data = review.get_json()

        if review.status_code != 201:
            raise Exception(f"Review creation failed: {data}")

        self.review_id = data["id"]

    # helpers

    def _login(self, email):
        response = self.client.post('/api/v1/auth/login', json={
            "email": email,
            "password": "Password123"
        })
        return response.get_json()["access_token"]

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    # ==================================================
    # UPDATE
    # ==================================================

    def test_author_update_review(self):
        response = self.client.put(
            f'/api/v1/reviews/{self.review_id}',
            headers=self._auth(self.reviewer_token),
            json={"comment": "Updated"}
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_update_review(self):
        response = self.client.put(
            f'/api/v1/reviews/{self.review_id}',
            headers=self._auth(self.admin_token),
            json={"comment": "Admin edit"}
        )

        self.assertEqual(response.status_code, 200)

    # ==================================================
    # DELETE
    # ==================================================

    def test_author_delete_review(self):
        response = self.client.delete(
            f'/api/v1/reviews/{self.review_id}',
            headers=self._auth(self.reviewer_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_delete_review(self):
        response = self.client.delete(
            f'/api/v1/reviews/{self.review_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()