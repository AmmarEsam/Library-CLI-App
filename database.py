import psycopg2

def connect():
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost", database="library_project", user="postgres", password='postgres'
        )
        cur = conn.cursor()
        conn.autocommit = True
        print('Connected to the PostgreSQL database Successfully...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    
