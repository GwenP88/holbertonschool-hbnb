"""Unit tests for Amenity API endpoints with JWT authentication and admin RBAC."""

import unittest
import uuid
from app import create_app
from app.services import facade


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        """Create test client and reset in-memory repositories."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # reset storage
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

        # seed admin
        admin_response = self.client.post('/api/v1/users/', json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@test.com",
            "password": "Password123"
        })

        self.admin_id = admin_response.get_json()["id"]

        # manually promote admin
        facade.user_repo.get(self.admin_id)._is_admin = True

        # normal user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Normal",
            "last_name": "User",
            "email": "user@test.com",
            "password": "Password123"
        })

        self.user_id = user_response.get_json()["id"]

        self.admin_token = self._login("admin@test.com")
        self.user_token = self._login("user@test.com")

    # -------------------------------------------------
    # helpers
    # -------------------------------------------------

    def _login(self, email):
        """Authenticate a user and return a JWT token."""
        response = self.client.post('/api/v1/auth/login', json={
            "email": email,
            "password": "Password123"
        })
        return response.get_json()["access_token"]

    def _auth_header(self, token):
        """Return Authorization header."""
        return {"Authorization": f"Bearer {token}"}

    def _create_amenity(self, name="wifi"):
        """Create amenity as admin."""
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self._auth_header(self.admin_token),
            json={"name": name}
        )
        return response.get_json()["id"]

    # =====================================================
    # CREATE — Authorization
    # =====================================================

    def test_create_amenity_without_token(self):
        """POST /amenities without token returns 401."""
        response = self.client.post('/api/v1/amenities/', json={"name": "wifi"})
        self.assertEqual(response.status_code, 401)

    def test_create_amenity_non_admin(self):
        """POST /amenities with normal user returns 403."""
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self._auth_header(self.user_token),
            json={"name": "wifi"}
        )
        self.assertEqual(response.status_code, 403)

    # =====================================================
    # CREATE — Success
    # =====================================================

    def test_create_amenity_admin_success(self):
        """Admin can create an amenity."""
        response = self.client.post(
            '/api/v1/amenities/',
            headers=self._auth_header(self.admin_token),
            json={
                "name": "WiFi",
                "description": "High speed internet"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "wifi")
        self.assertIn("id", data)

    # =====================================================
    # CREATE — Invalid
    # =====================================================

    def test_create_amenity_duplicate(self):
        """Duplicate amenity names return 400."""
        self._create_amenity("wifi")

        response = self.client.post(
            '/api/v1/amenities/',
            headers=self._auth_header(self.admin_token),
            json={"name": "wifi"}
        )

        self.assertEqual(response.status_code, 400)

    # =====================================================
    # GET
    # =====================================================

    def test_get_amenity_success(self):
        """GET /amenities/<id> returns correct amenity."""
        amenity_id = self._create_amenity("pool")

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "pool")

    def test_list_amenities(self):
        """GET /amenities returns list."""
        self._create_amenity("wifi")
        self._create_amenity("parking")

        response = self.client.get('/api/v1/amenities/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    # =====================================================
    # UPDATE — Authorization
    # =====================================================

    def test_update_amenity_without_token(self):
        """PUT /amenities/<id> without token returns 401."""
        amenity_id = self._create_amenity()

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "pool"}
        )

        self.assertEqual(response.status_code, 401)

    def test_update_amenity_non_admin(self):
        """Normal user cannot update amenity."""
        amenity_id = self._create_amenity()

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            headers=self._auth_header(self.user_token),
            json={"name": "pool"}
        )

        self.assertEqual(response.status_code, 403)

    # =====================================================
    # UPDATE — Success
    # =====================================================

    def test_update_amenity_admin(self):
        """Admin can update amenity."""
        amenity_id = self._create_amenity("wifi")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            headers=self._auth_header(self.admin_token),
            json={"name": "pool"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "pool")

    # =====================================================
    # UPDATE — Invalid
    # =====================================================

    def test_update_amenity_duplicate(self):
        """Updating to existing name returns 400."""
        self._create_amenity("wifi")
        amenity_id = self._create_amenity("parking")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            headers=self._auth_header(self.admin_token),
            json={"name": "wifi"}
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()