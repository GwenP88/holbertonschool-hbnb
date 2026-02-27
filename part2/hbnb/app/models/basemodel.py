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

    def update(self, data):
        if not isinstance(data, dict) or not data:
            raise ValueError("Update data must be a non-empty dictionary")

        protected_fields = {"id", "created_at", "updated_at"}

        for key in data:
            if key in protected_fields:
                raise ValueError(f"{key} cannot be modified.")

            attr = "_" + key
            if not hasattr(self, attr):
                raise ValueError(f"{key} is not a valid field.")

        for key, value in data.items():
            setattr(self, "_" + key, value)

        self.save()