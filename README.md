# NexHire Kappa Alpha

NexHire is a Python command-line recruitment application that connects job seekers with employers. Users can register, log in, manage job listings, search approved opportunities, apply for jobs, and review applicants.

## Features

- Role-based access for administrators, employers, and job seekers
- User registration and password authentication
- Required CV upload for job-seeker registration
- CV filenames based on the user's ID and name
- Employer job posting, viewing, and deletion
- Administrator job review, approval, and user management
- Job-seeker search and application by job ID
- Employer applicant viewing with applicant names and CV paths
- JSON-based persistence through `DataManager`

## Requirements

- Python 3.13 or a compatible recent Python 3 version
- `pip`
- Tk support for the optional graphical CV file picker

## Installation

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the Application

Start the complete interactive application with:

```bash
python3 main.py
```

The application opens the landing menu. From there, users can register, log in, access the dashboard for their role, or quit.

## User Roles

### Job seeker

Job seekers must upload a CV during registration. The CV is saved in `Data/Jobseeker_cvs/` using a filename similar to:

```text
1234_Ada_Lovelace.pdf
```

After logging in, job seekers can:

- View approved jobs
- Search approved jobs
- Apply using a job ID
- View their profile

### Employer

Employers can:

- Post jobs
- View their own jobs
- Delete their jobs
- Select a job and view its applicants
- See each applicant's name and CV path

Open the employer CLI directly with:

```bash
python3 CLI_commands/Employer_CLI.py interactive
```

### Administrator

Administrators can:

- List, create, and delete users
- Review pending jobs
- Approve jobs
- Post opportunities

Administrator actions are also available through the interactive application and the admin CLI.

## Command-Line Interfaces

Show authentication command help:

```bash
python3 CLI_commands/Auth_CLI.py --help
```

Show job-seeker command help:

```bash
python3 CLI_commands/jobseekercli.py --help
python3 CLI_commands/jobseekercli.py guide
python3 CLI_commands/jobseekercli.py search --keyword python
python3 CLI_commands/jobseekercli.py search --location Nairobi --skill Python
python3 CLI_commands/jobseekercli.py upload --path /path/to/cv.pdf
```

Show administrator command help:

```bash
python3 CLI_commands/Admin_CLI.py --help
python3 CLI_commands/Admin_CLI.py users --help
python3 CLI_commands/Admin_CLI.py jobs --help
```

Show employer command help:

```bash
python3 CLI_commands/Employer_CLI.py --help
```

## Project Structure

```text
main.py                  Application entry point
CLI_commands/             Direct command-line interfaces
Dashboards/               Role-specific interactive menus
Data/                     JSON data and uploaded CV storage
flow/                     Login, registration, landing, and routing flows
helpers/                  Password and email validation helpers
Models/                   Users, jobs, authentication, and persistence
Testing/                  Automated tests
requirements.txt         Python dependencies
```

## Data Files

The application stores runtime data under `Data/`:

- `users.json` stores user accounts and CV paths
- `jobs.json` stores job listings and their statuses
- `applications.json` stores job applications
- `Jobseeker_cvs/` stores uploaded CV files

`DataManager` is the shared persistence layer used to read and update these records.

## Testing

Run the test suite with:

```bash
.venv/bin/python -m pytest -q
```

Or, after activating the virtual environment:

```bash
python -m pytest -q
```

Run focused tests with:

```bash
python -m pytest Testing/test_authentication.py Testing/test_datamanager.py -q
```

## Notes

- Run commands from the project root so package imports resolve correctly.
- Use the project virtual environment to ensure all dependencies are available.
- Do not commit private CV files or production user data to source control.
