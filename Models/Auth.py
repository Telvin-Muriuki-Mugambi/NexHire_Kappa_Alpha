#Authentication Logic

# TODO: Registration of a user
# TODO: Login of a user
# TODO: Role Based Access [Job seeker, Employer, Admin]
# TODO: Password Hashing 

class Auth:
    ROLES = {"ADMIN", "JOB_SEEKER", "EMPLOYER"}

    def __init__(self):
        #Used to save the user's data
        self.user = {}
        #Set the user session
        self.current_user = None
