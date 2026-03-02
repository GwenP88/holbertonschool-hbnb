from app.models.basemodel import BaseModel


class Place(BaseModel):

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()

        self._validate_title(title)
        self._validate_description(description)

        price = self._to_number(price, "Price", float)
        latitude = self._to_number(latitude, "Latitude", float)
        longitude = self._to_number(longitude, "Longitude", float)

        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)

        self._title = title.strip()
        self._description = description
        self._price = price
        self._latitude = latitude
        self._longitude = longitude
        self._owner_id = owner_id
        self._amenities = []

    # -------- Helpers --------

    @staticmethod
    def _to_number(value, field_name, number_type=float):
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
        if not title or not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required and must be a non-empty string.")
        if len(title.strip()) > 100:
            raise ValueError("Title must not exceed 100 characters.")

    @staticmethod
    def _validate_description(description):
        if not description or not isinstance(description, str) or not description.strip():
            raise ValueError("Description is required and must be a non-empty string.")
        if len(description.strip()) > 255:
            raise ValueError("Description must not exceed 255 characters.")

    @staticmethod
    def _validate_price(price):
        if price <= 0:
            raise ValueError("Price must be non-negative.")

    @staticmethod
    def _validate_latitude(latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90.")

    @staticmethod
    def _validate_longitude(longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180.")

    # ------- Creation --------

    @classmethod
    def create_place(cls, data, owner_id):
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=owner_id
        )

    # ------- Serialization ---

    def get_details(self):
        return {
            "id": self.id,
            "title": self._title,
            "description": self._description,
            "price": self._price,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "owner_id": self._owner_id,
            "amenities": list(self._amenities),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_list_item(self):
        return {
            "id": self.id,
            "title": self._title,
            "price": self._price,
            "latitude": self._latitude,
            "longitude": self._longitude,
        }

    @classmethod
    def get_all_places(cls, place_repo):
        places = place_repo.get_all()
        return [place.to_list_item() for place in places]

    # -------- Update ---------

    def update(self, data: dict):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")

        if "title" in data:
            self._validate_title(data["title"])
            self._title = data["title"].strip()

        if "description" in data:
            self._validate_description(data["description"])
            self._description = data["description"]

        if "price" in data:
            price = self._to_number(data["price"], "Price", float)
            self._validate_price(price)
            self._price = price

        if "latitude" in data:
            latitude = self._to_number(data["latitude"], "Latitude", float)
            self._validate_latitude(latitude)
            self._latitude = latitude

        if "longitude" in data:
            longitude = self._to_number(data["longitude"], "Longitude", float)
            self._validate_longitude(longitude)
            self._longitude = longitude

        self.save()

    # ----- Amenities ---------

    def add_amenity(self, amenity_id):
        if amenity_id in self._amenities:
            raise ValueError("Amenity already added.")
        self._amenities.append(amenity_id)
        self.save()

    def remove_amenity(self, amenity_id):
        if amenity_id not in self._amenities:
            raise ValueError("Amenity not linked.")
        self._amenities.remove(amenity_id)
        self.save()

    # -------- Delete ---------

    def delete(self):
        pass  # handled by repository
