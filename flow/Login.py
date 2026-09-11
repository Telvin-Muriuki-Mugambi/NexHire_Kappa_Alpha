from Models.Auth import Auth, AuthenticationError, AuthorizationError
import getpass
#Provide access to Auth class

def login():
    #We simply take the email and password
    email = input ("Please enter your email address: ")
    password = getpass.getpass("Enter your password: ")

    auth = Auth()

    logged_in_user = auth.login(email, password)
    print(f"Logged in as {logged_in_user.name}")

if __name__ == "__main__":
    login()
