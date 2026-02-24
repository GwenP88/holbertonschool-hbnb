from amenity import Amenity

def main():
    # CREATE
    a = Amenity.create_amenity({"name": "WiFi"})
    print("Created:", a.get_details())
    print("In storage:", a.id in Amenity._storage)

    # READ
    same = Amenity._storage.get(a.id)
    print("Read by id works:", same is a)
    print("Read details:", same.get_details() if same else None)

    # UPDATE
    old = a.updated_at
    a.update_amenity({"description": "Fast internet"})
    print("Updated description:", a.description)
    print("updated_at changed:", a.updated_at != old)

    # DELETE
    a.delete()
    print("Deleted, still in storage:", a.id in Amenity._storage)

    # READ after delete
    print("Read after delete:", Amenity._storage.get(a.id))

if __name__ == "__main__":
    main()