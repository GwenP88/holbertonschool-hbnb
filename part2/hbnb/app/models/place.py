from basemodel import BaseModel
from user import User
from amenity import Amenity
from review import Review

class Place(BaseModel):

    _storage = {}

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self._title = title
        self._description = description
        self._price = float(price)
        self._latitude = float(latitude)
        self._longitude = float(longitude)
        self._owner = owner
        self._reviews = []
        self._amenities = []

    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description
    
    @property
    def price(self):
        return self._price

    @property
    def latitude(self):
        return self._latitude
    
    @property
    def longitude(self):
        return self._longitude
    
    @property
    def owner(self):
        return self._owner
    
    @staticmethod
    def _validate_title(title):
        if title is None or not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required and must be a non-empty string.")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters.")
        
    @staticmethod
    def _validate_desc(description):
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Description must be a string or None.")
            if len(description) > 255:
                raise ValueError("Description must not exceed 255 characters.")
            
    @staticmethod
    def _validate_price(price):
        if price is None:
            raise ValueError("Price is required")
        if not isinstance(price, (float, int)) or isinstance(price, bool):
            raise TypeError("Price must be an integer or a float")
        if price <= 0:
            raise ValueError("Price must be > 0")

    @staticmethod
    def _validate_latitude(latitude):
        if latitude is None:
            raise ValueError("Latitude is required")
        if not isinstance(latitude, (int,float)) or isinstance(latitude, bool):
            raise TypeError("Latitude and must be an integer or a float")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        
    @staticmethod
    def _validate_longitude(longitude):
        if longitude is None:
            raise ValueError("Longitude is required")
        if not isinstance(longitude, (int,float)) or isinstance(longitude, bool):
            raise TypeError("Longitude must be an integer or a float")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")

    @classmethod
    def _validate_owner(cls, owner):
        if isinstance(owner, User):
            if owner.id in User._storage:
                return True
        return False

    @classmethod
    def create_place(cls, data, owner):
        if not data or not isinstance(data, dict):
            raise ValueError("Place data must be a non-empty dictionary")
        title = data.get("title")
        description = data.get("description")
        price = data.get("price")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        cls._validate_title(title)
        cls._validate_desc(description)
        cls._validate_price(price)
        cls._validate_latitude(latitude)
        cls._validate_longitude(longitude)
        if not cls._validate_owner(owner):
            raise ValueError("Owner does not exist")
        place = cls(title, description, price, latitude, longitude, owner=owner)
        cls._storage[place.id] = place
        return place

    def update_details(self, data):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update")
        if "title" in data:
            self._validate_title(data["title"])
            self._title = data["title"]
        if "description" in data:
            self._validate_desc(data["description"])
            self._description = data["description"]
        if "price" in data:
            self._validate_price(data["price"])
            self._price = float(data["price"])
        if "latitude" in data:
            self._validate_latitude(data["latitude"])
            self._latitude = float(data["latitude"])
        if "longitude" in data:
            self._validate_longitude(data["longitude"])
            self._longitude = float(data["longitude"])
        if "owner" in data:
            raise ValueError("Owner cannot be updated")
        self.save()

    def get_details(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.id,
            "reviews": self._reviews,
            "amenities": self._amenities,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    @classmethod
    def get_all_places(cls):
        list_place = []
        for p in cls._storage.values():
            list_place.append(p.get_details())
        return list_place

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an instance of Amenity")
        if amenity.id not in Amenity._storage:
            raise ValueError("Amenity does not exist")
        if amenity.id in self._amenities:
            raise ValueError("Amenity already added to this place")
        self._amenities.append(amenity.id)
        self.save()

    def remove_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an instance of Amenity")
        if amenity.id not in Amenity._storage:
            raise ValueError("Amenity does not exist")
        if amenity.id not in self._amenities:
            raise ValueError("Amenity not added to this place")
        self._amenities.remove(amenity.id)
        self.save()

    def add_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("Review must be an instance of Review")
        if review.id not in Review._storage:
            raise ValueError("Review does not exist")
        if review.id in self._reviews:
            raise ValueError("Review already added to this place")
        self._reviews.append(review.id)
        self.save()

    def remove_review(self, review):
        if not isinstance(review, Review):
            raise TypeError("Review must be an instance of Review")
        if review.id not in Review._storage:
            raise ValueError("Review does not exist")
        if review.id not in self._reviews:
            raise ValueError("Review not added to this place")
        self._reviews.remove(review.id)
        self.save()
  
    def get_all_reviews(self):
        list_all_reviews = []
        for review_id in self._reviews:
            if review_id in Review._storage:
                review_obj = Review._storage[review_id]
                list_all_reviews.append(review_obj.get_details())
        return list_all_reviews

    def get_all_amenities(self):
        list_all_amenities = []
        for amenity_id in self._amenities:
            if amenity_id in Amenity._storage:
                amenity_obj = Amenity._storage[amenity_id]
                list_all_amenities.append(amenity_obj.get_details())
        return list_all_amenities

    def delete(self):
        storage = self.__class__._storage
        if self.id not in storage:
            raise ValueError("Place not found in storage.")
        for review_id in self._reviews:
            if review_id in Review._storage:
                del Review._storage[review_id]
        del storage[self.id]
