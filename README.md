# ProxySuite 2.0.0

![ProxySuite](https://cdn.discordapp.com/attachments/1342194903521955862/1348331124220231831/image.png?ex=67cf12b6&is=67cdc136&hm=9cf8c5dc571b864048c814536e3e6ce070578ea5e4c443c6ca4204081d5d9abb&)

------

## Features

- **Scrape all & check**: Scrapes all proxy types and automatically checks them.
- **Scrape all**: Scrapes all available proxy types (HTTP, SOCKS4, SOCKS5).
- **Scrape `<type>`**: Scrapes a specific proxy type (`scrape http`, `socks4`, or `socks5`).
- **Check `<type>`**: Checks the validity and responsiveness of scraped proxies.
- **Auto `<type>`**: Automates scraping and checking in one step.

### New Features:
- **Added new proxy sources**: Includes `proxyjudge`, `github`, `proxyscan`, and `openproxylist`
- **Anonymity checking**: Proxies are checked for anonymity levels (`Elite`, `Anonymous`, `Transparent`, `Unknown`)
- **Improved error handling**: Gracefully handles connection issues and skips problematic sources
- **Real-time progress bar**: Displays checking progress and anonymity counts dynamically
- **Increased worker threads**: Faster checking with `max_workers=50`
- **Auto-save on `Control + C`**: Saves working proxies without exiting the program
- **Grouped proxies by anonymity level**
- **Cleared and refreshed console**: Ensures clean and updated output

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NotAdl22/ProxySuite
   cd ProxySuite
   pip install -r requirements.txt
   python main.py
