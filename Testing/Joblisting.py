import random

class JobListing:
    def __init__(self, title, salary, location, employer_id, company_name):
        # Generate a simple 4-digit unique ID for the listing
        self.job_id = random.randint(1000, 9999)
        self.title = title
        self.salary = salary
        self.location = location
        self.employer_id = employer_id
        self.company_name = company_name
        self.applications = []  # List to store applications for this job

    def display_info(self):
        """Returns a single line summary of the job listing."""
        return f"ID: {self.job_id} | {self.title} at {self.company_name} | Salary: KES {self.salary}"

    def view_applications(self):
        """Displays all applications submitted for this specific job listing."""
        if not self.applications:
            print(f"\nNo applications found for Job ID: {self.job_id}")
            return []

        print(f"\n--- Applications for {self.title} (ID: {self.job_id}) ---")
        for index, app in enumerate(self.applications, start=1):
            status = app.get("status", "Pending")
            applicant_name = app.get("applicant_name", "Unknown")
            print(f"{index}. Applicant: {applicant_name} | Status: {status}")

        return self.applications

    def accept_application(self, applicant_identifier):
        """Updates the status of a specific application to 'Accepted'."""
        for app in self.applications:
            if (
                str(app.get("id")) == str(applicant_identifier) 
                or app.get("applicant_name", "").lower() == str(applicant_identifier).lower()
            ):
                app["status"] = "Accepted"
                print(f"\nApplication for {app.get('applicant_name')} has been ACCEPTED!")
                return True

        print(f"\nApplication/Applicant '{applicant_identifier}' not found.")
        return False