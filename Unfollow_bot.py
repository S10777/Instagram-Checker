from instagram_private_api import Client, ClientCompatPatch
from colorama import Fore, Style, init
from prettytable import PrettyTable
import time

init(autoreset=True)

username = ""
password = ""

creds_entered = False
api = None

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
    global username, password, creds_entered
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    creds_entered = True

def start_script():
    global username, password, api
    try:
        if not api:
            api = Client(username, password)
            api.login()

        rank_token_followers = Client.generate_uuid()
        followers = api.user_followers(api.authenticated_user_id, rank_token=rank_token_followers)
        followers_list = set((user['username'], user['is_private']) for user in followers['users'])

        rank_token_following = Client.generate_uuid()
        following = api.user_following(api.authenticated_user_id, rank_token=rank_token_following)
        following_list = set(user['username'] for user in following['users'])

        not_following_back = following_list - set(user[0] for user in followers_list)

        table = PrettyTable(['Username', 'Privacy Status'])
        table.align['Username'] = 'l'
        table.align['Privacy Status'] = 'l'

        print("\nPeople you follow but don't follow you back:\n")
        for username in not_following_back:
            user_info = api.username_info(username)["user"]
            is_private = user_info["is_private"]
            privacy_status = f"{Fore.RED}[PRIVATE]{Style.RESET_ALL}" if is_private else f"{Fore.GREEN}[PUBLIC]{Style.RESET_ALL}"
            table.add_row([username, privacy_status])
            time.sleep(2)

        if not table._rows:
            print(f"{Fore.WHITE}No users found.")
        else:
            print(table)

    except Exception as e:
        print(f"Script failed: {str(e)}")


def defollow_non_followers(not_following_back):
    global api
    try:
        if api is None:
            print(f"{Fore.WHITE}Please start the script (option 2) before unfollowing.{Style.RESET_ALL}")
            return

        if not_following_back:
            for username in not_following_back:
                user_id = api.username_info(username)["user"]["pk"]
                confirm_unfollow = input(f"Do you want to unfollow {username}? (y/n): ").lower()
                
                if confirm_unfollow == 'y':
                    api.friendships_destroy(user_id)
                    print(f"{Fore.YELLOW}Unfollowed: {username}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}Skipped: {username}{Style.RESET_ALL}")
                    
                time.sleep(2)
        else:
            print(f"{Fore.WHITE}No users found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"Error while unfollowing: {str(e)}")


def main():
    global creds_entered, api
    print_banner()
    followers_list = set()
    while True:
        print(f"\n{Fore.CYAN}[1] Enter Instagram credentials{Style.RESET_ALL}\n"
              f"{Fore.BLUE}[2] Start the script{Style.RESET_ALL}\n"
              f"{Fore.MAGENTA}[3] Exit{Style.RESET_ALL}\n"
              f"{Fore.YELLOW}[4] Unfollow non-followers{Style.RESET_ALL}\n")

        choice = input(f"{Fore.CYAN}Select an option: ")

        if choice == "1":
            enter_credentials()
        elif choice == "2":
            if not creds_entered:
                print(f"{Fore.WHITE}Please enter Instagram credentials first.{Style.RESET_ALL}")
            else:
                start_script()
        elif choice == "3":
            break
        elif choice == "4":
            if not creds_entered:
                print(f"{Fore.WHITE}Please enter Instagram credentials first.{Style.RESET_ALL}")
            else:
                rank_token_followers = Client.generate_uuid()
                followers = api.user_followers(api.authenticated_user_id, rank_token=rank_token_followers)
                followers_list = set((user['username'], user['is_private']) for user in followers['users'])
                rank_token_following = Client.generate_uuid()
                following = api.user_following(api.authenticated_user_id, rank_token=rank_token_following)
                following_list = set(user['username'] for user in following['users'])
                not_following_back = following_list - set(user[0] for user in followers_list)
                defollow_non_followers(not_following_back)
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
