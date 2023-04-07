import typer
import rich
from rich.console import Console
from rich.table import Table
from typing import Optional
from datetime import datetime, timedelta
from database import connect, close, is_username_exists


console = Console()
app = typer.Typer()
cur = connect()
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





@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n
        
        Enter [r]egister for signing up
        Enter [l]et me in for signing in.
        Press other button to continue without signing in''', fg=typer.colors.GREEN)
    log_out()
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
    '''Display the main menu of the app'''
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
          most_read_books()
       elif answer == '5':
           most_favorite_books()
       elif answer == '6':
           most_read_genre()
       elif answer == '7':
           most_read_author()
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
        15 - History
        16 - Exit
        \n ''', fg=typer.colors.BLUE)
       answer = input("Enter the number of the command:").strip()
       if answer == '1':
           search_by_name()
       elif answer == '2':
           search_by_author()
       elif answer == '3':
           recently_added()
       elif answer == '4':
           most_read_books()
       elif answer == '5':
           most_favorite_books()
       elif answer == '6':
           most_read_genre()
       elif answer == '7':
           most_read_author()
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
           statistics()
       elif answer == '15':
           show_history()  
       elif answer == '16':
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
            password = input('Enter your password: ')
            sign_in(username, password)
            
    else: 
        typer.secho('''This username doesn't exist!
                        Please enter an existing username!''',\
                        fg=typer.colors.RED)
        username = input('Enter your username: ').strip()
        password = input('Enter your password: ')
        sign_in(username, password)
        
    


@app.command("search_by_name")
def search_by_name():
    '''Search for the book by a given book name from the user'''
    
    typer.secho("Searching a book by name!", fg=typer.colors.BLUE)
    book_name = input('Enter book name: ').strip()
    c = 0
    cur = connect()
    select_queries = (f"""SELECT book_id,book_name,author,pages,genre
                      from book  
                      where LOWER(book_name) LIKE LOWER('%{book_name}%')""")
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
    '''Search for the book by a given author name from the user'''
    
    typer.secho("Searching a book by author!", fg=typer.colors.BLUE)
    author_name = input('Enter Author name: ').strip()
    c = 0
    cur = connect()
    select_queries = (f"""SELECT book_id,book_name,author,pages,genre
                      from book  
                      where LOWER(author) LIKE LOWER('%{author_name}%')""")
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


def recently_added(days: Optional[int] = 7):
    '''Display the recent added books based on the added date '''
    
    conn = connect()
    global cur
    now = datetime.now()
    start_date = now - timedelta(days=days)
    query = f"SELECT * FROM book WHERE add_date >= '{start_date}'"
    cur.execute(query)
    rows = cur.fetchmany(10)
    if not rows:
        typer.echo(f"No books were added in the last {days} days.")
        return
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", min_width=10, justify=True)
    table.add_column("Book ID", style="bold", min_width=10, justify=True)
    table.add_column("Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    table.add_column("Page", style="dim", min_width=10, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("Availability", style="dim", min_width=10, justify=True)
    count = 1
    for row in rows:
        table.add_row(
            f"{count}", f"{row[0]}", f"{row[2]}", f"{row[3]}", f"{row[4]}", f"{row[5]}",f"{is_available(row[0])}")
        count += 1
    console.print(table)
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()

# ______________________USERS___METHODS__________________________________________######
@app.command('history')
def show_history():
    '''Shows last 10 borrowed books.'''

    global cur
    tupl = login_check()
    user_id, first_name = tupl

    query = f"SELECT b.book_id, b.book_name, b.author, br.borowing_date, br.is_returned FROM book b \
            LEFT JOIN borrowing br USING (book_id) WHERE br.customer_id = {user_id} AND br.borowing_date IS NOT NULL ORDER BY is_returned \
            LIMIT 10"
    cur.execute(query)
    data = cur.fetchall()

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=4)
    table.add_column("Book ID", style="dim", width=7)
    table.add_column("Name", style="dim", width=23)
    table.add_column("Author", style="dim", width=16)
    table.add_column("Borrowing date", style="dim", width=16)
    table.add_column("Returned", style="dim", width=9, justify= True)

    count = 1

    for row in data:
        table.add_row(f"{count}", f"{row[0]}", f"{row[1]}", f"{row[2]}", f"{row[3]}", f"{row[4]}")
        count += 1

    print(f'Hey {first_name}! HERE ARE LAST 10 BOOKS YOU BORROWED')
    console.print(table)
    
    message = "If you want to return book, press [r] / [b]ack"
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
                VALUES ({last_id+1}, '{name.title()}', '{author.title()}', '{num_of_pages}', '{genre}', 1, CURRENT_DATE)"
        cur.execute(add_query)
    else:
        book_id_db = fetched_book[0]
        count_quere = f"UPDATE book SET num_of_copy = num_of_copy + 1 WHERE book_id = '{book_id_db}'"
        cur.execute(count_quere)
    typer.secho('Successfully added a copy of book!', fg=typer.colors.GREEN)
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()




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

    num_of_copy_query = f"SELECT num_of_copy FROM book WHERE book_id = {book_id}"
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
        typer.secho(message, fg=typer.colors.RED)
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()

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
    rate = 0
    valid_rate = False
    # let's chek if this book was borrowed bu signed-in user
    borrow_check_query = f"SELECT count(*) FROM borrowing WHERE book_id = {book_id} AND customer_id = {user_id} AND is_returned = FALSE"
    cur.execute(borrow_check_query)
    borrow_check = cur.fetchone()[0]
    if borrow_check:
        # let's add to is_read
        react_read = input(f'Have you read book {book_id}? [Y]es or [N]o   ')
        if react_read in 'yY':
            typer.secho("Please rate the book out of 5", fg=typer.colors.BLUE)
            while valid_rate is False:
             try:
              rate = float(input("Your rating:")) 
              if rate > 5:
               typer.secho("Rating should be less than 5",
                           fg=typer.colors.RED)
              else:
                 valid_rate = True
             except:
                typer.secho("Invalid input",
                            fg=typer.colors.RED)    
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
                is_read = {is_read_flag}, is_favorite = {is_fav_flag}, rating = {rate} \
                WHERE customer_id = {user_id} AND book_id = {book_id}"
        cur.execute(return_query)
        
        message = f"Hi {first_name}! You returned book {book_id}"
        typer.secho(message, fg=typer.colors.GREEN)

    else:
        message = f"Hi {first_name}! It looks like you didn't borrow the book or you've already return it."
        typer.secho(message, fg=typer.colors.RED)
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()

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
    message = f"Dear {first_name}. You marked book {book_id} as read"
    typer.secho(message, fg= typer.colors.GREEN)
    typer.secho(
        input('Press ENTER to go back to Main menu:'), fg=typer.colors.BLUE)
    main_menu()

