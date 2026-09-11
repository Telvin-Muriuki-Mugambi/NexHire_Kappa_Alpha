import json
import os
import uuid

class BaseManager:
    USERS_FILE = "Data/users.json"
    JOBS_FILE = "Data/jobs.json"

    def get_manager_description(self):
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
    USERS_FILE = "Data/users.json"
    JOBS_FILE = "Data/jobs.json"

    def get_manager_description(self):
        return "Admin-Level Security and Opportunity Manager"

    @classmethod
    def get_default_paths(cls):
        return {
            "users_path": cls.USERS_FILE,
            "jobs_path": cls.JOBS_FILE,
        }

    def _check_admin(self, user):
        if str(user.get("role", "")).lower() != "admin":
            raise PermissionError("User does not have admin privileges.")

    def manage_user(self, action, user_id=None, **user_data):
        users = self._load_data(self.USERS_FILE)

        if action == "create":
            user = {"user_id": str(uuid.uuid4()), **user_data}
            users.append(user)
            self._save_data(self.USERS_FILE, users)
            return user

        if action in {"read", "list"}:
            if user_id is None:
                return users
            return next(
                (user for user in users if user.get("user_id") == user_id),
                None,
            )

        if action == "update":
            user = next(
                (user for user in users if user.get("user_id") == user_id),
                None,
            )
            if user is None:
                return None

            user.update(user_data)
            self._save_data(self.USERS_FILE, users)
            return user

        if action == "delete":
            remaining = [
                user for user in users
                if user.get("user_id") != user_id
            ]
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
        jobs = self._load_data(self.JOBS_FILE)

        if "=" in status:
            status = status.split("=", 1)[1]

        job = {
            "job_id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "company": company,
            "admin_id": admin_id,
            "status": status.upper(),
        }

        jobs.append(job)
        self._save_data(self.JOBS_FILE, jobs)
        return job

    post_opportinity = post_opportunity

    def review_opportunity(self, user):
        self._check_admin(user)
        jobs = self._load_data(self.JOBS_FILE)
        return [
            job for job in jobs
            if job.get("status", "").upper() == "PENDING"
        ]

    def approve_job(self, job_id, user):
        self._check_admin(user)
        jobs = self._load_data(self.JOBS_FILE)

        job = next(
            (item for item in jobs if item.get("job_id") == job_id),
            None,
        )

        if job is None or job.get("status", "").upper() == "APPROVED":
            return False

        confirmation = input("Approve this listing? (yes/no): ")

        if confirmation.strip().lower() in {"y", "yes"}:
            job["status"] = "APPROVED"
            self._save_data(self.JOBS_FILE, jobs)
            return True

        return False