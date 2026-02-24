from basemodel import BaseModel

class User(BaseModel):

    _storage = {}

    def __init__(self, first_name, last_name, email, password, is_admin = False):
        super().__init__()
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._is_admin = is_admin

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

    def create_user():

    def get_all_users():

    def get_profil():

    def update_user():

    def set_password():

    def delete():
