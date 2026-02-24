from app.models.basemodel import BaseModel

class Place(BaseModel):

    _storage = {}
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self._title = title
        self._description = description
        self._price = price
        self._latitude = latitude
        self._longitude = longitude
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
            raise ValueError("First_name must not exceed 100 characters.")
        
    @staticmethod
    def _validate_desc(description):
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("Description must be a string or None.")
            if len(description) > 255:
                raise ValueError("Description must not exceed 255 characters.")
            
    @staticmethod
    def _validate_price(price):
        if price is None or not isinstance(price, float) or price < 0:
            raise ValueError("Price is required and must be a positive float")

    @staticmethod
    def _validate_latitude(latitude):
        if latitude is None or not isinstance(latitude, float) or latitude < -90 and latitude > 90:
            raise ValueError("Latitude is required and must be a float between -90 and 90")
        
    @staticmethod
    def _validate_longitude(longitude):
        if longitude is None or not isinstance(longitude, float) or longitude < -180 and longitude > 180:
            raise ValueError("longitude is required and must be a float between -180 and 180")
        
    @classmethod
    def _validate_owner(cls, owner):
        for user in cls._storage.values()

    @classmethod
    def create_place(cls, data, owner):

    @classmethod
    def update_details(self, data):

    
    def get_details(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner,
            "reviews": [],
            "amenities": [],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_list_items(self):

    
    

    def add_review(self, review):
        self.reviews.append(review)


    def add_amenity(self, amenity):

    def remove_amenity(self, amenity):        