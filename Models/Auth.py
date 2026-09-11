#Authentication Logic

# TODO: Registration of a user
# TODO: Login of a user
# TODO: Role Based Access [Job seeker, Employer, Admin]
# TODO: Password Hashing

from Models.User import User

#Improving feedback to user by creating new classes that handle errors

class DuplicateEmailError(ValueError):
    pass


class AuthenticationError(ValueError):
    pass


class AuthorizationError(PermissionError):
    pass


class Auth:
    ROLES = {"ADMIN", "JOB_SEEKER", "EMPLOYER"}

    def __init__(self):
        self.users = {}
        self.current_user = None

    #Method for registering the user
    def register(self, name, email, phone, password, role="JOB_SEEKER"):

        #Check if the email already exists
        if email in self.users:
            raise DuplicateEmailError("Email is already registered")
        role = role.upper()

        #Handle edge case if the role entered exist or not
        if role not in self.ROLES:
            raise ValueError("Unknown role")

        #create an instance of a user
        user = User(name, email, phone, password)
        user.role = role
        self.users[email] = user
        return user
    
    #Method of login of a user. Uses the email and password
    def login(self, email, password):
        #Retrives the email from the user's dictionary
        user = self.users.get(email)

        #Check if the email is there and if the password's match
        if user is None or not user.verify_password(password):
            raise AuthenticationError("Invalid email or password")
        
        #if it passes the current session is set for the current user
        self.current_user = user
        return user

    #Method to logout the user
    def logout(self):
        #Removes the user by setting the current user to None
        self.current_user = None

    #Checks if the user has a role
    def has_role(self, role):
        return self.current_user is not None and self.current_user.role == role.upper()

    #Method to check if the user is an admin
    def is_admin(self):
        return self.has_role("ADMIN")

    #Ensure the user has the correct authorization to perform a certain action
    def require_role(self, role):
        if not self.has_role(role):
            raise AuthorizationError("User is not authorized for this action")
        return True

