import psycopg2

def connect():
    global conn
    conn = None
    try:
        # print('Connecting to the PostgreSQL database...')
        
        conn = psycopg2.connect(
            host="localhost", database="library_v2", user="postgres", password='1234'
        )
        global cur
        cur = conn.cursor()
        conn.autocommit = True
        # print('Connected to the PostgreSQL database Successfully...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
            return cur
    
def close():
    if conn is not None:
        conn.close()
        print('Conn closed')

#____________COMMON METHODS_____________________:

def is_username_exists(name):
    
    querry = 'SELECT username FROM customer'
    cur.execute(querry)
    users_list = [i[0] for i in cur.fetchall()]
    if name in users_list:
        return True
    else:
        return False
    
