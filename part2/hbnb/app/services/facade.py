from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ==========================
    # ------ USER METHODS ------
    # ==========================

    def create_user(self, user_data):
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("User data must be a non-empty dictionary.")
        if "is_admin" in user_data:
            raise ValueError("Only an administrator can set is_admin.")

        email = user_data.get("email")
        if not email:
            raise ValueError("Email is required.")

        email = email.strip().lower()
        existing_user = self.user_repo.get_by_attribute("_email", email)
        if existing_user:
            raise ValueError("Email already exists.")

        user = User.create_user(user_data)
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        if not email:
            raise ValueError("Email is required.")
        email = email.strip().lower()
        return self.user_repo.get_by_attribute("_email", email)

    def update_user(self, user_id, user_data):
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("Update data must be a non-empty dictionary.")

        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "is_admin" in user_data:
            raise ValueError("Only an administrator can modify is_admin.")
        if "email" in user_data:
            new_email = user_data["email"].strip().lower()
            existing_user = self.user_repo.get_by_attribute("_email", new_email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("Email already exists.")
        if "password" in user_data:
            user.set_password(user_data["password"])
            del user_data["password"]
        if user_data:
            self.user_repo.update(user_id, user_data)
        return user

    # =============================
    # ------ AMENITY METHODS ------
    # =============================

    def create_amenity(self, amenity_data):
        if not amenity_data or not isinstance(amenity_data, dict):
            raise ValueError("Amenity data must be a non-empty dictionary.")
        
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Name is required.")

        name = name.strip().lower()
        amenity_data["name"] = name
        existing_amenity = self.amenity_repo.get_by_attribute("_name", name)
        if existing_amenity:
            raise ValueError("Name already exists.")
        
        amenity = Amenity.create_amenity(amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        if not amenity_data or not isinstance(amenity_data, dict):
            raise ValueError("Amenity data must be a non-empty dictionary.")
        
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if "name" in amenity_data:
            new_name = amenity_data["name"].strip().lower()
            existing_amenity = self.amenity_repo.get_by_attribute("_name", new_name)
            if existing_amenity and existing_amenity.id != amenity.id:
                raise ValueError("Name already exists.")
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
    
    # =============================
    # ------ PLACES METHODS ------
    # =============================

    def create_place(self, place_data):
        if not place_data or not isinstance(place_data, dict):
            raise ValueError("Place data must be a non-empty dictionary.")

        owner_id = place_data.get("owner_id")
        if not owner_id:
            raise ValueError("Owner is required.")
        existing_owner = self.user_repo.get(owner_id)
        if not existing_owner:
            raise ValueError("Owner not found")
        
        amenities_ids = place_data.get("amenities")
        if amenities_ids is None:
            amenities_ids = []
        else:
            if not isinstance(amenities_ids, list):
                raise ValueError("Amenities must be a list")
            for amenity_id in amenities_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity ID")

        place = Place.create_place(place_data, owner_id)
        for amenity_id in amenities_ids:
            place.add_amenity(amenity_id)
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place is None:
            return None
        data = place.get_details()
        owner = self.user_repo.get(data["owner_id"])
        data["owner"] = {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
            }
        amenities_list = []
        for amenity_id in data["amenities"]:
            a = self.amenity_repo.get(amenity_id)
            if a is None:
                raise ValueError("Invalid amenity ID")
            amenities_list.append({"id": a.id, "name": a.name})
        data["amenities"] = amenities_list
        return data

    def get_all_places(self):
        list_place = []
        places = self.place_repo.get_all()
        for p in places:
            list_place.append(p.to_list_item())
        return list_place

    def update_place(self, place_id, place_data):
        if not place_data or not isinstance(place_data, dict):
            raise ValueError("Place data must be a non-empty dictionary.")
        place = self.place_repo.get(place_id)
        if place is None:
            return None
        if "owner_id" in place_data:
            raise ValueError("Only an administrator can modify the owner.")
        if "amenities" in place_data:
            raise ValueError("Amenities must be modified using add_amenity or remove_amenity.")
        self.place_repo.update(place_id, place_data)
        return place

    # =============================
    # ------ REVIEWS METHODS ------
    # =============================