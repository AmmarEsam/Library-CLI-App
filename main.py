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
    '''Return user_id if user is logined and FALSE if not'''

    bd_query = "SELECT customer_id FROM customer where is_logined = TRUE LIMIT 1"
    cur.execute(bd_query)
    fetched_id = cur.fetchone()
    if fetched_id == None:
        return False
    else:
        return fetched_id[0]
    
    
def log_out():
    '''Make loged in status false'''
    bd_query = "UPDATE customer SET is_logined = FALSE where is_logined = TRUE"
    cur.execute(bd_query)

def login_check():
    '''Returns tuple (user_id, first_name) if user loged in and FALSE if not'''
    global cur
    status = is_logined(cur)
    if not status:
        message = "Please sing in for this operation!"
        typer.secho(message, fg=typer.colors.RED)
        start()
    else: 
        cur.execute(f"SELECT first_name FROM customer WHERE customer_id = {status}")
        first_name = cur.fetchone()[0]
        return (status, first_name)


console = Console()
app = typer.Typer()
cur = connect()

@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n
        You can execute command '--help' to see the possible commands
        Enter [r]egister for signing up
        Enter [l]et me in for signing in.
        Press other button for continue without signing in''', fg=typer.colors.GREEN)
    
    global cur
    answer = input().strip().lower()
    if answer in ['r', 'reg', 'register']:
        typer.secho("Let's sign you up!", fg=typer.colors.BLUE)
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')
        sign_up(username, password)
    if answer in ['l', 'let']:
        typer.secho("Let's sign you in!", fg=typer.colors.BLUE)
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')
        sign_in(username, password)
    else:
        pass
    close()

@app.command("sign_up")
def sign_up(username: str, password: str):
    global cur
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
    global cur
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



@app.command('add_book')
def add_book():
    '''It asks for the details of the book: name, author, # pages and genre. 
    Then it adds the book to the database.'''
    
    global cur
    tupl = login_check()
    
    first_name = tupl[1]
    
    message_require = f"Hi, {first_name}!\n Please enter the required book info to add!"
    typer.secho(message_require, fg=typer.colors.BLUE)
    name = input('Name: ').strip()
    author = input('Author: ').strip()
    num_of_pages = input('# Pages: ').strip()
    genre = input('Genre: ').strip()

    check_quire = f"SELECT book_id, book_name, author FROM book\
        WHERE book_name = '{name}' AND author = '{author}'"
    cur.execute(check_quire)
    fetched_book = cur.fetchone()
    if fetched_book == None:
        add_query = f"INSERT INTO book (book_name, author, pages, genre)\
                VALUES ('{name}', '{author}', '{num_of_pages}', '{genre}')"
        cur.execute(add_query)
    else:
        book_id_db = fetched_book[0]
        count_quere = f"UPDATE book SET num_of_copy = num_of_copy + 1 WHERE book_id = '{book_id_db}'"
        cur.execute(count_quere)
    typer.secho('Successfully added a copy of book!', fg=typer.colors.GREEN)
    close()

def is_available(book_id):
    '''Returns T (F) if amount of borrowed books less than amount of copy'''
    global cur
    fetch_query = "SELECT count(*) FROM borrowing WHERE book_id = 1"
    cur.execute(fetch_query)
    borrowed_amount = cur.fetchone()[0]

    num_of_copy_query = "SELECT num_of_copy FROM book"
    cur.execute(num_of_copy_query)
    num_of_copy = cur.fetchone()[0]

    if borrowed_amount < num_of_copy:
        return True
    else:
        return False


@app.command('borrow_book')
def borrow_book(book_id):
    '''Takes BOOK ID as an argument. 
    If this book is available, saves the data as the signed-in user borrowed the book 
    and reduces the available amount of the book. 
    If not available, then logs an error message saying this book 
    is not available.'''

    global cur
    tupl = login_check()
    user_id, first_name = tupl


    if is_available(book_id):
        borrow_query = f"INSERT INTO public.borrowing \
            (customer_id, book_id)\
            VALUES ('{user_id}', '{book_id}')"
        cur.execute(borrow_query)
        message = f"Hi {first_name}! You borrowed book {book_id}"
        typer.secho(message, fg=typer.colors.GREEN)
    else:
        message = f"Sorry, {first_name}. Book {book_id} is not available!\
                Try again later."
        typer.secho(message, fg=typer.colors.BLUE)


if __name__ == "__main__":
    print(is_available(56))