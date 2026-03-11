from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    # Specialized repository for reviews, designed to support place-specific queries later.
