import requests
import json
import traceback
from datetime import datetime
import time
import random
import logger


# db
import psycopg2 as pg
from psycopg2.sql import SQL, Literal
import psycopg2.extras
from uuid import uuid4

# twitter
from getTwitter import login, getProfile, getTweet

# playwright
import playwright
from playwright.sync_api import sync_playwright

def connect_to_db():
    conn = pg.connect(
        host=your_host,
        port= your_port,
        database= your_db,
        user= your_user,
        password= your_password,
    )
    return conn

def close_connection(conn):
    conn.close()

def connect_commit(conn):
    conn.commit()

def connect_rollback(conn):
    conn.rollback()

def insert_xhandle(conn, project_wallet_address, handle, data:json):

    condition = data.get('__typename')
    account_id = data.get('rest_id')
    legacy = data.get('legacy')
    description = legacy.get('description') if legacy else None
    created_date = legacy.get('created_at') if legacy else None
    
    # upsert the data
    insert_sql = """
    INSERT INTO XHandles 
        (project_wallet_address, handle, account_id, description,condition, created_date)
        VALUES
        (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (handle)
    DO UPDATE SET
        account_id = EXCLUDED.account_id,
        description = EXCLUDED.description,
        condition = EXCLUDED.condition;
    """

    cur = conn.cursor()
    cur.execute(insert_sql, (project_wallet_address, handle,account_id, description, condition, created_date))

def insert_empty_xhandle(conn, project_wallet_address, handle):

    sql = """
    INSERT INTO XHandles
    (project_wallet_address, handle, condition)
    VALUES
    (%s, %s, %s)
    On Conflict (handle)
    DO UPDATE SET
        condition = EXCLUDED.condition;
    """

    cur = conn.cursor()
    cur.execute(sql, (project_wallet_address ,handle ,'UnavailableUser'))

def insert_xactivitylog(conn, handle, data:json, crawl_date:datetime):

    # upsert the data 
    sql = """
    INSERT INTO xactivitylog
    (
        handle,
        tweet,
        retweet_count,
        reply_count,
        like_count,
        watch_count,
        datetime,
        updated_datetime
    )
    VALUES
    (
        %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (handle, datetime)
    DO UPDATE SET
        retweet_count = EXCLUDED.retweet_count,
        reply_count = EXCLUDED.reply_count,
        watch_count = EXCLUDED.watch_count,
        updated_datetime = EXCLUDED.updated_datetime;
    """

    cur = conn.cursor()

    for data_ in data:
        cur.execute(sql, 
                    (
                        handle, 
                        data_['text'],
                        data_['retweet_count'], 
                        data_['reply_count'], 
                        data_['like_count'],
                        data_['watch_count'], 
                        data_['date_time'], 
                        crawl_date)
                    )
    

def insert_xfollow(conn, handle, today:datetime, data:json):

    legacy = data.get('legacy')

    favourites_count = legacy.get('favourites_count') if legacy else None
    followers_count = legacy.get('followers_count') if legacy else None
    following_count = legacy.get('friends_count') if legacy else None
    listed_count = legacy.get('listed_count') if legacy else None
    media_count = legacy.get('media_count') if legacy else None

    # upsert the data
    sql = """
    INSERT INTO XHandlesDailyFollowInfo
    (
        handle,
        favourites_count,
        followers_count,
        following_count,
        listed_count,
        media_count,
        datetime
    )
    VALUES
    (
        %s, %s, %s, %s, %s, %s, %s
    )
    """

    cur = conn.cursor()
    cur.execute(sql, (handle, favourites_count, followers_count, following_count, listed_count, media_count, today))


def get_all_handles(conn):

    select_sql = """
    SELECT  
            project_wallet_address, 
            handle
    FROM xhandles
    where (handle IS NOT null and handle != '')  
    and (condition = 'User' or condition is null);
    """
    

    with conn.cursor() as cur:
        cur.execute(select_sql)
        data = cur.fetchall()

    return data

def main():
    logger.log_start_process("InsertTwitterData.py")
    #0. get all handles
    conn = connect_to_db()
    logger.log_info("connected to the DB")

    handles = get_all_handles(conn)
    print(f"handles length : {len(handles)}")
    logger.log_selction_data(len(handles))
    
    today = datetime.now().date()
    #1. login to twitter
    logined_browser, logined_page = login.login_x("bigtide211021", "gksruf0504", 'ladians@gmail.com')

    #2. get the twitter profile and tweet info for each handle

    failed_handles = []
    
    for wallet_address, handle in handles:
        try:
            # insert xhandle        
            user_url, request_header = getProfile.intercept_request(handle, browser=logined_browser, page=logined_page)
            # user_profile = getProfile.getUserProfile(user_url, request_header)['user']['result']
            user_profile = getProfile.getUserProfile(user_url, request_header)

            # the case like the user is suspended or not found
            if user_profile == {}:
                insert_empty_xhandle(conn, wallet_address, handle)
                failed_handles.append((wallet_address, handle))
                connect_commit(conn)
                continue
        
            user_profile = user_profile['user']['result']
            insert_xhandle(conn, wallet_address, handle, user_profile)
            logger.log_user_profile(handle)
            print(f"[INFO] inserted the xhandle data | user : {handle}")

            # insert xactivitylog
            user_tweets = getTweet.scroll_and_crawl(handle, logined_browser, logined_page, max_scrolls=10, crawl_interval=2)
            insert_xactivitylog(conn, handle, user_tweets, today)
            logger.log_user_tweets(handle)
            print("[INFO] inserted the xactivitylog data")

            # insert xfollow
            insert_xfollow(conn, handle, today, user_profile)
            logger.log_user_followers(handle)
            print("[INFO] inserted the xfollow data")

        except Exception as e:
            logger.log_error(handle, traceback.format_exc())
            print(f"[ERROR] raised while handling the twitter data on address : {wallet_address} / handle : {handle}")
            print(traceback.format_exc())
            connect_rollback(conn)
            failed_handles.append((wallet_address, handle))
            continue
        else:
            connect_commit(conn)

    # 3. close the connection
    close_connection(conn)
    logger.log_disconnection()

    print("[INFO] closed the DB connection")
    # 4. close the browser
    logined_browser.close()
    print("[INFO] closed the browser")
    print(f"[INFO] failed handles : {failed_handles}")
    logger.log_end_process("InsertTwitterData.py")

if __name__ == '__main__':
    main()

