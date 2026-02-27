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

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi",
            "description": "High speed internet"
        })

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "wifi")

    def test_create_amenity_duplicate(self):
        self.client.post('/api/v1/amenities/', json={
            "name": "wifi"
        })

        response = self.client.post('/api/v1/amenities/', json={
            "name": "wifi"
        })

        self.assertEqual(response.status_code, 400)

    def test_create_amenity_invalid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400)

    def test_get_amenity_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/amenities/{fake_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()