import hashlib
import random

class User:
    def __init__(self, name, email, phone, password, user_id=None):
        self.user_id = user_id if user_id is not None else random.randint(1000, 9999)
        self.name = name
        self.email = email
        self.phone = phone
        self.role = None
        self._password_hash = self._hash_password(password)

    @classmethod
    def from_dict(cls, record):
        user = cls(record["name"], record["email"], record["phone"], "", user_id=record["user_id"])
        user.role = record.get("role")
        user._password_hash = record.get("password_hash", user._password_hash)
        return user

    def _hash_password(self, password=None):
        if password is None:
            return self._password_hash
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password = None):
        return self._password_hash == self._hash_password(password)