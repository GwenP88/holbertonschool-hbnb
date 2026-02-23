from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name is None:
            raise ValueError("name is required")
        elif not isinstance(name, str):
            raise TypeError("name must be a string")
        elif name.strip() == "":
            raise ValueError("name must be not empty")
        elif len(name.strip()) > 50:
            raise ValueError("name must not exceed 50 characters")
        else:
            self.__name = name.strip()

    def update_amenity(self, data):
        super().update(data)
    
    def get_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