@app.command("fav_book")
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
    message = f"Dear {first_name}. You marked book {book_id} as read"
    typer.secho(message, fg= typer.colors.GREEN)
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()

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
    table_fav.add_column("Avaliability", style="dim", min_width=10, justify=True)


    count = 1
    for row in fav_data:
        table_fav.add_row(f"{count}", f"{row[0]}", f"{row[1]}", f"{row[2]}", f"{row[3]}", f"{row[4]}", f"{is_available(row[0])}")
        count += 1

    print('AND YOUR FAVORITE BOOKS')
    console.print(table_fav)

    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()

@app.command("most_read_books")
def most_read_books():
 
    global cur
    fetch_query='SELECT book.*, COUNT(borrowing.book_id) AS times_read \
        FROM book \
        JOIN borrowing ON book.book_id = borrowing.book_id \
        GROUP BY book.book_id \
        ORDER BY times_read DESC;'
        
    cur.execute(fetch_query)
    
    
   
    most_read_books=cur.fetchmany(10)
    
   
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Book ID", style="dim", min_width=4, justify=True)
    table.add_column("ISBN", style="dim", min_width=7, justify=True)
    table.add_column("Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    # table.add_column("Pages", style="dim", min_width=5, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("times_read", style="dim",min_width=10, justify=True)
    
    for i in range(0, 9):
    
        try:
            table.add_row(f'{i+1}', f'{most_read_books[i][0]}',
                   f'{most_read_books[i][1]}', f'{most_read_books[i][2]}', 
                   f'{most_read_books[i][3]}',
                   f'{most_read_books[i][5]}', f'{most_read_books[i][9]}',)
            table.add_row('--','---','---','---','---','---','---')
        except:
            continue

    console.print(table)
    
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()
        
    return 

@app.command("most_favorite_books")
def most_favorite_books():
    global cur
    fetch_query = "SELECT book.*, SUM(CASE WHEN borrowing.is_favorite THEN 1 ELSE 0 END) AS times_favorited \
                    FROM book \
                    JOIN borrowing ON book.book_id = borrowing.book_id \
                    GROUP BY book.book_id \
                    ORDER BY times_favorited DESC;"
    cur.execute(fetch_query)
    most_favorite_books = cur.fetchmany(10)
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Book ID", style="dim", min_width=4, justify=True)
    table.add_column("ISBN", style="dim", min_width=7, justify=True)
    table.add_column("Name", style="dim", min_width=10, justify=True)
    table.add_column("Author", style="dim", min_width=10, justify=True)
    # table.add_column("Pages", style="dim", min_width=5, justify=True)
    table.add_column("Genre", style="dim", min_width=10, justify=True)
    table.add_column("times_fav", style="dim",min_width=10, justify=True)
    
    for i in range(0, 9):
    
        try:
            table.add_row(f'{i+1}', f'{most_favorite_books[i][0]}',
                   f'{most_favorite_books[i][1]}', f'{most_favorite_books[i][2]}', 
                   f'{most_favorite_books[i][3]}',
                   f'{most_favorite_books[i][5]}', f'{most_favorite_books[i][9]}',)
            table.add_row('--','---','---','---','---','---','---')
        except:
            continue

    console.print(table)
   
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()
        
    return 
    
@app.command("most_read_genre")
def most_read_genre():
    '''This command doesn’t take any arguments. It displays the 5 most-read genres.'''
    
    global cur
    fetch_query='''select book.genre, COUNT(borrowing.book_id) As total from book
    join borrowing on book.book_id = borrowing.book_id
    where borrowing.is_read = 'True' 
    group by book.genre 
    order by total desc;'''
        
    cur.execute(fetch_query)
    most_read_genre=cur.fetchmany(5)
   
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Genre", style="dim", min_width=4, justify=True)
    table.add_column("Count", style="dim", min_width=7, justify=True)
  
    for i in range(0, 4):    
        try:
            table.add_row(f'{i+1}', f'{most_read_genre[i][0]}',
                          f'{most_read_genre[i][1]}')
           
        except:
            continue

    console.print(table)
    
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()

@app.command("most_read_author")
def most_read_author():
    '''This command doesn’t take any arguments. It displays the 3 most-read authors.'''
    global cur
    fetch_query='''select book.author, COUNT(borrowing.book_id) As total from book
    join borrowing on book.book_id = borrowing.book_id
    where borrowing.is_read = 'True' 
    group by book.author 
    order by total desc;'''
        
    cur.execute(fetch_query)
    most_read_author=cur.fetchmany(3)
   
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=3)
    table.add_column("Author", style="dim", min_width=4, justify=True)
    table.add_column("Count", style="dim", min_width=7, justify=True)
  
    for i in range(0, 3):    
        try:
            table.add_row(f'{i+1}', f'{most_read_author[i][0]}',
                          f'{most_read_author[i][1]}')
           
        except:
            continue

    console.print(table)
    
    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()


