import colorama
from colorama import Fore, Style

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
            print(f"Signed in as {current.name} ({current.role.replace('_', ' ').title()})")
            print("[L] Logout  [Q] Quit")
        else:
            print("[R] Register  [L] Login  [Q] Quit")

        choice = input("Choose an option: ").strip().upper()
        if choice == "R" and auth.current_user is None:
            register(auth)
        elif choice == "L" and auth.current_user is not None:
            auth.logout()
            print("You have been logged out.")
        elif choice == "L":
            login(auth)
        elif choice == "Q":
            print("Goodbye.")
            return
        else:
            print("Please choose one of the options shown above.")

if __name__ == "__main__":
    landing()
    
