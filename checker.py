import requests
import random
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

TEST_URLS = [
    'https://httpbin.org/ip',
    'https://api.ipify.org'
]

def check_proxy(proxy, proxy_type):
    proxy_dict = {}
    if proxy_type == 'http':
        proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    elif proxy_type == 'socks4':
        proxy_dict = {'http': f'socks4://{proxy}', 'https': f'socks4://{proxy}'}
    elif proxy_type == 'socks5':
        proxy_dict = {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
    
    test_url = random.choice(TEST_URLS)
    try:
        response = requests.get(test_url, proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def check_proxies(proxies, proxy_type, max_workers=10):
    working_proxies = []
    if not proxies:
        return working_proxies
    
    total = len(proxies)
    tested = 0
    working = 0
    
    print(f"{Fore.YELLOW}Checking {total} {proxy_type.upper()} proxies...")
    print(f"{Fore.CYAN}[{'=' * 0}{' ' * 30}] {0}%", end='\r')
    
    def check_and_update(proxy):
        nonlocal tested, working
        result = check_proxy(proxy, proxy_type)
        tested += 1
        if result:
            working += 1
            return proxy
        return None
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_and_update, proxy) for proxy in proxies]
        for i, future in enumerate(futures):
            result = future.result()
            if result:
                working_proxies.append(result)
            progress = int((i + 1) / total * 30)
            percentage = int((i + 1) / total * 100)
            print(f"{Fore.CYAN}[{'=' * progress}{' ' * (30 - progress)}] {percentage}% ({working}/{tested})", end='\r')
            
    print(f"\n{Fore.GREEN}Found {len(working_proxies)} working {proxy_type.upper()} proxies out of {total} checked.")
    return working_proxies