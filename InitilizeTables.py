import psycopg2 as pg
from psycopg2 import sql

# load sql file
def load_sql_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
# connect to db, with environment variables
def connect_to_db():
    conn = pg.connect(
        # host= os.getenv('DB_HOST'),
        host="host",
        port= "port",
        database= "database",
        user= 'user',
        password= 'password'
    )
    return conn

# initilize tables
def create_table(conn):
    cur = conn.cursor()
    loaded_sql = load_sql_file('InitializeTables.sql')
    cur.execute(loaded_sql)
    conn.commit()
    cur.close()

if __name__ == '__main__':

    conn = connect_to_db()
    print(conn)
    create_table(conn)
    print("Table initialized successfully.")
    conn.close()