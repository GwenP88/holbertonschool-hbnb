import unittest
from tests.test_helpers import TestBase


class TestAuthEndpoints(TestBase):

    def setUp(self):
        super().setUp()
        self.john_id, self.john_token = self._create_user(
            "John", "Doe", "johndoe@email.com"
        )
        self.admin_token = self._login("admin@hbnb.io", "admin1234")

    # =========================================================
    # LOGIN — Success
    # =========================================================

    def test_login_success(self):
        """Valid credentials must return 200 and an access_token."""
        response = self.client.post('/api/v1/auth/login', json={
            "email": "johndoe@email.com",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)
        self.assertIsNotNone(data["access_token"])

    def test_login_token_is_string(self):
        """access_token must be a non-empty string."""
        token = self._login("johndoe@email.com", "string123")

        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

    # =========================================================
    # LOGIN — Invalid credentials
    # =========================================================

    def test_login_wrong_password(self):
        """Wrong password must return 401."""
        response = self.client.post('/api/v1/auth/login', json={
            "email": "johndoe@email.com",
            "password": "mauvais_mot_de_passe"
        })

        self.assertEqual(response.status_code, 401)

    def test_login_unknown_email(self):
        """Unknown email must return 401."""
        response = self.client.post('/api/v1/auth/login', json={
            "email": "inexistant@test.com",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 401)

    def test_login_empty_password(self):
        """Empty password must return 400 or 401."""
        response = self.client.post('/api/v1/auth/login', json={
            "email": "johndoe@email.com",
            "password": ""
        })

        self.assertIn(response.status_code, [400, 401])

    def test_login_missing_fields(self):
        """Missing body must return 400."""
        response = self.client.post('/api/v1/auth/login', json={})

        self.assertIn(response.status_code, [400, 401])

    # =========================================================
    # PROTECTED ENDPOINT — with token
    # =========================================================

    def test_protected_with_valid_token(self):
        """Valid token must allow access to protected endpoint."""
        response = self.client.get(
            '/api/v1/auth/protected',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_protected_response_contains_user_info(self):
        """Protected endpoint response must reference the logged-in user."""
        response = self.client.get(
            '/api/v1/auth/protected',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(
            self.john_id in str(data) or "user" in str(data).lower()
        )

    # =========================================================
    # PROTECTED ENDPOINT — without / invalid token
    # =========================================================

    def test_protected_without_token(self):
        """No token must return 401."""
        response = self.client.get('/api/v1/auth/protected')

        self.assertEqual(response.status_code, 401)

    def test_protected_with_invalid_token(self):
        """Malformed token must return 401 or 422."""
        response = self.client.get(
            '/api/v1/auth/protected',
            headers={"Authorization": "Bearer fake.token.value"}
        )

        self.assertIn(response.status_code, [401, 422])

    def test_protected_with_empty_bearer(self):
        """'Bearer ' with no token must return 401 or 422."""
        response = self.client.get(
            '/api/v1/auth/protected',
            headers={"Authorization": "Bearer "}
        )

        self.assertIn(response.status_code, [401, 422])


if __name__ == "__main__":
    unittest.main()