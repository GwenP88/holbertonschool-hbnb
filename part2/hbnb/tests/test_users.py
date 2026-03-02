"""Unit tests for User API endpoints (create, retrieve, list, and update behaviors)."""
import unittest
import uuid
from app import create_app
from app.services import facade


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """Create a test client and reset all in-memory repositories."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Reset global storage
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

    # -------------------------
    # Helper
    # -------------------------

    def _create_default_user(self, email="jane@example.com"):
        """Helper to create a default user and return its id."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": email,
            "password": "Password123"
        })
        return response.get_json()["id"]

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_user_success(self):
        """POST /users creates a user and returns 201 with expected fields."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn("id", data)
        self.assertEqual(data["email"], "jane.doe@example.com")

    def test_create_user_password_not_returned(self):
        """POST /users never returns the password field in the response."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertNotIn("password", data)

    def test_create_user_email_normalized(self):
        """POST /users stores the email in lowercase."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "JANE@EXAMPLE.COM",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["email"], "jane@example.com")

    # =========================================================
    # CREATE — Invalid input
    # =========================================================

    def test_create_user_empty_first_name(self):
        """POST /users rejects an empty first_name and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_last_name(self):
        """POST /users rejects an empty last_name and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "",
            "email": "jane@example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_no_at(self):
        """POST /users rejects emails missing '@' and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid-email",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_no_dot_in_domain(self):
        """POST /users rejects emails without a dot in the domain and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@nodot",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_empty_local_part(self):
        """POST /users rejects emails with an empty local part and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "@example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_with_spaces(self):
        """POST /users rejects emails containing spaces and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test @example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_password_too_short(self):
        """POST /users rejects passwords shorter than 8 characters and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "short"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """POST /users rejects duplicate email addresses and returns 400."""
        self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "Password123"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "jane@example.com",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        """POST /users rejects payloads with multiple invalid fields and returns 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "Password123"
        })
        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success
    # =========================================================

    def test_get_user_success(self):
        """GET /users/<id> returns 200 with user fields and without password."""
        user_id = self._create_default_user()
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], user_id)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)
        self.assertIn("email", data)
        self.assertNotIn("password", data)

    def test_list_users_success(self):
        """GET /users returns 200 and lists all created users."""
        self._create_default_user("user1@example.com")
        self._create_default_user("user2@example.com")
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    # =========================================================
    # GET — Not found
    # =========================================================

    def test_get_user_not_found(self):
        """GET /users/<id> returns 404 when the user does not exist."""
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/users/{fake_id}')
        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Success
    # =========================================================

    def test_update_user_first_name(self):
        """PUT /users/<id> updates first_name and returns 200."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Updated"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["first_name"], "Updated")

    def test_update_user_success(self):
        """PUT /users/<id> updates multiple fields and returns 200."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Updated",
            "last_name": "Name"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["first_name"], "Updated")
        self.assertEqual(data["last_name"], "Name")

    def test_update_user_email_normalized(self):
        """PUT /users/<id> normalizes updated email to lowercase."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "email": "NEW.EMAIL@EXAMPLE.COM"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "new.email@example.com")

    def test_update_user_password_success(self):
        """PUT /users/<id> updates password without returning it in the response."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "password": "NewPass123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("password", response.get_json())

    # =========================================================
    # UPDATE — Invalid / forbidden
    # =========================================================

    def test_update_user_duplicate_email(self):
        """PUT /users/<id> rejects updating email to an existing one and returns 400."""
        self._create_default_user("user1@example.com")
        user2_id = self._create_default_user("user2@example.com")
        response = self.client.put(f'/api/v1/users/{user2_id}', json={
            "email": "user1@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_is_admin_forbidden(self):
        """PUT /users/<id> rejects is_admin changes and returns 400."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "is_admin": True
        })
        self.assertEqual(response.status_code, 400)

    def test_update_password_too_short(self):
        """PUT /users/<id> rejects too-short passwords and returns 400."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "password": "short"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_unknown_field(self):
        """PUT /users/<id> rejects unknown fields and returns 400."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "nickname": "JayJay"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_invalid_email_format(self):
        """PUT /users/<id> rejects malformed email updates and returns 400."""
        user_id = self._create_default_user()
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
