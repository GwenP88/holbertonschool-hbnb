"""Review model with validation, serialization, and update helpers."""
from app import db
from app.models.basemodel import BaseModel


class Review(BaseModel):
    """Represent a review with a comment, rating, author id, and place id."""
    __tablename__ = 'reviews'

    comment = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, comment, rating, author_id, place_id):
        """Initialize a review with a validated comment and rating."""

        self._validate_comment(comment)

        rating = self._to_number(rating, "Rating", int)
        self._validate_rating(rating)

        self.comment = comment.strip()
        self.rating = rating
        self._author_id = author_id
        self._place_id = place_id

    # -------- Helpers --------
    @staticmethod
    def _to_number(value, field_name, number_type=int):
        """Convert a value to a number type and raise a clear validation error."""
        if value is None:
            raise ValueError(f"{field_name} is required.")
        if isinstance(value, bool):
            raise ValueError(f"{field_name} must be a number.")
        try:
            return number_type(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a number.")

    # ------- Properties ------

    @property
    def author_id(self):
        """Return the review author id."""
        return self._author_id

    @property
    def place_id(self):
        """Return the reviewed place id."""
        return self._place_id

    # ------- Validations -----
    @staticmethod
    def _validate_comment(comment):
        """Validate that comment is a non-empty string."""
        if not comment or not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment is required.")
        if len(comment.strip()) > 500:
            raise ValueError("Comment must not exceed 500 characters.")

    @staticmethod
    def _validate_rating(rating):
        """Validate that rating is between 1 and 5."""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

    # -------- Creation -------
    @classmethod
    def create_review(cls, data: dict, author_id, place_id):
        """Create a Review instance from input data and related ids."""
        if not data or not isinstance(data, dict):
            raise ValueError("Review data must be a dictionary.")
        return cls(
            comment=data.get("comment"),
            rating=data.get("rating"),
            author_id=author_id,
            place_id=place_id
        )

    # ------- Serialization ---
    def get_details(self):
        """Return a serializable dictionary of review fields."""
        return {
            "id": self.id,
            "comment": self.comment,
            "rating": self.rating,
            "author_id": self._author_id,
            "place_id": self._place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    # -------- Update ---------
    def update(self, data: dict):
        """Update review fields with validation."""
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")
        if "comment" in data:
            self._validate_comment(data["comment"])
            data["comment"] = data["comment"].strip()
        if "rating" in data:
            rating = self._to_number(data["rating"], "Rating", int)
            self._validate_rating(rating)
            data["rating"] = rating
        super().update(data)

    # -------- Delete ---------
    def delete(self):
        """Delete the review."""
        pass  # handled by repository
