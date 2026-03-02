from app.models.basemodel import BaseModel
from werkzeug.security import generate_password_hash


class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self._validate_first_name(first_name)
        self._validate_last_name(last_name)
        email = self._validate_email(email)

        self._first_name = first_name.strip()
        self._last_name = last_name.strip()
        self._email = email
        self._password = None
        self._is_admin = is_admin

    # ----- Properties -----

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @property
    def is_admin(self):
        return self._is_admin

    # ----- Validations -----

    @staticmethod
    def _validate_first_name(first_name):
        if not first_name or not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name is required and must be a non-empty string.")
        if len(first_name.strip()) > 50:
            raise ValueError("first_name must not exceed 50 characters.")

    @staticmethod
    def _validate_last_name(last_name):
        if not last_name or not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name is required and must be a non-empty string.")
        if len(last_name.strip()) > 50:
            raise ValueError("last_name must not exceed 50 characters.")

    @staticmethod
    def _validate_email(email):
        if not email or not isinstance(email, str):
            raise ValueError("email is required and must be a string.")
        email = email.strip().lower()
        if " " in email:
            raise ValueError("Email must not contain spaces.")
        if email.count("@") != 1:
            raise ValueError("Email must contain exactly one '@'.")
        local, domain = email.split("@")
        if not local:
            raise ValueError("Email must have a non-empty part before '@'.")
        if not domain or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError("Email must have a valid domain with a '.' (ex: b.c).")
        return email

    @staticmethod
    def _validate_password(password):
        if not password or not isinstance(password, str):
            raise ValueError("password is required and must be a string.")
        password = password.strip()
        if len(password) < 8:
            raise ValueError("password must have at least 8 characters.")
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            raise ValueError("password must contain at least one letter and one digit.")

    # ----- Password management -----

    def set_password(self, password):
        self._validate_password(password)
        self._password = generate_password_hash(password.strip())
        self.save()

    # ----- Creation user -----

    @classmethod
    def create_user(cls, data):
        if not data or not isinstance(data, dict):
            raise ValueError("User data must be a non-empty dictionary.")
        if "is_admin" in data:
            raise ValueError("Only an administrator can set is_admin.")

        password = data.get("password")
        cls._validate_password(password)

        user = cls(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email")
        )

        user.set_password(password)
        return user

    # ---------- Serialization ----------

    def get_profile(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    # ----- Update User -----

    def update(self, data):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")
        if "first_name" in data:
            self._validate_first_name(data["first_name"])
            data["first_name"] = data["first_name"].strip()
        if "last_name" in data:
            self._validate_last_name(data["last_name"])
            data["last_name"] = data["last_name"].strip()
        if "email" in data:
            email = self._validate_email(data["email"])
            data["email"] = email
        super().update(data)

    # ----- delete profile -----

    def delete(self):
        raise NotImplementedError("Deletion must be handled by the repository.")
