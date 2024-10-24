import requests
from rich.console import Console
from rich.text import Text
import argparse
from sys import exit
from rich.progress import Progress
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='url to scan', required=True)
    parser.add_argument('-w', '--wordlist', type=str, help='wordlist to use')
    parser.add_argument('-r', '--robots', action='store_true', help='include robots.txt file', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode', default=False)
    parser.add_argument('-t', '--threads', type=int, help='number of threads to use', default=5)

    args = parser.parse_args()

    hello()

    url = refactor_url(args.url)
    print_info(f"URL: {url}")

    ua = UserAgent()
    random_ua = ua.random

    headers = {
        "User-Agent": random_ua
    }

    if not check_url(url, headers):
        print_error(f"Invalid URL: {url}")
        exit(1)

    pages = []
    if args.wordlist:
        pages += import_from_dict(args.wordlist)

    if args.robots:
        pages += robots(url, headers)

    print_info(f"Pages: {len(pages)}")

    good_pages = []

    with Progress() as progress:
        task = progress.add_task("[red]Scanning...", total=len(pages))

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(check_page, page, url, headers): page for page in pages}

            for future in as_completed(futures):
                result = future.result()
                good_pages.extend(result)
                progress.update(task, advance=1)

    # remove duplicates
    good_pages = list(dict.fromkeys(good_pages))

    print_info(f"Good pages: {len(good_pages)}")
    for good_page in good_pages:
        print_good(f"Found: {good_page}")


extensions = ["", ".html", ".htm", ".xhtml", ".css", ".js", ".json", ".xml", ".php"]


def check_page(page, url, headers):
    local_good_pages = []
    for extension in extensions:
        new_url = f"{url}/{page}{extension}"
        if check_url(new_url, headers):
            local_good_pages.append(new_url)
    return local_good_pages


def import_from_dict(dictionary: str) -> list:
    pages = []

    with open(dictionary, 'r') as f:
        for line in f:
            pages.append(line.strip())

    return pages


def hello() -> None:
    logo_text = """
         _ _      _               _   _____      
      __| (_)_ __| |__  _   _ ___| |_|___ / _ __ 
     / _` | | '__| '_ \| | | / __| __| |_ \| '__|
    | (_| | | |  | |_) | |_| \__ \ |_ ___) | |   
     \__,_|_|_|  |_.__/ \__,_|___/\__|____/|_|                                        
    """
    logo_text_ = Text(logo_text)
    logo_text_.stylize("bold magenta")
    console.print(logo_text_)
    console.print("made by eliassen", style="bold cyan")


def robots(url: str, headers: dict) -> list:
    if check_url(f"{url}/robots.txt", headers):
        response = requests.get(f"{url}/robots.txt", headers=headers)
        robots_pages = find_lines_with_substring(response.text, "Disallow: ")
        allows_pages = find_lines_with_substring(response.text, "Allow: ")
        robots_pages.extend(allows_pages)
        for i in range(len(robots_pages)):
            robots_pages[i] = robots_pages[i].replace("Disallow: ", "").replace("Allow: ", "").replace("/", "").replace(
                "?", "").replace("*", "").strip()
        print(robots_pages)
        return robots_pages
    else:
        return []


def find_lines_with_substring(text: str, substring: str) -> list:
    lines = text.splitlines()
    matching_lines = [line for line in lines if substring in line]
    return matching_lines


def refactor_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http"):
        url = f"http://{url}"
    return url


def check_url(url: str, headers: dict) -> bool:
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def print_error(message: str) -> None:
    console.print(f"[-] {message}", style="bold red")


def print_good(message: str) -> None:
    console.print(f"[+] {message}", style="bold green")


def print_info(message: str) -> None:
    console.print(f"[i] {message}", style="bold yellow")


if __name__ == '__main__':
    console = Console()
    main()
