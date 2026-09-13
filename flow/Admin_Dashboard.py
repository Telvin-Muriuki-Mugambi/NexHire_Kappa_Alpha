from Models.Admin import AdminManager


def main(auth=None):
    if auth is None:
        raise ValueError("An authenticated admin user is required.")

    if auth.current_user is None or str(getattr(auth.current_user, "role", "")).upper() != "ADMIN":
        raise PermissionError("This account does not have admin privileges.")

    manager = AdminManager()

    while True:
        print("\n=== NexHire Admin Dashboard ===")
        print("1. List users")
        print("2. Create user")
        print("3. Delete user")
        print("4. Review pending jobs")
        print("5. Approve job")
        print("6. Post opportunity")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().upper()

        if choice == "Q":
            print("Returning to the app.")
            return 0

        if choice == "1":
            users = manager.manage_user("list")
            print(f"\n--- Registered Users ({len(users)}) ---")
            for user in users:
                print(f"ID: {user.get('user_id')} | Name: {user.get('username', user.get('name'))} | Email: {user.get('email')} | Phone Number: {user.get('phone')} | Role: {user.get('role')}")

        elif choice == "2":
            name = input("Username: ").strip()
            email = input("Email address: ").strip()
            phone = input("Phone Number: ").strip()
            role = input("Role (JOB_SEEKER / EMPLOYER / ADMIN): ").strip().upper()
            created = manager.manage_user("create", username=name, email = email, phone = phone, role=role)
            print(f"User created successfully! ID: {created['user_id']}")

        elif choice == "3":
            user_id = input("User ID to delete: ").strip()
            manager.manage_user("delete", user_id=user_id)
            print("User deletion attempted.")

        elif choice == "4":
            pending_jobs = manager.review_opportunity(auth.current_user)
            print(f"\n--- Pending Jobs ({len(pending_jobs)}) ---")
            for job in pending_jobs:
                print(f"ID: {job.get('job_id')} | Title: {job.get('title')} | Company: {job.get('company')}")

        elif choice == "5":
            job_id = input("Job ID to approve: ").strip()
            success = manager.approve_job(job_id, auth.current_user)
            print("Job successfully approved!" if success else "Approval failed or job already approved.")

        elif choice == "6":
            title = input("Job title: ").strip()
            description = input("Job description: ").strip()
            company = input("Company: ").strip()
            job = manager.post_opportunity(
                title=title,
                description=description,
                company=company,
                admin_id=str(auth.current_user.user_id),
            )
            print(f"Opportunity posted successfully! ID: {job['job_id']} [Status: {job['status']}]")

        else:
            print("Please choose one of the listed options.")
