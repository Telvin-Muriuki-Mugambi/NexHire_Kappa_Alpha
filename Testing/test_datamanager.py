from pathlib import Path
#Used for handling file paths in Python

class DataManager:
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

