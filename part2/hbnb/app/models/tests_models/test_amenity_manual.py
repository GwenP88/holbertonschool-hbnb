import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from amenity import Amenity
from pprint import pprint

def main():
    # Ajout d'un amenity sans description
    a1 = Amenity.create_amenity({"name": "WiFi"})
    print("Amenity:")
    pprint(a1.get_details(), sort_dicts=False)
    print("\n")

    # Ajout d'un deuxième avec description
    a2 = Amenity.create_amenity({
        "name": "Machine à café",
        "description": "Nespresso"
    })
    print("Amenity:")
    pprint(a2.get_details(), sort_dicts=False)
    print("\n")

    # Ajout d'une description au premier amenity
    a1.update_amenity({"description": "Connexion fibre"})
    print("Amenity:")
    pprint(a1.get_details(), sort_dicts=False)
    print("\n")

    # Affichage de tous les amenities
    print("Amenities:")
    pprint(Amenity.get_all_amenities(), sort_dicts=False)
    print("\n")

    # Suppression du premier amenity
    a1.delete()

    # Affichage de tous les amenities après suppression
    print("Amenities:")
    pprint(Amenity.get_all_amenities(), sort_dicts=False)
    print("\n")

if __name__ == "__main__":
    main()