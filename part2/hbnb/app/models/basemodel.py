import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self):
        return self._id
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def updated_at(self):
        return self._updated_at

    def update_time(self):
        self._updated_at = datetime.now()
        
    def save(self):
        self.update_time()