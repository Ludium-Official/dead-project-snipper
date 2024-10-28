import requests
import psycopg2 as pg
import psycopg2.extras

import json
import traceback
import logger
from datetime import datetime
from psycopg2.sql import SQL, Literal
from uuid import uuid4

def connect_to_db():
    conn = pg.connect(
        # host= os.getenv('DB_HOST'),
        host=your_host,
        port= your_port,
        database= your_db,
        user= your_user,
        password= your_password,
    )
    return conn

def close_connection(conn):
    conn.close()

def in_usd_more_than_one(conn):
    select_sql = """
    SELECT 
        id, 
        near_social_profile_data::jsonb -> 'linktree' -> 'github' as github_link,
        near_social_profile_data::jsonb -> 'linktree' -> 'website' as website_link,
        near_social_profile_data::jsonb -> 'linktree' -> 'twitter' as twitter_link,
        near_social_profile_data::jsonb -> 'plGithubRepos'
    FROM AllUsers WHERE total_donations_in_usd > 0;
    """

    with conn.cursor() as cur:
        cur.execute(select_sql)
        data = cur.fetchall()

    return data

def parse_github_link(github_link):
    if github_link is None:
        return None, None

    split_link = github_link.replace("https://github.com/", '').replace("github.com/", '').replace("\\", '')
    split_link = split_link.split('/')

    # owner
    if len(split_link) < 2 :
        owner = split_link[-1]
        return owner
    
    # owner, repo
    elif len(split_link) == 2: 
        owner = split_link[-2]
        repo = split_link[-1]
        return owner, repo
    
    # org owner
    elif 'org' in split_link:
        owner = "org" + split_link[-2]
        repo = split_link[-1]
        return owner, repo
    
    # most of the case is like this : ['owner', 'repo', '']
    else:
        owner = split_link[0]
        repo = split_link[1]
        return owner, repo
    
def parse_twitter_link(twitter_link):

    if twitter_link is None:
        return None

    split_link = twitter_link.replace("https://twitter.com/", '').replace("twitter.com/", '')
    split_link = split_link.split('/')

    return split_link[-1]

def insert_to_related_table_at_once(conn, data_list):
    
    #upsert query for Projects table
    insert_query_on_proejcts_table = SQL(
    """
    INSERT INTO Projects (
        project_wallet_address,
        project_potlock_url,
        project_official_website_url,
        created_date
    )
    
    VALUES (%s, %s, %s, %s)
    ON CONFLiCT (project_wallet_address)
    DO UPDATE SET
        project_potlock_url = EXCLUDED.project_potlock_url,
        project_official_website_url = EXCLUDED.project_official_website_url;
    """
    )
    
    # upsert query for GithubRepos table
    insert_query_on_github_table = SQL("""
    INSERT INTO GithubRepos (
        project_wallet_address,
        github_repo_id,
        owner_name,
        repo_name
        )
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (github_repo_id)
    DO UPDATE SET
        owner_name = EXCLUDED.owner_name,
        repo_name = EXCLUDED.repo_name;                              
    """)

    # upsert query for Twitter table
    insert_query_on_twitter_table = SQL("""
    INSERT INTO XHandles (
        project_wallet_address,
        handle,
        created_date
    )
    VALUES (%s, %s, %s)
    ON CONFLICT (handle)
    DO NOTHING
    """)

    created_date = datetime.now()

    try:
        with conn.cursor() as cur:
            
            for near_address, github_link, website, twitter_link, github_repos in data_list:
                # to adapt uuid type, this line is necessary
                psycopg2.extras.register_uuid()

                # get the potlock url
                potlock_url = 'https://app.potlock.org/?tab=project&projectId='+near_address

                # insert into Projects table
                cur.execute(insert_query_on_proejcts_table, (near_address, potlock_url, website, created_date))

                # insert into GithubRepos table
                # gihub_repos is a json string of list of github links
                github_repos = json.loads(github_repos) if github_repos is not None else []
                github_repos.append(github_link)
                
                # delete None of '' from the list
                github_repos = list(filter(lambda x: x is not None and x != '', github_repos))
                github_repos = set(github_repos)

                github_repos = set(map(parse_github_link, github_repos)) if github_repos is not None else []


                for repo in github_repos:
                    
                    if isinstance(repo, str):
                        owner = repo
                        repo_name = None
                    else:
                        # print(repo)
                        owner, repo_name = repo
                
                    cur.execute(insert_query_on_github_table, (near_address, uuid4(), owner, repo_name))
                
                logger.log_insert_project(near_address)

                # insert into Twitter table
                twitter_link = parse_twitter_link(twitter_link)
                cur.execute(insert_query_on_twitter_table, (near_address, twitter_link, created_date))
                logger.log_insert_twitter(near_address, twitter_link)
                

    except Exception as e:
        logger.log_error(near_address, traceback.format_exc())
        print("[error] Failed to insert data, which is near_address and json :", near_address)
        print("[error] Failed to insert data, which is near_address and json :", (website, twitter_link, github_repos))
        print("[error] Error message :", traceback.format_exc())
        conn.rollback()
    else:
        conn.commit()



def main():
    logger.log_start_process("InsertProjects.py")
    conn = connect_to_db()
    logger.log_connection()
    print("[info] Connected to DB")
    user_list = in_usd_more_than_one(conn)
    logger.log_selction_data(len(user_list))
    print("[info] Got all users :", len(user_list))
    insert_to_related_table_at_once(conn, user_list)
    
    print("[info] Inserted all users to the table")
    close_connection(conn)
    print("[info] Connection closed")
    logger.log_disconnection()
    logger.log_end_process("InsertProjects.py")
if __name__ == "__main__":
    main()


