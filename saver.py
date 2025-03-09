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
    
    anonymity_groups = {}
    for proxy, anonymity in proxies:
        if anonymity not in anonymity_groups:
            anonymity_groups[anonymity] = []
        anonymity_groups[anonymity].append(proxy)

    for anonymity, proxy_list in anonymity_groups.items():
        filename = f"{save_dir}/{len(proxy_list)}-{anonymity.replace(' ', '_')}-{today}.txt"
        try:
            with open(filename, 'w') as f:
                for proxy in proxy_list:
                    f.write(f"{proxy}\n")
            print(f"{Fore.GREEN}Saved {len(proxy_list)} {anonymity} {proxy_type.upper()} proxies to {os.path.join(today, os.path.basename(filename))}")
        except Exception as e:
            print(f"{Fore.RED}Error saving {anonymity} {proxy_type.upper()} proxies to file: {str(e)}")
