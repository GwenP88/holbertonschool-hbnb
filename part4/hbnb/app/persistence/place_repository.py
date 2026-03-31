from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    """Specialized repository for Place persistence and future custom queries."""

    def __init__(self):
        """Initialize the repository with the Place model."""
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
            """Return all places for a given owner_id."""
            return self.model.query.filter_by(owner_id=owner_id).all()