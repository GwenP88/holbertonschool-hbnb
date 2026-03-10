"""Unit tests for Place endpoints with JWT ownership rules."""

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

        # other user
        other = self.client.post('/api/v1/users/', json={
            "first_name": "Other",
            "last_name": "User",
            "email": "other@test.com",
            "password": "Password123"
        })

        self.other_id = other.get_json()["id"]

        self.admin_token = self._login("admin@test.com")
        self.owner_token = self._login("owner@test.com")
        self.other_token = self._login("other@test.com")

        # create amenity
        amenity = self.client.post(
            '/api/v1/amenities/',
            headers=self._auth(self.admin_token),
            json={"name": "wifi"}
        )

        self.amenity_id = amenity.get_json()["id"]

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
    # UPDATE PLACE
    # ==================================================

    def test_owner_update_place(self):
        response = self.client.put(
            f'/api/v1/places/{self.place_id}',
            headers=self._auth(self.owner_token),
            json={"title": "Updated"}
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_update_place_forbidden(self):
        response = self.client.put(
            f'/api/v1/places/{self.place_id}',
            headers=self._auth(self.other_token),
            json={"title": "Hack"}
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_update_place(self):
        response = self.client.put(
            f'/api/v1/places/{self.place_id}',
            headers=self._auth(self.admin_token),
            json={"title": "AdminEdit"}
        )

        self.assertEqual(response.status_code, 200)

    # ==================================================
    # AMENITY LINK
    # ==================================================

    def test_owner_add_amenity(self):
        response = self.client.post(
            f'/api/v1/places/{self.place_id}/amenities/{self.amenity_id}',
            headers=self._auth(self.owner_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_add_amenity_forbidden(self):
        response = self.client.post(
            f'/api/v1/places/{self.place_id}/amenities/{self.amenity_id}',
            headers=self._auth(self.other_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_add_amenity(self):
        response = self.client.post(
            f'/api/v1/places/{self.place_id}/amenities/{self.amenity_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()