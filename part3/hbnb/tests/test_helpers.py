"""
Shared test helpers for HBnB part 3 unit tests.

Usage in setUp:
    from tests.test_helpers import TestBase
    class MyTest(TestBase):
        def setUp(self):
            super().setUp()
            # your extra setup here
"""
import unittest
from app import create_app, db, bcrypt
from app.models.user import User


class TestBase(unittest.TestCase):
    """Base test class: spins up an in-memory DB and tears it down after each test."""

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self._seed_admin()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _seed_admin(self):
        """Insert the admin user directly in DB (bypass API which blocks is_admin)."""
        with self.app.app_context():
            admin = User(
                first_name="Admin",
                last_name="HBnB",
                email="admin@hbnb.io",
                is_admin=True
            )
            admin.set_password("admin1234")
            db.session.add(admin)
            db.session.commit()

    def _login(self, email, password):
        """POST /auth/login and return the access_token string."""
        response = self.client.post('/api/v1/auth/login', json={
            "email": email,
            "password": password
        })
        return response.get_json().get("access_token")

    def _auth(self, token):
        """Return an Authorization header dict for the given token."""
        return {"Authorization": f"Bearer {token}"}

    def _create_user(self, first_name, last_name, email, password="string123"):
        """Create a regular user via the API and return (user_id, token)."""
        r = self.client.post('/api/v1/users/', json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        })
        user_id = r.get_json()["id"]
        token = self._login(email, password)
        return user_id, token

    def _create_amenity(self, name, description=None, token=None):
        """Create an amenity as admin and return its id."""
        if token is None:
            token = self._login("admin@hbnb.io", "admin1234")
        payload = {"name": name}
        if description:
            payload["description"] = description
        r = self.client.post(
            '/api/v1/amenities/',
            json=payload,
            headers=self._auth(token)
        )
        return r.get_json()["id"]

    def _create_place(self, token, title="Studio", price=50,
                      latitude=45.0, longitude=6.0,
                      description="Nice place", amenities=None):
        """Create a place for the authenticated user and return its id."""
        payload = {
            "title": title,
            "description": description,
            "price": price,
            "latitude": latitude,
            "longitude": longitude,
            "amenities": amenities or []
        }
        r = self.client.post(
            '/api/v1/places/',
            json=payload,
            headers=self._auth(token)
        )
        return r.get_json()["id"]

    def _create_review(self, token, place_id, comment="Very nice", rating=5):
        """Create a review for the authenticated user and return the response."""
        return self.client.post(
            '/api/v1/reviews/',
            json={"comment": comment, "rating": rating, "place_id": place_id},
            headers=self._auth(token)
        )
