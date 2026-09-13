import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Models.Auth import Auth
from Models.DataManager import DataManager

from flow.Landing import landing
from flow.Login import login
from flow.Register import register

#Commands the user can interact with for assistance
COMMANDS = ("interactive", "register", "login")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="nexhire",
        description="Connect young talent to opportunity.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.add_parser("interactive", help="Open the guided menu")
    subparsers.add_parser("register", help="Register a new account")
    subparsers.add_parser("login", help="Sign in to an existing account")
    return parser


def create_auth(data_dir=None):
    data_path = Path(data_dir) if data_dir else Path(__file__).resolve().parents[1] / "Data"
    return Auth(DataManager(data_path))


def run_command(command, auth):
    if command == "interactive":
        landing(auth)
        return 0

    user = register(auth) if command == "register" else login(auth)
    return 0 if user is not None else 1


def run_cli(argv=None, data_dir=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    auth = create_auth(data_dir)

    try:
        return run_command(args.command or "interactive", auth)
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Goodbye.")
        return 130


__all__ = ["build_parser", "create_auth", "run_cli", "run_command"]
