# tests/test_place_manual.py
import os
import sys
from pprint import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user import User
from place import Place
from amenity import Amenity
from review import Review


def reset_storages():
    """Reset in-memory storages to make manual tests reproducible."""
    if hasattr(User, "_storage"):
        User._storage.clear()
    if hasattr(Place, "_storage"):
        Place._storage.clear()
    if Amenity is not None and hasattr(Amenity, "_storage"):
        Amenity._storage.clear()
    if Review is not None and hasattr(Review, "_storage"):
        Review._storage.clear()


def main():
    reset_storages()

    print("==== 1) Create an owner user ====")
    owner = User.create_user({
        "first_name": "Gwenaelle",
        "last_name": "Pichot",
        "email": "GWENAELLE@MAIL.COM",
        "password": "Test1234"
    })
    print("Owner profile:")
    pprint(owner.get_profile(), sort_dicts=False)
    print("\n")

    print("==== 2) Create a second user (not owner) ====")
    u2 = User.create_user({
        "first_name": "Alex",
        "last_name": "Martin",
        "email": "alex.martin@mail.com",
        "password": "Hello1234"
    })
    print("User 2 profile:")
    pprint(u2.get_profile(), sort_dicts=False)
    print("\n")

    print("==== 3) Create first place (valid) ====")
    p1 = Place.create_place({
        "title": "Studio cosy centre-ville",
        "description": "Petit studio proche commerces",
        "price": 55.0,
        "latitude": 45.923,
        "longitude": 6.869
    }, owner=owner)
    print("Place 1 details:")
    pprint(p1.get_details(), sort_dicts=False)
    print("\n")

    print("==== 4) Create second place (valid, description None) ====")
    p2 = Place.create_place({
        "title": "Chalet vue montagne",
        "description": None,
        "price": 180,
        "latitude": 45.900,
        "longitude": 6.800
    }, owner=owner)
    print("Place 2 details:")
    pprint(p2.get_details(), sort_dicts=False)
    print("\n")

    print("==== 5) Get all places ====")
    pprint(Place.get_all_places(), sort_dicts=False)
    print("\n")

    print("==== 6) Update place details (valid) ====")
    p1.update_details({
        "title": "Studio cosy rénové",
        "price": 60,
        "latitude": 45.924,
        "longitude": 6.870,
        "description": "Refait à neuf, proche gare"
    })
    print("Place 1 after update:")
    pprint(p1.get_details(), sort_dicts=False)
    print("\n")

    print("==== 7) Expected error: try to update owner (should fail) ====")
    try:
        p1.update_details({"owner": u2})
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 8) Expected errors: create_place validations ====")

    print("-- 8.1) Empty title --")
    try:
        Place.create_place({
            "title": "   ",
            "description": "desc",
            "price": 10,
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.2) Title too long (>100) --")
    try:
        Place.create_place({
            "title": "A" * 101,
            "description": "desc",
            "price": 10,
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.3) Description wrong type --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": 123,
            "price": 10,
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.4) Description too long (>255) --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": "D" * 256,
            "price": 10,
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.5) Price None --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": "desc",
            "price": None,
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.6) Price wrong type (str) --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": "desc",
            "price": "100",
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except TypeError as e:
        print("Expected error:", e)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.7) Price <= 0 --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": "desc",
            "price": 0,
            "latitude": 0,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.8) Latitude out of range --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": "desc",
            "price": 10,
            "latitude": 100,
            "longitude": 0
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("-- 8.9) Longitude out of range --")
    try:
        Place.create_place({
            "title": "Valid title",
            "description": "desc",
            "price": 10,
            "latitude": 0,
            "longitude": 200
        }, owner=owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 9) Expected error: owner does not exist in User._storage ====")
    ghost_owner = User("Ghost", "Owner", "ghost.owner@mail.com")  # not created via create_user => not stored
    try:
        Place.create_place({
            "title": "Place with ghost owner",
            "description": "should fail",
            "price": 10,
            "latitude": 0,
            "longitude": 0
        }, owner=ghost_owner)
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 10) Delete a place ====")
    p2.delete()
    print("All places after deleting p2:")
    pprint(Place.get_all_places(), sort_dicts=False)
    print("\n")

    print("==== 11) Expected error: delete same place again ====")
    try:
        p2.delete()
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    print("==== 12) Amenities/Reviews (optional) ====")
    if Amenity is None:
        print("Amenity not available -> skipping amenity tests.")
    else:
        print("Amenity available, but create method may differ depending on your implementation.")
        print("If you have Amenity.create_amenity({...}), you can add tests here.")
    print("\n")

    if Review is None:
        print("Review not available -> skipping review tests.")
    else:
        print("Review available, but create method may differ depending on your implementation.")
        print("If you have Review.create_review(...), you can add tests here.")
    print("\n")


if __name__ == "__main__":
    main()