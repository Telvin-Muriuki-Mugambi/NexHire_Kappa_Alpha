import hashlib
import random

class User:
    def __init__(self, name, email, phone, password, user_id=None):
        self.user_id = user_id if user_id is not None else random.randint(1000, 9999)
        self.name = name
        self.email = email
        self.phone_number = phone
        self.role = None
        self._password_hash = self._hash_password(password)

    def _hash_password(self, password=None):
        if password is None:
            return self._password_hash
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password = None):
        return self._password_hash == self._hash_password(password)