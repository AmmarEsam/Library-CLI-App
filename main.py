import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from database import connect, close

console = Console()

app = typer.Typer()

is_loggined = False

#____________COMMON METHODS_____________________:
def is_username_exists(name):
    querry = 'SELECT username FROM customer'
    cur.execute(querry)
    users_list = [i[0] for i in cur.fetchall()]
    if name in users_list:
        return True
    else:
        return False
    
#____________END_COMMON_METHODS__________________

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
        sign_up(username, password)
    else:
        query = f"INSERT INTO customer (first_name, username, password) \
                VALUES ('{username.title()}', '{username}', '{password}')"
        cur.execute(query)
        typer.secho(f"Nice that you are signing up!", fg=typer.colors.GREEN)
        typer.secho('You can add your info for delivery later using function --help',\
            fg=typer.colors.BLUE)
    close()


@app.command("sign_in")
def sign_in(username: str, password: str):
    connect()
    querry = f"SELECT password FROM customer WHERE username = '{username}'"
    cur.execute(querry)
    password_db = cur.fetchone()
    print(f'pass = {password_db}')
    if is_username_exists(username):
        if password in password_db:
            global is_loggined
            is_loggined = True
            typer.secho("Successfully signed up!", fg=typer.colors.GREEN)
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
    start()