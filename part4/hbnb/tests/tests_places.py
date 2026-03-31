import unittest
import uuid
from tests.test_helpers import TestBase


class TestPlaceEndpoints(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.john_id, self.john_token = self._create_user(
            "John", "Doe", "johndoe@email.com"
        )
        self.jane_id, self.jane_token = self._create_user(
            "Jane", "Doe", "janedoe@email.com"
        )
        self.wifi_id = self._create_amenity("wifi", "High-speed wireless internet.")
        self.john_place_id = self._create_place(
            self.john_token,
            title="Sunny Loft in the City Center",
            price=95,
            latitude=48.8566,
            longitude=2.3522,
            description="A bright and modern loft."
        )

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_place_success(self):
        """Authenticated user can create a place."""
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Cozy Countryside Cottage",
                "description": "A charming stone cottage surrounded by nature.",
                "price": 75,
                "latitude": 45.7640,
                "longitude": 4.8357,
                "amenities": []
            },
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_place_with_amenities(self):
        """Creating a place with an existing amenity ID must succeed."""
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Studio with WiFi",
                "description": "A modern studio with high-speed internet.",
                "price": 80,
                "latitude": 43.2965,
                "longitude": 5.3698,
                "amenities": [self.wifi_id]
            },
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 201)

    def test_create_place_empty_amenities(self):
        """Creating a place with an empty amenities list must succeed."""
        place_id = self._create_place(self.jane_token)
        self.assertIsNotNone(place_id)

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
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Bad Place",
                "description": "Prix invalide",
                "price": -50,
                "latitude": 45.0,
                "longitude": 6.0,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_zero_price(self):
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Bad Place",
                "description": "Prix nul",
                "price": 0,
                "latitude": 45.0,
                "longitude": 6.0,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_too_high(self):
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Bad Lat",
                "description": "Latitude invalide",
                "price": 50,
                "latitude": 999.0,
                "longitude": 6.0,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_too_low(self):
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Bad Lat",
                "description": "Latitude invalide",
                "price": 50,
                "latitude": -91.0,
                "longitude": 6.0,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Bad Lon",
                "description": "Longitude invalide",
                "price": 50,
                "latitude": 45.0,
                "longitude": 181.0,
                "amenities": []
            },
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_amenity_id(self):
        """Unknown amenity ID must be rejected."""
        response = self.client.post(
            '/api/v1/places/',
            json={
                "title": "Bad Amenity",
                "description": "Amenity invalide",
                "price": 50,
                "latitude": 45.0,
                "longitude": 6.0,
                "amenities": [str(uuid.uuid4())]
            },
            headers=self._auth(self.john_token)
        )

        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success (public)
    # =========================================================

    def test_list_places(self):
        """GET /places/ returns a list with at least John's place."""
        response = self.client.get('/api/v1/places/')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_place_by_id(self):
        """GET /places/<id> returns the correct place."""
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
        self.assertEqual(response.get_json()["title"], "Sunny Loft - Rénové")

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

        self.assertIn(response.status_code, [400, 404])

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
        jane_place_id = self._create_place(self.jane_token, title="Jane's place")
        response = self.client.delete(
            f'/api/v1/places/{jane_place_id}',
            headers=self._auth(self.jane_token)
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_place_then_404(self):
        """After deletion, GET on the deleted place must return 404."""
        jane_place_id = self._create_place(self.jane_token, title="Jane's place")
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
        jane_place_id = self._create_place(self.jane_token, title="Jane's place")
        response = self.client.delete(
            f'/api/v1/places/{jane_place_id}',
            headers=self._auth(self.admin_token)
        )

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()