import unittest
import uuid
from app import create_app
from app.services import facade


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Reset global storage
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

    # -------------------------
    # CREATE SUCCESS
    # -------------------------
    def test_create_user_success(self):
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

    # -------------------------
    # CREATE INVALID
    # -------------------------
    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "Password123"
        })

        self.assertEqual(response.status_code, 400)

    # -------------------------
    # CREATE DUPLICATE EMAIL
    # -------------------------
    def test_create_user_duplicate_email(self):
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

    # -------------------------
    # GET NOT FOUND
    # -------------------------
    def test_get_user_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/users/{fake_id}')

        self.assertEqual(response.status_code, 404)

    # -------------------------
    # UPDATE SUCCESS
    # -------------------------
    def test_update_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "Password123"
        })

        user_id = response.get_json()["id"]

        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Updated"
        })

        self.assertEqual(update_response.status_code, 200)

        data = update_response.get_json()
        self.assertEqual(data["first_name"], "Updated")

    # -------------------------
    # UPDATE DUPLICATE EMAIL
    # -------------------------
    def test_update_user_duplicate_email(self):
        user1 = self.client.post('/api/v1/users/', json={
            "first_name": "User1",
            "last_name": "Test",
            "email": "user1@example.com",
            "password": "Password123"
        }).get_json()

        user2 = self.client.post('/api/v1/users/', json={
            "first_name": "User2",
            "last_name": "Test",
            "email": "user2@example.com",
            "password": "Password123"
        }).get_json()

        response = self.client.put(f'/api/v1/users/{user2["id"]}', json={
            "email": "user1@example.com"
        })

        self.assertEqual(response.status_code, 400)

    # -------------------------
    # UPDATE FORBIDDEN FIELD
    # -------------------------
    def test_update_user_is_admin_forbidden(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "Password123"
        })

        user_id = response.get_json()["id"]

        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "is_admin": True
        })

        self.assertEqual(update_response.status_code, 400)

    # -------------------------
    # PASSWORD TOO SHORT
    # -------------------------
    def test_update_password_too_short(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "Password123"
        })

        user_id = response.get_json()["id"]

        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "password": "short"
        })

        self.assertEqual(update_response.status_code, 400)


if __name__ == "__main__":
    unittest.main()