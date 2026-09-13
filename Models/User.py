"""Define the shared user identity, credentials, role, and CV record."""

import hashlib
import random


class User:
    """Represent an authenticated NexHire account."""

    def __init__(self, name, email, phone, password, user_id=None, cv=None):
        """Initialize identity data and hash the supplied password."""
        self.user_id = user_id if user_id is not None else random.randint(1000, 9999)
        self.name = name
        self.email = email
        self.phone_number = phone
        self.role = None
        self.cv = cv
        self._password_hash = self._hash_password(password)


    def to_dict(self):
        """Serialize the user for JSON persistence."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role": self.role,
            "cv": self.cv,
            "password_hash": self._password_hash,
        }


    @classmethod
    def from_dict(cls, record):
        """Recreate a user from current or legacy JSON fields."""
        if "name" in record and "email" in record and "phone_number" in record:
            name = record["name"]
            email = record["email"]
            phone = record["phone_number"]
        elif "username" in record:
            name = record["username"]
            email = record.get("email", f"{record.get('username', 'unknown').lower()}@legacy.local")
            phone = record.get("phone_number", "")
        else:
            raise KeyError("User record is missing required identity fields")

        user = cls(
            name,
            email,
            phone,
            "",
            user_id=record.get("user_id"),
            cv=record.get("cv"),
        )
        user.role = record.get("role")
        user._password_hash = record.get("password_hash", user._password_hash)
        return user


    def _hash_password(self, password=None):
        """Return the stored hash or hash a supplied password."""
        if password is None:
            return self._password_hash
        return hashlib.sha256(password.encode()).hexdigest()


    def verify_password(self, password=None):
        """Return whether a password matches the stored hash."""
        return self._password_hash == self._hash_password(password)

