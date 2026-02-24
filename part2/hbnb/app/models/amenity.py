from basemodel import BaseModel

class Amenity(BaseModel):

    _storage = {}

    def __init__(self, name: str, description: str = ""):
        super().__init__()
        self._name = name
        self._description = description

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description

    @staticmethod
    def _validate_name(name):
        if name is None or not isinstance(name, str) or not name.strip() or name is None:
            raise ValueError("Name is required and must be a non-empty string.")
        if len(name) > 50:
            raise ValueError("Name must not exceed 50 characters.")
        
    @staticmethod
    def _validate_desc(description):
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("description must be a string or None.")
            if len(description) > 255:
                raise ValueError("description must not exceed 255 characters.")    

    @classmethod
    def create_amenity(cls, data):
        name = data.get("name", "")
        description = data.get("description", "")
        cls._validate_name(name)
        cls._validate_desc(description)
        amenity = cls(name=name, description=description)
        cls._storage[amenity.id] = amenity
        return amenity
    
    @classmethod
    def get_all_amenities(cls):
        list_amenities = []
        for a in cls._storage.values():
            list_amenities.append(a.get_details())
        return list_amenities
    
    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update_amenity(self, data):
        if not data: 
            raise ValueError("No data to update")
        if "name" in data:
            self._validate_name(data["name"])
            self._name = data["name"]
        if "description" in data:
            self._validate_desc(data["description"])
            self._description = data["description"]
        self.save()
        

    def delete(self):
        storage = self.__class__._storage
        if self.id not in storage:
            raise ValueError("Amenity not found in storage.")
        del storage[self.id]
