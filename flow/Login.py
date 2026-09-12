from Models.Auth import Auth, AuthenticationError
from Models.DataManager import DataManager
from pathlib import Path

import getpass
def _default_auth():
    data_dir = Path(__file__).resolve().parents[1] / "Data"
    return Auth(DataManager(data_dir))

def login(auth=None):
    auth = auth or _default_auth()
    try: 

        #We simply take the email and password
        email = input ("Please enter your email address: ")
        password = getpass.getpass("Enter your password: ")

        logged_in_user = auth.login(email, password)
        return logged_in_user

    except AuthenticationError as error:
        print(f"Login failed: {error}. Check your email and password and try again.")
        return None

if __name__ == "__main__":
    login()

