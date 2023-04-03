import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from database import connect
from datetime import datetime, timedelta

console = Console()

app = typer.Typer()

# Recently Added Books


@app.command("start")
def start():
    connect()
    typer.secho(f'''Welcome to Library CLI!\n\n
     You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)

@app.command("sign_up")
def sign_up(username: str):
    typer.echo(f"Nice that you are signing up!")

@app.command("display_table")
def display_table():
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Column 1", style="dim", width=10)
    table.add_column("Column 2", style="dim", min_width=10, justify=True)

    table.add_row('Value 1', 'Value 2')
    table.add_row('Value 3', 'Value 4')
    table.add_row('Value 5', 'Value 6')

    console.print(table)

@app.command("recently_added")
def recently_added(days: Optional[int] = 7):
    conn = connect()
    cur = conn.cursor()

    now = datetime.now()
    start_date = now - timedelta(days=days)

    query = f"SELECT * FROM books WHERE date_added >= '{start_date}'"
    cur.execute(query)
    rows = cur.fetchall()

    if not rows:
        typer.echo(f"No books were added in the last {days} days.")
        return

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Title", style="bold")
    table.add_column("Author", style="dim", width=20)
    table.add_column("Genre", style="dim", width=20)
    table.add_column("Date Added", style="dim", width=20)

    for row in rows:
        book_id, title, author, genre, date_added = row
        table.add_row(str(book_id), title, author, genre, str(date_added))

    console.print(table)
    conn.close()


if __name__ == "__main__":
    connect()
