"""Test the actual authentication CLI parser and command dispatch."""

import sys
import types

module = types.ModuleType("email_validator")

class FakeEmailNotValidError(ValueError):
    pass


def fake_validate_email(email, check_deliverability=True):
    if "@" not in email:
        raise FakeEmailNotValidError("invalid email")
    return types.SimpleNamespace(normalized=email)


module.validate_email = fake_validate_email
module.EmailNotValidError = FakeEmailNotValidError
sys.modules.setdefault("email_validator", module)

from CLI_commands.Auth_CLI import build_parser, run_command


class FakeAuth:
    """Minimal auth stand-in used to test command dispatch."""

    pass


def test_parser_exposes_authentication_subcommands():
    parser = build_parser()

    assert parser.parse_args(["register"]).command == "register"
    assert parser.parse_args(["login"]).command == "login"
    assert parser.parse_args(["interactive"]).command == "interactive"
    assert parser.parse_args([]).command is None


def test_run_command_interactive_routes_to_landing(monkeypatch):
    called = {}

    def fake_landing(auth):
        called["auth"] = auth
        return 0

    monkeypatch.setattr("CLI_commands.Auth_CLI.landing", fake_landing)

    auth = FakeAuth()
    assert run_command("interactive", auth) == 0
    assert called["auth"] is auth


def test_run_command_returns_success_when_login_succeeds(monkeypatch):
    expected_user = object()
    monkeypatch.setattr("CLI_commands.Auth_CLI.login", lambda auth: expected_user)

    assert run_command("login", FakeAuth()) == 0


def test_run_command_returns_failure_when_register_is_cancelled(monkeypatch):
    monkeypatch.setattr("CLI_commands.Auth_CLI.register", lambda auth: None)

    assert run_command("register", FakeAuth()) == 1


def test_run_command_returns_failure_when_login_fails(monkeypatch):
    monkeypatch.setattr("CLI_commands.Auth_CLI.login", lambda auth: None)

    assert run_command("login", FakeAuth()) == 1