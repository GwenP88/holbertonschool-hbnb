from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    """Specialized repository for Review persistence and future custom queries."""

    def __init__(self):
        """Initialize the repository with the Review model."""
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """Return all reviews for a given place id."""
        return self.model.query.filter_by(place_id=place_id).all()

