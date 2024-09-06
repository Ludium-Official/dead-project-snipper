from SQLScript import SQL_tools as SSS
import requests
from datetime import datetime, timedelta

class get_git_data:
    def github_api_request(owner, repo, endpoint, params={}):
        if endpoint:
            base_url = f'https://api.github.com/repos/{owner}/{repo}/{endpoint}'
        else:
            base_url = f'https://api.github.com/repos/{owner}/{repo}'
        response = requests.get(base_url, params=params)
        return response.json()

    def count_commits(owner, repo, params={}):
        commits = get_git_data.github_api_request(owner, repo, 'commits', params)
        return len(commits)

    def count_issues(owner, repo, params={}):
        issues_data = get_git_data.github_api_request(owner, repo, 'issues', params)
        issue_count = len([issue for issue in issues_data if 'pull_request' not in issue])
        return issue_count

    def count_pull_requests(owner, repo, params={}):
        pulls = get_git_data.github_api_request(owner, repo, 'pulls', params)
        return len(pulls)

    def count_watcher(owner, repo, parmas={}):
        repo = get_git_data.github_api_request(owner, repo, '')
        # pprint(repo)
        return repo['watchers_count']
    
# X에 대한 코드인데 무조건 고쳐야함
class get_X_data:
    def X_api_request(owner, repo, endpoint, params={}):
        if endpoint:
            base_url = f''
        else:
            base_url = f''
        response = requests.get(base_url, params=params)
        return response.json()

    def check_tweet(owner, repo, params={}):
        tweets = get_X_data.X_api_request(owner, repo, 'tweet', params)
        return len(tweets)

    def retweet_count(owner, repo, params={}):
        retweet_count = get_X_data.X_api_request(owner, repo, 'retweet', params)
        return retweet_count

    def like_count(owner, repo, params={}):
        likes = get_git_data.github_api_request(owner, repo, 'pulls', params)
        return likes

    def reply_count(owner, repo, params={}):
        replys = get_git_data.github_api_request(owner, repo, 'pulls', params)
        return replys
    
    def quote_count(owner, repo, params={}):
        quotes = get_git_data.github_api_request(owner, repo, 'pulls', params)
        return quotes
    
    def follower_count(owner, repo, params={}):
        follower = get_git_data.github_api_request(owner, repo, 'pulls', params)
        return follower

# set the owner and repo
owner = 'octocat'
repo = 'Hello-World'

# get the diff between today and month
git_today = datetime.utcnow()
last_month = git_today - timedelta(days=30)

# change the datetime foramt as ISO 8601
since = last_month.isoformat() + 'Z'
until = git_today.isoformat() + 'Z'

# request the number of Commits
params = {'since': since, 'until': until}
commit_count = get_git_data.count_commits(owner, repo, params)
print(f"Commits in the last day: {commit_count}")

# request the number of Issues
issue_count = get_git_data.count_issues(owner, repo, params)
print(f"Issues in the last day: {issue_count}")

# request the number of Pull Requests
pull_count = get_git_data.count_pull_requests(owner, repo, params)
print(f"Pull Requests in the last day: {pull_count}")

# request the number of Watchers

before_month_watcher_params = {"since": since, "until": since}
before_month_watcher_count = get_git_data.count_watcher(owner, repo, before_month_watcher_params)

after_month_watcher_params = {"since": until, "until": until}
after_month_watcher_count = get_git_data.count_watcher(owner, repo, after_month_watcher_params)

watcher_diff = after_month_watcher_count - before_month_watcher_count
print(f"Watchers in the last day: {watcher_diff}")

git_date_time = git_today
git_df = {
    "github_repo_id" : owner,
    "commit_count" : commit_count,
    "issue_count" : issue_count,
    "PR_count" : pull_count,
    "watcher_count" : watcher_diff,
    "datetime" : git_date_time
}
git_data_table = "GithubRepoActivityLog"

SSS.insert_to_db(git_data_table, git_df)

# X에 대한 데이터 모음

# set the owner and repo
owner = 'octocat'
repo = 'Hello-World'

# get the diff between today and month
x_today = datetime.utcnow()
last_month = x_today - timedelta(days=30)

# change the datetime foramt as ISO 8601
since = last_month.isoformat() + 'Z'
until = x_today.isoformat() + 'Z'

params = {'since': since, 'until': until}

# request the number of Tweets
tweet = get_X_data.check_tweet(owner, repo, params)
print(f"tweets in the last day: {tweet}")

# request the number of Retweets
retweet_count = get_X_data.retweet_count(owner, repo, params)
print(f"retweets in the last day: {retweet_count}")

# request the number of Likes
like_count = get_X_data.like_count(owner, repo, params)
print(f"Likes in the last day: {like_count}")

# request the number of Reply
reply_count = get_X_data.reply_count(owner, repo, params)
print(f"Replys in the last day: {reply_count}")

# request the number of Quote
quote_count = get_X_data.quote_count(owner, repo, params)
print(f"Quotes in the last day: {reply_count}")

# request the number of Follower
follower_count = get_X_data.follower_count(owner, repo, params)
print(f"Followers in the last day: {follower_count}")

x_date_time = x_today
x_df = {
    "account_id" : owner,
    "tweet" : tweet,
    "retweet_count" : retweet_count,
    "like_count" : like_count,
    "reply_count" : reply_count,
    "quote_count" : quote_count,
    "follower_count" : follower_count,
    "datetime" : x_date_time
}
x_data_table = "XActivityLog"

SSS.insert_to_db(x_data_table, git_df)