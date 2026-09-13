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
from CLI_commands.Admin_CLI import main as admin_main
from CLI_commands.Employer_CLI import main as employer_main
from CLI_commands.jobseekercli import main as jobseeker_main


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


def test_employer_main_prompts_for_interactive_when_no_command_is_given(monkeypatch):
    class FakeLoggedInEmployer:
        role = "EMPLOYER"
        name = "Acme"
        email = "employer@example.com"
        phone_number = "123456"
        company_name = "Acme Inc"
        user_id = "emp-1"

    class FakeAuth:
        def __init__(self):
            self.current_user = FakeLoggedInEmployer()

        def has_role(self, role):
            return getattr(self.current_user, "role", "") == role

    accessed = {}

    monkeypatch.setattr("builtins.input", lambda prompt="": "interactive")
    monkeypatch.setattr("CLI_commands.Employer_CLI.create_auth", lambda data_dir=None: FakeAuth())
    monkeypatch.setattr("CLI_commands.Employer_CLI.login", lambda auth: auth.current_user)
    def fake_show_employer_menu(auth):
        accessed["menu"] = True
        return 0

    monkeypatch.setattr("CLI_commands.Employer_CLI.show_employer_menu", fake_show_employer_menu)

    assert employer_main([]) == 0
    assert accessed.get("menu") is True


def test_admin_main_routes_to_dashboard_for_interactive_launch(monkeypatch):
    class FakeLoggedInAdmin:
        role = "ADMIN"
        name = "Admin User"
        email = "admin@example.com"
        phone_number = "123456"
        user_id = "admin-1"

    class FakeAuth:
        def __init__(self):
            self.current_user = FakeLoggedInAdmin()

        def has_role(self, role):
            return getattr(self.current_user, "role", "") == role

    accessed = {}

    monkeypatch.setattr("builtins.input", lambda prompt="": "interactive")
    monkeypatch.setattr("CLI_commands.Admin_CLI.create_auth", lambda data_dir=None: FakeAuth())
    monkeypatch.setattr("CLI_commands.Admin_CLI.login", lambda auth: auth.current_user)

    def fake_show_admin_menu(auth):
        accessed["menu"] = True
        return 0

    monkeypatch.setattr("CLI_commands.Admin_CLI.show_admin_menu", fake_show_admin_menu)

    assert admin_main([]) == 0
    assert accessed.get("menu") is True


def test_jobseeker_main_routes_to_dashboard_for_interactive_launch(monkeypatch):
    class FakeLoggedInJobSeeker:
        role = "JOB_SEEKER"
        name = "Jane Doe"
        email = "jane@example.com"
        phone_number = "123456"
        user_id = "user-1"
        cv = "/tmp/jane_cv.pdf"

    class FakeAuth:
        def __init__(self):
            self.current_user = FakeLoggedInJobSeeker()

        def has_role(self, role):
            return getattr(self.current_user, "role", "") == role

    accessed = {}

    monkeypatch.setattr("builtins.input", lambda prompt="": "interactive")
    monkeypatch.setattr("CLI_commands.jobseekercli.create_auth", lambda data_dir=None: FakeAuth())
    monkeypatch.setattr("CLI_commands.jobseekercli.login", lambda auth: auth.current_user)
    def fake_show_jobseeker_menu(auth):
        accessed["menu"] = True
        return 0

    monkeypatch.setattr("CLI_commands.jobseekercli.show_jobseeker_menu", fake_show_jobseeker_menu)

    assert jobseeker_main([]) == 0
    assert accessed.get("menu") is True