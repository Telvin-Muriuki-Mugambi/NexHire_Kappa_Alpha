import re
#Library for regular expressions
import getpass
#Library that hides the characters

# Breaking down the pattern:
# ^                         - Start of the string
# (?=.*[a-z])               - Must contain at least one lowercase letter
# (?=.*[A-Z])               - Must contain at least one uppercase letter
# (?=.*[!@#$%^&*(),.?":{}|<>]) - Must contain at least one special symbol
# .{8,}                     - Must be at least 8 characters long
# $                         - End of the string

password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'

def validate_password():
    password = getpass.getpass("Create a password: ")
    confirm_password = getpass.getpass("Confirm your password: ")

    if password == confirm_password:

        if re.match(password_pattern, password):
            print("✅ Password is valid and secure!\n")
            return password
        
        else:
            print("❌ Password does not meet the requirements.")
            print("- Must be at least 8 characters long")
            print("- Must contain at least one uppercase letter")
            print("- Must contain at least one lowercase letter")
            print("- Must contain at least one special character\n")
            return None
    else:
        print("Passwords do not match\n")
        return None

