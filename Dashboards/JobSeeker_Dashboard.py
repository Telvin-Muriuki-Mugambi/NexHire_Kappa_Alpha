"""Interactive dashboard for viewing and applying to approved jobs."""

from Models.jobseeker import JobSeeker


def show_jobseeker_menu(auth=None):
    """Display job-seeker actions for the authenticated job seeker."""
    if auth is None:
        raise ValueError("An authenticated job seeker user is required.")

    if auth.current_user is None or str(getattr(auth.current_user, "role", "")).upper() != "JOB_SEEKER":
        raise PermissionError("This account does not have job seeker privileges.")

    seeker = JobSeeker(
        auth.data_manager,
        auth.current_user.user_id,
        auth.current_user.name,
        getattr(auth.current_user, "cv", None),
    )

    while True:
        print("\n=== NexHire Job Seeker Dashboard ===")
        print("1. View jobs")
        print("2. Apply for a job")
        print("3. Search for a job")
        print("4. View profile")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().upper()

        if choice == "Q":
            print("Returning to the app.")
            return 0

        if choice == "1":
            jobs = seeker.available_jobs()
            if not jobs:
                print("There are no approved jobs available.")
            for job in jobs:
                print(job.display_info())

        elif choice == "2":
            job_id = input("Enter the job ID to apply for: ").strip()
            try:
                applied_id = seeker.apply_job(job_id)
                print(f"Application submitted for job {applied_id}.")
            except ValueError as error:
                print(error)

        elif choice == "3":
            keyword = input("Search by keyword: ").strip()
            matches = seeker.search_jobs(keyword)
            if not matches:
                print("No approved jobs matched your search.")
            for job in matches:
                print(JobSeeker._as_dict(job))

        elif choice == "4":
            user = auth.current_user
            print(f"Profile: {user.name} | {user.email} | {user.phone_number}")
        else:
            print("Please choose one of the listed options.")
