from colorama import Fore, Style
from utils import clear_screen, show_help, BANNER
from scraper import scrape_from_all_sources, scrape_proxies
from checker import check_proxies
from saver import save_proxies
from flood import flood
from KD import kd_function
from spoof import spoof_function


from saver import save_proxies

def auto_scrape_and_check(proxy_type):
    print(f"{Fore.YELLOW}Auto-scraping and checking {proxy_type.upper()} proxies...")
    
    
    proxies = scrape_from_all_sources(proxy_type)
    if not proxies:
        print(f"{Fore.RED}No proxies scraped. Skipping {proxy_type.upper()}.")
        return
    
    working_proxies = check_proxies(proxies, proxy_type)
    if not working_proxies:
        print(f"{Fore.RED}No working {proxy_type.upper()} proxies found.")
        return
    
    save_proxies(working_proxies, proxy_type)

def scrape_and_save(proxy_type):
    print(f"{Fore.YELLOW}Scraping {proxy_type.upper()} proxies...")
    
    proxies = scrape_from_all_sources(proxy_type)
    print(f"{Fore.GREEN}Scraped {len(proxies)} {proxy_type.upper()} proxies.")
    
    save_proxies([(proxy, "Unknown") for proxy in proxies], proxy_type)
    print(f"{Fore.GREEN}Saved {proxy_type.upper()} proxies.")

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
                
                if proxy_type == 'all':
                    if len(args) > 2 and args[2] == '&' and args[3] == 'check':
                        # Scrape all & check
                        for ptype in ['http', 'socks4', 'socks5']:
                            auto_scrape_and_check(ptype)
                    else:
                        # Scrape all
                        for ptype in ['http', 'socks4', 'socks5']:
                            scrape_and_save(ptype)
                elif proxy_type in ['http', 'socks4', 'socks5']:
                    if len(args) > 2 and args[2] == '&' and args[3] == 'check':
                        # Scrape specific type & check
                        auto_scrape_and_check(proxy_type)
                    else:
                        # Scrape specific type
                        scrape_and_save(proxy_type)
                else:
                    print(f"{Fore.RED}Error: Invalid proxy type. Use 'http', 'socks4', 'socks5', or 'all'.")
            
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
