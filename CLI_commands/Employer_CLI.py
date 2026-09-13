import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Models.Auth import Auth, AuthenticationError
from Models.DataManager import DataManager
from flow.Login import login
from Dashboards.Employer_Menu import show_employer_menu


def create_auth(data_dir=None):
    data_path = Path(data_dir) if data_dir else PROJECT_ROOT / "Data"
    return Auth(DataManager(data_path))


def build_parser():
    parser = argparse.ArgumentParser(
        prog="nexhire-employer",
        description="NexHire employer command interface.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("interactive", help="Log in and open the employer dashboard")
    subparsers.add_parser("help", help="Show employer command help")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command in {None, "help"}:
        build_parser().print_help()
        return 0

    auth = create_auth()
    try:
        if login(auth) is None:
            return 1
        if not auth.has_role("EMPLOYER"):
            print("This account does not have employer privileges.")
            return 1
        return show_employer_menu(auth)
    except (AuthenticationError, EOFError, KeyboardInterrupt):
        print("\nEmployer session ended.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())