import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Models.User import User

class Employer(User):
    def __init__(self, name, email, phone, password, company_name=None):
        super().__init__(name, email, phone, password)
        self.role = "employer"
        self.company_name = company_name if company_name else name
        self.my_jobs = []

    def post_job(self, job_listing):
        self.my_jobs.append(job_listing)

    def delete_job(self, job_id):
        initial_count = len(self.my_jobs)
        self.my_jobs = [job for job in self.my_jobs if job.job_id != job_id]
        return len(self.my_jobs) < initial_count
