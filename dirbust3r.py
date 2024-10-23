import requests
from rich.console import Console
from rich.text import Text
import argparse



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='url to scan', required=True)
    parser.add_argument('-w', '--wordlist', type=str, help='wordlist to use')
    parser.add_argument('-r', '--robots', action='store_true', help='include robots.txt file', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity', default=False)
    args = parser.parse_args()

    hello()

    pages = []
    if args.wordlist:
        pages = import_from_dict(args.wordlist)


    if args.robots:
        robots_pages = robots(args.url)



def import_from_dict(dictionary: str) -> list:
    pages = []

    with open(dictionary, 'r') as f:
        for line in f:
            pages.append(line.strip())

    return pages


def hello():
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
    console.print("made by eliassen", style="bold red")


def robots(url: str) -> list:
    response = requests.get(f"http://{url}/robots.txt")
    dissallow = find_lines_with_substring(response.text, "Disallow: ")
    for i in range(len(dissallow)):
        dissallow[i] = dissallow[i].replace("Disallow: ", "").replace("/", "")
    return dissallow


def find_lines_with_substring(text, substring):
    lines = text.splitlines()
    matching_lines = [line for line in lines if substring in line]
    return matching_lines

if __name__ == '__main__':
    console = Console()
    main()