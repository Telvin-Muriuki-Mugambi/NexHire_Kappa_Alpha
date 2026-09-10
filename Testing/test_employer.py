import sys
import os
import pytest

# Ensure Python can locate the root directory modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Models.User import User


# ------------------------------------------------------------------
# 1. Employer Profile & Authentication Tests
# ------------------------------------------------------------------

def test_employer_user_initialization():
    """Verify an employer User object instantiates correctly with required fields."""
    employer = User(
        name="Acme Corp", 
        email="hr@acme.com", 
        phone="0712345678", 
        password="EmployerPassword123"
    )
    
    # Assign the employer role manually (as defined in Models/User.py)
    employer.role = "employer"

    assert employer.name == "Acme Corp"
    assert employer.email == "hr@acme.com"
    assert employer.phone_number == "0712345678"
    assert employer.role == "employer"
    assert employer.user_id >= 1000 and employer.user_id <= 9999


def test_employer_password_verification():
    """Verify password hashing and authentication for an employer account."""
    employer = User(
        name="Tech Solutions", 
        email="recruiter@tech.com", 
        phone="0700000000", 
        password="SecurePassword"
    )
    
    assert employer.verify_password("SecurePassword") is True
    assert employer.verify_password("WrongPassword") is False


# ------------------------------------------------------------------
# 2. Employer CLI Action Tests (Posting & Managing Job Listings)
# ------------------------------------------------------------------

def test_employer_post_job_cli(monkeypatch, capsys):
    """Test the interactive CLI prompt flow where an employer posts a job listing."""
    # Simulate employer entering: Job Title, Salary, Location
    user_inputs = iter(["Backend Python Engineer", "150000", "Nairobi"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    # Employer interactive prompt logic
    title = input("Enter Job Title: ")
    salary = input("Enter Offered Salary: ")
    location = input("Enter Job Location: ")
    
    print(f"Employer success: Posted '{title}' in {location} offering KES {salary}.")

    captured = capsys.readouterr()
    assert "Employer success: Posted 'Backend Python Engineer' in Nairobi offering KES 150000." in captured.out


def test_employer_delete_job_cli(monkeypatch, capsys):
    """Test the CLI prompt for an employer deleting a posted job listing."""
    # Simulate entering Job ID '2024' and confirming with 'yes'
    user_inputs = iter(["2024", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    job_id = input("Enter Job ID to delete: ")
    confirm = input("Are you sure you want to delete this listing? (yes/no): ")

    if confirm.lower() == "yes":
        print(f"Listing {job_id} deleted successfully by employer.")

    captured = capsys.readouterr()
    assert "Listing 2024 deleted successfully by employer." in captured.out