import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
import argparse
import time
import logging
from typing import List, Dict, Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Dir_Hide")

class Dir_Hide:
    def __init__(
        self,
        base_url: str,
        wordlist_path: str,
        max_threads: int = 10,
        timeout: int = 5,
        user_agent: str = "Dir_Hide/1.0",
        proxy: Optional[Dict[str, str]] = None,
        extensions: Optional[List[str]] = None,
        output_file: Optional[str] = None,
    ):
        self.base_url = base_url
        self.wordlist_path = wordlist_path
        self.max_threads = max_threads
        self.timeout = timeout
        self.user_agent = user_agent
        self.proxy = proxy
        self.extensions = extensions if extensions else [""]
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        self.found_paths = []
        self.scan_start_time = None

    def load_wordlist(self) -> List[str]:
        """Загружает словарь для перебора."""
        try:
            with open(self.wordlist_path, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            logger.error(f"Failed to load wordlist: {e}")
            raise

    def check_path(self, path: str) -> Optional[str]:
        """Проверяет, существует ли путь на сервере."""
        for ext in self.extensions:
            full_path = f"{path}{ext}"
            url = urljoin(self.base_url, full_path)
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    proxies=self.proxy,
                )
                if response.status_code == 200:
                    logger.info(f"[+] Found: {url} (Status: {response.status_code})")
                    return url
                elif response.status_code == 403:
                    logger.warning(f"[!] Forbidden: {url} (Status: {response.status_code})")
                elif response.status_code == 404:
                    logger.debug(f"[-] Not Found: {url} (Status: {response.status_code})")
                else:
                    logger.info(f"[?] Unknown: {url} (Status: {response.status_code})")
            except requests.RequestException as e:
                logger.error(f"[!] Error: {url} - {e}")
        return None

    def run(self):
        """Запускает перебор директорий и файлов."""
        logger.info(f"[*] Starting directory brute-force on {self.base_url}")
        self.scan_start_time = time.time()

        wordlist = self.load_wordlist()
        logger.info(f"[*] Loaded {len(wordlist)} paths from the wordlist.")

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.check_path, path): path for path in wordlist}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.found_paths.append(result)

        self.scan_end_time = time.time()
        self.report()

    def report(self):
        """Генерирует отчет о результатах сканирования."""
        logger.info("[*] Scan complete.")
        logger.info(f"[*] Time taken: {self.scan_end_time - self.scan_start_time:.2f} seconds")
        if self.found_paths:
            logger.info("[+] Found paths:")
            for path in self.found_paths:
                logger.info(f"  - {path}")
            if self.output_file:
                with open(self.output_file, "w", encoding="utf-8") as file:
                    file.write("\n".join(self.found_paths))
                logger.info(f"[*] Results saved to {self.output_file}")
        else:
            logger.info("[-] No paths found.")

def main():
    parser = argparse.ArgumentParser(description="Advanced Directory Brute-Force Tool")
    parser.add_argument("url", help="Base URL to scan (e.g., http://example.com/)")
    parser.add_argument("wordlist", help="Path to the wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    parser.add_argument("-x", "--extensions", nargs="+", default=[""], help="File extensions to check (e.g., .php .html)")
    parser.add_argument("-o", "--output", help="Output file to save results")
    parser.add_argument("-p", "--proxy", help="Proxy to use (e.g., http://127.0.0.1:8080)")
    parser.add_argument("-T", "--timeout", type=int, default=5, help="Request timeout in seconds (default: 5)")
    parser.add_argument("-u", "--user-agent", default="Dir_Hide/1.0", help="Custom User-Agent string")
    args = parser.parse_args()

    proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    dir_buster = Dir_hide(
        base_url=args.url,
        wordlist_path=args.wordlist,
        max_threads=args.threads,
        timeout=args.timeout,
        user_agent=args.user_agent,
        proxy=proxy,
        extensions=args.extensions,
        output_file=args.output,
    )
    dir_buster.run()

if __name__ == "__main__":
    main()
