from xmlrpc.client import boolean

from rich.console import Console
from rich.text import Text
import argparse



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='url to scan', required=True)
    parser.add_argument('-w', '--wordlist', type=str, help='wordlist to use', required=True)
    parser.add_argument('-r', '--robots', action='store_true', help='include robots.txt file', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity', default=False)
    args = parser.parse_args()

    hello()

    if args.robots:
        ...



def import_from_dict():
    ...


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


def robots():
    ...

if __name__ == '__main__':
    console = Console()
    main()