from Models.Auth import Auth, AuthenticationError, AuthorizationError
from Models.DataManager import DataManager
from pathlib import Path

import getpass
#Provide access to Auth class

def login():
    try: 

        #We simply take the email and password
        email = input ("Please enter your email address: ")
        password = getpass.getpass("Enter your password: ")

        data_manager = DataManager(Path("Data"))
        auth = Auth(data_manager)
        logged_in_user = auth.login(email, password)
        print(f"Logged in as {logged_in_user.name}")

    except (AuthenticationError, AuthorizationError) as error:
        print(error)

if __name__ == "__main__":
    login()

