import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Models.Employer import Employer
from Models.JobListing import JobListing


def show_employer_menu(auth=None):
    if auth is None:
        raise ValueError("An authenticated employer user is required.")

    current_employer = auth.current_user
    if current_employer is None or str(getattr(current_employer, "role", "")).upper() != "EMPLOYER":
        raise PermissionError("This account does not have employer privileges.")

    employer = Employer(
        current_employer.name,
        current_employer.email,
        current_employer.phone_number,
        "",
        company_name=getattr(current_employer, "company_name", current_employer.name),
        data_manager=auth.data_manager,
        user_id=current_employer.user_id,
    )

    while True:
        print("\n=== NexHire Employer Dashboard ===")
        print(f"Employer: {employer.company_name}")
        print("1. View my jobs")
        print("2. Post a job")
        print("3. View Applicants")
        print("4. View profile")
        print("5. Delete a job")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().upper()

        if choice == "Q":
            print("Returning to the app.")
            return 0

        if choice == "1":
            employer.load_jobs()
            if not employer.my_jobs:
                print("You have not posted any jobs yet.")
            for job in employer.my_jobs:
                print(job.display_info())
        elif choice == "2":
            title = input("Job title: ").strip()
            description = input("Job description: ").strip()
            location = input("Location: ").strip()
            skills = [skill.strip() for skill in input("Skills (comma-separated): ").split(",") if skill.strip()]
            pay_rate = input("Pay rate. Kindly do not use commas: ").strip()
            experience_level = input("Experience level (entry/mid/senior): ").strip()
            availability = input("Availability: ").strip()

            try:
                job = JobListing(
                    title,
                    description,
                    location,
                    skills,
                    float(pay_rate),
                    experience_level,
                    availability,
                )
                employer.post_job(job)
                print(f"Job posted successfully. ID: {job.job_id}")
            except (ValueError, TypeError) as error:
                print(f"Unable to post job: {error}")
        elif choice == "4":
            print(f"Profile: {current_employer.name} | {current_employer.email} | {current_employer.phone_number}")
        elif choice == "5":
            job_id = input("Job ID to delete: ").strip()
            if employer.delete_job(job_id):
                print("Job deleted successfully.")
            else:
                print("That job was not found in your listings.")
        else:
            print("Please choose one of the listed options.")
