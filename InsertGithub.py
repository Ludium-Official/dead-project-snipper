import psycopg2 as pg
import psycopg2.extras
from datetime import datetime
from datetime import timedelta
from psycopg2 import sql
from getGithub import getGithubInfo
from pprint import pprint
from copy import deepcopy
import statistics
import requests
import traceback
import logger

def connect_to_db():
    conn = pg.connect(
        host=your_host,
        port= 5432,
        database= your_db,
        user= your_user,
        password= your_password,
    )
    return conn

def close_connection(conn):
    conn.close()

def connect_commit(conn):
    conn.commit()

def rollback(conn):
    conn.rollback()

def get_all_github_repos(conn):
    sql = """
    SELECT project_wallet_address, github_repo_id, owner_name, repo_name
    FROM githubrepos
    WHERE repo_name IS NOT NULL
    and repo_name != '' 
    and owner_name IS NOT NULL
    and owner_name != '';
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def insert_activitylog_data(
        conn,
        github_repo_id, 
        forks, 
        stars, 
        subscribers, 
        commit_count, 
        issue_open_count, 
        issue_closed_count, 
        pulls_open_count, 
        pulls_closed_count,
        date_time
        ):
    

    sql = sql = """
    INSERT INTO githubrepoactivitylog
        (
            github_repo_id,
            github_repo_id, 
            stars_count, 
            subscribers_count, 
            daily_commit_count, 
            daily_open_issue_count, 
            daily_closed_issue_count, 
            daily_pull_count, 
            daily_merge_count, 
            datetime
        )
        VALUES
        (
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s
        );
    """

    psycopg2.extras.register_uuid()

    cur = conn.cursor()
    cur.execute(sql, (
        github_repo_id,
        forks,
        stars,
        subscribers,
        commit_count,
        issue_open_count,
        issue_closed_count,
        pulls_open_count,
        pulls_closed_count,
        date_time
    ))


# if response has pages
def get_unitl_last_page(response):
    last = response.links['last']['url']
    last_page = int(last.split('=')[-1])
    return last_page

def count_commits(owner, repo, endpoint, last_page ,params={}, headers={}):
    params['page'] = last_page
    last_page_reponse = getGithubInfo.github_api_request(owner, repo, endpoint, params=params, headers=headers)
    last_page = last_page_reponse.json()
    return len(last_page) + (last_page - 1) * 100

def count_response_data(owner_name, repo_name, endpoint=None ,headers={}, params={}):
    response = getGithubInfo.github_api_request(owner_name, repo_name, endpoint, headers=headers, params=params)
    if 'last' in response.links:
        last_page = get_unitl_last_page(response)
        count_response = count_response_data(owner_name, repo_name, last_page, headers=headers,params=params)
    else:
        count_response = len(response.json())

    return count_response

def get_pat(path):
    with open(path, 'r') as f:
        pat = f.read()
    return pat

if __name__=="__main__":

    # get all github repos
    logger.log_start_process('InsertGithub.py')
    conn = connect_to_db()
    logger.log_connection()
    all_github_repos = get_all_github_repos(conn)

    print(len(all_github_repos))
    logger.log_selction_data(len(all_github_repos))

    # get the pat token
    pat = get_pat('pat.txt')

    headers = {'authorization': f'Bearer {pat}'}

    issue_open_params = {
        'state': 'open',
        'per_page': 100
        }
    issue_closed_params = {
        'state': 'closed',
        'per_page': 100
        }
    
    pulls_open_params = {
        'state': 'open',
        'per_page': 100
        }
    pulls_closed_params = {
        'state': 'closed',
        'per_page': 100
        }
    
    daily_commits_params = {
        'since': datetime.now() - timedelta(days=1),
        'until': datetime.now(),
        'per_page': 100
        }
    
    today = datetime.now().date()

    for project_wallet_address, github_repo_id, owner_name, repo_name in all_github_repos:
        try:
            print(f"Processing {owner_name}/{repo_name}")

            # get the response data
            response = getGithubInfo.github_api_request(owner_name, repo_name, '', headers=headers)

            # get forks, stars, subscribers
            forks = response.json()['forks']
            stars = response.json()['stargazers_count']
            subscribers = response.json()['subscribers_count']
            logger.log_insert_github(owner_name, repo_name, 'engagement (forks, stars, subscribers)')

            # get the commits
            commits = count_response_data(owner_name, repo_name, 'commits', headers=headers, params=daily_commits_params)
            logger.log_insert_github(owner_name, repo_name, 'commits')

            # get the issues
            issue_open_count = count_response_data(owner_name, repo_name, 'issues', headers=headers, params=issue_open_params)
            issue_closed_count = count_response_data(owner_name, repo_name, 'issues', headers=headers, params=issue_closed_params)
            logger.log_insert_github(owner_name, repo_name, 'issues')

            # get the pull requests
            pulls_open_count = count_response_data(owner_name, repo_name, 'pulls', headers=headers, params=pulls_open_params)
            pulls_closed_count = count_response_data(owner_name, repo_name, 'pulls', headers=headers, params=pulls_closed_params)
            

            # insert the data
            insert_activitylog_data(
                conn,
                github_repo_id, #uuid to string
                forks,
                stars,
                subscribers,
                commits,
                issue_open_count,
                issue_closed_count,
                pulls_open_count,
                pulls_closed_count,
                today
            )
            logger.log_insert_github(owner_name, repo_name, 'githubrepos')
        except Exception as e:
            logger.log_error(owner_name+'/'+repo_name, traceback.format_exc())
            print(f"Error while processing {owner_name}/{repo_name}")
            print(traceback.format_exc())
            rollback(conn)
            continue
        else:
            connect_commit(conn)

    close_connection(conn)
    logger.log_disconnection()





        
        

