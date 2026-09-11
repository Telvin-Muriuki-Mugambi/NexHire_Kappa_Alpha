import json
from pathlib import Path


from Models.JobListing import JobListing
from Models.User import User

 
class DataManager:
   """Persist users and job listings as JSON collections."""


   def __init__(self, data_dir):
       self.data_dir = Path(data_dir)
       self.data_dir.mkdir(parents=True, exist_ok=True)
       self.users_file = self.data_dir / "users.json"
       self.jobs_file = self.data_dir / "jobs.json"
       self._ensure_file(self.users_file)
       self._ensure_file(self.jobs_file)


   @staticmethod
   def _ensure_file(path):
       if not path.exists():
           path.write_text("[]", encoding="utf-8")


   @staticmethod
   def _read_records(path):
       try:
           content = path.read_text(encoding="utf-8")
           if not content.strip():
               return []
           records = json.loads(content)
       except (FileNotFoundError, json.JSONDecodeError):
           return []
       return records if isinstance(records, list) else []


   @staticmethod
   def _write_records(path, records):
       path.write_text(json.dumps(records, indent=2), encoding="utf-8")


   def save_user(self, user):
       records = self._read_records(self.users_file)
       payload = user.to_dict() if hasattr(user, "to_dict") else user
       for index, record in enumerate(records):
           if record.get("user_id") == payload.get("user_id"):
               records[index] = payload
               break
       else:
           records.append(payload)
       self._write_records(self.users_file, records)


   def save_job(self, job):
       records = self._read_records(self.jobs_file)
       payload = job.to_dict() if hasattr(job, "to_dict") else job
       for index, record in enumerate(records):
           if record.get("job_id") == payload.get("job_id"):
               records[index] = payload
               break
       else:
           records.append(payload)
       self._write_records(self.jobs_file, records)


   def load_users(self):
       return [User.from_dict(record) for record in self._read_records(self.users_file)]


   def load_jobs(self):
       return [JobListing.from_dict(record) for record in self._read_records(self.jobs_file)]


   def get_job_by_id(self, job_id):
       return next((job for job in self.load_jobs() if job.job_id == job_id), None)