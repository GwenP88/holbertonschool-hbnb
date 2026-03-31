"""Base model providing id generation, timestamps, and generic update helpers."""
from app import db
import uuid
from datetime import datetime, UTC

def utc_now():
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(UTC)

class BaseModel(db.Model):
    """Provide common id, timestamps, and persistence helpers for models."""
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    def update(self, data):
        """Update allowed fields from a non-empty dictionary."""
        if not isinstance(data, dict) or not data:
            raise ValueError("Update data must be a non-empty dictionary")
        protected_fields = {"id", "created_at", "updated_at"}
        for key in data:
            if key in protected_fields:
                raise ValueError(f"{key} cannot be modified.")
            if not hasattr(self, key):
                raise ValueError(f"{key} is not a valid field.")
        for key, value in data.items():
            setattr(self, key, value)

