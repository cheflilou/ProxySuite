import os
from datetime import datetime
from colorama import Fore

OUTPUT_DIR = 'proxies'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def save_proxies(proxies, proxy_type):
    if not proxies:
        print(f"{Fore.YELLOW}No {proxy_type.upper()} proxies to save.")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    save_dir = os.path.join(OUTPUT_DIR, today)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    timestamp = datetime.now().strftime("%H-%M-%S")
    filename = f"{save_dir}/{proxy_type}_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            for proxy in proxies:
                f.write(f"{proxy}\n")
        print(f"{Fore.GREEN}Saved {len(proxies)} {proxy_type.upper()} proxies to {os.path.join(today, os.path.basename(filename))}")
    except Exception as e:
        print(f"{Fore.RED}Error saving proxies to file: {str(e)}")