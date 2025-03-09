import requests
from utils import animated_loading
from colorama import Fore
import warnings


requests.packages.urllib3.disable_warnings()

PROXY_SOURCES = {
    'proxyscrape': {
        'http': 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'socks4': 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all',
        'socks5': 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all'
    },
    'proxyjudge': {
        'http': 'https://www.proxy-list.download/api/v1/get?type=http',
        'https': 'https://www.proxy-list.download/api/v1/get?type=https',
    },
    'github': {
        'http': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    },
    'proxyscan': {
        'http': 'https://www.proxyscan.io/download?type=http',
    },
    'openproxylist': {
        'http': 'https://api.openproxylist.xyz/http.txt',
    }
}

def scrape_proxies(proxy_type, source='proxyscrape'):
    url = PROXY_SOURCES.get(source, {}).get(proxy_type)
    if not url:
        print(f"{Fore.RED}Error: Invalid proxy type or source.")
        return []
    
    proxies = []
    animated_loading(f"Scraping {proxy_type.upper()} proxies from {source}...", 1.5)
    
    try:

        response = requests.get(url, timeout=20, verify=False)
        if response.status_code == 200:
            if source in ['proxyscrape', 'github', 'openproxylist']:
                proxies = [proxy.strip() for proxy in response.text.splitlines() if proxy.strip()]
            elif source in ['proxyjudge', 'proxyscan']:
                proxies = [proxy.strip() for proxy in response.text.split('\r\n') if proxy.strip()]
        else:
            print(f"{Fore.RED}Error: Failed to fetch proxies from {source}. Status code: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}Error scraping {proxy_type} proxies from {source}: {str(e)}")
    
    return proxies

def scrape_from_all_sources(proxy_type):
    all_proxies = []
    for source in PROXY_SOURCES.keys():
        proxies = scrape_proxies(proxy_type, source)
        all_proxies.extend(proxies)
    
    unique_proxies = list(set(all_proxies))
    return unique_proxies
