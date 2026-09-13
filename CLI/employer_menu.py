import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Models.JobListing import JobListing

def show_employer_menu(current_employer, shared_jobs_db):
    while True:
        print("\n==========================================")
        print(f"       EMPLOYER DASHBOARD - {current_employer.company_name.upper()}")
        print("==========================================")
        print("1. Post a New Job Listing")
        print("2. View My Posted Jobs")
        print("3. Delete a Job Listing")
        print("4. Logout")
        
        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            print("\n--- POST A NEW JOB ---")
            title = input("Enter Job Title: ").strip()
            salary = input("Enter Offered Salary (KES): ").strip()
            location = input("Enter Job Location: ").strip()

            if title and salary and location:
                new_job = JobListing(
                    title=title,
                    salary=salary,
                    location=location,
                    employer_id=current_employer.user_id,
                    company_name=current_employer.company_name
                )
                
                current_employer.post_job(new_job)
                shared_jobs_db.append(new_job)
                
                print(f"\nSuccess: Posted '{title}' in {location} offering KES {salary}.")
            else:
                print("\nError: All fields (Title, Salary, Location) are required!")

        elif choice == "2":
            print("\n--- MY POSTED JOBS ---")
            if not current_employer.my_jobs:
                print("You haven't posted any jobs yet.")
            else:
                for idx, job in enumerate(current_employer.my_jobs, start=1):
                    print(f"{idx}. {job.display_info()}")

        elif choice == "3":
            print("\n--- DELETE A JOB LISTING ---")
            if not current_employer.my_jobs:
                print("No jobs available to delete.")
                continue

            job_id_input = input("Enter Job ID to delete: ").strip()
            
            if not job_id_input.isdigit():
                print("\nError: Please enter a valid numerical Job ID.")
                continue

            job_id = int(job_id_input)
            confirm = input(f"Are you sure you want to delete listing {job_id}? (yes/no): ").strip().lower()

            if confirm == "yes":
                was_deleted = current_employer.delete_job(job_id)
                
                if was_deleted:
                    shared_jobs_db[:] = [j for j in shared_jobs_db if j.job_id != job_id]
                    print(f"\nListing {job_id} deleted successfully by employer.")
                else:
                    print(f"\nError: Could not find a job listing with ID {job_id}.")
            else:
                print("\nDeletion cancelled.")

        elif choice == "4":
            print("\nLogging out... Returning to main menu.")
            break

        else:
            print("\nInvalid choice! Please select between 1 and 4.")
