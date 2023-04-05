import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from database import connect, close, is_username_exists
from datetime import datetime, timedelta

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
        # print(f'{first_name} is loged in')
        return (status, first_name)


console = Console()
app = typer.Typer()
cur = connect()

@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n
        
        Enter [r]egister for signing up
        Enter [l]et me in for signing in.
        Press other button for continue without signing in''', fg=typer.colors.GREEN)
    # log_out()
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
        main_menu()
    


@app.command("main_menu")
def main_menu():
    global cur
    status = is_logined(cur)
    if not status: 
       typer.secho(f'''
        1 - Search a book by Name
        2 - Search a book by Author
        3 - Recently Added Books
        4 - Most Read Books
        5 - Most Favorite Books
        6 - Most Read Genres
        7 - Most Read Authors
        8 - Exit
        \n ''', fg=typer.colors.BLUE)
       answer = input("Enter the number of the command:").strip()
       if answer == '1':
           search_by_name()
       elif answer == '2':
           search_by_author()
       elif answer == '3':
           recently_added()
       elif answer == '4':
           pass
       elif answer == '5':
           pass
       elif answer == '6':
           pass
       elif answer == '7':
           pass
       elif answer == '8':
           close()
       else:
        typer.secho('Invalid input', fg=typer.colors.RED)
        main_menu()
    else :
       typer.secho(f'''
        1  - Search a book by Name
        2  - Search a book by Author
        3  - Recently Added Books
        4  - Most Read Books
        5  - Most Favorite Books
        6  - Most Read Genres
        7  - Most Read Authors
        8  - Add Book
        9  - Borrow Book
        10 - Return Book
        11 - Mark Book as Read
        12 - Add Book to Favorite
        13 - Display All my Books
        14 - Statistics
        15 - Exit
        \n ''', fg=typer.colors.BLUE)
       answer = input("Enter the number of the command:").strip()
       if answer == '1':
           search_by_name()
       elif answer == '2':
           search_by_author()
       elif answer == '3':
           recently_added()
       elif answer == '4':
           pass
       elif answer == '5':
           pass
       elif answer == '6':
           pass
       elif answer == '7':
           pass
       elif answer == '8':
           add_book()
       elif answer == '9':
           borrow_book()
       elif answer == '10':
           return_book()
       elif answer == '11':
           mark_read()
       elif answer == '12':
           fav_book()
       elif answer == '13':
           my_books()
       elif answer == '14':
           pass
       elif answer == '15':
           close()
       
       else:
        typer.secho('Invalid input', fg=typer.colors.RED)
        main_menu()
        
        
    
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
            main_menu()
        else:
            typer.secho("Wrong password", fg=typer.colors.RED)
            
    else: 
        typer.secho('''This username doesn't exist!
                        Please enter an existing username!''',\
                        fg=typer.colors.RED)
        
    


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


@app.command("search_by_name")
def search_by_name():
    typer.secho("Searching a book by name!", fg=typer.colors.BLUE)
    book_name = input('Enter book name: ').strip()
    c = 0
    cur = connect()
    select_queries = (f"""SELECT book_id,book_name,author,pages,genre
                      from book  
                      where book_name LIKE '%{book_name}%'""")
    cur.execute(select_queries)
    data = cur.fetchall()
    if data:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=10)
        table.add_column("Book ID", style="dim", min_width=10, justify=True)
        table.add_column("Name", style="dim", min_width=10, justify=True)
        table.add_column("Author", style="dim", min_width=10, justify=True)
        table.add_column("Pages", style="dim", min_width=10, justify=True)
        table.add_column("Genre", style="dim", min_width=10, justify=True)
        table.add_column("Availability", style="dim",
                         min_width=10, justify=True)
        for i in range(0, len(data)):
            c += 1
            availability = is_available(data[i][0])
            table.add_row(f'{c}', f'{data[i][0]}',
                          f'{data[i][1]}', f'{data[i][2]}', f'{data[i][3]}', f'{data[i][4]}', f'{availability}')

        console.print(table)
        typer.secho(
            'Press 1 to search again, OR any button to go back to Main menu', fg=typer.colors.BLUE)
        answer = input().strip()
        if answer == '1':
            search_by_name()
        else:
            main_menu()
    else:
        typer.secho('No book is found', fg=typer.colors.RED)
        typer.secho('Press 1 to search again, OR any button to go back to Main menu', fg=typer.colors.BLUE)
        answer = input().strip()
        if answer =='1':
            search_by_name()
        else:
            main_menu()
        


@app.command("search_by_author")
def search_by_author():
    typer.secho("Searching a book by author!", fg=typer.colors.BLUE)
    author_name = input('Enter Author name: ').strip()
    c = 0
    cur = connect()
    select_queries = (f"""SELECT book_id,book_name,author,pages,genre
                      from book  
                      where author LIKE '%{author_name}%'""")
    cur.execute(select_queries)
    data = cur.fetchall()
    if data:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=10)
        table.add_column("Book ID", style="dim", min_width=10, justify=True)
        table.add_column("Name", style="dim", min_width=10, justify=True)
        table.add_column("Author", style="dim", min_width=10, justify=True)
        table.add_column("Pages", style="dim", min_width=10, justify=True)
        table.add_column("Genre", style="dim", min_width=10, justify=True)
        table.add_column("Availability", style="dim",
                         min_width=10, justify=True)
        for i in range(0, len(data)):
            c += 1
            availability = is_available(data[i][0])
            table.add_row(f'{c}', f'{data[i][0]}',
                          f'{data[i][1]}', f'{data[i][2]}', f'{data[i][3]}', f'{data[i][4]}', f'{availability}')

        console.print(table)
        typer.secho(
            'Press 1 to search again, OR any button to go back to Main menu', fg=typer.colors.BLUE)
        answer = input().strip()
        if answer == '1':
            search_by_author()
        else:
            main_menu()
    else:
        typer.secho('No Author is found', fg=typer.colors.RED)
        typer.secho(
            'Press 1 to search again, OR any button to go back to Main menu', fg=typer.colors.BLUE)
        answer = input().strip()
        if answer == '1':
            search_by_author()
        else:
            main_menu()


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
    
# ______________________USERS___METHODS__________________________________________######
@app.command('history')
def show_history():
    '''Shows last 10 borrowed books.'''

    global cur
    tupl = login_check()
    user_id, first_name = tupl

    query = f"SELECT b.book_id, b.book_name, b.author, br.borowing_date, br.is_returned FROM book b \
            LEFT JOIN borrowing br USING (book_id) WHERE br.customer_id = {user_id} ORDER BY is_returned \
            LIMIT 10"
    cur.execute(query)
    data = cur.fetchall()

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=4)
    table.add_column("Book ID", style="dim", width=7)
    table.add_column("Name", style="dim", width=23)
    table.add_column("Author", style="dim", width=16)
    table.add_column("Borrowing date", style="dim", width=16)
    table.add_column("Returned", style="dim", width=7, justify= True)

    count = 1

    for row in data:
        table.add_row(f"{count}", f"{row[0]}", f"{row[1]}", f"{row[2]}", f"{row[3]}", f"{row[4]}")
        count += 1

    print(f'Hey {first_name}! HERE ARE LAST 10 BOOKS YOU BORROWED')
    console.print(table)
    
    message = "If you want to return book, press [r]"
    typer.secho(message, fg=typer.colors.GREEN)
    answer = input()
    if answer in 'rR':
        return_book()
    else:
        main_menu()

    close()


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
        WHERE book_name = '{name.title()}' AND author = '{author.title()}'"
    cur.execute(check_quire)
    fetched_book = cur.fetchone()
    if fetched_book == None:
        last_id_query = "SELECT max(book_id) FROM book"
        cur.execute(last_id_query)
        last_id = cur.fetchone()[0]

        add_query = f"INSERT INTO book (book_id, book_name, author, pages, genre, num_of_copy, add_date)\
                VALUES ({last_id+1}, '{name}', '{author}', '{num_of_pages}', '{genre}', 0, CURRENT DATE)"
        cur.execute(add_query)
    else:
        book_id_db = fetched_book[0]
        count_quere = f"UPDATE book SET num_of_copy = num_of_copy + 1 WHERE book_id = '{book_id_db}'"
        cur.execute(count_quere)
    typer.secho('Successfully added a copy of book!', fg=typer.colors.GREEN)
    close()

def is_book_exists(book_id: Optional[int] = False):
    if not book_id:
        book_id = int(input('Enter id of book, please...   '))

    book_exists_query = f"SELECT count(*) FROM book WHERE book_id = {book_id}"
    cur.execute(book_exists_query)
    book_exists = cur.fetchone()[0]
    if book_exists:
        return True
    else:
        message = "Book not exists in this library!"
        typer.secho(message, fg=typer.colors.RED)
        return False

def is_available(book_id: Optional[int] = False):
    '''Returns T (F) if amount of borrowed books less than amount of copy'''

    if not book_id:
        book_id = int(input('Enter id of book, please...   '))

    global cur
    fetch_query = f"SELECT count(*) FROM borrowing WHERE book_id = {book_id}"
    cur.execute(fetch_query)
    borrowed_amount = cur.fetchone()[0]

    num_of_copy_query = "SELECT num_of_copy FROM book"
    cur.execute(num_of_copy_query)
    num_of_copy = cur.fetchone()[0]

    book_exists = is_book_exists(book_id)

    if book_exists:
        if borrowed_amount < num_of_copy:
            return True
        else:
            return False
    close()


@app.command('borrow_book')
def borrow_book(book_id: Optional[int] = False):
    '''Takes BOOK ID as an argument. 
    If this book is available, saves the data as the signed-in user borrowed the book 
    and reduces the available amount of the book. 
    If not available, then logs an error message saying this book 
    is not available.'''

    if not book_id:
        book_id = int(input('Enter id of book, please...   '))

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
    close()

@app.command('return_book')
def return_book(book_id: Optional[int] = False):
    '''This command takes BOOK ID as an argument. 
    If the signed-in user borrowed the book previously, 
    it saves the data as this user returned the book.'''

    if not book_id:
        book_id = int(input('Enter id of book, please...   '))

    global cur
    tupl = login_check()
    user_id, first_name = tupl

    # let's chek if this book was borrowed bu signed-in user
    borrow_check_query = f"SELECT count(*) FROM borrowing WHERE book_id = {book_id} AND customer_id = {user_id} AND is_returned = FALSE"
    cur.execute(borrow_check_query)
    borrow_check = cur.fetchone()[0]
    if borrow_check:
        # let's add to is_read
        react_read = input(f'Have you read book {book_id}? [Y]es or [N]o   ')
        if react_read in 'yY':
            is_read_flag = True
        else: 
            is_read_flag = False
        # let's add to favorite
        react_fav = input(f'Would you like to add book {book_id} to you favorite books? [Y]es or [N]o   ')
        if react_fav in 'Yy':
            is_fav_flag = True
        else:
            is_fav_flag = False

        return_query = f"UPDATE borrowing SET return_date = CURRENT_DATE, is_returned = TRUE,\
                is_read = {is_read_flag}, is_favorite = {is_fav_flag} \
                WHERE customer_id = {user_id} AND book_id = {book_id}"
        cur.execute(return_query)
        
        message = f"Hi {first_name}! You retirned book {book_id}"
        typer.secho(message, fg=typer.colors.GREEN)

    else:
        message = f"Hi {first_name}! It looks like you didn't borrow the book or you've already return it."
        typer.secho(message, fg=typer.colors.RED)
    close()

@app.command("mark_read")
def mark_read(book_id: Optional[int] = 0):
    '''This command takes BOOK ID as an argument. 
    It marks this book as “read” for the signed-in user.'''

    if not book_id:
        book_id = int(input('Enter id of book, please...   '))

    global cur
    tupl = login_check()
    user_id, first_name = tupl

    read_query = f"INSERT INTO public.borrowing \
                (customer_id, book_id, is_read, borowing_date) \
                    VALUES ({user_id}, {book_id}, true, NULL)"
    cur.execute(read_query)
    message = f"Dear {first_name}. You marked book 5 as read"
    typer.secho(message, fg= typer.colors.GREEN)
    close()

@app.command("fav_nook")
def fav_book(book_id: Optional[int] = False):
    '''This command takes BOOK ID as an argument. 
    It adds this book to signed-in userʼs favorites.'''

    if not book_id:
        book_id = int(input('Enter id of book, please...   '))

    global cur
    tupl = login_check()
    user_id, first_name = tupl

    read_query = f"INSERT INTO public.borrowing \
                (customer_id, book_id, is_favorite, borowing_date) \
                    VALUES ({user_id}, {book_id}, true, NULL)"
    cur.execute(read_query)
    message = f"Dear {first_name}. You marked book 5 as read"
    typer.secho(message, fg= typer.colors.GREEN)
    close()

@app.command("my_books")
def my_books():
    '''This command doesnʼt take any arguments. 
    It displays the books read and favorited by the signed-in user.'''

    global cur
    tupl = login_check()
    user_id, first_name = tupl

    def fetch_table(column):
        query = f"SELECT DISTINCT b.book_id, b.book_name, b.author, b.pages, b.genre FROM book b\
                INNER JOIN borrowing br USING(book_id)\
                WHERE br.customer_id = {user_id} AND br.{column} = TRUE"
        cur.execute(query)
        return cur.fetchall()

    # READ table
    read_data = fetch_table('is_read')

    #create a table:
    table_read = Table(show_header=True, header_style="bold blue")
    table_read.add_column("#", style="dim", width=4)
    table_read.add_column("Book ID", style="dim", width=7)
    table_read.add_column("Name", style="dim", width=23)
    table_read.add_column("Author", style="dim", width=16)
    table_read.add_column("# Pages", style="dim", width=7)
    table_read.add_column("Genre", style="dim", width=10)
    table_read.add_column("Abaliability", style="dim", min_width=10, justify=True)

    count = 1

    for row in read_data:
        table_read.add_row(f"{count}", f"{row[0]}", f"{row[1]}", f"{row[2]}", f"{row[3]}", f"{row[4]}", f"{is_available(row[0])}")
        count += 1

    print(f'Hey {first_name}! HERE ARE BOOKS YOU READ')
    console.print(table_read)

    # FAVORITE table:
    fav_data = fetch_table('is_favorite')

    #create a table:
    table_fav = Table(show_header=True, header_style="bold blue")
    table_fav.add_column("#", style="dim", width=4)
    table_fav.add_column("Book ID", style="dim", width=7)
    table_fav.add_column("Name", style="dim", width=23)
    table_fav.add_column("Author", style="dim", width=16)
    table_fav.add_column("# Pages", style="dim", width=7)
    table_fav.add_column("Genre", style="dim", width=10)
    table_fav.add_column("Abaliability", style="dim", min_width=10, justify=True)


    count = 1
    for row in fav_data:
        table_fav.add_row(f"{count}", f"{row[0]}", f"{row[1]}", f"{row[2]}", f"{row[3]}", f"{row[4]}", f"{is_available(row[0])}")
        count += 1

    print('AND YOUR FAVORITE BOOKS')
    console.print(table_fav)

    close()


if __name__ == "__main__":
    add_book()
