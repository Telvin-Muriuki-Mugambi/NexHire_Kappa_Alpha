from flow.CLI import build_parser, run_command


class FakeAuth:
    pass


def test_parser_exposes_authentication_subcommands():
    parser = build_parser()

    assert parser.parse_args(["register"]).command == "register"
    assert parser.parse_args(["login"]).command == "login"
    assert parser.parse_args(["interactive"]).command == "interactive"
    assert parser.parse_args([]).command is None


def test_run_command_returns_success_when_user_flow_succeeds(monkeypatch):
    expected_user = object()
    monkeypatch.setattr("flow.CLI.login", lambda auth: expected_user)

    assert run_command("login", FakeAuth()) == 0


def test_run_command_returns_failure_when_user_flow_is_cancelled(monkeypatch):
    monkeypatch.setattr("flow.CLI.register", lambda auth: None)

    assert run_command("register", FakeAuth()) == 1