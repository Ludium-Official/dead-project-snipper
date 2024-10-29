
# db related libraries
import psycopg2 as pg
import psycopg2.extras
import random
from uuid import uuid4
from datetime import datetime
import json
import traceback
from pprint import pprint

# llm related libraries
from langchain import LLMChain, PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_teddynote import logging
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_teddynote.messages import stream_response

def connect_to_db():
    conn = pg.connect(
        host="ls-8598f5e3b856b24e455508ee2c5a79fd219ed693.cnqgcgguumqr.ap-northeast-2.rds.amazonaws.com",
        port= 5432,
        database= 'dead_project_snipper',
        user= 'dbmasteruser',
        password= 'BG.7.U>p(6&F3B]*c.*qBWw6Jp`J~~nU',
    )
    return conn

def close_connection(conn):
    conn.close()

def connect_commit(conn):
    conn.commit()

def connect_rollback(conn):
    conn.rollback()

# get near address from the database
def get_join_near_address_github_repo_xhandle(conn):
    """
    return (project_wallet_address, github_repo_id, handle)
    """

    sql = """
    SELECT p.project_wallet_address, g.github_repo_id, x.handle
    from projects as p
    JOIN githubrepos as g ON p.project_wallet_address = g.project_wallet_address
    JOIN xhandles as x ON p.project_wallet_address = x.project_wallet_address;
    """
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall() 

# get the twitter(xhandle) activity data from the database
def get_daily_metric_data(conn, handle):
    """
    return (
        favourites_count, 
        following_count, 
        followers_count, 
        listed_count, 
        media_count, 
        datetime
        )
    """

    sql = """
    SELECT favourites_count, following_count, followers_count, listed_count, media_count, datetime
    FROM XHandlesDailyFollowInfo
    WHERE handle = %s
    and datetime > now() - interval '7 days';
    """
    cur = conn.cursor()
    cur.execute(sql, (handle,))
    return cur.fetchall()

# get the tweet activity data from the database
def get_tweet_engagement_data(conn, handle):
    """
    return (
        tweets, 
        likes_count, 
        retweets_count, 
        reply_count, 
        watch_count,
        datetime
        )
    """

    sql = """
    SELECT 
        tweet, 
        retweet_count, 
        like_count, 
        reply_count, 
        watch_count, 
        datetime
    FROM XActivityLog
    WHERE handle = %s
    and datetime > now() - interval '7 days';
    """
    cur = conn.cursor()
    cur.execute(sql, (handle,))
    return cur.fetchall()

# get the github activity data from the database
def get_github_activity_data(conn, github_repo_id):

    """
    return (
        daily_commit_count,
        daily_open_issue_count,
        daily_closed_issue_count,
        daily_pull_count,
        daily_merge_count,
        subscribers_count,
        stars_count,
        forks_count,
        datetime
        )
    """

    sql = """
    SELECT  
        daily_commit_count, 
        daily_open_issue_count, 
        daily_closed_issue_count, 
        daily_pull_count, 
        daily_merge_count, 
        subscribers_count, 
        stars_count, 
        forks_count, 
        datetime
    FROM githubrepoactivitylog
    WHERE github_repo_id = %s
    and datetime > now() - interval '7 days';
    """

    cur = conn.cursor()
    cur.execute(sql, (github_repo_id,))
    return cur.fetchall()

# get the near activity data from the database
def get_near_activity_data(conn, project_wallet_address):
    
        """
        return (
            transactions,
            datetime
            )
        """
    
        sql = """
        SELECT transaction_count, datetime
        FROM walletactivitylog
        WHERE project_wallet_address = %s
        and datetime > now() - interval '7 days';
        """
    
        cur = conn.cursor()
        cur.execute(sql, (project_wallet_address,))
        return cur.fetchall()

# insert the report data into the database
def insert_report_data(conn, response_json, report_uuid, today):

    sql = """
    INSERT INTO projectreport
        (
            project_wallet_address, 
            report_uuid, 
            report, 
            score,
            github_score, 
            twitter_score, 
            near_score, 
            dead_or_alive, 
            created_date, 
            modified_date, 
            most_recent
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
            %s,
            %s
        );
    """

    total_score = int(response_json['github_score']) + int(response_json['twitter_score']) + int(response_json['near_score'])

    psycopg2.extras.register_uuid()

    with conn.cursor() as cur:
        cur.execute(sql, (
            response_json['project_name'],
            report_uuid,
            json.dumps(response_json),
            total_score,
            response_json['github_score'],
            response_json['twitter_score'],
            response_json['near_score'],
            True if response_json['alive'] in ('true', 'True') else False,
            today,
            today,
            True
        ))

        # conn.commit()


# get the project data from the database


