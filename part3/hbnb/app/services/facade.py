"""HBnB facade providing high-level services over in-memory repositories."""
from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Coordinate user, amenity, place, and review operations through repositories."""
    def __init__(self):
        """Initialize repositories used by the facade."""
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ==========================
    # ------ USER METHODS ------
    # ==========================

    def create_user(self, user_data):
        """Create and store a new user with unique email validation."""
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
        """Return all stored users."""
        return self.user_repo.get_all()

    def get_user(self, user_id):
        """Return a user by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Return a user by normalized email."""
        if not email:
            raise ValueError("Email is required.")
        email = email.strip().lower()
        return self.user_repo.get_by_attribute("_email", email)

    def update_user(self, user_id, user_data):
        """Update a user profile (first_name and last_name only)"""
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("Update data must be a non-empty dictionary.")
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "is_admin" in user_data:
            raise ValueError("Only an administrator can modify is_admin.")
        if "email" in user_data or "password" in user_data:
            raise ValueError("You cannot modify email or password.")
        if user_data:
            self.user_repo.update(user_id, user_data)
        return user
    
    def update_user_email(self, user_id, user_data):
        """Update a user's email with validation and uniqueness check."""
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("Update data must be a non-empty dictionary.")
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "email" not in user_data:
            raise ValueError("Email is required.")
        new_email = user_data["email"].strip().lower()
        existing_user = self.user_repo.get_by_attribute("_email", new_email)
        if existing_user and existing_user.id != user.id:
            raise ValueError("Email already exists.")
        self.user_repo.update(user_id, {"email": new_email})   
        return user
        

    def update_user_password(self, user_id, user_data):
        """Update a user's password with validation."""
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("Update data must be a non-empty dictionary.")
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "password" not in user_data:
            raise ValueError("Password is required.")
        new_password = user_data["password"]
        user.update_password(new_password)
        return user

    # =============================
    # ------ AMENITY METHODS ------
    # =============================

    def create_amenity(self, amenity_data):
        """Create and store a new amenity with unique name validation."""
        if not amenity_data or not isinstance(amenity_data, dict):
            raise ValueError("Amenity data must be a non-empty dictionary.")
        name = amenity_data.get("name")
        if not name:
            raise ValueError("Name is required.")
        name = name.strip().lower()
        amenity_data["name"] = name
        existing_amenity = self.amenity_repo.get_by_attribute("_name", name)
        if existing_amenity:
            raise ValueError("Amenity already exists.")
        amenity = Amenity.create_amenity(amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Return an amenity by id or None if not found."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Return all stored amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity with validation and name uniqueness checks."""
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
        """Create and store a place after validating owner and amenity ids."""
        if not place_data or not isinstance(place_data, dict):
            raise ValueError("Place data must be a non-empty dictionary.")
        owner_id = place_data.get("owner_id")
        if not owner_id:
            raise ValueError("Owner is required.")
        existing_owner = self.user_repo.get(owner_id)
        if not existing_owner:
            raise ValueError("Owner not found.")
        amenities_ids = place_data.get("amenities")
        if amenities_ids is None:
            amenities_ids = []
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
        """Return a detailed place representation with owner, amenities, and reviews."""
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
        del data["owner_id"]
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
        """Return a list of serialized places for listing endpoints."""
        return Place.get_all_places(self.place_repo)

    def update_place(self, place_id, place_data):
        """Update a place while protecting owner and amenities modifications."""
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
        """Link an amenity to a place after validating both ids."""
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found.")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        place.add_amenity(amenity_id)
        return place

    def remove_amenity_from_place(self, place_id, amenity_id):
        """Unlink an amenity from a place after validating both ids."""
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found.")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        place.remove_amenity(amenity_id)
        return place

    # =============================
    # ------ REVIEWS METHODS ------
    # =============================

    def create_review(self, review_data):
        """Create and store a review while enforcing place/user existence and uniqueness."""
        if not review_data or not isinstance(review_data, dict):
            raise ValueError("Review data must be a non-empty dictionary.")
        place_id = review_data.get("place_id")
        author_id = review_data.get("author_id")
        if place_id is None or author_id is None:
            raise ValueError("author_id and place_id are required.")
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found.")
        if self.user_repo.get(author_id) is None:
            raise ValueError("User not found.")
        if place.owner_id == author_id:
            raise ValueError("You cannot review your own place.")
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
        """Return review details by id or None if not found."""
        review = self.review_repo.get(review_id)
        if review is None:
            return None
        return review.get_details()

    def get_all_reviews(self):
        """Return a list of serialized reviews."""
        reviews = self.review_repo.get_all()
        list_review = []
        for review in reviews:
            details = review.get_details()
            list_review.append(details)
        return list_review

    def get_reviews_by_place(self, place_id):
        """Return a list of reviews for a place or None if place does not exist."""
        if self.place_repo.get(place_id) is None:
            return None
        reviews = self.review_repo.get_all()
        list_review_by_place = []
        for review in reviews:
            if review.place_id == place_id:
                list_review_by_place.append(review.get_details())
        return list_review_by_place

    def update_review(self, review_id, review_data):
        """Update a review while preventing author_id and place_id changes."""
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
        """Delete a review by id and return True when successful."""
        review = self.review_repo.get(review_id)
        if review is None:
            return None
        self.review_repo.delete(review_id)
        return True
