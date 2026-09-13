import argparse
from Models.Admin import AdminManager

def main():
    parser = argparse.ArgumentParser(description="NexHire Kappa Alpha CLI Interface")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Users command parser
    users_parser = subparsers.add_parser("users", help="Manage users")
    users_parser.add_argument("action", choices=["list", "create", "delete"], help="Action to perform")
    users_parser.add_argument("--id", help="User UUID (required for delete)")
    users_parser.add_argument("--username", help="Username (required for create)")
    users_parser.add_argument("--role", help="User role (required for create)")

    # Jobs command parser
    jobs_parser = subparsers.add_parser("jobs", help="Manage and verify jobs")
    jobs_parser.add_argument("action", choices=["review", "approve", "post"], help="Action to perform")
    jobs_parser.add_argument("--id", help="Job UUID (required for approve)")
    jobs_parser.add_argument("--title", help="Job title (required for post)")
    jobs_parser.add_argument("--description", help="Job description (required for post)")
    jobs_parser.add_argument("--company", help="Company name (required for post)")
    jobs_parser.add_argument("--admin-id", help="Admin UUID (required for post)")

    args = parser.parse_args()
    manager = AdminManager()
    dummy_admin = {"role": "admin"}

    if args.command == "users":
        if args.action == "list":
            users = manager.manage_user("list")
            print(f"\n--- Registered Users ({len(users)}) ---")
            for u in users:
                print(f"ID: {u.get('user_id')} | Name: {u.get('username')} | Role: {u.get('role')}")
        
        elif args.action == "create":
            if not args.username or not args.role:
                print("Error: --username and --role are required to create a user.")
                return
            created = manager.manage_user("create", username=args.username, role=args.role)
            print(f"User created successfully! ID: {created['user_id']}")
        
        elif args.action == "delete":
            if not args.id:
                print("Error: --id is required to delete a user.")
                return
            success = manager.manage_user("delete", user_id=args.id)
            print(f"User deleted: {success}")

    elif args.command == "jobs":
        if args.action == "review":
            try:
                pending_jobs = manager.review_opportunity(dummy_admin)
                print(f"\n--- Pending Jobs ({len(pending_jobs)}) ---")
                for j in pending_jobs:
                    print(f"ID: {j.get('job_id')} | Title: {j.get('title')} | Company: {j.get('company')} | Status: {j.get('status')}")
            except PermissionError as e:
                print(f"Permission Error: {e}")
        
        elif args.action == "approve":
            if not args.id:
                print("Error: --id is required to approve a job.")
                return
            try:
                success = manager.approve_job(args.id, dummy_admin)
                if success:
                    print("Job successfully approved!")
                else:
                    print("Approval failed, skipped, or job already approved.")
            except PermissionError as e:
                print(f"Permission Error: {e}")

        elif args.action == "post":
            if not all([args.title, args.description, args.company, args.admin_id]):
                print("Error: --title, --description, --company, and --admin-id are required to post a job.")
                return
            job = manager.post_opportunity(
                title=args.title,
                description=args.description,
                company=args.company,
                admin_id=args.admin_id
            )
            print(f"Opportunity posted successfully! ID: {job['job_id']} [Status: {job['status']}]")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
