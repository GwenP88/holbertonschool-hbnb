from basemodel import BaseModel


class Place(BaseModel):

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()

        self._validate_title(title)
        self._validate_desc(description)
        self._validate_price(price)
        self._validate_latitude(latitude)
        self._validate_longitude(longitude)

        self._title = title.strip()
        self._description = description
        self._price = float(price)
        self._latitude = float(latitude)
        self._longitude = float(longitude)
        self._owner_id = owner_id
        self._amenities = []

    @staticmethod
    def _validate_title(title):
        if not title or not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required and must be a non-empty string.")
        if len(title.strip()) > 100:
            raise ValueError("Title must not exceed 100 characters.")

    @staticmethod
    def _validate_desc(description):
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Description must be a string.")
            if len(description) > 255:
                raise ValueError("Description must not exceed 255 characters.")

    @staticmethod
    def _validate_price(price):
        if price is None:
            raise ValueError("Price is required.")
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise ValueError("Price must be a number.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

    @staticmethod
    def _validate_latitude(latitude):
        if latitude is None:
            raise ValueError("Latitude is required.")
        if not isinstance(latitude, (int, float)) or isinstance(latitude, bool):
            raise ValueError("Latitude must be a number.")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90.")

    @staticmethod
    def _validate_longitude(longitude):
        if longitude is None:
            raise ValueError("Longitude is required.")
        if not isinstance(longitude, (int, float)) or isinstance(longitude, bool):
            raise ValueError("Longitude must be a number.")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180.")

    @classmethod
    def create_place(cls, data: dict, owner_id):
        if not data or not isinstance(data, dict):
            raise ValueError("Place data must be a dictionary.")
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=owner_id
        )

    def update_details(self, data: dict):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")

        if "title" in data:
            self._validate_title(data["title"])
            self._title = data["title"].strip()

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

        self.save()

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

    def get_details(self):
        return {
            "id": self.id,
            "title": self._title,
            "description": self._description,
            "price": self._price,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "owner_id": self._owner_id,
            "amenities": self._amenities,
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

    def delete(self):
        pass  # handled by repository