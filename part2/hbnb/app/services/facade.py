from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

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
            raise ValueError("Owner not found.")

        if "amenities" not in place_data:
            raise ValueError("Amenities field is required (can be an empty list).")

        amenities_ids = place_data.get("amenities")
        if not isinstance(amenities_ids, list):
            raise ValueError("Amenities must be a list.")

        for amenity_id in amenities_ids:
            if not self.amenity_repo.get(amenity_id):
                raise ValueError("Invalid amenity ID.")

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
        if not owner:
            raise ValueError("Owner not found.")
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
                raise ValueError("Invalid amenity ID.")
            amenities_list.append({"id": a.id, "name": a.name, "description": a.description})
        data["amenities"] = amenities_list
        data["reviews"] = self.get_reviews_by_place(place_id)
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
    
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        if place is None:
            return None
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        place.add_amenity(amenity_id)
        return place

    def remove_amenity_from_place(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        if place is None:
            return None
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        place.remove_amenity(amenity_id)
        return place

    # =============================
    # ------ REVIEWS METHODS ------
    # =============================

    def create_review(self, review_data):
        if not review_data or not isinstance(review_data, dict):
            raise ValueError("Review data must be a non-empty dictionary.")

        place_id = review_data.get("place_id")
        author_id = review_data.get("author_id")

        if place_id is None or author_id is None:
            raise ValueError("author_id and place_id are required.")

        if self.place_repo.get(place_id) is None:
            return None

        if self.user_repo.get(author_id) is None:
            raise ValueError("User not found.")

        for review in self.review_repo.get_all():
            if review.place_id == place_id and review.author_id == author_id:
                raise ValueError("Review already exists for this user and place.")

        comment = review_data.get("comment")
        rating = review_data.get("rating")

        if comment is None or rating is None:
            raise ValueError("comment and rating are required.")

        review = Review.create_review(review_data, author_id, place_id)
        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review is None:
            return None
        return review.get_details()

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        list_review = []
        for review in reviews:
            details = review.get_details()
            list_review.append(details)
        return list_review

    def get_reviews_by_place(self, place_id):
        if self.place_repo.get(place_id) is None:
            return None
        reviews = self.review_repo.get_all()
        list_review_by_place = []
        for review in reviews:
            if review.place_id == place_id:
                list_review_by_place.append(review.get_details())
        return list_review_by_place


    def update_review(self, review_id, review_data):
        if not review_data or not isinstance(review_data, dict):
            raise ValueError("Review data must be a non-empty dictionary.")

        review = self.review_repo.get(review_id)
        if review is None:
            return None
        if "author_id" in review_data or "place_id" in review_data:
            raise ValueError("author_id and place_id cannot be modified.")
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review is None:
            return None
        self.review_repo.delete(review_id)
        return True