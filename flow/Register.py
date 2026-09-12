from pathlib import Path

from Models.Auth import Auth, AuthenticationError, AuthorizationError, DuplicateEmailError
from Models.DataManager import DataManager
from helpers import validate_password, verify_email


def _default_auth():
    data_dir = Path(__file__).resolve().parents[1] / "Data"
    return Auth(DataManager(data_dir))


def register(auth=None):
    #We need to know the user role as soon as possible
    #Check if user wants to register as a job seeker or as an employer
    user_role = input(
        "Would you like to proceed as a Job Seeker or Employer\n"
        " Job Seeker type (JB)\n"
        " Employer type (E)\n: "
    ).strip().upper()

    auth = auth or _default_auth()

    #Improvement from previous logic
    #Conditional statement to set the role of the user
    if user_role == "JB":
        role = "JOB_SEEKER"
    elif user_role == "E":
        role = "EMPLOYER"
    else:
        print("Please enter JB for Job Seeker or E for Employer.\n")
        return None

    #Collection of user details
    name = input("Please enter your full name: ")

    email = verify_email()
    #Loop that ensures a verified email is returned in case the user inserts an incorrect email
    while email is None:
        email = verify_email()

    phone = input("Please enter your phone number: ")

    password = validate_password()
    #Loop to run till a password is returned incase the user inserts an incorrect password
    while password is None:
        password = validate_password()

    #Calling the auth class to supply the register method
    try:
        user = auth.register(name, email, phone, password, role=role)
    except DuplicateEmailError as error:
        print(f"Registration failed: {error}. Please use a different email address.\n")
        return None

    #Information display to user to show what is happening behind the scenes
    print(f"Registered {user.email} as {user.role}\n")

    #Login user after registration and catching any errors
    try:
        logged_in_user = auth.login(email, password)
        print(f"Logged in as {logged_in_user.name}\n")
        auth.require_role(role)
        print(f"{role.replace('_', ' ').title()} access granted\n")
        return logged_in_user

    except (AuthenticationError, AuthorizationError) as error:
        print(f"Registration succeeded, but automatic login failed: {error}\n")
        return user

#Rather than running the function directly, it will be run on the main file
if __name__ == "__main__":
    register()
    
