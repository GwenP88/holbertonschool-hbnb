from basemodel import BaseModel

class User(BaseModel):

    _storage = {}

    def __init__(self, first_name: str, last_name: str = "", email: str, password: str, is_admin: bool):
        super().__init__()
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._is_admin = is_admin