import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from user import User
from pprint import pprint

def main():
    # 1) Création d'un premier user
    u1 = User.create_user({
        "first_name": "Gwenaelle",
        "last_name": "Pichot",
        "email": "GWENAELLE@MAIL.COM",
        "password": "Test1234"
    })
    print("User 1 profile:")
    pprint(u1.get_profile(), sort_dicts=False)
    print("\n")

    # 2) Création d'un second user (email différent)
    u2 = User.create_user({
        "first_name": "Alex",
        "last_name": "Martin",
        "email": "alex.martin@mail.com",
        "password": "Hello1234"
    })
    print("User 2 profile:")
    pprint(u2.get_profile(), sort_dicts=False)
    print("\n")

    # 3) Affichage de tous les users
    print("All users:")
    pprint(User.get_all_users(), sort_dicts=False)
    print("\n")

    # 4) Update du prénom/nom du premier user
    u1.update_user({
        "first_name": "Gwen",
        "last_name": "Pichot-Dev"
    })
    print("User 1 after name update:")
    pprint(u1.get_profile(), sort_dicts=False)
    print("\n")

    # 5) Update de l'email du second user (avec normalisation)
    u2.update_user({
        "email": "  ALEX.MARTIN@MAIL.COM "
    })
    print("User 2 after email update (normalized):")
    pprint(u2.get_profile(), sort_dicts=False)
    print("\n")

    # 6) Update du password du premier user
    u1.update_user({
        "password": "Newpass123"
    })
    print("User 1 after password update (profile should NOT show password):")
    pprint(u1.get_profile(), sort_dicts=False)
    print("\n")

    # 7) Test erreur: création avec email déjà existant
    print("Try to create user with existing email:")
    try:
        User.create_user({
            "first_name": "Dup",
            "last_name": "Email",
            "email": "alex.martin@mail.com",
            "password": "Test1234"
        })
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    # 8) Test erreur: update email vers un email déjà utilisé
    print("Try to update u1 email to an existing email:")
    try:
        u1.update_user({
            "email": "alex.martin@mail.com"
        })
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    # 9) Test erreur: tentative de set is_admin via create_user
    print("Try to create user with is_admin (should fail):")
    try:
        User.create_user({
            "first_name": "Admin",
            "last_name": "Hack",
            "email": "admin.hack@mail.com",
            "password": "Admin1234",
            "is_admin": True
        })
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    # 10) Test erreur: tentative de set is_admin via update_user
    print("Try to update u1 with is_admin (should fail):")
    try:
        u1.update_user({
            "is_admin": True
        })
    except ValueError as e:
        print("Expected error:", e)
    print("\n")

    # 11) Suppression d'un user
    u2.delete()
    print("All users after deleting u2:")
    pprint(User.get_all_users(), sort_dicts=False)
    print("\n")

if __name__ == "__main__":
    main()