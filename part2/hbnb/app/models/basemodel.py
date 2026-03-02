"""Base model providing id generation, timestamps, and generic update helpers."""
import uuid
from datetime import datetime


class BaseModel:
    """Provide common id, timestamps, and persistence helpers for models."""

    def __init__(self):
        """Initialize the model with a unique id and timestamps."""
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def id(self):
        """Return the model id."""
        return self._id

    @property
    def created_at(self):
        """Return the creation timestamp."""
        return self._created_at

    @property
    def updated_at(self):
        """Return the last update timestamp."""
        return self._updated_at

    def update_time(self):
        """Refresh the updated_at timestamp."""
        self._updated_at = datetime.now()

    def save(self):
        """Persist changes by updating the updated_at timestamp."""
        self.update_time()

    def update(self, data):
        """Update allowed fields from a non-empty dictionary and persist changes."""
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
