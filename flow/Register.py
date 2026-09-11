from pathlib import Path

from Models.Auth import Auth, AuthenticationError, AuthorizationError
from Models.DataManager import DataManager
from helpers import validate_password, verify_email


def register():
    #We need to know the user role as soon as possible
    #Check if user wants to register as a job seeker or as an employer
    user_role = input(
        "Would you like to proceed as a Job Seeker or Employer\n"
        " Job Seeker type (JB)\n"
        " Employer type (E)\n: "
    ).strip().upper()

    #First Order function saving Auth to a variable
    data_dir = Path(__file__).resolve().parents[1] / "Data"
    data_manager = DataManager(data_dir)
    auth = Auth(data_manager)

    #Improvement from previous logic
    #Conditional statement to set the role of the user
    if user_role == "JB":
        role = "JOB_SEEKER"
    elif user_role == "E":
        role = "EMPLOYER"
    else:
        raise ValueError("Please enter a valid input. Either JB/jb or E/e")

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
    user = auth.register(name, email, phone, password, role=role)

    #Information display to user to show what is happening behind the scenes
    print(f"Registered {user.email} as {user.role}")

    #Login user after registration and catching any errors
    try:
        logged_in_user = auth.login(email, password)
        print(f"Logged in as {logged_in_user.name}")
        auth.require_role(role)
        print(f"{role.replace('_', ' ').title()} access granted")

    except (AuthenticationError, AuthorizationError) as error:
        print(error)

    finally:
        auth.logout()

#Rather than running the function directly, it will be run on the main file
if __name__ == "__main__":
    register()
    
