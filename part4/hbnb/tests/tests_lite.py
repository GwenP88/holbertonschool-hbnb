"""
tests_lite.py — Version allégée des tests HBnB Part 3.
Couvre les cas essentiels : auth, users, amenities, places, reviews.
Lance avec : python3 -m unittest tests/tests_lite.py -v
"""
import unittest
import uuid
from app import create_app, db, bcrypt
from app.models.user import User


class TestBase(unittest.TestCase):
    """Base : in-memory DB + admin seedé + helpers communs."""

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            admin = User("Admin", "HBnB", "admin@hbnb.io", is_admin=True)
            admin.set_password("admin1234")
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _login(self, email, password):
        r = self.client.post('/api/v1/auth/login',
                             json={"email": email, "password": password})
        return r.get_json().get("access_token")

    def _auth(self, token):
        return {"Authorization": f"Bearer {token}"}

    def _make_user(self, email, password="string123"):
        r = self.client.post('/api/v1/users/', json={
            "first_name": "Test", "last_name": "User",
            "email": email, "password": password
        })
        return r.get_json()["id"], self._login(email, password)

    def _make_amenity(self, name="wifi"):
        token = self._login("admin@hbnb.io", "admin1234")
        r = self.client.post('/api/v1/amenities/', json={"name": name},
                             headers=self._auth(token))
        return r.get_json()["id"]

    def _make_place(self, token, title="Studio"):
        r = self.client.post('/api/v1/places/', json={
            "title": title, "description": "Nice place",
            "price": 50, "latitude": 45.0, "longitude": 6.0, "amenities": []
        }, headers=self._auth(token))
        return r.get_json()["id"]

    def _make_review(self, token, place_id, rating=5):
        return self.client.post('/api/v1/reviews/', json={
            "comment": "Great place!", "rating": rating, "place_id": place_id
        }, headers=self._auth(token))


