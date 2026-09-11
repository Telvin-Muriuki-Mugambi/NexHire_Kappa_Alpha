import colorama
from colorama import Fore, Style

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
