"""Provide job-seeker search, application, and CV upload behavior."""

import os
import shutil
import tkinter as tk
from tkinter import filedialog
from Models.JobListing import JobListing


class JobSeeker:
    """Represent a seeker who can search approved jobs and submit applications."""


    cv_file_path = "Data/Jobseeker_cvs"

    def __init__(self, data_manager=None, user_id=None, name=None, cv=None):
        """Initialize seeker identity, CV metadata, and available job data."""
        self.data_manager = data_manager
        self.user_id = user_id
        self.name = name
        self.cv_path = cv
        self.applied_jobs = []
        self.job_postings = self._load_jobs()

    def _load_jobs(self):
        """Load jobs from the configured DataManager or return an empty list."""
        if self.data_manager is None:
            return []
        return self.data_manager.load_jobs()

    @staticmethod
    def _as_dict(job):
        return job.to_dict() if isinstance(job, JobListing) else job

    def available_jobs(self):
        """Return only listings whose persisted status is APPROVED."""
        self.job_postings = self._load_jobs()
        approved = []
        for job in self.job_postings:
            status = job.status if isinstance(job, JobListing) else job.get("status", "")
            if str(status).upper() == "APPROVED":
                approved.append(job)
        return approved

    def filter_jobs(self, any_keyword=None, title=None, location=None, job_type=None, skill=None):
        """Filters job postings based on provided parameters."""
        filtered_list = []
        for job in self.available_jobs():
            record = self._as_dict(job)
            if any_keyword:
                combined_text = f"{record.get('title', '')} {record.get('location', '')} {record.get('availability', record.get('type', ''))} {' '.join(record.get('skills', []))} {record.get('company_name', '')}".lower()
                if any_keyword.lower() not in combined_text:
                    continue

            if title and title.lower() not in record.get("title", "").lower():
                continue
                
            if location and location.lower() not in record.get("location", "").lower():
                continue
                        
            job_type_value = record.get("availability", record.get("type", ""))
            if job_type and job_type.lower() not in job_type_value.lower():
                continue
                
            if skill:
                skills = [s.lower() for s in record.get("skills", [])]
                if skill.lower() not in skills:
                    continue

            filtered_list.append(record)

        return filtered_list

    def search_jobs(self, keyword):
        """Search approved listings using a keyword across their fields."""
        return self.filter_jobs(any_keyword=keyword)

    def apply_job(self, job_id):
        """Apply to an approved job and persist the seeker's application."""
        approved_jobs = self.available_jobs()
        job = next((job for job in approved_jobs if str(job.job_id) == str(job_id)), None)
        if self.data_manager is None:
            self.applied_jobs.append(job_id)
            return job_id
        if job is None:
            raise ValueError("You can only apply for an approved job with that ID.")
        if self.data_manager is not None:
            self.data_manager.save_application(
                job_id=job.job_id,
                user_id=self.user_id,
                name=self.name,
                cv=self.cv_path,
            )
        if str(job.job_id) not in {str(applied_id) for applied_id in self.applied_jobs}:
            self.applied_jobs.append(job.job_id)
        return job.job_id

    def upload_file(self, target_directory=None, file_path=None):
        """Opens native OS file chooser and copies selected CV to predetermined destination directory."""
        save_directory = target_directory or self.cv_file_path

        if file_path is None:
            print("\n📂 Opening file selection window...")
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)

            file_path = filedialog.askopenfilename(
                title="Select CV / Resume to Upload",
                filetypes=[
                    ("Supported CV Formats", "*.pdf *.docx *.txt"),
                    ("All Files", "*.*")
                ]
            )

        if not file_path:
            print("⚠️ Upload cancelled: No file selected.")
            return None

        os.makedirs(save_directory, exist_ok=True)
        file_name = self.cv_filename(file_path)
        destination_path = os.path.join(save_directory, file_name)
        shutil.copy(file_path, destination_path)
        self.cv_path = destination_path

        print("✨ Success! CV copied to target directory:")
        print(f"   📁 {os.path.abspath(destination_path)}")
        return destination_path

    def cv_filename(self, source_path):
        """Return the required CV filename for this registered job seeker."""
        if self.user_id is None:
            raise ValueError("A user ID is required before naming a CV.")
        safe_name = "_".join(
            part for part in "".join(
                character if character.isalnum() else " "
                for character in str(getattr(self, "name", "job_seeker"))
            ).split()
            if part
        ) or "job_seeker"
        extension = os.path.splitext(source_path)[1].lower()
        return f"{self.user_id}_{safe_name}{extension}"

    def upload_registration_cv(self, target_directory=None):
        """Upload the CV used to complete job-seeker registration."""
        return self.upload_file(target_directory)

    def upload_cv(self, file_path):
        """Record a directly supplied CV path for compatibility with CLI usage."""
        save_directory = os.path.dirname(file_path) or "."
        self.cv_path = file_path
        return file_path


job_seeker = JobSeeker



if __name__ == "__main__":
    job_seeker()
        
               


    

    


