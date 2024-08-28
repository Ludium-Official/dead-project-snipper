import psycopg2 as pg
from psycopg2 import sql
import os

# load sql file
def load_sql_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
# connect to db, with environment variables
def connect_to_db():
    conn = pg.connect(
        host= your_host,
        port= your_port,
        database= your_db,
        user= yout_user,
        password= your_password,
    )
    return conn

# create table
def create_table(conn):
    cur = conn.cursor()
    loaded_sql = load_sql_file('CreateTables.sql')
    cur.execute(loaded_sql)
    conn.commit()
    cur.close()

if __name__ == '__main__':
    conn = connect_to_db()
    create_table(conn)
    conn.close()
