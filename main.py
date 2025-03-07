from colorama import Fore, Style
from utils import clear_screen, show_help, BANNER
from scraper import scrape_from_all_sources, scrape_proxies
from checker import check_proxies
from saver import save_proxies
from flood import flood
from KD import kd_function
from spoof import spoof_function

def auto_scrape_and_check(proxy_type):
    print(f"{Fore.YELLOW}Auto-scraping and checking {proxy_type.upper()} proxies...")
    
    proxies = scrape_from_all_sources(proxy_type)
    print(f"{Fore.GREEN}Scraped {len(proxies)} {proxy_type.upper()} proxies.")
    
    working_proxies = check_proxies(proxies, proxy_type)
    print(f"{Fore.GREEN}Found {len(working_proxies)} working {proxy_type.upper()} proxies.")
    
    save_proxies(working_proxies, proxy_type)
    print(f"{Fore.GREEN}Saved working {proxy_type.upper()} proxies.")

def main():
    try:
        clear_screen()
        show_help()
        
        while True:
            command = input(Fore.YELLOW + "\n┌──(" + Fore.GREEN + "ProxySuite" + Fore.YELLOW + ")-[" + Fore.CYAN + "BETA" + Fore.YELLOW + "]\n└─$ " + Style.RESET_ALL).strip().lower()
            args = command.split()
            
            if not args:
                continue
            
            main_cmd = args[0]
            
            if main_cmd == 'scrape':
                if len(args) < 2:
                    print(f"{Fore.RED}Error: Missing proxy type. Usage: scrape <type>")
                    continue
                
                proxy_type = args[1]
                source = 'proxyscrape'
                
                if len(args) > 3 and args[2] == '-s':
                    source = args[3]
                
                if proxy_type == 'all':
                    all_proxies = {}
                    for ptype in ['http', 'socks4', 'socks5']:
                        if source == 'all':
                            proxies = scrape_from_all_sources(ptype)
                        else:
                            proxies = scrape_proxies(ptype, source)
                        all_proxies[ptype] = len(proxies)
                        save_proxies(proxies, ptype)  # Save each type automatically
                    
                    print(f"{Fore.CYAN}────────────────── SCRAPING SUMMARY ──────────────────")
                    for ptype, count in all_proxies.items():
                        print(f"{Fore.CYAN}Proxy Type: {Fore.YELLOW}{ptype.upper()}")
                        print(f"{Fore.CYAN}Total Scraped: {Fore.YELLOW}{count}")
                        if count > 0:
                            print(f"{Fore.CYAN}Sample: {Fore.YELLOW}{proxies[0]}")
                        print(f"{Fore.CYAN}────────────────────────────────────────────")
                
                elif proxy_type in ['http', 'socks4', 'socks5']:
                    if source == 'all':
                        proxies = scrape_from_all_sources(proxy_type)
                    else:
                        proxies = scrape_proxies(proxy_type, source)
                    
                    save_proxies(proxies, proxy_type)  # Save automatically
                    
                    print(f"{Fore.CYAN}────────────────── SCRAPING SUMMARY ──────────────────")
                    print(f"{Fore.CYAN}Proxy Type: {Fore.YELLOW}{proxy_type.upper()}")
                    print(f"{Fore.CYAN}Source: {Fore.YELLOW}{source}")
                    print(f"{Fore.CYAN}Total Scraped: {Fore.YELLOW}{len(proxies)}")
                    if proxies:
                        print(f"{Fore.CYAN}Sample: {Fore.YELLOW}{proxies[0]}")
                    print(f"{Fore.CYAN}────────────────────────────────────────────")
                else:
                    print(f"{Fore.RED}Error: Invalid proxy type. Use 'http', 'socks4', 'socks5', or 'all'.")
            
            elif main_cmd == 'check':
                if len(args) < 2:
                    print(f"{Fore.RED}Error: Missing proxy type. Usage: check <type>")
                    continue
                
                proxy_type = args[1]
                
                if proxy_type in ['http', 'socks4', 'socks5']:
                    proxies = scrape_proxies(proxy_type)
                    working = check_proxies(proxies, proxy_type)
                    
                    save_proxies(working, proxy_type)  # Save working proxies automatically
                    
                    print(f"{Fore.CYAN}────────────────── CHECKING SUMMARY ──────────────────")
                    print(f"{Fore.CYAN}Proxy Type: {Fore.YELLOW}{proxy_type.upper()}")
                    print(f"{Fore.CYAN}Total Checked: {Fore.YELLOW}{len(proxies)}")
                    print(f"{Fore.CYAN}Working Proxies: {Fore.YELLOW}{len(working)}")
                    print(f"{Fore.CYAN}Success Rate: {Fore.YELLOW}{(len(working)/len(proxies)*100):.2f}%")
                    if working:
                        print(f"{Fore.CYAN}Sample: {Fore.YELLOW}{working[0]}")
                    print(f"{Fore.CYAN}────────────────────────────────────────────")
                else:
                    print(f"{Fore.RED}Error: Invalid proxy type. Use 'http', 'socks4', or 'socks5'.")
            
            elif main_cmd == 'auto':
                if len(args) < 2:
                    print(f"{Fore.RED}Error: Missing proxy type. Usage: auto <type>")
                    continue
                
                proxy_type = args[1]
                
                if proxy_type in ['http', 'socks4', 'socks5']:
                    auto_scrape_and_check(proxy_type)
                else:
                    print(f"{Fore.RED}Error: Invalid proxy type. Use 'http', 'socks4', or 'socks5'.")
            
            elif command == 'scrape all & check':
                for proxy_type in ['http', 'socks4', 'socks5']:
                    auto_scrape_and_check(proxy_type)
            
            elif main_cmd == 'save':
                if len(args) < 2:
                    print(f"{Fore.RED}Error: Missing proxy type. Usage: save <type>")
                    continue
                
                proxy_type = args[1]
                
                if proxy_type in ['http', 'socks4', 'socks5']:
                    proxies = scrape_proxies(proxy_type)
                    save_proxies(proxies, proxy_type)
                else:
                    print(f"{Fore.RED}Error: Invalid proxy type. Use 'http', 'socks4', or 'socks5'.")
            
            elif command == 'show stats':
                stats = {
                    'http': len(scrape_proxies('http')),
                    'socks4': len(scrape_proxies('socks4')),
                    'socks5': len(scrape_proxies('socks5'))
                }
                print(Fore.CYAN + "\n" + "─" * 60)
                print(Fore.CYAN + "PROXY STATISTICS")
                print(Fore.CYAN + "─" * 60)
                for ptype, count in stats.items():
                    if count > 0:
                        color = Fore.GREEN
                    else:
                        color = Fore.RED
                    print(f"{Fore.CYAN}  {ptype.upper()} Proxies: {color}{count}")
                print(Fore.CYAN + "─" * 60)
                total = sum(stats.values())
                print(f"{Fore.CYAN}  TOTAL: {Fore.GREEN if total > 0 else Fore.RED}{total}")
                print(Fore.CYAN + "─" * 60 + "\n")
            
            elif command == 'help':
                show_help()
            
            elif command == 'clear':
                clear_screen()
            
            elif command == 'exit':
                print(f"{Fore.GREEN}Exiting ProxySuite. Goodbye!")
                break
            
            else:
                print(f"{Fore.RED}Invalid command. Type 'help' to see the available commands.")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}")
    finally:
        print(f"{Fore.GREEN}Thanks for using ProxySuite!")

if __name__ == "__main__":
    main()