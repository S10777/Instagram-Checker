from instagram_private_api import Client, ClientCompatPatch
from colorama import Fore, Back, Style, init
import keyboard

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
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

def start_script():
    global username, password
    try:
        api = Client(username, password)
        api.login()

        rank_token_followers = Client.generate_uuid()
        followers = api.user_followers(api.authenticated_user_id, rank_token=rank_token_followers)
        followers_list = set(user['username'] for user in followers['users'])

        rank_token_following = Client.generate_uuid()
        following = api.user_following(api.authenticated_user_id, rank_token=rank_token_following)
        following_list = set(user['username'] for user in following['users'])

        not_following_back = following_list - followers_list

        print("People you follow but don't follow you back:")
        for username in not_following_back:
            print(username)

        print("Script executed successfully!")

    except Exception as e:
        print(f"Script failed: {str(e)}")

def main():
    print_banner()

    step = input("[1] Input credentials\n[2] Start")

    if step == '1':
        enter_credentials()
        main()
    elif step == '2':
        start_script()
    else:
        print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
