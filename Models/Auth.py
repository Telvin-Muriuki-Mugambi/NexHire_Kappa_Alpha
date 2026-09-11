#Authentication Logic

# TODO: Registration of a user
# TODO: Login of a user
# TODO: Role Based Access [Job seeker, Employer, Admin]
# TODO: Password Hashing 

from Models.User import User


class Auth:
    ROLES = {"ADMIN", "JOB_SEEKER", "EMPLOYER"}

    def __init__(self):
        #Used to save the user's data
        self.users = {}
        #Set the user session
        self.current_user = None

    #Method for registering the user
    def register(self,name,email,phone,password,role="job_seeker"):

        #create an instance of a user
        user = User (name, email, password) 
        user.role = role
        self.users[email] = user

        #Check if the email already exists
        if email  in self.users:
            raise ValueError("The email already exists")
        
        role = role.upper()
        #Handle edge case if the role entered exist or not
        if role not in self.ROLES:
            raise ValueError("Role does not exist")

        return user
    #Method of login of a user. Uses the email and password

    def login(self, email, password):

        #Retrives the email from the user's dictionary
        user = self.users.get(email)

        #Check if the email is there and if the password's match
        if user is None or not user.verify_password(password):
            raise ValueError("Invalid email or password")
        #if it passes the current session is set for the current user
        self.current_user = user
        return user

    #Method to logout the user
    def logout(self):
        #Removes the user by setting the current user to None
        self.current_user = None

