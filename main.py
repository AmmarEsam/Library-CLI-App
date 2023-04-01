import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from database import connect, close, is_username_exists

def set_logined_true(username, cur):
    '''Set True for logined user in Customer table'''
    status_query = f"UPDATE customer SET is_logined = TRUE WHERE username = '{username}'"
    cur.execute(status_query)

def is_logined(cur):
    '''Return True if user is logined'''
    bd_query = "SELECT username FROM customer where is_logined = TRUE LIMIT 1"
    cur.execute(bd_query)
    status = cur.fetchone()
    if status:
        return True


console = Console()
app = typer.Typer()

@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n
        You can execute command '--help' to see the possible commands
        Enter [r]egister for signing up
        Enter [l]et me in for signing in''', fg=typer.colors.GREEN)
    
    global cur
    cur = connect()

    answer = input().strip().lower()
    if answer in ['r', 'reg', 'register']:
        typer.secho("Let's sign you up!", fg=typer.colors.BLUE)
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')
        sign_up(username, password)
    else:
        typer.secho("Let's sign you in!", fg=typer.colors.BLUE)
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')
        sign_in(username, password)
    close()

@app.command("sign_up")
def sign_up(username: str, password: str):
    connect()
    if is_username_exists(username):
        err_message = 'This username already exists! Try another username'
        typer.secho(err_message, fg=typer.colors.RED)
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')
        sign_up(username, password)
    else:
        query = f"INSERT INTO customer (first_name, username, password) \
                VALUES ('{username.title()}', '{username}', '{password}')"
        cur.execute(query)
        set_logined_true(username, cur)
        typer.secho(f"Successfully signed up and signied in!", fg=typer.colors.GREEN)
        typer.secho('You can add your info for delivery later using function --help',\
            fg=typer.colors.BLUE)
    close()


@app.command("sign_in")
def sign_in(username: str, password: str):
    cur = connect()
    querry = f"SELECT password FROM customer WHERE username = '{username}'"
    cur.execute(querry)
    password_db = cur.fetchone()
    if is_username_exists(username):
        if password in password_db:
            typer.secho("Successfully signed in!", fg=typer.colors.GREEN)
            set_logined_true(username, cur)
            is_logined(cur)
        else:
            typer.secho("Wrong password", fg=typer.colors.RED)
    else: 
        typer.secho('''This username doesn't exist!
                        Please enter an existing username!''',\
                        fg=typer.colors.RED)
    close()


# Example function for tables, you can add more columns/row.

@app.command("display_table")
def display_table():
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Column 1", style="dim", width=10)
    table.add_column("Column 2", style="dim", min_width=10, justify=True)

    table.add_row('Value 1', 'Value 2')
    table.add_row('Value 3', 'Value 4')
    table.add_row('Value 5', 'Value 6')

    console.print(table)


if __name__ == "__main__":
    app()