import unittest
import uuid
from app import create_app, db


class TestPlaceEndpointsPart3(unittest.TestCase):

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

        # Create John
        r_john = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@email.com",
            "password": "string123"
        })
        self.john_id = r_john.get_json()["id"]
        self.john_token = self._login("johndoe@email.com", "string123")

        # Create Jane
        r_jane = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@email.com",
            "password": "string123"
        })
        self.jane_id = r_jane.get_json()["id"]
        self.jane_token = self._login("janedoe@email.com", "string123")

        # Create WiFi amenity (admin only)
        r_wifi = self.client.post(
            '/api/v1/amenities/',
            json={"name": "wifi", "description": "High-speed wireless internet."},
            headers=self._auth(self.admin_token)
        )
        self.wifi_id = r_wifi.get_json()["id"]

        # Create John's place
        r_place = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Sunny Loft in the City Center",
                "description": "A bright and modern loft.",
                "price": 95,
                "latitude": 48.8566,
                "longitude": 2.3522,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )
        self.john_place_id = r_place.get_json()["id"]

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

    def _create_place(self, token, **overrides):
        payload = {
            "title": "Studio",
            "description": "Nice place",
            "price": 50,
            "latitude": 45.0,
            "longitude": 6.0,
            "amenities": []
        }
        payload.update(overrides)
        return self.client.post(
            '/api/v1/places/',
            json=payload,
            headers=self._auth(token)
        )

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_place_success(self):
        """Authenticated user can create a place."""
        response = self._create_place(
            self.jane_token,
            title="Cozy Countryside Cottage",
            description="A charming stone cottage surrounded by nature.",
            price=75,
            latitude=45.7640,
            longitude=4.8357
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_place_with_amenities(self):
        """Creating a place with existing amenity IDs must succeed."""
        response = self._create_place(
            self.jane_token,
            amenities=[self.wifi_id]
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_empty_amenities(self):
        """Creating a place with an empty amenities list must succeed."""
        response = self._create_place(self.jane_token, amenities=[])

        self.assertEqual(response.status_code, 201)

    # =========================================================
    # CREATE — Forbidden / Invalid
    # =========================================================

    def test_create_place_without_token_forbidden(self):
        """Creating a place without a token must return 401."""
        response = self.client.post('/api/v1/places/', json={
            "title": "No token",
            "description": "Test",
            "price": 50,
            "latitude": 45.0,
            "longitude": 6.0,
            "amenities": []
        })

        self.assertEqual(response.status_code, 401)

    def test_create_place_negative_price(self):
        response = self._create_place(self.john_token, price=-50)

        self.assertEqual(response.status_code, 400)

    def test_create_place_zero_price(self):
        response = self._create_place(self.john_token, price=0)

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_too_high(self):
        response = self._create_place(self.john_token, latitude=999.0)

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_too_low(self):
        response = self._create_place(self.john_token, latitude=-91.0)

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        response = self._create_place(self.john_token, longitude=181.0)

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_amenity_id(self):
        """Unknown amenity ID must be rejected."""
        response = self._create_place(
            self.john_token,
            amenities=[str(uuid.uuid4())]
        )

        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success (public)
    # =========================================================

    def test_list_places(self):
        """GET /places/ returns a list of all places."""
        response = self.client.get('/api/v1/places/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_place_by_id(self):
        """GET /places/<id> returns the correct place with nested data."""
        response = self.client.get(f'/api/v1/places/{self.john_place_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], self.john_place_id)

    def test_get_place_not_found(self):
        response = self.client.get(
            '/api/v1/places/00000000-0000-0000-0000-000000000000'
        )

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Owner
    # =========================================================

    def test_owner_can_update_own_place(self):
        """Place owner can update title and price."""
        response = self.client.put(
            f'/api/v1/places/{self.john_place_id}',
            json={"title": "Sunny Loft - Rénové", "price": 150.0},
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["title"], "Sunny Loft - Rénové")

    def test_non_owner_cannot_update_place(self):
        """A user who is not the owner cannot update the place."""
        response = self.client.put(
            f'/api/v1/places/{self.john_place_id}',
            json={"title": "Hacked place"},
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_update_place_without_token_forbidden(self):
        response = self.client.put(
            f'/api/v1/places/{self.john_place_id}',
            json={"title": "No token"}
        )

        self.assertEqual(response.status_code, 401)

    # =========================================================
    # UPDATE — Admin override
    # =========================================================

    def test_admin_can_update_any_place(self):
        """Admin can update a place they don't own."""
        response = self.client.put(
            f'/api/v1/places/{self.john_place_id}',
            json={"title": "Sunny Loft - Modified by admin", "price": 180.0},
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    # =========================================================
    # AMENITY LINK — Add
    # =========================================================

    def test_owner_can_add_amenity_to_place(self):
        """Owner can link an amenity to their place."""
        response = self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_add_amenity(self):
        """Non-owner cannot link an amenity to someone else's place."""
        response = self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_add_amenity_already_linked(self):
        """Adding an already-linked amenity must return 400."""
        self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )
        response = self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_add_nonexistent_amenity(self):
        """Adding a non-existent amenity must return 404."""
        response = self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/00000000-0000-0000-0000-000000000000',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_can_add_amenity_to_any_place(self):
        """Admin can link an amenity to a place they don't own."""
        response = self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    # =========================================================
    # AMENITY LINK — Remove
    # =========================================================

    def test_owner_can_remove_amenity_from_place(self):
        """Owner can remove a linked amenity."""
        self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )
        response = self.client.delete(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_remove_amenity_not_linked(self):
        """Removing an amenity that is not linked must return 400."""
        response = self.client.delete(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_non_owner_cannot_remove_amenity(self):
        """Non-owner cannot remove an amenity from someone else's place."""
        self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token)
        )
        response = self.client.delete(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_remove_amenity_from_any_place(self):
        """Admin can remove a linked amenity from a place they don't own."""
        self.client.post(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.admin_token)
        )
        response = self.client.delete(
            f'/api/v1/places/{self.john_place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)

    # =========================================================
    # DELETE — Place
    # =========================================================

    def test_owner_can_delete_own_place(self):
        """Place owner can delete their place."""
        r = self._create_place(self.jane_token, title="Jane's place")
        jane_place_id = r.get_json()["id"]

        response = self.client.delete(
            f'/api/v1/places/{jane_place_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_place_then_404(self):
        """After deletion, GET on the deleted place must return 404."""
        r = self._create_place(self.jane_token, title="Jane's place")
        jane_place_id = r.get_json()["id"]

        self.client.delete(
            f'/api/v1/places/{jane_place_id}',
            headers=self._auth(self.jane_token)
        )

        response = self.client.get(f'/api/v1/places/{jane_place_id}')
        self.assertEqual(response.status_code, 404)

    def test_non_owner_cannot_delete_place(self):
        """Non-owner cannot delete someone else's place."""
        response = self.client.delete(
            f'/api/v1/places/{self.john_place_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_nonexistent_place(self):
        """Deleting a non-existent place must return 404."""
        response = self.client.delete(
            '/api/v1/places/00000000-0000-0000-0000-000000000000',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_can_delete_any_place(self):
        """Admin can delete a place they don't own."""
        r = self._create_place(self.jane_token, title="Jane's place")
        jane_place_id = r.get_json()["id"]

        response = self.client.delete(
            f'/api/v1/places/{jane_place_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()