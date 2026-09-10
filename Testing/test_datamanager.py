from pathlib import Path
#Used for handling file paths in Python

class DataManager:
    # Test file used to test for persistence users and job listings as JSON.

    #Test case to check exisitence of files
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.jobs_file = self.data_dir / "jobs.json"
        self._ensure_file(self.users_file)
        self._ensure_file(self.jobs_file)