if __name__ == "__main__":

    # 데이터베이스에 연결합니다.
    conn = connect_to_db()

    # 프로젝트 데이터를 가져옵니다.
    projects_data = get_join_near_address_github_repo_xhandle(conn)
    print("[info] projects_data: ", len(projects_data))


    # model_name = "llama3.1:8b-instruct-q8_0"
    # model_name = "llama3.2:3b"


    # # Ollama 모델을 불러옵니다.
    # llm = ChatOllama(
    #     model=model_name,
    #     format="json",
    #     )

    # # openai model
    api_key = your_api_key

    llm = ChatOpenAI(
        api_key=api_key,
        model="gpt-4o",
    )


    template = """
You are a helpful assistant and professional trend analyst. Your task is to evaluate projects funded by NEAR Protocol, based on their activity on Twitter, GitHub, and NEAR transaction frequency. Your goal is to determine if each project is ongoing ("alive") or inactive ("dead"), using the specific criteria provided.

### Instructions

1. Analyze the project data provided for Twitter, GitHub, and NEAR activity.
2. Calculate a score based on the criteria in each section.
3. Generate a report for each project summarizing its status.
4. Provide the results as a JSON object in the following format:
    
    {{
        "project_name": "project_name",
        "alive": "True/False",
        "twitter_score": "score",
        "github_score": "score",
        "near_score": "score",
        "overall_report": "report",
        "twitter_report": "report",
        "github_report": "report",
        "near_report": "report"
    }}
    
5. Scoring:
    - The total score is out of 100 points.
    - A score below 30 indicates the project is "dead," and a score of 30 or more indicates it is "alive."
    - If a data source is unavailable (e.g., Twitter = None), calculate the score based only on the available data sources.

### Scoring Criteria

1. **Twitter Score** (Max: 30 points)
    - Followers count:
        - 0–200 followers: 0 points
        - 201–500 followers: 5 points
        - 501–1,000 followers: 10 points
        - Over 1,000 followers: 15 points
    - Engagement (based on the last week’s tweet activity):
        - Fewer than 5 combined tweets/retweets/likes: 0 points
        - 5–10 combined tweets/retweets/likes: 5 points
        - 11–20 combined tweets/retweets/likes: 10 points
        - Over 20 combined tweets/retweets/likes: 15 points

2. **GitHub Score** (Max: 40 points)
    - Repository commits in the last week:
        - No commits: 0 points
        - 1–2 commits: 10 points
        - 3–5 commits: 20 points
        - Over 5 commits: 30 points
    - Issues and Pull Requests in the last week:
        - 0 issues or pull requests: 0 points
        - 1–2 issues or pull requests: 5 points
        - 3–5 issues or pull requests: 10 points

3. **NEAR Score** (Max: 30 points)
    - Transaction frequency in the last week:
        - No transactions: 0 points
        - 1–5 transactions: 5 points
        - 6–15 transactions: 15 points
        - Over 15 transactions: 30 points
"""

    for project_wallet_address, github_repo_id, handle in projects_data:
        try:
            # twitter daily engagement data
            twitter_daily_metrics = get_daily_metric_data(conn, handle)
            print("[info] twitter_daily_metrics: ", len(twitter_daily_metrics))

            # twitter tweet engagement data
            twitter_engagement_data = get_tweet_engagement_data(conn, handle)
            print("[info] twitter_engagement_data: ", len(twitter_engagement_data))

            # github activity data
            github_data = get_github_activity_data(conn, github_repo_id)
            print("[info] github_data: ", len(github_data))

            # near activity data
            near_data = get_near_activity_data(conn, project_wallet_address)
            print("[info] near_data: ", len(near_data))

            user_input_data = f"""
            ### Project Name

            {project_wallet_address}

            ### Input Data Format

            1. **Twitter Data**
                - Provided in two lists of tuples: Daily Metrics and Engagement Metrics.
                
                #### Part 1: Daily Metrics
                - Headers:
                    ```plaintext
                    ['favourites_count', 'following_count', 'followers_count', 'listed_count', 'media_count', 'datetime']
                    ```
                - Data: {twitter_daily_metrics}
                
                #### Part 2: Engagement Metrics
                - Headers:
                    ```plaintext
                    ['tweets', 'likes_count', 'retweets_count', 'reply_count', 'watch_count', 'datetime']
                    ```
                - Note: Evaluate tweet relevance based on profile description if provided.
                - Data: {twitter_engagement_data}

            2. **GitHub Data**
                - Provided as a list of tuples, each representing metrics for a repository.
                - Headers:
                    ```plaintext
                    [ 'daily_commit_count', 'daily_open_issue_count', 'daily_closed_issue_count', 'daily_pull_count', 'daily_merge_count', 'subscribers_count', 'stars_count', 'forks_count', 'datetime']
                    ```
                - Data: {github_data}

            3. **NEAR Data**
                - Provided as a list of tuples, each representing a project’s weekly transaction record.
                - Headers:
                    ```plaintext
                    ['transaction_count', 'datetime']
                    ```
                - Data: {near_data}

            ---

            ### Output

            Follow the JSON format specified in the instructions to ensure consistent structure and clear reporting. Please make sure your final output is a valid JSON object without any additional text or formatting errors.
            Make ONLY json-format answer. Do not include any other text or formatting in your answer.

            {{
                "project_name": "project_name",
                "alive": "True/False",
                "twitter_score": "score",
                "github_score": "score",
                "near_score": "score",
                "overall_report": "report",
                "twitter_report": "report",
                "github_report": "report",
                "near_report": "report"
            }}
            """

            # 프롬프트
            prompt = ChatPromptTemplate.from_messages(
                [("system", template), ("user", "{data}")]
                )

            # 체인 생성
            chain = prompt | llm | StrOutputParser()

            # input data

            # 간결성을 위해 응답은 터미널에 출력됩니다.
            answer = chain.invoke({'data' : user_input_data})

            answer = answer.replace("```json", "")
            answer = answer.replace("```", "")
            answer = answer.replace("plaintext", "")
            answer = answer.strip()

            # jsonify answer
            
            answer = json.loads(answer)

            # insert the report data into the database
            report_uuid = uuid4()
            today = datetime.now().date()

            insert_report_data(conn, answer, report_uuid, today)
            print(f"[info] report data inserted / {project_wallet_address} - {github_repo_id} - {handle}")
            
        except Exception as e:

            print("[error] ", traceback.format_exc())
            continue

        else:
            conn.commit()
        
    print("done")