# =============================================================================
# AUTH
# =============================================================================
class TestAuth(TestBase):

    def setUp(self):
        super().setUp()
        self._make_user("john@test.com")

    def test_login_valid(self):
        r = self.client.post('/api/v1/auth/login',
                             json={"email": "john@test.com", "password": "string123"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("access_token", r.get_json())

    def test_login_wrong_password(self):
        r = self.client.post('/api/v1/auth/login',
                             json={"email": "john@test.com", "password": "wrong"})
        self.assertEqual(r.status_code, 401)

    def test_login_unknown_email(self):
        r = self.client.post('/api/v1/auth/login',
                             json={"email": "ghost@test.com", "password": "string123"})
        self.assertEqual(r.status_code, 401)

    def test_protected_with_token(self):
        token = self._login("john@test.com", "string123")
        r = self.client.get('/api/v1/auth/protected', headers=self._auth(token))
        self.assertEqual(r.status_code, 200)

    def test_protected_without_token(self):
        r = self.client.get('/api/v1/auth/protected')
        self.assertEqual(r.status_code, 401)


# =============================================================================
# USERS
# =============================================================================
class TestUsers(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.john_id, self.john_token = self._make_user("john@test.com")
        self.jane_id, self.jane_token = self._make_user("jane@test.com")

    def test_create_user_ok(self):
        r = self.client.post('/api/v1/users/', json={
            "first_name": "Gwen", "last_name": "A",
            "email": "gwen@test.com", "password": "string123"
        })
        self.assertEqual(r.status_code, 201)
        self.assertNotIn("password", r.get_json())

    def test_create_user_duplicate_email(self):
        r = self.client.post('/api/v1/users/', json={
            "first_name": "X", "last_name": "Y",
            "email": "john@test.com", "password": "string123"
        })
        self.assertEqual(r.status_code, 400)

    def test_create_user_invalid_email(self):
        r = self.client.post('/api/v1/users/', json={
            "first_name": "X", "last_name": "Y",
            "email": "not-an-email", "password": "string123"
        })
        self.assertEqual(r.status_code, 400)

    def test_get_user_by_id(self):
        r = self.client.get(f'/api/v1/users/{self.john_id}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["id"], self.john_id)

    def test_get_user_not_found(self):
        r = self.client.get('/api/v1/users/00000000-0000-0000-0000-000000000000')
        self.assertEqual(r.status_code, 404)

    def test_update_own_profile(self):
        r = self.client.put(f'/api/v1/users/{self.john_id}',
                            json={"first_name": "Johnny"},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 200)

    def test_update_other_user_forbidden(self):
        r = self.client.put(f'/api/v1/users/{self.jane_id}',
                            json={"first_name": "Hacked"},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 403)

    def test_update_email_via_put_forbidden(self):
        r = self.client.put(f'/api/v1/users/{self.john_id}',
                            json={"email": "new@test.com"},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 400)

    def test_update_email_dedicated_endpoint(self):
        r = self.client.put(f'/api/v1/users/{self.john_id}/email',
                            json={"email": "john_new@test.com"},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 200)

    def test_update_password_dedicated_endpoint(self):
        r = self.client.put(f'/api/v1/users/{self.john_id}/password',
                            json={"password": "newpass123"},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 200)

    def test_admin_can_update_any_user(self):
        r = self.client.put(f'/api/v1/users/{self.john_id}',
                            json={"first_name": "AdminEdit"},
                            headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 200)

    def test_delete_own_account(self):
        gwen_id, gwen_token = self._make_user("gwen@test.com")
        r = self.client.delete(f'/api/v1/users/{gwen_id}',
                               headers=self._auth(gwen_token))
        self.assertEqual(r.status_code, 200)

    def test_delete_other_user_forbidden(self):
        r = self.client.delete(f'/api/v1/users/{self.jane_id}',
                               headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 403)


# =============================================================================
# AMENITIES
# =============================================================================
class TestAmenities(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.user_id, self.user_token = self._make_user("user@test.com")

    def test_create_amenity_admin(self):
        r = self.client.post('/api/v1/amenities/',
                             json={"name": "Sauna", "description": "Private sauna"},
                             headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["name"], "sauna")

    def test_create_amenity_no_token(self):
        r = self.client.post('/api/v1/amenities/', json={"name": "Jacuzzi"})
        self.assertEqual(r.status_code, 401)

    def test_create_amenity_non_admin_forbidden(self):
        r = self.client.post('/api/v1/amenities/', json={"name": "Jacuzzi"},
                             headers=self._auth(self.user_token))
        self.assertEqual(r.status_code, 403)

    def test_create_amenity_duplicate(self):
        self._make_amenity("wifi")
        r = self.client.post('/api/v1/amenities/', json={"name": "wifi"},
                             headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 400)

    def test_get_amenity_by_id(self):
        amenity_id = self._make_amenity("fireplace")
        r = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(r.status_code, 200)

    def test_get_amenity_not_found(self):
        r = self.client.get('/api/v1/amenities/00000000-0000-0000-0000-000000000000')
        self.assertEqual(r.status_code, 404)

    def test_update_amenity_admin(self):
        amenity_id = self._make_amenity("sauna")
        r = self.client.put(f'/api/v1/amenities/{amenity_id}',
                            json={"name": "Sauna VIP"},
                            headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 200)

    def test_update_amenity_non_admin_forbidden(self):
        amenity_id = self._make_amenity("sauna")
        r = self.client.put(f'/api/v1/amenities/{amenity_id}',
                            json={"name": "Hacked"},
                            headers=self._auth(self.user_token))
        self.assertEqual(r.status_code, 403)

    def test_delete_amenity_admin(self):
        amenity_id = self._make_amenity("gym")
        r = self.client.delete(f'/api/v1/amenities/{amenity_id}',
                               headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 200)

    def test_delete_amenity_non_admin_forbidden(self):
        amenity_id = self._make_amenity("gym")
        r = self.client.delete(f'/api/v1/amenities/{amenity_id}',
                               headers=self._auth(self.user_token))
        self.assertEqual(r.status_code, 403)


# =============================================================================
# PLACES
# =============================================================================
class TestPlaces(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.john_id, self.john_token = self._make_user("john@test.com")
        self.jane_id, self.jane_token = self._make_user("jane@test.com")
        self.wifi_id = self._make_amenity("wifi")
        self.place_id = self._make_place(self.john_token, "John's Loft")

    def test_create_place_ok(self):
        r = self.client.post('/api/v1/places/', json={
            "title": "Cottage", "description": "Cozy",
            "price": 75, "latitude": 45.0, "longitude": 6.0, "amenities": []
        }, headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 201)

    def test_create_place_no_token(self):
        r = self.client.post('/api/v1/places/', json={
            "title": "X", "description": "Y",
            "price": 50, "latitude": 45.0, "longitude": 6.0, "amenities": []
        })
        self.assertEqual(r.status_code, 401)

    def test_create_place_invalid_price(self):
        r = self.client.post('/api/v1/places/', json={
            "title": "X", "description": "Y",
            "price": -10, "latitude": 45.0, "longitude": 6.0, "amenities": []
        }, headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 400)

    def test_create_place_invalid_latitude(self):
        r = self.client.post('/api/v1/places/', json={
            "title": "X", "description": "Y",
            "price": 50, "latitude": 999.0, "longitude": 6.0, "amenities": []
        }, headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 400)

    def test_get_place_by_id(self):
        r = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(r.status_code, 200)

    def test_get_place_not_found(self):
        r = self.client.get('/api/v1/places/00000000-0000-0000-0000-000000000000')
        self.assertEqual(r.status_code, 404)

    def test_owner_update_own_place(self):
        r = self.client.put(f'/api/v1/places/{self.place_id}',
                            json={"title": "Updated", "price": 120},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 200)

    def test_non_owner_update_forbidden(self):
        r = self.client.put(f'/api/v1/places/{self.place_id}',
                            json={"title": "Hacked"},
                            headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 403)

    def test_add_amenity_owner(self):
        r = self.client.post(
            f'/api/v1/places/{self.place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 200)

    def test_add_amenity_non_owner_forbidden(self):
        r = self.client.post(
            f'/api/v1/places/{self.place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 403)

    def test_add_amenity_already_linked(self):
        self.client.post(f'/api/v1/places/{self.place_id}/amenities/{self.wifi_id}',
                         headers=self._auth(self.john_token))
        r = self.client.post(
            f'/api/v1/places/{self.place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 400)

    def test_remove_amenity_owner(self):
        self.client.post(f'/api/v1/places/{self.place_id}/amenities/{self.wifi_id}',
                         headers=self._auth(self.john_token))
        r = self.client.delete(
            f'/api/v1/places/{self.place_id}/amenities/{self.wifi_id}',
            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 200)

    def test_delete_place_owner(self):
        jane_place = self._make_place(self.jane_token, "Jane's place")
        r = self.client.delete(f'/api/v1/places/{jane_place}',
                               headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 200)

    def test_delete_place_non_owner_forbidden(self):
        r = self.client.delete(f'/api/v1/places/{self.place_id}',
                               headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 403)


# =============================================================================
# REVIEWS
# =============================================================================
class TestReviews(TestBase):

    def setUp(self):
        super().setUp()
        self.admin_token = self._login("admin@hbnb.io", "admin1234")
        self.john_id, self.john_token = self._make_user("john@test.com")
        self.jane_id, self.jane_token = self._make_user("jane@test.com")
        self.gwen_id, self.gwen_token = self._make_user("gwen@test.com")
        self.place_id = self._make_place(self.john_token, "John's Loft")

    def test_create_review_ok(self):
        r = self._make_review(self.jane_token, self.place_id)
        self.assertEqual(r.status_code, 201)
        self.assertIn("id", r.get_json())

    def test_create_review_no_token(self):
        r = self.client.post('/api/v1/reviews/', json={
            "comment": "Nice", "rating": 4, "place_id": self.place_id
        })
        self.assertEqual(r.status_code, 401)

    def test_create_review_own_place_forbidden(self):
        r = self._make_review(self.john_token, self.place_id)
        self.assertEqual(r.status_code, 400)

    def test_create_review_duplicate_forbidden(self):
        self._make_review(self.jane_token, self.place_id)
        r = self._make_review(self.jane_token, self.place_id, rating=3)
        self.assertEqual(r.status_code, 400)

    def test_create_review_rating_too_high(self):
        r = self._make_review(self.jane_token, self.place_id, rating=10)
        self.assertEqual(r.status_code, 400)

    def test_create_review_rating_too_low(self):
        r = self._make_review(self.jane_token, self.place_id, rating=0)
        self.assertEqual(r.status_code, 400)

    def test_get_review_by_id(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(r.status_code, 200)

    def test_get_reviews_by_place(self):
        self._make_review(self.jane_token, self.place_id)
        self._make_review(self.gwen_token, self.place_id)
        r = self.client.get(f'/api/v1/places/{self.place_id}/reviews')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 2)

    def test_get_reviews_nonexistent_place(self):
        r = self.client.get('/api/v1/places/00000000-0000-0000-0000-000000000000/reviews')
        self.assertEqual(r.status_code, 404)

    def test_author_update_own_review(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.put(f'/api/v1/reviews/{review_id}',
                            json={"comment": "Updated!", "rating": 4},
                            headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 200)

    def test_non_author_update_forbidden(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.put(f'/api/v1/reviews/{review_id}',
                            json={"comment": "Hacked"},
                            headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 403)

    def test_admin_update_any_review(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.put(f'/api/v1/reviews/{review_id}',
                            json={"comment": "Admin edit", "rating": 3},
                            headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 200)

    def test_author_delete_own_review(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.delete(f'/api/v1/reviews/{review_id}',
                               headers=self._auth(self.jane_token))
        self.assertEqual(r.status_code, 200)

    def test_non_author_delete_forbidden(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.delete(f'/api/v1/reviews/{review_id}',
                               headers=self._auth(self.john_token))
        self.assertEqual(r.status_code, 403)

    def test_admin_delete_any_review(self):
        review_id = self._make_review(self.jane_token, self.place_id).get_json()["id"]
        r = self.client.delete(f'/api/v1/reviews/{review_id}',
                               headers=self._auth(self.admin_token))
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()