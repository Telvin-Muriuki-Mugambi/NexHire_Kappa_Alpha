#Data Manager Class: 

#TODO: Add new records
#TODO: Read records
#TODO: Save Users in JSON
#TODO: Save Jobs in JSON
#TODO: Load Users from JSON
#TODO: Load Jobs from JSON

from pathlib import Path
# used for handling and manipulating file and folder paths

class DataManager:
    #Initializing the class with the directory path to the data

    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)

    #Ensuring the file exists
    #It's function is closely related to the class hence use os static method
    @staticmethod
    def _ensure_file(path):
        if not path.exists():
            #Encodes the text so that the computer may understand
            path.write_text("[]", encoding = "utf-8")