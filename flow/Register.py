from Models.Auth import Auth, AuthenticationError, AuthorizationError
#Importing the Auth class

def register(): 
    user_role = input("Would you like to proceed as a Job Seeker or Employer\n Job Seeker type (JB)\n Employer type(E)\n: ")

    if user_role == "JB" or "jb":
        pass
    elif user_role == "E" or "e":
        pass
    else:
        pass