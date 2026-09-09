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

#Test to see if the admin is recognized as a role
def test_admin_role_is_recognized(auth):
    register_user(auth, "ADMIN")
    auth.login("ada@example.com", "secret")

    assert auth.is_admin()

#Test invalid logins are rejected. Used parametrized testing to test multiple entries
@pytest.mark.parametrize("email,password", [("missing@example.com", "secret"), ("ada@example.com", "wrong")])
def test_invalid_login_is_rejected(auth, email, password):
    register_user(auth)

    with pytest.raises(AuthenticationError):
        auth.login(email, password)

    assert auth.current_user is None

#Test if an action requires a specific role 
def test_protected_action_requires_a_logged_in_user(auth):
    with pytest.raises(AuthorizationError):
        auth.require_role("EMPLOYER")

#Test the action rejects the wrong role
def test_protected_action_rejects_the_wrong_role(auth):
    register_user(auth, "JOB_SEEKER")
    auth.login("ada@example.com", "secret")

    with pytest.raises(AuthorizationError):
        auth.require_role("EMPLOYER")

def test_role_helpers_support_admin_employer_and_job_seeker(auth):
    register_user(auth, "EMPLOYER")
    auth.login("ada@example.com", "secret")

    assert auth.has_role("employer")
    assert not auth.is_admin()