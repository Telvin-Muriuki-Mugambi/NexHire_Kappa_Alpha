try:
    import colorama
    from colorama import Fore, Style
except ModuleNotFoundError:
    class _NoColor:
        CYAN = ""
        BRIGHT = ""

    class _NoColorama:
        @staticmethod
        def init(*args, **kwargs):
            return None

    colorama = _NoColorama()
    Fore = Style = _NoColor()


def admin_menu(auth):
    from Dashboards.Admin_Dashboard import show_admin_menu as admin_main

    print("\nAdmin privileges detected. Opening admin menu...\n")
    return admin_main(auth)


def jobseeker_menu(auth):
    from Dashboards.JobSeeker_Dashboard import show_jobseeker_menu as dashboard_main

    print("\nJob seeker privileges detected. Opening menu...\n")
    return dashboard_main(auth)

def employer_menu(auth):
    from Dashboards.Employer_Menu import show_employer_menu as employer_main

    print("\nEmployer priviledges detected. Opening menu...")
    return employer_main(auth)

def landing(auth=None):
    if auth is None:
        from Models.Auth import Auth
        from Models.DataManager import DataManager
        from pathlib import Path

        data_dir = Path(__file__).resolve().parents[1] / "Data"
        auth = Auth(DataManager(data_dir))

    # Initialize colorama (required for Windows support)
    colorama.init(autoreset=True)

    #Use of ASCII to implment the logo
    nexhire_logo = r"""
    _   _             _   _ _           

    | \ | |           | | | (_)          
    |  \| | ___ _   _ | |_| |_ _ __ ___  
    | . ` |/ _ \ \/ / |  _  | | '__/ _ \ 
    | |\  |  __/>  <  | | | | | | |  __/ 
    |_| \_|\___/_/\_\ |_| |_|_|_|  \___| 
    """

    # Fore.CYAN makes the text cyan, Style.BRIGHT makes it vivid
    print(Fore.CYAN + Style.BRIGHT + nexhire_logo)
    print(
        "Welcome to NexHire \n\n"
        "Connecting young talent to opportunity\n\n"
    )

    from .Login import login
    from .Register import register

    while True:
        if auth.current_user is not None:
            current = auth.current_user
            role = str(getattr(current, "role", "")).upper()
            if role == "ADMIN":
                return admin_menu(auth)
            if role == "JOB_SEEKER":
                return jobseeker_menu(auth)
            if role == "EMPLOYER":
                return employer_menu(auth)

            print(f"Signed in as {current.name} ({current.role.replace('_', ' ').title()})\n")
            print("[L] Logout  [Q] Quit")
        else:
            print("[R] Register  [L] Login  [Q] Quit")

        choice = input("Choose an option: ").strip().upper()
        if choice == "R" and auth.current_user is None:
            register(auth)
        elif choice == "L" and auth.current_user is not None:
            auth.logout()
            print("You have been logged out.\n")
        elif choice == "L":
            login(auth)
        elif choice == "Q":
            print("Goodbye.")
            return
        else:
            print("\nPlease choose one of the options shown above.")


if __name__ == "__main__":
    landing()
    
