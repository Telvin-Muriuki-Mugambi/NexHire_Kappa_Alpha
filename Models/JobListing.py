import random

class JobListing:
    def __init__(self, title, salary, location, employer_id, company_name):
        self.job_id = random.randint(1000, 9999)
        self.title = title
        self.salary = salary
        self.location = location
        self.employer_id = employer_id
        self.company_name = company_name

    def display_info(self):
        return f"ID: {self.job_id} | {self.title} at {self.company_name} | Salary: KES {self.salary} | Location: {self.location}"
