"""Place model with validation, serialization, amenity linking, and update helpers."""
from app import db
from app.models.basemodel import BaseModel

# Association table for many-to-many relationship for amenities and places
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """Represent a place with location, price, owner, and linked amenities."""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # relation Place/User
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', back_populates='places', lazy=True)

    # relation Place/Review
    reviews = db.relationship('Review', back_populates='place', lazy=True)

    # relation Place/Amenity
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, user_id):
        """Initialize a place with validated fields and normalized numeric values."""


        self._validate_title(title)
        self._validate_description(description)

        price = self._to_number(price, "Price", float)
        latitude = self._to_number(latitude, "Latitude", float)
        longitude = self._to_number(longitude, "Longitude", float)

        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)

        self.title = title.strip()
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.user_id = user_id

    # -------- Helpers --------
    @staticmethod
    def _to_number(value, field_name, number_type=float):
        """Convert a value to a number type and raise a clear validation error."""
        if value is None:
            raise ValueError(f"{field_name} is required.")

        if isinstance(value, bool):
            raise ValueError(f"{field_name} must be a number.")

        try:
            return number_type(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a number.")

    # ------- Validations -----
    @staticmethod
    def _validate_title(title):
        """Validate that title is a non-empty string within 100 characters."""
        if not title or not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required and must be a non-empty string.")
        if len(title.strip()) > 100:
            raise ValueError("Title must not exceed 100 characters.")

    @staticmethod
    def _validate_description(description):
        """Validate that description is a non-empty string within 255 characters."""
        if not description or not isinstance(description, str) or not description.strip():
            raise ValueError("Description is required and must be a non-empty string.")
        if len(description.strip()) > 255:
            raise ValueError("Description must not exceed 255 characters.")

    @staticmethod
    def _validate_price(price):
        """Validate that price is non-negative."""
        if price <= 0:
            raise ValueError("Price must be a positive number.")

    @staticmethod
    def _validate_latitude(latitude):
        """Validate that latitude is between -90 and 90."""
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90.")

    @staticmethod
    def _validate_longitude(longitude):
        """Validate that longitude is between -180 and 180."""
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180.")

    # ------- Creation --------
    @classmethod
    def create_place(cls, data, user_id):
        """Create a Place instance from input data and an owner id."""
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            user_id=user_id
        )

    # ------- Serialization ---
    def get_details(self):
        """Return a serializable dictionary of place fields and amenities."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "user_id": self.user_id,
            "amenities": list(self.amenities),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_list_item(self):
        """Return a lightweight dictionary representation for place listings."""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def get_all_places(cls, place_repo):
        """Return a list of serialized places from the given repository."""
        places = place_repo.get_all()
        return [place.to_list_item() for place in places]

    # -------- Update ---------
    def update(self, data: dict):
        """Update place fields with validation and persistence."""
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")
        if "title" in data:
            self._validate_title(data["title"])
            data["title"] = data["title"].strip()
        if "description" in data:
            self._validate_description(data["description"])
            data["description"] = data["description"].strip()
        if "price" in data:
            price = self._to_number(data["price"], "Price", float)
            self._validate_price(price)
            data["price"] = price
        if "latitude" in data:
            latitude = self._to_number(data["latitude"], "Latitude", float)
            self._validate_latitude(latitude)
            data["latitude"] = latitude
        if "longitude" in data:
            longitude = self._to_number(data["longitude"], "Longitude", float)
            self._validate_longitude(longitude)
            data["longitude"] = longitude
        super().update(data)

    # ----- Amenities ---------
    def add_amenity(self, amenity_id):
        """Link an amenity id to the place and persist the change."""
        if amenity_id in self.amenities:
            raise ValueError("Amenity already added.")
        self.amenities.append(amenity_id)

    def remove_amenity(self, amenity_id):
        """Unlink an amenity id from the place and persist the change."""
        if amenity_id not in self.amenities:
            raise ValueError("Amenity not linked.")
        self.amenities.remove(amenity_id)

    # -------- Delete ---------

    def delete(self):
        """Delete the place."""
        pass  # handled by repository
