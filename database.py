import psycopg2

def connect():
    '''This function will check if the database exist, if not it will create the database and connect to it'''
    
    db_name = 'library_cli'
    password = '123456'  # change server password to connect
    
    global conn
    global cur
    conn = None
    
    try:
        
        conn = psycopg2.connect(
            host="localhost", user="postgres", password=f'{password}'
        )
        cur = conn.cursor()
        conn.autocommit = True
        cur.execute(
            f"select exists(SELECT datname FROM pg_database WHERE lower(datname)=lower('{db_name}'))")
        database = cur.fetchall()
        
        if database[0][0] == False:
            print("Creating the database ....")
            
            cur.execute(
                f"CREATE DATABASE {db_name} WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';")
            conn.close()
            
            conn = psycopg2.connect(
                host="localhost", database=f'{db_name}', user="postgres", password=f'{password}'
            )
            cur = conn.cursor()
            conn.autocommit = True
            cur.execute(open(f"{db_name}.sql", "r").read())
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        conn = psycopg2.connect(
            host="localhost", database=f'{db_name}', user="postgres", password=f'{password}'
        )
        cur = conn.cursor()
        conn.autocommit = True
        return cur
    
def close():
    if conn is not None:
        conn.close()
#____________COMMON METHODS_____________________:

def is_username_exists(name):
    
    querry = 'SELECT username FROM customer'
    cur.execute(querry)
    users_list = [i[0] for i in cur.fetchall()]
    if name in users_list:
        return True
    else:
        return False
    
