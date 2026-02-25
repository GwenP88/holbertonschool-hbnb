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