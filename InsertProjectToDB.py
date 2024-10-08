import PotLockCrawler
import psycopg2 as pg
import re

from datetime import datetime, timedelta
from psycopg2 import sql
import psycopg2.extras

from uuid import uuid4

# PostgreSQL 연결 정보
def connect_to_db():
    conn = pg.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return conn

def close_db_connection(conn):
    conn.close()

# Get Data with PotLockCrawler
def get_data(url):
    playwright, browser = PotLockCrawler.launch_browser()
    html = PotLockCrawler.get_page_content(url, browser)
    soup = PotLockCrawler.get_soup(html)
    github_link = PotLockCrawler.get_github_link(soup)
    twitter_link = PotLockCrawler.get_twitter_link(soup)
    members = PotLockCrawler.get_members(soup)
    PotLockCrawler.close_browser(playwright, browser)
    return github_link, twitter_link, members

def insert_to_db(conn, table : str, data : dict):
    cur = conn.cursor()
    insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
        table=sql.Identifier(table),
        columns=sql.SQL(', ').join(map(sql.Identifier, data.keys())),
        values=sql.SQL(', ').join(map(sql.Literal, data.values()))
    )
    cur.execute(insert_query)
    conn.commit()
    cur.close()

# insert into Project table
def insert_to_project_table(conn, url, uuid, created_time):

    insert_query = sql.SQL("INSERT INTO Projects (project_id, project_url, created_date) VALUES (%s, %s, %s);")
    
    with conn.cursor() as cur:
        # to adapt uuid type, this line is necessary
        psycopg2.extras.register_uuid() 
        cur.execute(insert_query, (uuid, url, created_time))
        connection.commit()

# insert into Github table
def insert_to_github_table(conn, uuid, github_link):

    if github_link is None:
        return
    
    parsed_github_link = parse_github_link(github_link)
    
    if isinstance(parsed_github_link, str):
        repo_uuid = uuid4()
        insert_query = sql.SQL("INSERT INTO GithubRepos (project_id, github_repo_id, owner_name) VALUES ( %s, %s, %s)")
    else:
        insert_query = sql.SQL("INSERT INTO GithubRepos (project_id, github_repo_id, owner_name, github_repo) VALUES ( %s, %s, %s, %s)")

    
    with conn.cursor() as cur:
        # to adapt uuid type, this line is necessary
        psycopg2.extras.register_uuid()
        if isinstance(parsed_github_link, str):
            cur.execute(insert_query, (uuid, repo_uuid, parsed_github_link))
        else:
            cur.execute(insert_query, (uuid, repo_uuid, parsed_github_link[-2], parsed_github_link[-1]))
        conn.commit()
    

# insert into Twitter table
def insert_to_twitter_table(conn, uuid, account_id):

    if account_id is None:
        return

    insert_query = sql.SQL("INSERT INTO XAccounts (project_id, account_id) VALUES (%s, %s)")
        
    with conn.cursor() as cur:
        # to adapt uuid type, this line is necessary
        psycopg2.extras.register_uuid()
        cur.execute(insert_query, (uuid, account_id))
        conn.commit()
    

# insert into Member table
def insert_to_member_table(conn, uuid, members : list):
    cur = conn.cursor()

    if members is None:
        return

    # to adapt uuid type, this line is necessary
    psycopg2.extras.register_uuid()

    members = parse_members(members)

    for member in members:
        insert_query = sql.SQL("INSERT INTO FundedMembers (project_id, name) VALUES ( %s, %s)")
        cur.execute(insert_query, (uuid, member))    
    conn.commit()
    cur.close()

# check whether the project is already in the database
def check_project_existence(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Projects WHERE project_url = %s", (url,))
    if cur.fetchone() is not None:
        return True
    else:
        return False
    
# parse the github link as owner and repo
def parse_github_link(github_link):
    if github_link is None:
        return None, None
    split_link = github_link.replace("https://github.com/", '')
    split_link = split_link.split('/')

    if len(split_link) < 2 :
        owner = split_link[-1]
        return owner
    else:
        owner = split_link[-2]
        repo = split_link[-1]
        return owner, repo

# extract account id from the url
def extract_account_id(url):
    pattern = r'[?&]accountId=([^&]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# parse the members data
def parse_members(members):
    if members is None:
        return None
    members = list(map(extract_account_id, members))
    return members

if __name__=="__main__":

    # PostgreSQL 연결 정보
    connection = connect_to_db()

    # Get Data with PotLockCrawler
    # url = "https://app.potlock.org/?tab=project&projectId=shitzu.sputnik-dao.near"
    # url = "https://app.potlock.org/?tab=project&projectId=yearofchef.near"
    # url = "https://app.potlock.org/?tab=project&projectId=theclan.near"
    url = "https://app.potlock.org/?tab=project&projectId=noondao.near"

    '''
    the url part can be replace by the csv file, or google spreadsheet or other sources
    '''
    
    # check whether the project is already in the database
    assert not check_project_existence(connection, url), "The project is already in the database."

    github_link, twitter_link, members = get_data(url)

    project_uuid = uuid4()
    current_date = datetime.now()

    # Insert Data to DB
    insert_to_project_table(connection, url, project_uuid, current_date)
    print("[INFO] Successfully inserted to Project table")
    
    # Insert Data to Github Table
    insert_to_github_table(connection, project_uuid, github_link)
    print("[INFO] Successfully inserted to Github table")

    # Insert Data to Twitter Table
    insert_to_twitter_table(connection, project_uuid, twitter_link)
    print("[INFO] Successfully inserted to Twitter table")

    # Insert Data to Member Table
    insert_to_member_table(connection, project_uuid, members)
    print("[INFO] Successfully inserted to Member table")

    # Close DB Connection
    close_db_connection(connection)
    print("DB Connection Closed.")

'''
to be tested project cases

1. project without github link
2. project without twitter link
3. project without members
4. project with multiple members
5. project with multiple members and github link
6. project with multiple members and twitter link
7. project with multiple members, github link, twitter link
'''