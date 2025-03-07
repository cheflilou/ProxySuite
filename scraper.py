import requests
from utils import animated_loading
from colorama import Fore

PROXY_SOURCES = {
    'proxyscrape': {
        'http': 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'socks4': 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all',
        'socks5': 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all'
    },
    'geonode': {
        'http': 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,https',
        'socks4': 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4',
        'socks5': 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5'
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
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            if source == 'proxyscrape':
                proxies = [proxy.strip() for proxy in response.text.splitlines() if proxy.strip()]
            elif source == 'geonode':
                data = response.json()
                proxies = [f"{item['ip']}:{item['port']}" for item in data.get('data', [])]
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