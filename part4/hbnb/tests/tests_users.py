import unittest
from tests.test_helpers import TestBase


class TestUserEndpoints(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.john_id, self.john_token = self._create_user(
            "John", "Doe", "johndoe@email.com"
        )
        self.jane_id, self.jane_token = self._create_user(
            "Jane", "Doe", "janedoe@email.com"
        )

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_user_success(self):
        """Creating a valid user returns 201 with an id."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Gwen",
            "last_name": "Aelle",
            "email": "gwenaelle@email.com",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["email"], "gwenaelle@email.com")

    def test_create_user_password_not_returned(self):
        """Password must never appear in the response."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Clem",
            "last_name": "Ent",
            "email": "clement@email.com",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.get_json())

    # =========================================================
    # CREATE — Invalid
    # =========================================================

    def test_create_user_duplicate_email(self):
        """Registering with an already-used email must return 400."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Duplicate",
            "last_name": "User",
            "email": "johndoe@email.com",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_no_at(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bad",
            "last_name": "Email",
            "email": "pas_un_email",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_with_space(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bad",
            "last_name": "Space",
            "email": "john doe@test.com",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email_no_domain_dot(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bad",
            "last_name": "Domain",
            "email": "john@test",
            "password": "string123"
        })

        self.assertEqual(response.status_code, 400)

    def test_create_user_password_too_short(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Short",
            "last_name": "Pass",
            "email": "short@test.com",
            "password": "abc"
        })

        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success
    # =========================================================

    def test_list_users(self):
        """GET /users/ returns a list with at least admin + john + jane."""
        response = self.client.get('/api/v1/users/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)

    def test_get_user_by_id(self):
        """GET /users/<id> returns the correct user without password."""
        response = self.client.get(f'/api/v1/users/{self.john_id}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], self.john_id)
        self.assertNotIn("password", data)

    def test_get_user_not_found(self):
        response = self.client.get(
            '/api/v1/users/00000000-0000-0000-0000-000000000000'
        )

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Own profile
    # =========================================================

    def test_update_own_profile(self):
        """A user can update their own first_name/last_name."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}',
            json={"first_name": "Johnny", "last_name": "Doe"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["first_name"], "Johnny")

    def test_update_other_user_profile_forbidden(self):
        """A user cannot modify another user's profile."""
        response = self.client.put(
            f'/api/v1/users/{self.jane_id}',
            json={"first_name": "Hacked"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_update_email_via_put_forbidden(self):
        """Email must not be modifiable via PUT /users/<id>."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}',
            json={"email": "newemail@test.com"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_update_password_via_put_forbidden(self):
        """Password must not be modifiable via PUT /users/<id>."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}',
            json={"password": "newpassword123"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_update_without_token_forbidden(self):
        """PUT without a token must return 401."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}',
            json={"first_name": "NoToken"}
        )

        self.assertEqual(response.status_code, 401)

    # =========================================================
    # UPDATE EMAIL — dedicated endpoint
    # =========================================================

    def test_update_own_email(self):
        """A user can update their own email."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}/email',
            json={"email": "john_new@test.com"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_update_email_duplicate_rejected(self):
        """Updating to an already-used email must return 400."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}/email',
            json={"email": "janedoe@email.com"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_update_other_user_email_forbidden(self):
        """A non-admin cannot update another user's email."""
        response = self.client.put(
            f'/api/v1/users/{self.jane_id}/email',
            json={"email": "hacked@test.com"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # UPDATE PASSWORD — dedicated endpoint
    # =========================================================

    def test_update_own_password(self):
        """A user can update their own password."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}/password',
            json={"password": "newpassword123"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_update_other_user_password_forbidden(self):
        """A non-admin cannot update another user's password."""
        response = self.client.put(
            f'/api/v1/users/{self.jane_id}/password',
            json={"password": "hacked123"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # ADMIN — override capabilities
    # =========================================================

    def test_admin_can_update_other_user(self):
        """Admin can update another user's first_name/last_name."""
        response = self.client.put(
            f'/api/v1/users/{self.jane_id}',
            json={"first_name": "Janette", "last_name": "Doe"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["first_name"], "Janette")

    def test_admin_cannot_update_email_via_put(self):
        """Even admin cannot bypass the email restriction on PUT /users."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}',
            json={"email": "adminchange@test.com"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_admin_can_update_other_user_email(self):
        """Admin can update another user's email via dedicated endpoint."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}/email',
            json={"email": "john_admin_update@test.com"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_can_update_other_user_password(self):
        """Admin can update another user's password via dedicated endpoint."""
        response = self.client.put(
            f'/api/v1/users/{self.john_id}/password',
            json={"password": "adminreset123"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_admin_update_nonexistent_user(self):
        """Admin updating a non-existent user must return 404."""
        response = self.client.put(
            '/api/v1/users/00000000-0000-0000-0000-000000000000',
            json={"first_name": "Ghost"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # DELETE
    # =========================================================

    def test_delete_own_account(self):
        """A user can delete their own account."""
        gwen_id, gwen_token = self._create_user(
            "Gwen", "Aelle", "gwenaelle@email.com"
        )
        response = self.client.delete(
            f'/api/v1/users/{gwen_id}',
            headers=self._auth(gwen_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_own_account_then_404(self):
        """After deletion, GET on the deleted user must return 404."""
        gwen_id, gwen_token = self._create_user(
            "Gwen", "Aelle", "gwenaelle@email.com"
        )
        self.client.delete(
            f'/api/v1/users/{gwen_id}',
            headers=self._auth(gwen_token)
        )

        response = self.client.get(f'/api/v1/users/{gwen_id}')
        self.assertEqual(response.status_code, 404)

    def test_delete_other_user_forbidden(self):
        """A non-admin cannot delete another user's account."""
        response = self.client.delete(
            f'/api/v1/users/{self.jane_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_nonexistent_user(self):
        """Deleting a non-existent user must return 404."""
        response = self.client.delete(
            '/api/v1/users/00000000-0000-0000-0000-000000000000',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_can_delete_other_user(self):
        """Admin can delete another user's account."""
        jen_id, _ = self._create_user("Jen", "Peplu", "jenpeplu@email.com")
        response = self.client.delete(
            f'/api/v1/users/{jen_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()