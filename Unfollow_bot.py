from prettytable import PrettyTable
from instagram_private_api import Client, ClientCompatPatch
from colorama import Fore, Style, init

init(autoreset=True)

username = ""
password = ""

def print_banner():
    banner = f"""
    {Fore.CYAN}    dP                     dP             a88888b. dP                         dP                         
        88                     88            d8'   `88 88                         88                         
    {Fore.BLUE}    88 88d888b. .d8888b. d8888P .d8888b. 88        88d888b. .d8888b. .d8888b. 88  .dP  .d8888b. 88d888b. 
        88 88'  `88 Y8ooooo.   88   88'  `88 88        88'  `88 88ooood8 88'  `"" 88888"   88ooood8 88'  `88 
    {Fore.MAGENTA}    88 88    88       88   88   88.  .88 Y8.   .88 88    88 88.  ... 88.  ... 88  `8b. 88.  ... 88       
        dP dP    dP `88888P'   dP   `88888P8  Y88888P' dP    dP `88888P' `88888P' dP   `YP `88888P' dP                                                                                    
    """
    print(banner)

def enter_credentials():
    global username, password
    print(f"{Fore.CYAN}Enter your Instagram username:{Style.RESET_ALL}", end=" ")
    username = input(f"{Fore.BLUE}")
    print(f"{Style.RESET_ALL}{Fore.MAGENTA}Enter your Instagram password:{Style.RESET_ALL}", end=" ")
    password = input(f"{Fore.BLUE}")
    print(Style.RESET_ALL)

def start_script():
    global username, password
    try:
        api = Client(username, password)
        api.login()
        rank_token_followers = Client.generate_uuid()
        followers = api.user_followers(api.authenticated_user_id, rank_token=rank_token_followers)
        table = PrettyTable()
        table.field_names = ["ID", "Username", "Full Name", "Info"]
        for user in followers['users']:
            user_id = user.get('pk', '')
            username = user.get('username', '')
            full_name = user.get('full_name', '')
            is_private = user.get('is_private', False)
            privacy_status = "Private" if is_private else "Public"
            table.add_row([user_id, username, full_name, privacy_status])
        print(table)
    except Exception as e:
        print(f"Script failed: {str(e)}")

def main():
    print_banner()
    while True:
        print(f"\n{Fore.CYAN}[1] Enter Instagram credentials{Style.RESET_ALL}\n{Fore.BLUE}[2] Start the script{Style.RESET_ALL}\n{Fore.MAGENTA}[3] Exit{Style.RESET_ALL}\n")

        choice = input(f"{Fore.CYAN}Select an option: ")

        if choice == "1":
            enter_credentials()
        elif choice == "2":
            start_script()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()
