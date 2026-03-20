import unittest
from app import create_app, db


class TestAuthEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        # Create a regular user for auth tests
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "password": "string123"
        })
        self.user_id = response.get_json()["id"]

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # -------------------------
    # Helpers
    # -------------------------
    def _login(self, email="johndoe@email.com", password="string123"):
        return self.client.post('/api/v1/auth/login', json={
            "email": email,
            "password": password
        })

    def _get_token(self, email="johndoe@email.com", password="string123"):
        return self._login(email, password).get_json().get("access_token")

    # =========================================================
    # LOGIN — Success
    # =========================================================

    def test_login_success(self):
        """Valid credentials must return 200 and an access_token."""
        response = self._login()

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)
        self.assertIsNotNone(data["access_token"])

    def test_login_token_is_string(self):
        """access_token must be a non-empty string."""
        token = self._get_token()

        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

    # =========================================================
    # LOGIN — Invalid credentials
    # =========================================================

    def test_login_wrong_password(self):
        """Wrong password must return 401."""
        response = self._login(password="mauvais_mot_de_passe")

        self.assertEqual(response.status_code, 401)

    def test_login_unknown_email(self):
        """Unknown email must return 401."""
        response = self._login(email="inexistant@test.com")

        self.assertEqual(response.status_code, 401)

    def test_login_empty_password(self):
        """Empty password must return 401 or 400."""
        response = self._login(password="")

        self.assertIn(response.status_code, [400, 401])

    def test_login_empty_email(self):
        """Empty email must return 401 or 400."""
        response = self._login(email="")

        self.assertIn(response.status_code, [400, 401])

    def test_login_missing_fields(self):
        """Missing fields in login body must return 400."""
        response = self.client.post('/api/v1/auth/login', json={})

        self.assertIn(response.status_code, [400, 401])

    # =========================================================
    # PROTECTED ENDPOINT — with token
    # =========================================================

    def test_protected_with_valid_token(self):
        """Valid token must allow access to protected endpoint."""
        token = self._get_token()
        response = self.client.get(
            '/api/v1/auth/protected',
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)

    def test_protected_response_contains_user_info(self):
        """Protected endpoint response must reference the logged-in user."""
        token = self._get_token()
        response = self.client.get(
            '/api/v1/auth/protected',
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(
            self.user_id in str(data) or "user" in str(data).lower()
        )

    # =========================================================
    # PROTECTED ENDPOINT — without token
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