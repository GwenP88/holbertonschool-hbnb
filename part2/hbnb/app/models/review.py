from basemodel import BaseModel
from user import User
from place import Place

class Review(BaseModel):

    _storage = {}
    
    def __init__ (self, comment, rating, author, place):
        super().__init__()
        self._comment = comment
        self._rating = rating
        self._author_id = author
        self._place_id = place
        
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
    
    @staticmethod
    def _validate_comment(comment):
        if comment is None or not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment is required and must be a non-empty string.")
            
    @staticmethod
    def _validate_rating(rating):
        if rating is None:
            raise ValueError("Rating is required.")
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        
    @classmethod
    def _validate_author(cls, author_id):
        if isinstance(author_id, str) and author_id.strip():
            if author_id in User._storage:
                return True
        return False
    
    @classmethod
    def _validate_place(cls, place_id):
        if isinstance(place_id, str) and place_id.strip():
            if place_id in Place._storage:
                return True
        return False
    
    @classmethod
    def create_review(cls, data, author_id, place_id):
        if not data or not isinstance(data, dict):
            raise ValueError("Review data must be a non-empty dictionary")
        comment = data.get("comment")
        rating = data.get("rating")
        cls._validate_comment(comment)
        cls._validate_rating(rating)
        if not cls._validate_author(author_id):
            raise ValueError("Author does not exist")
        if not cls._validate_place(place_id):
            raise ValueError("Place does not exist")
        review = cls(comment, rating, author=author_id, place=place_id)
        cls._storage[review.id] = review
        place_obj = Place._storage[place_id]
        place_obj.add_review(review)
        return review

    def get_details(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "rating": self.rating,
            "author_id": self.author_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def update_review(self, data):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update")
        if "comment" in data:
            self._validate_comment(data["comment"])
            self._comment = data["comment"]
        if "rating" in data:
            self._validate_rating(data["rating"])
            self._rating = data["rating"]
        if "author" in data:
            raise ValueError("Author cannot be updated")
        if "place" in data:
            raise ValueError("Place cannot be updated")
        self.save()

    def delete(self):
        storage = self.__class__._storage
        if self.id not in storage:
            raise ValueError("Review not found in storage.")
        if self.place_id in Place._storage:
            place_obj = Place._storage[self.place_id]
            if self.id in place_obj._reviews:
                place_obj._reviews.remove(self.id)
                place_obj.save()
        del storage[self.id]