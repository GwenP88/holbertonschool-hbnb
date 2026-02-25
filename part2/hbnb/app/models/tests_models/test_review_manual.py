# tests/test_review_manual.py
import os
import sys
from pprint import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user import User
from place import Place
from review import Review


def reset_storages():
    """Reset in-memory storages to make manual tests reproducible."""
    if hasattr(User, "_storage"):
        User._storage.clear()
    if hasattr(Place, "_storage"):
        Place._storage.clear()
    if hasattr(Review, "_storage"):
        Review._storage.clear()


def main():
    reset_storages()

    print("==== 1) Create users ====")
    owner = User.create_user({
        "first_name": "Gwenaelle",
        "last_name": "Pichot",
        "email": "gwenaelle@mail.com",
        "password": "Test1234"
    })
    u2 = User.create_user({
        "first_name": "Alex",
        "last_name": "Martin",
        "email": "alex.martin@mail.com",
        "password": "Hello1234"
    })
    print("Owner:")
    pprint(owner.get_profile(), sort_dicts=False)
    print("User 2:")
    pprint(u2.get_profile(), sort_dicts=False)
    print("\n")

    print("==== 2) Create a place ====")
    p1 = Place.create_place({
        "title": "Studio cosy centre-ville",
        "description": "Petit studio proche commerces",
        "price": 55.0,
        "latitude": 45.923,
        "longitude": 6.869
    }, owner=owner)
    print("Place:")
    pprint(p1.get_details(), sort_dicts=False)
    print("\n")

    print("==== 3) Create a review (valid) ====")
    r1 = Review.create_review({
        "comment": "Super séjour !",
        "rating": 5
    }, author_id=u2.id, place_id=p1.id)
    print("Review 1 details:")
    pprint(r1.get_details(), sort_dicts=False)
    print("Place reviews (details) after adding r1:")
    pprint(p1.get_all_reviews(), sort_dicts=False)
    print("\n")

    print("==== 4) Update review (valid) ====")
    r1.update_review({"comment": "Super séjour, je recommande.", "rating": 4})
    print("Review 1 after update:")
    pprint(r1.get_details(), sort_dicts=False)
    print("\n")

    print("==== 5) Expected errors: create_review validations ====")

    print("-- 5.1) Missing comment (None) --")
    try:
        Review.create_review({"comment": None, "rating": 5}, author_id=u2.id, place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 5.2) Empty comment (spaces) --")
    try:
        Review.create_review({"comment": "   ", "rating": 5}, author_id=u2.id, place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 5.3) Comment wrong type (int) --")
    try:
        Review.create_review({"comment": 123, "rating": 5}, author_id=u2.id, place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 5.4) Rating None --")
    try:
        Review.create_review({"comment": "ok", "rating": None}, author_id=u2.id, place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 5.5) Rating wrong type (str) --")
    try:
        Review.create_review({"comment": "ok", "rating": "5"}, author_id=u2.id, place_id=p1.id)
    except TypeError as e:
        print("Expected error:", e)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 5.6) Rating out of range (0) --")
    try:
        Review.create_review({"comment": "ok", "rating": 0}, author_id=u2.id, place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 5.7) Rating out of range (6) --")
    try:
        Review.create_review({"comment": "ok", "rating": 6}, author_id=u2.id, place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 6) Expected errors: author/place must exist in storage ====")

    print("-- 6.1) Ghost author id --")
    try:
        Review.create_review({"comment": "ok", "rating": 5}, author_id="not-a-real-id", place_id=p1.id)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 6.2) Ghost place id --")
    try:
        Review.create_review({"comment": "ok", "rating": 5}, author_id=u2.id, place_id="not-a-real-id")
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 7) Delete review and ensure it is removed from Place._reviews ====")
    r1_id = r1.id
    r1.delete()
    print("Review deleted.")
    print("Review still in Review._storage ? ->", r1_id in Review._storage)
    print("Place reviews (details) after deleting r1:")
    pprint(p1.get_all_reviews(), sort_dicts=False)
    print("\n")

    print("==== 8) Expected error: delete same review again ====")
    try:
        r1.delete()
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 9) Cascade check (optional): delete place should delete its reviews ====")
    r2 = Review.create_review({"comment": "Bien", "rating": 4}, author_id=u2.id, place_id=p1.id)
    r3 = Review.create_review({"comment": "Moyen", "rating": 2}, author_id=owner.id, place_id=p1.id)
    print("Reviews in storage before deleting place:", len(Review._storage))
    p1.delete()
    print("Place deleted.")
    print("Reviews in storage after deleting place:", len(Review._storage))
    print("\n")


if __name__ == "__main__":
    main()
