"""Offer search, CV upload, and help commands for job seekers."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Models.Auth import Auth, AuthenticationError
from Models.DataManager import DataManager
from Models.jobseeker import JobSeeker
from flow.Login import login
from Dashboards.JobSeeker_Dashboard import show_jobseeker_menu

def show_user_guide():
    """Displays friendly, step-by-step help for users who get stuck."""
    print("\n" + "╔" + "═" * 46 + "╗")
    print("║             📖 NEXHIRE USER GUIDE             ║")
    print("╚" + "═" * 46 + "╝")
    print("  Welcome! You can use this app interactively or via terminal commands.\n")
    
    print("  👉 OPTION A: Interactive Mode (Recommended for beginners)")
    print("     Just run the script without any commands:")
    print("     $ python jobseekercli.py")
    print("     Then follow the on-screen menu using numbers 1 to 3.\n")
    
    print("  👉 OPTION B: Command-Line (CLI) Mode (For advanced users)")
    print("     1. Searching for jobs:")
    print("        $ python jobseekercli.py search --skill Python")
    print("        $ python jobseekercli.py search --location Remote --type Full-time")
    print("     2. Uploading a CV:")
    print("        $ python jobseekercli.py upload")
    print("        $ python jobseekercli.py upload --path \"path/to/resume.pdf\"\n")
    
    print("  💡 Need quick help on a specific command? Add --help")
    print("     $ python jobseekercli.py search --help")
    print("═" * 48 + "\n")

def interactive_search(seeker):
    """Collect interactive filters and display matching approved jobs."""
    print("\n" + "═" * 40)
    print("        🔍 JOB SEARCH FILTER MENU        ")
    print("═" * 40)
    print("  [1] Filter by any keyword")
    print("  [2] Filter by job title")
    print("  [3] Filter by location")
    print("  [4] Filter by job type (e.g., Full-time)")
    print("  [5] Filter by skill")
    print("═" * 40)

    choice = input("\n👉 Choose an option (1-5): ").strip()

    any_keyword = title = location = job_type = skill = None

    if choice == "1":
        any_keyword = input("💬 Enter search keyword: ").strip()
    elif choice == "2":
        title = input("💼 Enter job title: ").strip()
    elif choice == "3":
        location = input("📍 Enter location: ").strip()
    elif choice == "4":
        job_type = input("⏳ Enter job type: ").strip()
    elif choice == "5":
        skill = input("⚡ Enter skill: ").strip()
    else:
        print("❌ Invalid choice. Returning to main menu.")
        return

    results = seeker.filter_jobs(
        any_keyword=any_keyword,
        title=title,
        location=location,
        job_type=job_type,
        skill=skill
    )

    print("\n" + "─" * 45)
    print(f" 🎯 MATCHING OPPORTUNITIES FOUND ({len(results)}) ")
    print("─" * 45)
    
    if not results:
        print("📭 No jobs match your criteria. Try different filters!")
    else:
        for job in results:
            print(f"\n🔹 ID: {job['job_id']} | {job['title']}")
            print(f"   📍 Location : {job['location']}")
            print(f"   ⌛ Type     : {job.get('availability', '')}")
            print(f"   🛠️ Skills   : {', '.join(job['skills'])}")
            print("   " + "─" * 40)

def create_auth(data_dir=None):
    """Create a job-seeker CLI authentication session for the selected data directory."""
    data_path = Path(data_dir) if data_dir else PROJECT_ROOT / "Data"
    return Auth(DataManager(data_path))


def main(argv=None):
    """Parse and execute a job-seeker command or open its interactive dashboard."""
    parser = argparse.ArgumentParser(
        description="NexHire Kappa Alpha Job Seeker CLI",
        epilog="Tip: Run 'python jobseekercli.py guide' if you get stuck!"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search and filter job postings")
    search_parser.add_argument("--keyword", help="Filter by any keyword across fields")
    search_parser.add_argument("--title", help="Filter by job title")
    search_parser.add_argument("--location", help="Filter by location")
    search_parser.add_argument("--type", help="Filter by job type (Full-time/Part-time/Contract)")
    search_parser.add_argument("--skill", help="Filter by a specific skill")

    upload_parser = subparsers.add_parser("upload", help="Upload a CV/Resume")
    upload_parser.add_argument("--path", help="Direct file path to CV (optional)")

    subparsers.add_parser("guide", help="Show a friendly guide on how to use the app")
    subparsers.add_parser("interactive", help="Log in and open the job seeker dashboard")

    cli_args = list(sys.argv[1:] if argv is None else argv)
    if not cli_args:
        print("Job seeker CLI. Type 'interactive' to open the dashboard, 'guide' to see help, or 'q' to quit.")
        while True:
            try:
                command = input("jobseeker> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nJob seeker session ended.")
                return 1

            if command in {"", None}:
                continue
            if command in {"q", "quit", "exit"}:
                return 0
            if command == "guide":
                cli_args = ["guide"]
                break
            if command == "interactive":
                cli_args = ["interactive"]
                break
            cli_args = [command]
            break

    args = parser.parse_args(cli_args)
    seeker = JobSeeker()

    if args.command == "search":
        results = seeker.filter_jobs(
            any_keyword=args.keyword,
            title=args.title,
            location=args.location,
            job_type=args.type,
            skill=args.skill
        )
        print(f"\n--- Matching Jobs Found ({len(results)}) ---")
        if not results:
            print("No jobs match your criteria.")
        for job in results:
            print(f"ID: {job['job_id']} | {job['title']} ({job['location']}) - {job.get('availability', '')}")
            print(f"   Skills: {', '.join(job['skills'])}")

    elif args.command == "upload":
        seeker.upload_file(file_path=args.path)

    elif args.command == "guide":
        show_user_guide()

    elif args.command == "interactive":
        auth = create_auth()
        try:
            if login(auth) is None:
                return 1
            if not auth.has_role("JOB_SEEKER"):
                print("This account does not have job seeker privileges.")
                return 1
            return show_jobseeker_menu(auth)
        except (AuthenticationError, EOFError, KeyboardInterrupt):
            print("\nJob seeker session ended.")
            return 1

    else:
        while True:
            print("\n" + "╔" + "═" * 38 + "╗")
            print("║        🌟 NEXHIRE JOB SEEKER 🌟       ║")
            print("╚" + "═" * 38 + "╝")
            print("  [1] 🔎 Search Job Postings")
            print("  [2] 📄 Upload CV / Resume")
            print("  [3] 📖 Help / Guide (Stuck?)")
            print("  [4] 🚪 Exit Application")
            print("═" * 40)

            choice = input("\n👉 Select an option (1-4): ").strip()

            if choice == "1":
                interactive_search(seeker)
            elif choice == "2":
                seeker.upload_file()
            elif choice == "3":
                show_user_guide()
            elif choice == "4":
                print("\n👋 Thank you for using NexHire. Goodbye!\n")
                return 0
            else:
                print("❌ Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()