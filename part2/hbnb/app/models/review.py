from app.models.basemodel import BaseModel


class Review(BaseModel):

    def __init__(self, comment, rating, author_id, place_id):
        super().__init__()

        self._validate_comment(comment)

        rating = self._to_number(rating, "Rating", int)
        self._validate_rating(rating)

        self._comment = comment.strip()
        self._rating = rating
        self._author_id = author_id
        self._place_id = place_id

    # -------- Helpers --------

    @staticmethod
    def _to_number(value, field_name, number_type=int):
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
    def comment(self):
        return self._comment

    @property
    def rating(self):
        return self._rating

    @property
    def author_id(self):
        return self._author_id

    @property
    def place_id(self):
        return self._place_id

    # ------- Validations -----

    @staticmethod
    def _validate_comment(comment):
        if not comment or not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment is required.")

    @staticmethod
    def _validate_rating(rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

    # -------- Creation -------

    @classmethod
    def create_review(cls, data: dict, author_id, place_id):
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
        return {
            "id": self.id,
            "comment": self._comment,
            "rating": self._rating,
            "author_id": self._author_id,
            "place_id": self._place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    # -------- Update ---------

    def update(self, data: dict):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")

        if "comment" in data:
            self._validate_comment(data["comment"])
            self._comment = data["comment"].strip()

        if "rating" in data:
            rating = self._to_number(data["rating"], "Rating", int)
            self._validate_rating(rating)
            self._rating = rating

        self.save()

    # -------- Delete ---------

    def delete(self):
        pass  # handled by repository
