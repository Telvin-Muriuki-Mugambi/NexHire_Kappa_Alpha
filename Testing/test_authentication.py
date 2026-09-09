import pytest
from Models.Auth import Auth, AuthenticationError, AuthorizationError, DuplicateEmailError


@pytest.fixture
def auth():
    return Auth()


def register_user(auth, role="JOB_SEEKER"):
    return auth.register("Ada", "ada@example.com", "0712345678", "secret", role)

def test_register_hashes_password_before_storing(auth):
    user = register_user(auth)

    assert user._password_hash != "secret"
    assert user.verify_password("secret")

def test_login_returns_user_and_sets_current_user(auth):
    user = register_user(auth)

    assert auth.login("ada@example.com", "secret") is user
    assert auth.current_user is user
