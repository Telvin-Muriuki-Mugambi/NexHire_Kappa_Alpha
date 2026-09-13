"""Authenticate users and enforce role-based access to NexHire features."""

#Authentication Logic

# TODO: Registration of a user
# TODO: Login of a user
# TODO: Role Based Access [Job seeker, Employer, Admin]
# TODO: Password Hashing

from Models.User import User

#Improving feedback to user by creating new classes that handle errors

class DuplicateEmailError(ValueError):
    """Signal that registration attempted to reuse an existing email address."""
    pass


class AuthenticationError(ValueError):
    """Signal that supplied login credentials are invalid."""
    pass


class AuthorizationError(PermissionError):
    """Signal that a user lacks the role required for an operation."""
    pass


class Auth:
    """Manage registered users, active sessions, and role checks."""
    ROLES = {"ADMIN", "JOB_SEEKER", "EMPLOYER"}

    def __init__(self, data_manager=None):
        self.data_manager = data_manager
        self.users = {
            user.email: user
            for user in data_manager.load_users()
        } if data_manager is not None else {}
        self.current_user = None

    #Method for registering the user
    def register(self, name, email, phone, password, role):
        """Create, persist, and return a user with the requested valid role."""

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
        if self.data_manager is not None:
            self.data_manager.save_user(user)
        return user
    
    #Method of login of a user. Uses the email and password
    def login(self, email, password):
        """Authenticate an email and password and set the active user session."""
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
        """Clear the active user session."""
        #Removes the user by setting the current user to None
        self.current_user = None

    #Checks if the user has a role
    def has_role(self, role):
        """Return whether the active session belongs to the requested role."""
        return self.current_user is not None and self.current_user.role == role.upper()

    #Method to check if the user is an admin
    def is_admin(self):
        """Return whether the active session belongs to an administrator."""
        return self.has_role("ADMIN")

    #Ensure the user has the correct authorization to perform a certain action
    def require_role(self, role):
        """Validate the active role or raise an authorization error."""
        if not self.has_role(role):
            raise AuthorizationError("User is not authorized for this action")
        return True

