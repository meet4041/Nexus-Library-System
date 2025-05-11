# ------------ main.py ------------
from strategy import KeywordSearchStrategy as kes
from singleton_db import Database
from facade import LibraryFacade
from richtext import print_all
from dummy_data import generate_dummy_data
from librarian_panel import librarian_panel
from user_panel import user_panel

# ------------ formatting ------------
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def main():
    db = Database()
    facade = LibraryFacade(db)

    facade.set_search_strategy(kes())
    
    if not db.users:
        generate_dummy_data()

    print_all()

    while True:

        console.print(Panel.fit("[bold white]Nexus Library Interface[/bold  white]", 
                      style="bold blue"))
        
        console.print("[bold white] Main Menu[/bold white]\n",
                "[bold white]1.[/] Librarian Panel\n",
                "[bold white]2.[/] User Panel\n",
                "[bold white]3.[/] Exit System\n"
        )


        choice = input("Enter choice: ")

        if choice == "1":
            console.clear()
            librarian_panel(facade)
        elif choice == "2":
            console.clear()
            user_panel(facade)
        elif choice == "3":
            print(Panel.fit("[bold green]Thank you for using Nexus Library![/bold green]", style="green"))
            break
        else:
            console.print("\n[blink][bold red]⚠ Invalid choice! Please enter 1-3[/][/]\n")

if __name__ == "__main__":
    main()