import json
# Imported JSON which provides all the tools necessary to parse, manipulate, and generate JSON
from pathlib import Path
#Used for handling file paths in Python
from Models.User import User
#Provides access to the user methods

class TestDataManager:
    # Test file used to test for persistence users and job listings as JSON.

    #Test case to check exisitence of files by checking the path
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.jobs_file = self.data_dir / "jobs.json"
        self._ensure_file(self.users_file)
        self._ensure_file(self.jobs_file)

    #Used static methods to be bound to the data manager class
    @staticmethod
    def _ensure_file(path):
        if not path.exists():
            path.write_text("[]", encoding="utf-8")

    #Test used for reading the file records
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
    
    #Ensures that records are written in the JSON 
    @staticmethod
    def _write_records(path, records):
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    #Ensure that the details of the user are saved and can be retrived
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

    #Test to load the users from the JSON file
    def load_users(self):
        return [User.from_dict(record) for record in self._read_records(self.users_file)]



