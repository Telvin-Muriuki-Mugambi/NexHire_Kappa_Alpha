import argparse
from jobseeker import JobSeeker

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
            print(f"\n🔹 ID: {job['id']} | {job['title']}")
            print(f"   📍 Location : {job['location']}")
            print(f"   ⌛ Type     : {job['type']}")
            print(f"   🛠️ Skills   : {', '.join(job['skills'])}")
            print("   " + "─" * 40)

def main():
    parser = argparse.ArgumentParser(
        description="NexHire Kappa Alpha Job Seeker CLI",
        epilog="Tip: Run 'python jobseekercli.py guide' if you get stuck!"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command parser
    search_parser = subparsers.add_parser("search", help="Search and filter job postings")
    search_parser.add_argument("--keyword", help="Filter by any keyword across fields")
    search_parser.add_argument("--title", help="Filter by job title")
    search_parser.add_argument("--location", help="Filter by location")
    search_parser.add_argument("--type", help="Filter by job type (Full-time/Part-time/Contract)")
    search_parser.add_argument("--skill", help="Filter by a specific skill")

    # Upload command parser
    upload_parser = subparsers.add_parser("upload", help="Upload a CV/Resume")
    upload_parser.add_argument("--path", help="Direct file path to CV (optional)")

    # Guide/Help command parser (Catches users when stuck)
    subparsers.add_parser("guide", help="Show a friendly guide on how to use the app")

    args = parser.parse_args()
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
            print(f"ID: {job['id']} | {job['title']} ({job['location']}) - {job['type']}")
            print(f"   Skills: {', '.join(job['skills'])}")
            
    elif args.command == "upload":
        seeker.upload_file(file_path=args.path)

    elif args.command == "guide":
        show_user_guide()
        
    else:
        # Interactive Menu with a Built-in "Stuck?" Help Option
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
                break
            else:
                print("❌ Invalid option. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()