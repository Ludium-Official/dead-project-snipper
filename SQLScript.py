import psycopg2 as pg
from psycopg2 import sql
import pandas as pd
import getpass

class SQL_tools():
    # connect to db, with environment variables
    def __init__(self):
        your_host = getpass.getpass("host: ")
        your_port = input("port: ")
        your_user = input("user:")
        your_password = getpass.getpass("password: ")
        your_db = getpass.getpass("dbName:")

        conn = pg.connect(
            host= your_host,
            port= your_port,
            database= your_db,
            user= your_user,
            password= your_password,
        )
        self.conn = conn
        return self.conn
    
    # load sql file
    def load_sql_file(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    # create table
    def create_table(self):
        conn = self.conn
        cur = conn.cursor()
        loaded_sql = SQL_tools.load_sql_file('CreateTables.sql')
        cur.execute(loaded_sql)
        conn.commit()
        cur.close()

    def insert_to_parent(self, table: str, data: dict):
        """
        부모 테이블에 데이터를 삽입하고, 생성된 기본 키를 반환합니다.
        :param table: 부모 테이블의 이름
        :param data: 삽입할 데이터가 포함된 딕셔너리
        :return: 생성된 기본 키 (id)
        """
        conn = self.conn
        cur = conn.cursor()
        columns = sql.SQL(', ').join(map(sql.Identifier, data.keys()))
        values = sql.SQL(', ').join(map(sql.Literal, data.values()))
        
        insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id").format(
            table=sql.Identifier(table),
            columns=columns,
            values=values
        )
        cur.execute(insert_query)
        # 생성된 기본 키를 가져옵니다.
        generated_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return generated_id
    
    def insert_to_child(self, table: str, data: dict):
        """
        자식 테이블에 데이터를 삽입합니다.
        :param table: 자식 테이블의 이름
        :param data: 삽입할 데이터가 포함된 딕셔너리 (부모 테이블의 기본 키를 포함해야 함)
        """
        conn = self.conn
        cur = conn.cursor()
        columns = sql.SQL(', ').join(map(sql.Identifier, data.keys()))
        values = sql.SQL(', ').join(map(sql.Literal, data.values()))
        
        insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(table),
            columns=columns,
            values=values
        )
        cur.execute(insert_query)
        conn.commit()
        cur.close()


    # def insert_to_db(self, table : str, data : dict):
    #     conn = self.conn
    #     cur = conn.cursor()
    #     insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
    #         table=sql.Identifier(table),
    #         columns=sql.SQL(', ').join(map(sql.Identifier, data.keys())),
    #         values=sql.SQL(', ').join(map(sql.Literal, data.values()))
    #     )
    #     cur.execute(insert_query)
    #     conn.commit()
    #     cur.close()

    # read_data
    def read_to_db(self):
        conn = self.conn
        cur = conn.cursor()

        read_query = sql.SQL("SELECT * FROM projects")
        cur.execute(read_query)
        result = conn.fetchall()
        column_names = [desc[0] for desc in conn.description]

        df = pd.DataFrame(result, columns=column_names)
        conn.commit()
        cur.close()

        return df

    def pick_project_to_db(self,project_name : str):
        conn = self.conn
        cur = conn.cursor()

        cur.execute("SELECT * FROM projects WHERE project_name = %s", (project_name,))
        result = conn.fetchall()
        column_names = [desc[0] for desc in conn.description]

        df = pd.DataFrame(result, columns=column_names)
        conn.commit()
        cur.close()

        return df
    
    def read_X_data(self, project_id : str):
        conn = self.conn
        cur = conn.cursor()

        cur.execute(
            """SELECT * 
            FROM xaccounts XA
            JOIN xactivityLog XAL ON XA.account_id = XAL.account_id
            WHERE XA.project_id = %s;
            """, (project_id,))
        result = conn.fetchall()
        
        column_names = [desc[0] for desc in conn.description]
        df = pd.DataFrame(result, columns=column_names)
        conn.commit()
        cur.close()

        return df

    def read_git_data(self, project_id : str):
        conn = self.conn
        cur = conn.cursor()

        cur.execute(
            """SELECT * 
            FROM githubrepos GR
            JOIN githubrepoactivitylog GRAL ON GR.github_repo_id = GRAL.github_repo_id
            WHERE GR.project_id = %s;
            """, (project_id,))
        result = conn.fetchall()
        
        column_names = [desc[0] for desc in conn.description]

        df = pd.DataFrame(result, columns=column_names)
        conn.commit()
        cur.close()

        return df
    
    def read_chain_data(self, project_id : str):
        conn = self.conn
        cur = conn.cursor()

        cur.execute(
            """SELECT * 
            FROM nearaddress NA
            JOIN onchainactivitylog OCA ON NA.near_address = OCA.near_address
            WHERE NA.project_id = %s;
            """, (project_id,))
        result = conn.fetchall()
        column_names = [desc[0] for desc in conn.description]
        df = pd.DataFrame(result, columns=column_names)
        conn.commit()
        cur.close()

        return df

    

# if __name__ == '__main__':
#     conn = connect_to_db()
#     create_table(conn)
#     conn.close()
