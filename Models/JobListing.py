"""Define the validated job listing domain object and its filters."""

import random


class JobListing:
    """Represent a job opportunity with status, ownership, and search metadata."""

    def __init__(
        self,
        title,
        description="",
        location="",
        skills=None,
        pay_rate=0,
        experience_level="entry",
        availability="FULL_TIME",
        job_id=None,
        status="PENDING",
        employer_id=None,
        company_name=None,
        salary=None,
    ):
        """Create a listing while validating pay and experience-level values."""
        if isinstance(pay_rate, str) and not isinstance(skills, (list, tuple)):
            salary = description
            employer_id = skills
            company_name = pay_rate
            description = ""
            skills = []
        if salary is not None:
            pay_rate = salary
        if isinstance(pay_rate, str):
            pay_rate = float(pay_rate)
        if pay_rate < 0:
            raise ValueError("pay_rate cannot be negative")
        if experience_level.lower() not in {"entry", "mid", "senior"}:
            raise ValueError("invalid experience level")
        self.job_id = job_id if job_id is not None else random.randint(1000, 9999)
        self.title = title
        self.description = description
        self.location = location
        self.skills = skills or []
        self.pay_rate = pay_rate
        self.experience_level = experience_level
        self.availability = availability
        self.status = status
        self.employer_id = employer_id
        self.company_name = company_name or ""

    @property
    def salary(self):
        """Return the pay rate using the legacy salary property name."""
        return self.pay_rate

    def display_info(self):
        """Return a concise human-readable summary of the listing."""
        company = f" at {self.company_name}" if self.company_name else ""
        return f"ID: {self.job_id} | {self.title}{company} | Salary: KES {self.pay_rate} | Location: {self.location}"


    def approve(self):
        """Mark the listing as approved for job-seeker visibility."""
        self.status = "APPROVED"


    def reject(self):
        """Mark the listing as rejected."""
        self.status = "REJECTED"


    def matches_criteria(self, filters):
        """Return whether the listing satisfies the supplied search filters."""
        if "location" in filters and filters["location"].lower() not in self.location.lower():
            return False
        if "skills" in filters:
            listing_skills = {skill.lower() for skill in self.skills}
            if not all(skill.lower() in listing_skills for skill in filters["skills"]):
                return False
        if "min_pay" in filters and self.pay_rate < filters["min_pay"]:
            return False
        if "availability" in filters and self.availability.lower() != filters["availability"].lower():
            return False
        return True


    def to_dict(self):
        """Serialize the listing into a JSON-compatible dictionary."""
        return {
            "job_id": self.job_id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "skills": self.skills,
            "pay_rate": self.pay_rate,
            "experience_level": self.experience_level,
            "availability": self.availability,
            "status": self.status,
            "employer_id": self.employer_id,
            "company_name": self.company_name,
        }


    @classmethod
    def from_dict(cls, record):
        """Recreate a listing from a stored JSON-compatible dictionary."""
        return cls(
            record["title"],
            record.get("description", ""),
            record.get("location", ""),
            record.get("skills", []),
            record.get("pay_rate", record.get("salary", 0)),
            record.get("experience_level", "entry"),
            record.get("availability", "FULL_TIME"),
            job_id=record.get("job_id"),
            status=record.get("status", "PENDING"),
            employer_id=record.get("employer_id"),
            company_name=record.get("company_name", record.get("company", "")),
        )

    @staticmethod
    def load_jobs(data_manager=None):
        """Load listings through a validated DataManager instance."""
        if data_manager is None:
            raise ValueError("A DataManager instance is required to load job listings.")
        from Models.DataManager import DataManager
        if not isinstance(data_manager, DataManager):
            raise TypeError("data_manager must be a DataManager instance.")
        return data_manager.load_jobs()

    def save(self, data_manager):
        """Persist this listing through a validated DataManager instance."""
        from Models.DataManager import DataManager
        if not isinstance(data_manager, DataManager):
            raise TypeError("data_manager must be a DataManager instance.")
        data_manager.save_job(self)

