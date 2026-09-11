#Data Manager Class: 

#TODO: Add new records
#TODO: Read records
#TODO: Save Users in JSON
#TODO: Save Jobs in JSON
#TODO: Load Users from JSON
#TODO: Load Jobs from JSON

from pathlib import Path
# used for handling and manipulating file and folder paths
import json

class DataManager:
    #Initializing the class with the directory path to the data

    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)

        #Setting the path to the JSON file(s)
        self.users_file = self.data_directory / "Data/users.json"
        self.jobs_file = self.data_directory / "Data/jobs.json"

        #Calling the method
        self._ensure_file(self.users_file)
        self._ensure_file(self.jobs_file)

    #Ensuring the file exists
    #It's function is closely related to the class hence use os static method
    @staticmethod
    def _ensure_file(path):
        if not path.exists():
            #Encodes the text so that the computer may understand
            path.write_text("[]", encoding = "utf-8")

    @staticmethod
    def _read_records(path):
        
        try:
            content = path.read_text(encoding = "utf-8")

            if not content.strip():
                return []
            
            records = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        return records if isinstance(records, list) else []