import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Models.Admin import AdminManager
from Models.Auth import Auth, AuthorizationError
from Models.DataManager import DataManager



def main(auth=None):
    parser = argparse.ArgumentParser(description="NexHire Kappa Alpha CLI Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    users_parser = subparsers.add_parser("users", help="Manage users")
    users_parser.add_argument("action", choices=["list", "create", "delete"], help="Action to perform")
    users_parser.add_argument("--id", help="User UUID (required for delete)")
    users_parser.add_argument("--username", help="Username (required for create)")
    users_parser.add_argument("--role", help="User role (required for create)")

    jobs_parser = subparsers.add_parser("jobs", help="Manage and verify jobs")
    jobs_parser.add_argument("action", choices=["review", "approve", "post"], help="Action to perform")
    jobs_parser.add_argument("--id", help="Job UUID (required for approve)")
    jobs_parser.add_argument("--title", help="Job title (required for post)")
    jobs_parser.add_argument("--description", help="Job description (required for post)")
    jobs_parser.add_argument("--company", help="Company name (required for post)")
    jobs_parser.add_argument("--admin-id", help="Admin UUID (required for post)")

    args = parser.parse_args()

    if auth is None:
        print("Permission Error: No authenticated admin user is available.")
        return 1

    if not isinstance(auth, Auth):
        print("Permission Error: No authenticated admin user is available.")
        return 1

    if auth.current_user is None or getattr(auth.current_user, "role", "").upper() != "ADMIN":
        print("Permission Error: This account does not have admin privileges.")
        return 1

    manager = AdminManager()

    if args.command == "users":
        if args.action == "list":
            users = manager.manage_user("list")
            print(f"\n--- Registered Users ({len(users)}) ---")
            for user in users:
                print(f"ID: {user.get('user_id')} | Name: {user.get('username', user.get('name'))} | Role: {user.get('role')}")
        elif args.action == "create":
            if not args.username or not args.role:
                print("Error: --username and --role are required to create a user.")
                return 1
            created = manager.manage_user("create", username=args.username, role=args.role)
            print(f"User created successfully! ID: {created['user_id']}")
        elif args.action == "delete":
            if not args.id:
                print("Error: --id is required to delete a user.")
                return 1
            success = manager.manage_user("delete", user_id=args.id)
            print(f"User deleted: {success}")

    elif args.command == "jobs":
        if args.action == "review":
            try:
                pending_jobs = manager.review_opportunity(auth.current_user)
                print(f"\n--- Pending Jobs ({len(pending_jobs)}) ---")
                for job in pending_jobs:
                    print(f"ID: {job.get('job_id')} | Title: {job.get('title')} | Company: {job.get('company')}")
            except PermissionError as exc:
                print(f"Permission Error: {exc}")
        elif args.action == "approve":
            if not args.id:
                print("Error: --id is required to approve a job.")
                return 1
            try:
                success = manager.approve_job(args.id, auth.current_user)
                if success:
                    print("Job successfully approved!")
                else:
                    print("Approval failed, skipped, or job already approved.")
            except PermissionError as exc:
                print(f"Permission Error: {exc}")
        elif args.action == "post":
            if not all([args.title, args.description, args.company, args.admin_id]):
                print("Error: --title, --description, --company, and --admin-id are required to post a job.")
                return 1
            job = manager.post_opportunity(title=args.title, description=args.description, company=args.company, admin_id=args.admin_id)
            print(f"Opportunity posted successfully! ID: {job['job_id']} [Status: {job['status']}]")
    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())