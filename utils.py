import os
import sys
import time
from colorama import Fore, Back, Style, init

init(autoreset=True)

BANNER = Fore.GREEN + '''
  ___                   _____       _ _       
 | _ \\_ _ ___ __ ___ _ / ____|     (_) |      
 |  _/ \'_/ _ \\ \\ //_| (___  _   _ _| |_ ___ 
 |_| |_| \\___/_\\_\\\\(_) \\___ \\| | | | | __/ _ \\
               |___/  ____) | |_| | | ||  __/
                     |_____/ \\__,_|_|\\__\\___|
                     
''' + Style.BRIGHT + Fore.CYAN + " BETA VERSION 2.0.0 " + Style.RESET_ALL

LOADING_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

def animated_loading(message, duration=3):
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        frame = LOADING_FRAMES[i % len(LOADING_FRAMES)]
        sys.stdout.write(f'\r{Fore.CYAN}{frame} {message}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * (len(message) + 10) + '\r')
    sys.stdout.flush()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

def show_help():
    print(Fore.GREEN + '''
┌─────────────────────────────────────────────────────────────────────┐
│                      AVAILABLE COMMANDS                              │
├─────────────────────────────────────────────────────────────────────┤
│  scrape all & check         - Scrape and check all proxy types       │
│  scrape all                - Scrape all proxy types                  │
│  scrape <type>             - Scrape specific proxy type              │
│                              (http, socks4, socks5)                  │
│  check <type>              - Check scraped proxies                   │
│  auto <type>               - Auto-scrape and check in one step       │
│  save <type>               - Save proxies to file                    │
│  show stats                - Display proxy statistics                │
│  clear                     - Clear the screen                        │
│  help                      - Show this help message                  │
│  exit                      - Exit the tool                           │
└─────────────────────────────────────────────────────────────────────┘
    ''')
