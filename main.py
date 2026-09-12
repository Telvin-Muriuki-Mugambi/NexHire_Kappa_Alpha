from pathlib import Path

from flow import landing
from Models.Auth import Auth
from Models.DataManager import DataManager



def main():
    data_dir = Path(__file__).resolve().parent / "Data"
    auth = Auth(DataManager(data_dir))
    landing(auth)

if __name__ == "__main__":
    main()