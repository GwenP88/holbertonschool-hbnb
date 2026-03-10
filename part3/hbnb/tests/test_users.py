"""Unit tests for User API endpoints with JWT authentication and RBAC."""

import unittest
import uuid
from app import create_app
from app.services import facade


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

        # create admin
        admin_response = self.client.post('/api/v1/users/', json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@test.com",
            "password": "Password123"
        })

        self.admin_id = admin_response.get_json()["id"]
        facade.user_repo.get(self.admin_id)._is_admin = True

        # create normal user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Normal",
            "last_name": "User",
            "email": "user@test.com",
            "password": "Password123"
        })

        self.user_id = user_response.get_json()["id"]

        self.admin_token = self._login("admin@test.com")
        self.user_token = self._login("user@test.com")

    # -----------------------
    # helpers
    # -----------------------

    def _login(self, email):
        response = self.client.post('/api/v1/auth/login', json={
            "email": email,
            "password": "Password123"
        })
        return response.get_json()["access_token"]

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    # ==================================================
    # CREATE
    # ==================================================

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@test.com",
            "password": "Password123"
        })

        self.assertEqual(response.status_code, 201)

    # ==================================================
    # GET
    # ==================================================

    def test_get_user(self):
        response = self.client.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)

    def test_list_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    # ==================================================
    # UPDATE PROFILE
    # ==================================================

    def test_user_update_own_profile(self):
        response = self.client.put(
            f'/api/v1/users/{self.user_id}',
            headers=self._auth(self.user_token),
            json={"first_name": "Updated"}
        )

        self.assertEqual(response.status_code, 200)

    def test_user_update_other_user_forbidden(self):
        response = self.client.put(
            f'/api/v1/users/{self.admin_id}',
            headers=self._auth(self.user_token),
            json={"first_name": "Hack"}
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_update_other_user(self):
        response = self.client.put(
            f'/api/v1/users/{self.user_id}',
            headers=self._auth(self.admin_token),
            json={"first_name": "AdminEdit"}
        )

        self.assertEqual(response.status_code, 200)

    # ==================================================
    # EMAIL
    # ==================================================

    def test_update_email_self(self):
        response = self.client.put(
            f'/api/v1/users/{self.user_id}/email',
            headers=self._auth(self.user_token),
            json={"email": "new@test.com"}
        )

        self.assertEqual(response.status_code, 200)

    def test_update_email_other_forbidden(self):
        response = self.client.put(
            f'/api/v1/users/{self.admin_id}/email',
            headers=self._auth(self.user_token),
            json={"email": "hack@test.com"}
        )

        self.assertEqual(response.status_code, 403)

    # ==================================================
    # PASSWORD
    # ==================================================

    def test_update_password_self(self):
        response = self.client.put(
            f'/api/v1/users/{self.user_id}/password',
            headers=self._auth(self.user_token),
            json={"password": "NewPass123"}
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()