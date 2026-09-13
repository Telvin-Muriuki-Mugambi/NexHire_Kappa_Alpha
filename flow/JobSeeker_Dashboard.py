def main(auth=None):
    if auth is None:
        raise ValueError("An authenticated job seeker user is required.")

    if auth.current_user is None or str(getattr(auth.current_user, "role", "")).upper() != "JOB_SEEKER":
        raise PermissionError("This account does not have job seeker privileges.")

    while True:
        print("\n=== NexHire Job Seeker Dashboard ===")
        print("1. View jobs")
        print("2. Apply for a job")
        print("3. View profile")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().upper()

        if choice == "Q":
            print("Returning to the app.")
            return 0

        if choice == "1":
            print("Showing available jobs...")
        elif choice == "2":
            print("Application flow goes here.")
        elif choice == "3":
            user = auth.current_user
            print(f"Profile: {user.name} | {user.email} | {user.phone_number}")
        else:
            print("Please choose one of the listed options.")
