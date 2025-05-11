from datetime import datetime
from strategy import KeywordSearchStrategy as kes, AuthorSearchStrategy as aus, GenreSearchStrategy as gs

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

def user_panel(facade):
    db = facade.db

    # Authenticate User
    console.print(Panel.fit("[bold blue]User Authentication[/bold blue]"))
    user_id = input("Enter User ID: ").strip()
    user = db.find_user(user_id)

    if not user:
        console.print("[bold red]⚠ User not found![/bold red]")
        return

    console.clear()
    console.print(Panel.fit(f"[bold green]{user.role.capitalize()} user: {user.name}[/bold green]", style="green"))

    while True:
        console.print(Panel.fit(f"[bold white]{user.name} User Panel[/bold white]", style="bold blue"))

        console.print(
            "[bold blue]1.[/] Borrow Book        [bold blue]2.[/] Return Book\n"
            "[bold blue]3.[/] Show Borrowed      [bold blue]4.[/] Search Books\n"
            "[bold blue]5.[/] Undo Last Action   [bold blue]6.[/] Back"
        )

        choice = input("\nEnter choice: ").strip()

        if choice == "1":   # Borrow Book
            item_id = input("\nEnter Item ID: ").strip()
            if facade.borrow_item(user_id, item_id):
                console.print(f"\n[bold green]Successfully borrowed item: {item_id}[/bold green]")
                console.input("\n")
                console.clear()
            else:
                console.print(f"\n[bold red]Failed to borrow item: {item_id}[/bold red]")
                console.input("\n")
                console.clear()

        elif choice == "2": # Return Book
            item_id = input("Enter Item ID: ").strip()
            return_date = input("Enter Return Date (YYYY-MM-DD): ").strip()
            try:
                return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
                if facade.return_item(user_id, item_id, return_date):
                    console.print(f"\n[bold green]Successfully returned item: {item_id}[/bold green]")
                    console.input("\n")
                    console.clear()
                else:
                    console.print(f"\n[bold red]Failed to return item: {item_id}[/bold red]")
                    console.input("\n")
                    console.clear()
            except ValueError:
                console.print("\n[bold red]Invalid date format. Use YYYY-MM-DD.[/bold red]")

        elif choice == "3": # Show Borrowed Books
            items = facade.get_user_borrowed_items(user_id)

            if not items:
                console.print("[bold yellow]No items currently borrowed.[/bold yellow]")
                console.input("\n")
                console.clear()
                continue

            table = Table(title="Borrowed Items",box=box.SQUARE)
            table.add_column("ID", style="cyan")
            table.add_column("Title", width=30)
            table.add_column("Type", width=15)

            for item in items:
                table.add_row(item.item_id, item.title[:25] + "..." if len(item.title) > 25 else item.title, item.item_type)

            console.print(table)

        elif choice == "4": # Search Books
            console.print(
                Panel.fit(
                    "[bold blue]Search Options[/bold blue]\n"
                    "1. By Keyword     2.By Author\n"
                    "3. By Genre       4.List All Items",
                    title="Search",
                )
            )

            search_choice = input("Enter choice: ").strip()

            if search_choice == "1":
                keyword = input("Enter keyword: ")
                results = facade.search_items(keyword, strategy=kes())

            elif search_choice == "2":
                author = input("Enter author name: ")
                results = facade.search_items(author, strategy=aus())

            elif search_choice == "3":
                genre = input("Enter genre: ")
                results = facade.search_items(genre, strategy=gs())

            elif search_choice == "4":
                results = db.items

            else:
                console.print("\n[bold red]Invalid choice in search menu.[/bold red]")
                continue

            if not results:
                console.print("\n[bold white]No items found.[/bold white]")
                continue

            table = Table(title="Search Results")
            table.add_column("ID", style="cyan", width=10)
            table.add_column("Title", width=30)
            table.add_column("Author", width=25)
            table.add_column("Status", style="green", width=15)

            for item in results:
                status = type(item.state).__name__.replace("State", "")
                table.add_row(
                    item.item_id,
                    item.title[:27] + "..." if len(item.title) > 27 else item.title,
                    item.author[:23] + "..." if len(item.author) > 23 else item.author,
                    status
                )

            console.print(table)

        elif choice == "5": # Undo last action
            if facade.undo_last_action():
                console.print("\n[bold green]✔ Last action undone successfully.[/bold green]")
            else:
                console.print("\n [bold white]⚠ Nothing to undo.[/bold white]")

        elif choice == "6": # Back
            break

        else:
            console.print("[blink][bold red]⚠ Invalid choice! Please select from 1–6.[/][/]")
