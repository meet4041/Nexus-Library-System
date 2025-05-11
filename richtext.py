from rich.console import Console
from rich.text import Text
import time
hs = '\u200A'
ts = '\u2009'

console = Console()

def print_logo():
    console.print("\n    [bold white]|\\  /|[/bold white]")
    console.print(f"    [bold white]| \\/ |[/bold white]")
    console.print("    [bold white]\\_||_/[/bold white]\n")


def print_nexus_text():
    nexus_text = Text()
    nexus_text.append("n", style="bold white")
    nexus_text.append("e", style="bold yellow")
    nexus_text.append("x", style="bold red")     
    nexus_text.append("u", style="bold green")  
    nexus_text.append("s", style="bold white")
    
    console.print("    ", nexus_text)

def print_library_text():
    console.print("   \u2009[bold black]Library [/bold black]\n")

def print_all():
    console.clear()
    print_logo()
    print_nexus_text()
    print_library_text()


if __name__ == "__main__":
    print_all()
