import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore
import warnings
import os

requests.packages.urllib3.disable_warnings()

TEST_URLS = [
    'https://httpbin.org/ip',
    'https://api.ipify.org'
]

def check_anonymity(proxy):
    try:
        response = requests.get("http://httpbin.org/get", proxies={"http": f"http://{proxy}"}, timeout=3, verify=False)
        if "X-Forwarded-For" in response.text:
            return "Transparent"
        elif "Via" in response.text:
            return "Anonymous"
        else:
            return "Elite (High Anonymity)"
    except requests.RequestException:
        return "Unknown"

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
        response = requests.get(test_url, proxies=proxy_dict, timeout=10, verify=False)
        if response.status_code == 200:
            anonymity = check_anonymity(proxy)
            return proxy, anonymity, True  
    except:
        pass
    return None, None, False  

def check_proxies(proxies, proxy_type, max_workers=50):  
    working_proxies = []
    anonymity_counts = {
        "Elite (High Anonymity)": 0,
        "Anonymous": 0,
        "Transparent": 0,
        "Unknown": 0
    }
    live_count = 0
    death_count = 0
    
    if not proxies:
        return working_proxies
    
    total = len(proxies)
    tested = 0
    
    
    print(f"{Fore.YELLOW}Press Control + C at any time to save and exit.{Fore.RESET}")
    print()  
    
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render_output():
       
        clear_console()
        print(f"{Fore.YELLOW}Press Control + C at any time to save and exit.{Fore.RESET}")
        print() 
        print(f"{Fore.YELLOW}Loaded Count: {total} Proxies")
        print(f"Anonymity Counts:")
        print(f"  Elite (High Anonymity): {anonymity_counts['Elite (High Anonymity)']}")
        print(f"  Anonymous: {anonymity_counts['Anonymous']}")
        print(f"  Transparent: {anonymity_counts['Transparent']}")
        print(f"  Unknown: {anonymity_counts['Unknown']}")
        print(f"Live: {live_count} | Death: {death_count}")
        progress = int((tested) / total * 30)
        percentage = int((tested) / total * 100)
        print(f"[{'=' * progress}{' ' * (30 - progress)}] {percentage}% ({tested}/{total})")
    
   
    render_output()
    
    def check_and_update(proxy):
        nonlocal tested, live_count, death_count
        proxy_result, anonymity, is_live = check_proxy(proxy, proxy_type)
        tested += 1
        if is_live:
            live_count += 1
            working_proxies.append((proxy_result, anonymity))
            anonymity_counts[anonymity] += 1
        else:
            death_count += 1
        
       
        render_output()
        
        return proxy_result, anonymity
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_and_update, proxy) for proxy in proxies]
        try:
            for future in as_completed(futures):  
                future.result()  
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Program interrupted. Saving working proxies...")
            save_proxies(working_proxies, proxy_type)
            print(f"{Fore.YELLOW}Proxies saved. Press 'exit' to quit or continue using the tool.{Fore.RESET}")
    
    
    print(f"\n{Fore.GREEN}Found {len(working_proxies)} working {proxy_type.upper()} proxies out of {total} checked.")
    print(f"{Fore.CYAN}Final Anonymity Counts:")
    for level, count in anonymity_counts.items():
        print(f"{Fore.CYAN}  {level}: {Fore.YELLOW}{count}")
    
    return working_proxies
