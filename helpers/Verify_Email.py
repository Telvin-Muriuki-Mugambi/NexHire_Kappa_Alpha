"""Validate and normalize registration email addresses."""

import re
from types import SimpleNamespace

try:
    from email_validator import validate_email, EmailNotValidError
except ModuleNotFoundError:
    class EmailNotValidError(ValueError):
        """Fallback validation error when email-validator is unavailable."""

    def validate_email(email_str, check_deliverability=True):
        """Perform basic syntax validation without the optional dependency."""
        candidate = (email_str or "").strip()
        pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
        if not re.fullmatch(pattern, candidate):
            raise EmailNotValidError("Invalid email address.")
        return SimpleNamespace(normalized=candidate.lower())


def verify_email():
    """Prompt for an email and return its normalized form when valid."""
    email_str = input("Please enter your email address: ")
    try:
        email_info = validate_email(email_str, check_deliverability=True)
        return email_info.normalized
    except EmailNotValidError as e:
        print(f"❌ Invalid email: {str(e)}\n")
        return None


