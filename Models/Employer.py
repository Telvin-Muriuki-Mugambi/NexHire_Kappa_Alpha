"""Represent employers and their DataManager-backed job listings."""

from Models.DataManager import DataManager
from Models.JobListing import JobListing
from Models.User import User


class Employer(User):
    """Extend User with company identity and employer job-management actions."""

    def __init__(self, name, email, phone, password, company_name=None, data_manager=None, user_id=None):
        """Initialize an employer and load the employer's persisted jobs."""
        super().__init__(name, email, phone, password, user_id=user_id)
        self.role = "EMPLOYER"
        self.company_name = company_name if company_name else name
        self.data_manager = data_manager
        self.my_jobs = []
        self.load_jobs()

    def post_job(self, job_listing):
        """Assign ownership, persist a JobListing, and refresh employer jobs."""
        if not isinstance(job_listing, JobListing):
            raise TypeError("job_listing must be a JobListing instance")
        job_listing.employer_id = self.user_id
        job_listing.company_name = self.company_name
        if self.data_manager is not None:
            self.data_manager.save_job(job_listing)
        self.load_jobs()
        return job_listing

    def load_jobs(self):
        """Load only the job listings owned by this employer."""
        if self.data_manager is None:
            self.my_jobs = []
        else:
            self.my_jobs = [
                job for job in self.data_manager.load_jobs()
                if str(job.employer_id) == str(self.user_id)
            ]
        return self.my_jobs

    def delete_job(self, job_id):
        """Delete an owned job from persistence and report success."""
        self.load_jobs()
        owned_job = next(
            (job for job in self.my_jobs if str(job.job_id) == str(job_id)),
            None,
        )
        if owned_job is None:
            return False
        if self.data_manager is not None:
            deleted = self.data_manager.delete_job(owned_job.job_id)
            self.load_jobs()
            return deleted
        self.my_jobs.remove(owned_job)
        return True
