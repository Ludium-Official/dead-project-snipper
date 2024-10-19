import requests
import psycopg2 as pg

import json
from psycopg2.sql import SQL, Literal

def connect_to_db():
    conn = pg.connect(
        # host= os.getenv('DB_HOST'),
        host=your_host,
        port= your_port,
        database= your_database,
        user= your_user,
        password= your_password,
    )
    return conn

def close_connection(conn):
    conn.close()

def get_all_users():
    url = "https://dev.potlock.io/api/v1/accounts"

    data = []
    while url != None:
        response = requests.get(url)
        response_json = response.json()
        data += response_json['results']
        url = response_json['next']

    return data

def insert_to_project_table(conn, user_list):
    
    #upsert query
    insert_query = SQL(
        """
    INSERT INTO AllUsers (
        id, 
        total_donations_in_usd, 
        total_donations_out_usd, 
        total_matching_pool_allocations_usd, donors_count, 
        near_social_profile_data
    )
    
    VALUES (%s, %s, %s, %s, %s, %s)
    
    ON CONFLICT (id)
    
    DO UPDATE SET 
        total_donations_in_usd = EXCLUDED.total_donations_in_usd,
        total_donations_out_usd = EXCLUDED.total_donations_out_usd,
        total_matching_pool_allocations_usd = EXCLUDED.total_matching_pool_allocations_usd,
        donors_count = EXCLUDED.donors_count,
        near_social_profile_data = EXCLUDED.near_social_profile_data;
    """
    )
    
    with conn.cursor() as cur:
        # to adapt uuid type, this line is necessary
        for user in user_list:
            if user['near_social_profile_data'] != None:
                json_near_social_profile = json.dumps(user['near_social_profile_data'])

                # users values except near_social_profile_data is list(user.values())[:-1]
                cur.execute(insert_query, list(user.values())[:-1] + [json_near_social_profile])
            else:
                cur.execute(insert_query, list(user.values()))
        conn.commit()


def main():
    conn = connect_to_db()
    print("[info] Connected to DB")
    user_list = get_all_users()
    print("[info] Got all users :", len(user_list))
    insert_to_project_table(conn, user_list)
    print("[info] Inserted all users to the table")
    close_connection(conn)
    print("[info] Connection closed")

if __name__ == "__main__":
    main()


