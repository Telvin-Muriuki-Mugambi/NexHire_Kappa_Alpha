from email_validator import validate_email, EmailNotValidError
#A package that provides the tools to validate an email
def Verify_Email(email_str):
    try:
        # Validates syntax and checks if the domain exists
        email_info = validate_email(email_str, check_deliverability=True)
        
        # Returns the normalized, clean version of the email
        return f"Valid! Normalized email: {email_info.normalized}"
    except EmailNotValidError as e:
        # Provides a friendly error message explaining why it failed
        return f"Invalid: {str(e)}"


