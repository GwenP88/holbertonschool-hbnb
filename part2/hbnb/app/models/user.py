from basemodel import BaseModel
from werkzeug.security import generate_password_hash

class User(BaseModel):

    _storage = {}

    def __init__(self, first_name, last_name, email, is_admin = False):
        super().__init__()
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = None
        self._is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name
    
    @property
    def is_admin(self):
        return self._is_admin

    @property
    def email(self):
        return self._email

    @staticmethod
    def _validate_first_name(first_name):
        if first_name is None or not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name is required and must be a non-empty string.")
        if len(first_name) > 50:
            raise ValueError("first_name must not exceed 50 characters.")
        
    @staticmethod
    def _validate_last_name(last_name):
        if last_name is None or not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name is required and must be a non-empty string.")
        if len(last_name) > 50:
            raise ValueError("last_name must not exceed 50 characters.")
        
    @staticmethod
    def _validate_email(email):
        if email is None or not isinstance(email, str):
            raise ValueError("email is required and must be a string.")
        email = email.strip().lower()
        if not email:
            raise ValueError("email must not be empty")
        if email.count("@") != 1:
            raise ValueError("Email must contain exactly one '@'.")
        return email

    @staticmethod
    def _validate_password(password):
        if password is None or not isinstance(password, str):
            raise ValueError("password is required and must be a string.")
        pswd = password.strip()
        if not pswd:
            raise ValueError("password must not be empty")
        if len(pswd) < 8:
            raise ValueError("password must have 8 characters min.")
        has_letter = any(letter.isalpha() for letter in pswd)
        has_digit = any(digit.isdigit() for digit in pswd)
        if not has_letter or not has_digit:
            raise ValueError("password must have 1 letter and 1 digit")
        
    def set_password(self, password):
        self._validate_password(password)
        self._password = generate_password_hash(password.strip())
        self.save()

    @classmethod
    def _email_exists(cls, email):
        for user in cls._storage.values():
            if user.email == email:
                return True
        return False
  
    @classmethod
    def create_user(cls, data):
        if not data or not isinstance(data, dict):
            raise ValueError("User data must be a non-empty dictionary")
        if "is_admin" in data:
            raise ValueError("Only an administrator can set is_admin.")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        email = data.get("email", "")
        password = data.get("password", "")
        cls._validate_first_name(first_name)
        cls._validate_last_name(last_name)
        email = cls._validate_email(email)
        if cls._email_exists(email): 
            raise ValueError("Email already exists")
        user = cls(first_name, last_name, email, is_admin=False)
        user.set_password(password)
        cls._storage[user.id] = user
        return user

    @classmethod
    def get_all_users(cls):
        list_users = []
        for u in cls._storage.values():
            list_users.append(u.get_profile())
        return list_users

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

    def update_user(self, data):
        if not data or not isinstance(data, dict):
            raise ValueError("No data to update")
        if "is_admin" in data:
            raise ValueError("Only an administrator can set is_admin.")
        if "first_name" in data:
            self._validate_first_name(data["first_name"])
            self._first_name = data["first_name"]
        if "last_name" in data:
            self._validate_last_name(data["last_name"])
            self._last_name = data["last_name"]
        if "email" in data:
            new_email = self._validate_email(data["email"])
            if new_email != self.email:
                if User._email_exists(new_email):
                    raise ValueError("Email already exists")
                self._email = new_email
        if "password" in data:
            self.set_password(data["password"])
        else :
            self.save()

    def delete(self):
        storage = self.__class__._storage
        if self.id not in storage:
            raise ValueError("User not found in storage.")
        del storage[self.id]
