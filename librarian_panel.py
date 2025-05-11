# ---- librarian_panel.py ---------
from rich import print
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from rich.panel import Panel
from rich import box
# ---- formatting -------
from singleton_db import Database
from factory import UserFactory, LibraryItemFactory

console = Console()

def librarian_panel(facade):
    db = facade.db

    while True:
        print(Panel.fit("[bold white]Librarian Panel[/bold white]", style="bold blue"))
        console.print(
            "[bold blue]1.[/] Add User        [bold blue]2.[/] Remove User\n"
            "[bold blue]3.[/] Add Item        [bold blue]4.[/] Remove Item\n"
            "[bold blue]5.[/] Analytics       [bold blue]6.[/] Return",
        )

        choice = input("Enter choice:")

        if choice == "1":

            print(Panel.fit("[bold green]Add New User[/bold green]", style="green"))
            roles = ["student", "faculty", "researcher", "guest", "professor"]
            role_cols = Columns(
                [f"[bold]{i+1}. {role.capitalize()}[/]" for i, role in enumerate(roles)],
                    equal=True, expand=True
            )
            print(Panel(role_cols, title="Available Roles", title_align="left"))

            while True:
                try:
                    choice = int(input("Enter role number (1-5): "))
                    if 1 <= choice <= 5:
                        role = roles[choice-1] 
                        break
                    else:
                        print("[bold red]Invalid choice! Please enter 1-4[/bold red]")
                except ValueError:
                    print("[bold red]Invalid input! Please enter a number[/bold red]")

            print(f"Selected role: {role.capitalize()}")
            user_id = input("Enter user ID: ").strip()
            name = input("Enter full name: ").strip()

            if db.find_user(user_id):
                print(f"[bold red]Error: User ID {user_id} already exists![/bold red]")
                continue

            try:
                new_user = UserFactory.create_user(
                    role=role,
                    user_id=user_id,
                    name=name
                )
                
                db.add_user(new_user)
                console.print(f"\n[bold green]Successfully added {role} user: {name} (ID: {user_id})[/bold green]")
                console.input("\n")

            except ValueError as e:
                print(f"[bold red]Error creating user: {str(e)}[/bold red]")
                print("Valid roles: student, faculty, researcher, guest")

        elif choice == "2":  # Remove User
            user_id = input("Enter user ID to remove: ")
            user = db.find_user(user_id)
            if user and db.remove_user(user_id):
                console.print(f"[bold green] User {user_id}: {user.name} removed successfully[/bold green]")
                console.input("\n")
            else:
                console.print("[bold red]Failed to remove user (either not found or has borrowed items)[/bold red]")

        elif choice == "3": # Add Book
            print(Panel.fit("[bold green]Add New Library Item[/bold green]", style="green"))
                
            item_types = ["ebook", "printed", "researchpaper", "audiobook"]
            type_cols = Columns(
                [f"[bold]{i+1}. {typ.capitalize()}[/]" for i, typ in enumerate(item_types)],
                equal=True, expand=True
            )
            print(Panel(type_cols, title="Item Types", title_align="left"))

            while True:
                try:
                    choice = int(console.input("\n[cyan]Select item type (1-4): [/]"))
                    if 1 <= choice <= 4:
                        item_type = item_types[choice-1]
                        break
                    console.print("[blink][bold red]⚠ Invalid choice! Please enter 1-4[/][/]")
                except ValueError:
                    console.print("[blink][bold red]⚠ Please enter a number![/][/]")

            item_id = input("Enter item ID:")
            if db.find_item(item_id):
                console.print(Panel.fit("[bold red] Item ID already exists![/]", style="red"))
                continue

            title = input("Title: ").strip()
            author = input("Author: ").strip()

            # Type-specific attributes
            metadata = {}
            if item_type == "ebook":
                metadata["format"] = input("Format (PDF/EPUB/MOBI): ").upper()
                metadata["genre"] = input("Genre: ")
            elif item_type == "printed":
                metadata["pages"] = int(input("Number of pages: "))
                metadata["genre"] = input("Genre: ")
            elif item_type == "audiobook":
                metadata["duration"] = int(input("Duration (minutes): "))

            try:
                new_item = LibraryItemFactory.create_item(
                    item_type=item_type,
                    item_id=item_id,
                    title=title,
                    author=author,
                    **metadata
                )
                db.add_item(new_item)
                console.print(f"[bold green]Successfully added {item_type}: {title}[/bold green]")
                
            except Exception as e:
                console.print(f"[bold red]Error creating item: {str(e)}[/bold red]")

        elif choice == "4":  # Remove Book
            item_id = input("Enter item ID to remove: ")
            book = db.find_item(item_id)
            if db.remove_item(item_id):
                console.print(f"[bold green]ID : {item_id} {book.title} removed successfully[/bold green]")
                console.input("\n")
            else:
                console.print("[bold red]Failed to remove item (either not found or currently checked out)[/bold red]")

        elif choice == "5":
            while True:
                console.clear()
                print(Panel.fit("[bold cyan]Library Analytics[/bold cyan]", style="blue"))
                
                stats = Columns([
                    f"[bold]Total Items:[/] {db.total_items}",
                    f"[bold]Available:[/]   {db.available_items}",
                    f"[bold]Borrowed:[/]    {db.borrowed_items}",
                    f"[bold]Reserved:[/]    {db.reserved_items}",
                    f"[bold]Users:[/]       {db.total_users}"
                ], expand=True)
                print(Panel(stats, title="Quick Stats", border_style="cyan", padding=(1, 0, 0, 0)))

                options = Panel(
                    "[bold blue]1.[/] User Stats      [bold blue]2.[/] Borrow Stats\n"
                    "[bold blue]3.[/] All Items       [bold blue]4.[/] Transactions\n"
                    "[bold blue]5.[/] Return",
                    title="Analytics Options"
                )
                print(options)

                sub_choice = input("\nEnter choice:")

                if sub_choice == "1":
                    table = Table(title="User Statistics", show_header=True, box=box.SQUARE)
                    table.add_column("ID", style="cyan", width=10)
                    table.add_column("Name", width=25)
                    table.add_column("Type",width=15)
                    for user in db.users:
                        table.add_row(user.user_id, user.name[:20]+'...' if len(user.name)>20 else user.name, user.role)
                    print(table)

                elif sub_choice == "2":
                    table = Table(title="Borrow Statistics", show_header=True, box=box.SQUARE)
                    table.add_column("ID", style="cyan", width=10)
                    table.add_column("Name", width=25)
                    table.add_column("Type", width=15)
                    table.add_column("Borrowed",width=10)
                    for user in db.users:
                        table.add_row(
                            user.user_id, 
                            user.name[:20]+'...' if len(user.name)>20 else user.name,
                            user.role,
                            str(len(user.borrowed_items))
                        )
                    print(table)

                elif sub_choice == "3":
                    table = Table(title="Library Catalog", show_header=True, box=box.SQUARE)
                    table.add_column("ID", style="cyan", width=8)
                    table.add_column("Type", width=12)
                    table.add_column("Title", width=30)
                    table.add_column("Author", width=25)
                    table.add_column("Status", style="green", width=15)
                    for item in db.items:
                        status = type(item.state).__name__.replace("State", "")
                        table.add_row(
                            item.item_id,
                            item.item_type,
                            item.title[:25]+'...' if len(item.title)>25 else item.title,
                            item.author[:20]+'...' if len(item.author)>20 else item.author,
                            f"[green]{status}[/]" if status == "Available" else f"[yellow]{status}[/]" if status == "Reserved" else f"[red]{status}[/]"
                        )
                    print(table)

                elif sub_choice == "4":
                    table = Table(title="Recent Transactions", show_header=True, box=box.SQUARE)
                    table.add_column("Date", style="cyan", width=12)
                    table.add_column("User ID", width=10)
                    table.add_column("Item ID", width=10)
                    table.add_column("Action", width=15)
                    for t in reversed(db.transactions[-10:]):
                        date = t['timestamp'].split('T')[0]
                        table.add_row(date, t['user_id'], t['item_id'], t['action'])
                    print(table)

                elif sub_choice == "5":
                    break

                console.input("\n[bold italic]Press Enter to continue...[/]")
                

        elif choice == "6": # Back
            break