from basemodel import BaseModel


class Amenity(BaseModel):

    def __init__(self, name, description=None):
        super().__init__()
        self._validate_name(name)
        self._validate_desc(description)

        self._name = name.strip().lower()
        self._description = description

    # ----- Properties -----

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description
    
    # ----- Validations -----

    @staticmethod
    def _validate_name(name):
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Name is required and must be a non-empty string.")
        if len(name.strip()) > 50:
            raise ValueError("Name must not exceed 50 characters.")

    @staticmethod
    def _validate_desc(description):
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Description must be a string.")
            if len(description) > 255:
                raise ValueError("Description must not exceed 255 characters.")

    # ----- Creation user -----

    @classmethod
    def create_amenity(cls, data: dict):
        if not data or not isinstance(data, dict):
            raise ValueError("Amenity data must be a dictionary.")
        return cls(
            name=data.get("name"),
            description=data.get("description")
        )
    
    # ----- Update Amenity -----

    def update(self, data):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")
        if "name" in data:
            self._validate_name(data["name"])
            data["name"] = data["name"].strip().lower()
        if "description" in data:
            self._validate_desc(data["description"])
        super().update(data)

    # ----- get details amenity-----

    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    # ----- delete amenity -----

    def delete(self):
        pass  # handled by repository