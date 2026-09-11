from Models.Auth import Auth, AuthenticationError, AuthorizationError
#Importing the Auth class
from helpers import validate_password, verify_email
#Importing the function that validates the password

def register(): 
    user_role = input("Would you like to proceed as a Job Seeker or Employer\n Job Seeker type (JB)\n Employer type(E)\n: ")
    auth = Auth()
    if user_role == "JB" or "jb":

        name = input ("Please enter your full name: ")
        email = verify_email()
        phone = input ("Please enter your phone number: ")
        password = validate_password()

        user = auth.register(name, email, phone, password, role = "JOB_SEEKER")

        print(f"Registered {user.email} as {user.role}")

        try:

            logged_in_user = auth.login(name, password)
            print(f"Logged in as {logged_in_user.name}")
            auth.require_role("JOB_SEEKER")
            print("Job seeker access granted")

        except (AuthenticationError, AuthorizationError) as error:
            print(error)

    elif user_role == "E" or "e":
        name = input ("Please enter your full name: ")
        email = verify_email(email)
        phone = input ("Please enter your phone number: ")
        password = validate_password()
        role = "JOB_SEEKER"
    else:
        raise ValueError("Please enter a valid input. Either JB/jb or E/e")