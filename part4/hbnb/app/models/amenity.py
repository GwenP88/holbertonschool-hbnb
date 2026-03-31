"""Amenity model with validation, serialization, and update helpers."""
from app import db
from app.models.basemodel import BaseModel
from app.models.place import place_amenity


class Amenity(BaseModel):
    """Represent an amenity with a validated name and optional description."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))

    # relation Place/Amenity
    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities', lazy=True)

    def __init__(self, name, description=None):
        """Initialize an amenity with a validated name and optional description."""
        self._validate_name(name)
        self._validate_desc(description)

        self.name = name.strip().lower()
        self.description = description

    # ----- Validations -----
    @staticmethod
    def _validate_name(name):
        """Validate that the name is a non-empty string within 50 characters."""
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Name is required and must be a non-empty string.")
        if len(name.strip()) > 50:
            raise ValueError("Name must not exceed 50 characters.")

    @staticmethod
    def _validate_desc(description):
        """Validate that the description is a string within 255 characters when provided."""
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Description must be a string.")
            if len(description) > 255:
                raise ValueError("Description must not exceed 255 characters.")

    # ----- Creation user -----
    @classmethod
    def create_amenity(cls, data: dict):
        """Create an Amenity instance from a validated data dictionary."""
        if not data or not isinstance(data, dict):
            raise ValueError("Amenity data must be a dictionary.")
        return cls(
            name=data.get("name"),
            description=data.get("description")
        )

    # ---------- Serialization ----------
    def get_details(self):
        """Return a serializable dictionary of amenity fields."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    # ----- Update Amenity -----
    def update(self, data):
        """Update amenity fields with validation and normalization."""
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")
        if "name" in data:
            self._validate_name(data["name"])
            data["name"] = data["name"].strip().lower()
        if "description" in data:
            self._validate_desc(data["description"])
        super().update(data)
