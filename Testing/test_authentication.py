import pytest
from Models.Auth import Auth, AuthenticationError, AuthorizationError, DuplicateEmailError


@pytest.fixture
def auth():
    return Auth()


def register_user(auth, role="JOB_SEEKER"):
    return auth.register("Ada", "ada@example.com", "0712345678", "secret", role)

#Tests to see if the password is hashed before storing
def test_register_hashes_password_before_storing(auth):
    user = register_user(auth)

    assert user._password_hash != "secret"
    assert user.verify_password("secret")

#Tests to see if the login returns a registered user and is set as the current user
def test_login_returns_user_and_sets_current_user(auth):
    user = register_user(auth)

    assert auth.login("ada@example.com", "secret") is user
    assert auth.current_user is user

#Tests whether the user is cleared and logged out
def test_logout_clears_current_user(auth):
    register_user(auth)
    auth.login("ada@example.com", "secret")

    auth.logout()

    assert auth.current_user is None

#Test to ensure that emails remain unique and is not duplicated
def test_duplicate_email_is_rejected(auth):
    register_user(auth)

    with pytest.raises(DuplicateEmailError):
        register_user(auth)