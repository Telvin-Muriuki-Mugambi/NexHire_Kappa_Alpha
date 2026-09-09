import pytest
from Models.Auth import Auth, AuthenticationError, AuthorizationError, DuplicateEmailError


@pytest.fixture
def auth():
    return Auth()


def register_user(auth, role="JOB_SEEKER"):
    return auth.register("Ada", "ada@example.com", "0712345678", "secret", role)


