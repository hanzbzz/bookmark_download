import os
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
                host=os.environ["DB_URL"],
                database=os.environ["DB_DB"],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'])
    return conn

def insert_to_login(conn, username, action):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO login (username, action) VALUES (%s, %s)", (username, action))
    conn.commit()
    cur.close()