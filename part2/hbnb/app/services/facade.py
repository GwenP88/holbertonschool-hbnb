from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    # ==========================
    # ------ USER METHODS ------
    # ==========================

    def create_user(self, user_data):
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("User data must be a non-empty dictionary.")
        if "is_admin" in user_data:
            raise ValueError("Only an administrator can set is_admin.")

        email = user_data.get("email")
        if not email:
            raise ValueError("Email is required.")

        email = email.strip().lower()
        existing_user = self.user_repo.get_by_attribute("_email", email)
        if existing_user:
            raise ValueError("Email already exists.")

        user = User.create_user(user_data)
        self.user_repo.add(user)
        return user

    def get_user(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("Update data must be a non-empty dictionary.")

        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "is_admin" in user_data:
            raise ValueError("Only an administrator can modify is_admin.")
        if "email" in user_data:
            new_email = user_data["email"].strip().lower()
            existing_user = self.user_repo.get_by_attribute("_email", new_email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("Email already exists.")
            user_data["email"] = new_email
        if "password" in user_data:
            user.set_password(user_data["password"])
            del user_data["password"]
        if user_data:
            self.user_repo.update(user_id, user_data)
        return user