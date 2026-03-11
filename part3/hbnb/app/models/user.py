"""User model with validation, password hashing, serialization, and update helpers."""
from app import db, bcrypt
from app.models.basemodel import BaseModel

class User(BaseModel):
    """Represent a user with validated identity fields and optional admin flag."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a user with validated names, email, and optional admin flag."""

        self._validate_first_name(first_name)
        self._validate_last_name(last_name)
        email = self._validate_email(email)

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email
        self.password = None
        self.is_admin = is_admin

    # ----- Validations -----

    @staticmethod
    def _validate_first_name(first_name):
        """Validate that first_name is a non-empty string within 50 characters."""
        if not first_name or not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name is required and must be a non-empty string.")
        if len(first_name.strip()) > 50:
            raise ValueError("first_name must not exceed 50 characters.")

    @staticmethod
    def _validate_last_name(last_name):
        """Validate that last_name is a non-empty string within 50 characters."""
        if not last_name or not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name is required and must be a non-empty string.")
        if len(last_name.strip()) > 50:
            raise ValueError("last_name must not exceed 50 characters.")

    @staticmethod
    def _validate_email(email):
        """Validate and normalize an email address to lowercase."""
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
            raise ValueError("Email must have a valid domain with a '.'")
        return email

    @staticmethod
    def _validate_password(password):
        """Validate password strength and formatting requirements."""
        if not password or not isinstance(password, str):
            raise ValueError("password is required and must be a string.")
        password = password.strip()
        if len(password) < 8:
            raise ValueError("password must have at least 8 characters.")
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            raise ValueError("password must contain at least one letter and one digit.")

    # ----- Password management -----

    def set_password(self, password):
        """Hashes the password before storing it."""
        self._validate_password(password)
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    # ----- Creation user -----

    @classmethod
    def create_user(cls, data):
        """Create a user from input data while enforcing creation rules."""
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
        """Return a serializable dictionary of user profile fields."""
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
        """Update user fields with validation and normalization."""
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update.")
        if "first_name" in data:
            self._validate_first_name(data["first_name"])
            data["first_name"] = data["first_name"].strip()
        if "last_name" in data:
            self._validate_last_name(data["last_name"])
            data["last_name"] = data["last_name"].strip()
        super().update(data)

    def update_email(self, email):
        """Update user email field with validation and normalization."""
        if not email:
            raise ValueError("No email to update.")
        email = self._validate_email(email)
        self.email = email

    def update_password(self, password):
        """Update user password field with validation."""
        if not password:
            raise ValueError("No password to update.")
        self.set_password(password)

    # ----- delete profile -----

    def delete(self):
        """Delete the user."""
        pass  # handled by repository
