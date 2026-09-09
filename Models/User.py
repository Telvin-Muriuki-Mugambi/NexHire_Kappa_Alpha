import hashlib
import random

class User:
    def __init__(self, name, email, phone, password):
        self.user_id = random.randint(1000, 9999)
        self.name = name
        self.email = email
        self.phone_number = phone
        self.role = None
        self._password = password

    def _hash_password(self):
        return hashlib.sha256(self._password.encode()).hexdigest()

    # def verify_password(self, password):
    #     return self._password_hash == self._hash_password(password)