@app.command("statistics")
def statistics():
    '''This command doesn’t take any arguments. It displays the following statistics for the signed-in user in
        a table: number of books you read, number of authors you read, number of genres you read, and number
        of total pages you read.'''
    global cur
    tupl = login_check()
    customr_id,first_name = tupl
    print(customr_id)
    query1 = f'''select COUNT(borrowing.borrow_id) As total from borrowing 
    join customer on customer.customer_id = borrowing.customer_id 
    where borrowing.customer_id = {customr_id} and borrowing.is_read='True'
    group by borrowing.customer_id 
    order by total desc ;'''
    cur.execute(query1)
    read_book = cur.fetchall()
    
    query2 = f''' select  SUM(count(DISTINCT book.author)) OVER() 
    from book
    join borrowing on book.book_id = borrowing.book_id
    where borrowing.is_read = 'True' AND borrowing.customer_id = {customr_id}
    group by book.author; '''
    cur.execute(query2)
    read_author = cur.fetchall()
    
    query3 = f''' select  SUM(count(DISTINCT book.genre)) OVER() 
    from book
    join borrowing on book.book_id = borrowing.book_id
    where borrowing.is_read = 'True' AND borrowing.customer_id = {customr_id}
    group by book.genre; '''
    cur.execute(query3)
    read_genre = cur.fetchall()
    
    query4 = f''' select  SUM(book.pages)  
    from book
    join borrowing on book.book_id = borrowing.book_id
    where borrowing.is_read = 'True' AND borrowing.customer_id = {customr_id}; '''
    cur.execute(query4)
    pages = cur.fetchall()
    
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Statistics", style="dim", width=20)
    table.add_column("Number", style="dim", min_width=4, justify=True)
    

    for i in range(0, 3):
        try:
            table.add_row("Books you read",f'{read_book[i][0]}')
            table.add_row("Authors you read", f'{read_author[i][0]}')
            table.add_row("Geners you read", f'{read_genre[i][0]}')
            table.add_row("Total pages you read", f'{pages[i][0]}')
        except:
            continue

    console.print(table)

    typer.secho(
        input('Press ENTER to go back to Main menu...'), fg=typer.colors.BLUE)
    main_menu()
if __name__ == "__main__":
    app()
