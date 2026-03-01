import unittest
import uuid
from app import create_app
from app.services import facade


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Reset storage
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

    # -------------------------
    # Helper
    # -------------------------
    def _create_amenity(self, name="wifi"):
        response = self.client.post('/api/v1/amenities/', json={"name": name})
        return response.get_json()["id"]

    # =========================================================
    # CREATE — Success
    # =========================================================

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi",
            "description": "High speed internet"
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "wifi")

    def test_create_amenity_without_description(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Parking"
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)

    def test_create_amenity_name_normalized(self):
        """Name must be stored in lowercase."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "POOL"
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "pool")

    # =========================================================
    # CREATE — Invalid
    # =========================================================

    def test_create_amenity_invalid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_name_spaces_only(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "   "
        })

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_name_too_long(self):
        """Name longer than 50 characters must be rejected."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "a" * 51
        })

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_description_too_long(self):
        """Description longer than 255 characters must be rejected."""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "pool",
            "description": "a" * 256
        })

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_duplicate(self):
        self.client.post('/api/v1/amenities/', json={"name": "wifi"})

        response = self.client.post('/api/v1/amenities/', json={"name": "wifi"})

        self.assertEqual(response.status_code, 400)

    # =========================================================
    # GET — Success
    # =========================================================

    def test_get_amenity_success(self):
        amenity_id = self._create_amenity("sauna")
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], amenity_id)
        self.assertEqual(data["name"], "sauna")

    def test_list_amenities_success(self):
        self._create_amenity("wifi")
        self._create_amenity("parking")

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertEqual(len(response.get_json()), 2)

    # =========================================================
    # GET — Not found
    # =========================================================

    def test_get_amenity_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/amenities/{fake_id}')

        self.assertEqual(response.status_code, 404)

    # =========================================================
    # UPDATE — Success
    # =========================================================

    def test_update_amenity_success(self):
        """PUT valid name returns 200 and normalizes to lowercase."""
        amenity_id = self._create_amenity("parking")
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Garden"
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "garden")

    # =========================================================
    # UPDATE — Invalid / forbidden
    # =========================================================

    def test_update_amenity_duplicate(self):
        """PUT with an already existing name must be rejected."""
        self._create_amenity("wifi")
        amenity_id = self._create_amenity("parking")

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "wifi"
        })

        self.assertEqual(response.status_code, 400)

    def test_update_amenity_empty_name(self):
        amenity_id = self._create_amenity()
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400)

    def test_update_amenity_name_too_long(self):
        amenity_id = self._create_amenity()
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "a" * 51
        })

        self.assertEqual(response.status_code, 400)

    def test_update_amenity_unknown_field(self):
        amenity_id = self._create_amenity()
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "color": "green"
        })

        self.assertEqual(response.status_code, 400)

    def test_update_amenity_modify_id_forbidden(self):
        amenity_id = self._create_amenity()
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "id": "123"
        })

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()