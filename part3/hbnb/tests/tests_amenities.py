import unittest
from app import create_app, db


class TestAmenityEndpointsPart3(unittest.TestCase):

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

        # Create regular user (John)
        r_john = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "password": "string123"
        })
        self.john_id = r_john.get_json()["id"]
        self.john_token = self._login("johndoe@email.com", "string123")

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

    def _create_amenity(self, name, description=None):
        payload = {"name": name}
        if description:
            payload["description"] = description
        response = self.client.post(
            '/api/v1/amenities/',
            json=payload,
            headers=self._auth(self.admin_token)
        )
        return response.get_json()["id"]

    # =========================================================
    # CREATE — Success (admin)
    # =========================================================

    def test_create_amenity_with_description(self):
        """Admin can create an amenity with a description."""
        response = self.client.post(
            '/api/v1/amenities/',
            json={
                "name": "Rooftop Terrace",
                "description": "A spacious rooftop terrace with panoramic city views."
            },
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "rooftop terrace")

    def test_create_amenity_without_description(self):
        """Admin can create an amenity without a description."""
        response = self.client.post(
            '/api/v1/amenities/',
            json={"name": "Hot Tub"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_amenity_name_normalized(self):
        """Amenity name must be stored in lowercase."""
        response = self.client.post(
            '/api/v1/amenities/',
            json={"name": "GYM ROOM"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "gym room")

    # =========================================================
    # CREATE — Forbidden (non-admin)
    # =========================================================

    def test_create_amenity_without_token_forbidden(self):
        """Creating an amenity without a token must return 401."""
        response = self.client.post(
            '/api/v1/amenities/',
            json={"name": "Jacuzzi"}
        )

        self.assertEqual(response.status_code, 401)

    def test_create_amenity_as_regular_user_forbidden(self):
        """A non-admin user cannot create amenities."""
        response = self.client.post(
            '/api/v1/amenities/',
            json={"name": "Jacuzzi", "description": "Luxury jacuzzi"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    # =========================================================
    # CREATE — Invalid data
    # =========================================================

    def test_create_amenity_duplicate_name(self):
        """Creating an amenity with an already-existing name must return 400."""
        self._create_amenity("wifi")

        response = self.client.post(
            '/api/v1/amenities/',
            json={"name": "wifi", "description": "Another wifi"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_empty_name(self):
        response = self.client.post(
            '/api/v1/amenities/',
            json={"name": ""},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success (public)
    # =========================================================

    def test_list_amenities(self):
        """GET /amenities/ returns the full list."""
        self._create_amenity("Fireplace", "A cozy wood-burning fireplace.")
        self._create_amenity("Sauna")

        response = self.client.get('/api/v1/amenities/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_amenity_by_id(self):
        """GET /amenities/<id> returns the correct amenity."""
        amenity_id = self._create_amenity(
            "Private Parking",
            "Secure underground parking space included, available 24/7."
        )
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], amenity_id)
        self.assertEqual(data["name"], "private parking")

    def test_get_amenity_not_found(self):
        response = self.client.get(
            '/api/v1/amenities/00000000-0000-0000-0000-000000000000'
        )

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Success (admin)
    # =========================================================

    def test_update_amenity_as_admin(self):
        """Admin can update an amenity's name and description."""
        amenity_id = self._create_amenity("Private Parking")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "Parking gratuit", "description": "Free private parking"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "parking gratuit")

    # =========================================================
    # UPDATE — Forbidden (non-admin)
    # =========================================================

    def test_update_amenity_as_regular_user_forbidden(self):
        """A non-admin cannot update an amenity."""
        amenity_id = self._create_amenity("Sauna")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "Hacked amenity"},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_update_amenity_without_token_forbidden(self):
        """Updating an amenity without a token must return 401."""
        amenity_id = self._create_amenity("Sauna")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "No token"}
        )

        self.assertEqual(response.status_code, 401)

    # =========================================================
    # UPDATE — Invalid data
    # =========================================================

    def test_update_amenity_duplicate_name(self):
        """Renaming to an already-existing name must return 400."""
        self._create_amenity("wifi")
        amenity_id = self._create_amenity("sauna")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "wifi"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_update_amenity_not_found(self):
        """Updating a non-existent amenity must return 404."""
        response = self.client.put(
            '/api/v1/amenities/00000000-0000-0000-0000-000000000000',
            json={"name": "Ghost amenity"},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 404)

    def test_update_amenity_empty_name(self):
        amenity_id = self._create_amenity("Sauna")

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": ""},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 400)

    # =========================================================
    # DELETE — Success (admin)
    # =========================================================

    def test_delete_amenity_as_admin(self):
        """Admin can delete an amenity."""
        amenity_id = self._create_amenity("Gym Room")

        response = self.client.delete(
            f'/api/v1/amenities/{amenity_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_amenity_then_404(self):
        """After deletion, GET on the deleted amenity must return 404."""
        amenity_id = self._create_amenity("Gym Room")

        self.client.delete(
            f'/api/v1/amenities/{amenity_id}',
            headers=self._auth(self.admin_token)
        )

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 404)

    # =========================================================
    # DELETE — Forbidden (non-admin)
    # =========================================================

    def test_delete_amenity_as_regular_user_forbidden(self):
        """A non-admin cannot delete an amenity."""
        amenity_id = self._create_amenity("Gym Room")

        response = self.client.delete(
            f'/api/v1/amenities/{amenity_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_amenity_not_found(self):
        """Deleting a non-existent amenity must return 404."""
        response = self.client.delete(
            '/api/v1/amenities/00000000-0000-0000-0000-000000000000',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()