"""Repository interfaces and an in-memory implementation for CRUD operations."""
from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Define the required CRUD operations for repository implementations."""
    @abstractmethod
    def add(self, obj):
        """Store a new object."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Return an object."""
        pass

    @abstractmethod
    def get_all(self):
        """Return all objects."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Remove an object."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Return the first object matching an attribute value."""
        pass


class InMemoryRepository(Repository):
    """Implement repository operations using an in-memory dictionary."""
    def __init__(self):
        """Initialize an empty in-memory storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """Add an object to in-memory storage using its id as key."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object from storage by id."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return a list of all objects in storage."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update a stored object by id if it exists."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete a stored object by id if it exists."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Find an object by attribute value in storage."""
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

class SQLAlchemyRepository(Repository):
    """Implement repository operations using SQLAlchemy persistence."""
    def __init__(self, model):
        """Initialize the repository with the SQLAlchemy model."""
        self.model = model

    def add(self, obj):
        """Add an object to the database session and commit it."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieve an object from the database by id."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Return all objects from the database."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update a stored object by id if it exists."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, "_" + key, value)
            obj.update_time()
            db.session.commit()

    def delete(self, obj_id):
        """Delete a stored object by id if it exists."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Find an object by attribute value in the database."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()