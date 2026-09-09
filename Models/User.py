import hashlib

class User:
    def __init__(self, user_id, name, email, phone, role, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone_number = phone
        self.role = role
        self._password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._password_hash == self._hash_password(password)