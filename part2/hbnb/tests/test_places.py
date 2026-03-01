import unittest
import uuid
from app import create_app
from app.services import facade


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

        # Create required user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "Password123"
        })
        self.user_id = user_response.get_json()["id"]

        # Create required amenity
        amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "wifi"
        })
        self.amenity_id = amenity_response.get_json()["id"]

    # -------------------------
    # Helper
    # -------------------------
    def _create_place(self, **overrides):
        payload = {
            "title": "Studio",
            "description": "Nice place",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": self.user_id,
            "amenities": []
        }
        payload.update(overrides)
        return self.client.post('/api/v1/places/', json=payload)

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_place_success(self):
        response = self._create_place()
        self.assertEqual(response.status_code, 201)

    def test_create_place_with_amenity(self):
        """Creating a place with a valid amenity_id must succeed."""
        response = self._create_place(amenities=[self.amenity_id])

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

    def test_create_place_empty_amenities(self):
        """Creating a place with an empty amenities list must succeed."""
        response = self._create_place(amenities=[])
        self.assertEqual(response.status_code, 201)

    # =========================================================
    # CREATE — Invalid
    # =========================================================

    def test_create_place_no_amenities_field(self):
        """Missing 'amenities' key: API accepts it and defaults to empty list."""
        payload = {
            "title": "Studio",
            "description": "Nice place",
            "price": 50,
            "latitude": 45,
            "longitude": 6,
            "owner_id": self.user_id
        }
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertIn(response.status_code, [200, 201])

    def test_create_place_invalid_price_negative(self):
        """Negative price must be rejected."""
        response = self._create_place(price=-10)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_price_zero(self):
        """Price of 0 must be rejected (must be > 0)."""
        response = self._create_place(price=0)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        response = self._create_place(latitude=200)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_negative(self):
        response = self._create_place(latitude=-91)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        response = self._create_place(longitude=181)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        response = self._create_place(owner_id=str(uuid.uuid4()))
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_amenity(self):
        response = self._create_place(amenities=[str(uuid.uuid4())])
        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success
    # =========================================================

    def test_get_place_success(self):
        place_id = self._create_place().get_json()["id"]
        response = self.client.get(f'/api/v1/places/{place_id}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], place_id)

    def test_list_places_success(self):
        self._create_place(title="Place 1")
        self._create_place(title="Place 2")

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertEqual(len(response.get_json()), 2)

    # =========================================================
    # GET — Not found
    # =========================================================

    def test_get_place_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/places/{fake_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()