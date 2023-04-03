import psycopg2
from datetime import datetime, timedelta


def connect():
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost", database="library_project", user="postgres", password=123456
        )
        conn.autocommit = True
        print('Connected to the PostgreSQL database Successfully...')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    
