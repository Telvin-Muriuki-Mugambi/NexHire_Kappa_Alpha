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
   def _normalize_id(value):
       return str(value)


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
           if self._normalize_id(record.get("user_id")) == self._normalize_id(payload.get("user_id")):
               records[index] = payload
               break
       else:
           records.append(payload)
       self._write_records(self.users_file, records)


   def update_user(self, user_id, **updates):
       records = self._read_records(self.users_file)
       target_id = self._normalize_id(user_id)
       for index, record in enumerate(records):
           if self._normalize_id(record.get("user_id")) == target_id:
               record.update(updates)
               self._write_records(self.users_file, records)
               return record
       return None


   def delete_user(self, user_id):
       records = self._read_records(self.users_file)
       target_id = self._normalize_id(user_id)
       remaining = [record for record in records if self._normalize_id(record.get("user_id")) != target_id]
       self._write_records(self.users_file, remaining)
       return len(remaining) != len(records)


   def get_user_by_id(self, user_id):
       target_id = self._normalize_id(user_id)
       for record in self._read_records(self.users_file):
           if self._normalize_id(record.get("user_id")) == target_id:
               return User.from_dict(record)
       return None


   def save_job(self, job):
       records = self._read_records(self.jobs_file)
       payload = job.to_dict() if hasattr(job, "to_dict") else job
       for index, record in enumerate(records):
           if self._normalize_id(record.get("job_id")) == self._normalize_id(payload.get("job_id")):
               records[index] = payload
               break
       else:
           records.append(payload)
       self._write_records(self.jobs_file, records)


   def delete_job(self, job_id):
       records = self._read_records(self.jobs_file)
       target_id = self._normalize_id(job_id)
       remaining = [record for record in records if self._normalize_id(record.get("job_id")) != target_id]
       self._write_records(self.jobs_file, remaining)
       return len(remaining) != len(records)


   def load_users(self):
       users = []
       for record in self._read_records(self.users_file):
           if not isinstance(record, dict):
               continue
           try:
               users.append(User.from_dict(record))
           except (KeyError, TypeError, ValueError):
               continue
       return users


   def load_jobs(self):
       return [JobListing.from_dict(record) for record in self._read_records(self.jobs_file)]


   def get_job_by_id(self, job_id):
       target_id = self._normalize_id(job_id)
       for record in self._read_records(self.jobs_file):
           if self._normalize_id(record.get("job_id")) == target_id:
               return JobListing.from_dict(record)
       return None