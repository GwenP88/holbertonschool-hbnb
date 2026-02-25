from basemodel import BaseModel


class Review(BaseModel):

    def __init__(self, comment, rating, author_id, place_id):
        super().__init__()

        self._validate_comment(comment)
        self._validate_rating(rating)

        self._comment = comment.strip()
        self._rating = rating
        self._author_id = author_id
        self._place_id = place_id

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

    @staticmethod
    def _validate_comment(comment):
        if not comment or not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment is required.")

    @staticmethod
    def _validate_rating(rating):
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

    def update_review(self, data: dict):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")

        if "comment" in data:
            self._validate_comment(data["comment"])
            self._comment = data["comment"]

        if "rating" in data:
            self._validate_rating(data["rating"])
            self._rating = data["rating"]

        self.save()

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

    def delete(self):
        pass  # handled by repository