from rich.console import Console
from rich.text import Text
from rich.panel import Panel



def main():
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



if __name__ == '__main__':
    console = Console()
    hello()