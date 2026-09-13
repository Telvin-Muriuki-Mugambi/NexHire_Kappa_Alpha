"""Define administrator users and persistence-backed admin management actions."""

import json
import os
import uuid
import random
from pathlib import Path

from Models.DataManager import DataManager
from Models.User import User


class Admin(User):
    """User subclass with admin-level permissions and role-aware access."""

    def __init__(self, name, email, phone, password, user_id=None):
        super().__init__(name, email, phone, password, user_id=user_id)
        self.role = "ADMIN"

    def is_admin(self):
        """Return whether this user has administrator privileges."""
        return True


class BaseManager:
    """Provide shared JSON file-management utilities for administrative services."""
    USERS_FILE = "Data/users.json"
    JOBS_FILE = "Data/jobs.json"

    def __init__(self, data_dir=None):
        base_dir = Path(data_dir) if data_dir is not None else Path(self.USERS_FILE).parent
        self.data_manager = DataManager(base_dir)
        self.USERS_FILE = str(self.data_manager.users_file)
        self.JOBS_FILE = str(self.data_manager.jobs_file)

    def get_manager_description(self):
        """Return a human-readable description of this manager type."""
        return "Base Data Manager System"

    def _ensure_file_exists(self, file_path):
        directory = os.path.dirname(str(file_path))
        if directory:
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump([], file)

    def _load_data(self, file_path):
        self._ensure_file_exists(file_path)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def _save_data(self, file_path, data):
        self._ensure_file_exists(file_path)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)


class AdminManager(BaseManager):
    """Authorize admin operations over users and job opportunities."""
    USERS_FILE = "Data/users.json"
    JOBS_FILE = "Data/jobs.json"

    def get_manager_description(self):
        """Return the admin manager's human-readable description."""
        return "Admin-Level Security and Opportunity Manager"

    @classmethod
    def get_default_paths(cls):
        return {
            "users_path": cls.USERS_FILE,
            "jobs_path": cls.JOBS_FILE,
        }

    def _check_admin(self, user):
        """Raise PermissionError unless the supplied user has the ADMIN role."""
        if hasattr(user, "role"):
            role = str(user.role).upper()
            if role == "ADMIN":
                return
        if isinstance(user, dict):
            role = str(user.get("role", "")).upper()
            if role == "ADMIN":
                return
        raise PermissionError("User does not have admin privileges.")

    def manage_user(self, action, user_id=None, **user_data):
        """Create, read, update, or delete user records for admin workflows."""
        users = self._load_data(self.USERS_FILE)

        if action == "create":
            user = {"user_id": str(random.randint(1000, 9999)), **user_data}
            users.append(user)
            self._save_data(self.USERS_FILE, users)
            return user

        if action in {"read", "list"}:
            if user_id is None:
                return users
            target_id = str(user_id)
            return next((user for user in users if str(user.get("user_id")) == target_id), None)

        if action == "update":
            if user_id is None:
                return None
            target_id = str(user_id)
            for user in users:
                if str(user.get("user_id")) == target_id:
                    user.update(user_data)
                    self._save_data(self.USERS_FILE, users)
                    return user
            return None

        if action == "delete":
            target_id = str(user_id)
            remaining = [user for user in users if str(user.get("user_id")) != target_id]
            self._save_data(self.USERS_FILE, remaining)
            return len(remaining) < len(users)

        raise ValueError(f"Unsupported user action: {action}")

    def post_opportunity(
        self,
        title,
        description,
        company,
        admin_id,
        status="pending",
    ):
        """Create and persist a pending opportunity posted by an administrator."""
        if "=" in status:
            status = status.split("=", 1)[1]

        from Models.JobListing import JobListing

        job = JobListing(
            title=title,
            description=description,
            location="Not specified",
            skills=[],
            pay_rate=0,
            experience_level="entry",
            availability="FULL_TIME",
            job_id=str(uuid.uuid4()),
            status=status.upper(),
            employer_id=admin_id,
            company_name=company,
        )
        self.data_manager.save_job(job)
        return job.to_dict()

    post_opportinity = post_opportunity

    def review_opportunity(self, user):
        """Return pending opportunities after verifying administrator access."""
        self._check_admin(user)
        jobs = self.data_manager.load_jobs()
        return [
            job.to_dict() for job in jobs
            if str(job.status).upper() == "PENDING"
        ]

    def approve_job(self, job_id, user):
        """Confirm and persist approval for a pending job listing."""
        self._check_admin(user)
        job = self.data_manager.get_job_by_id(job_id)

        if job is None or str(job.status).upper() == "APPROVED":
            return False

        confirmation = input("Approve this listing? (yes/no): ")

        if confirmation.strip().lower() in {"y", "yes"}:
            job.approve()
            self.data_manager.save_job(job)
            return True

        return False