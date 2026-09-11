from email_validator import validate_email, EmailNotValidError
#A package that provides the tools to validate an email
def verify_email():
    email_str = input("Please enter your email address: ")
    try:
        # Validates syntax and checks if the domain exists
        email_info = validate_email(email_str, check_deliverability=True)
        
        # Returns the normalized, clean version of the email
        return email_info.normalized
    except EmailNotValidError as e:
        # Provides a friendly error message explaining why it failed
        print(f"❌ Invalid email: {str(e)}")
        return None


