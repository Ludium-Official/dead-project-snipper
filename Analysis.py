import Analysis_tools as AT
import matplotlib as plt

target_project = ""

social_df = AT.SocialMediaScore.read_df(target_project)
git_df = AT.GithubScore.read_df(target_project)
chain_df = AT.OnchainActivityScore.read_df(target_project)

# Social Media Score (30 points total)
FOP = AT.SocialMediaScore.frequency_of_posts(target_project) # Frequency of posts
ER = AT.SocialMediaScore.engagement_rates(target_project) # Engagement rates
GODF = AT.SocialMediaScore.growth_decline_followers(target_project) # Growth or decline in followers

# Github Score (30 points total)
FOC = AT.GithubScore.frequency_of_commit(target_project) # Frequency of commits
NOAC = AT.GithubScore.number_of_active_contributors(target_project) # Number of active Contributors
IPR = AT.GithubScore.issues_pull_request(target_project) # Issues and pull request activity

# On-chain Activity Score (40 points total)
TV = AT.OnchainActivityScore.transaction(target_project) # Transaction volume
UAA = AT.OnchainActivityScore.unique_active_addresses(target_project) # Unique active addresses
SMI = AT.OnchainActivityScore.smart_contract_interactions(target_project) # Smart contract interactions

total_score = sum(FOP, ER, GODF, FOC, NOAC, IPR, TV, UAA, SMI)
minimum = 30

if total_score < minimum :
    result = 'dead'
else :
    result = 'alive'

# git_repo에 대한 그래프
plt.figure(figsize=(10, 6))

# commit_count 꺾은선 그래프
plt.plot(git_df.index, git_df['commit_count'], marker='o', color='b', label='commit_count')

# issue_count 꺾은선 그래프
plt.plot(git_df.index, git_df['issue_count'], marker='o', color='g', label='issue_count')

# PR_count 꺾은선 그래프
plt.plot(git_df.index, git_df['PR_count'], marker='o', color='r', label='PR_count')

# watcher_count 꺾은선 그래프
plt.plot(git_df.index, git_df['watcher_count'], marker='o', color='orange', label='watcher_count')


# 그래프 제목과 라벨 설정
plt.title(f"{target_project} - commit, issue, PR, watcher")
plt.xlabel('Month')
plt.ylabel('Count')

# 범례 추가
plt.legend()

# 그래프 표시
plt.tight_layout()
plt.show()

# X에 대한 그래프
plt.figure(figsize=(10, 6))

# tweet 꺾은선 그래프
plt.plot(git_df.index, social_df['tweet'], marker='o', color='b', label='tweet')

# retweet_count 꺾은선 그래프
plt.plot(git_df.index, social_df['retweet_count'], marker='o', color='g', label='retweet_count')

# like_count 꺾은선 그래프
plt.plot(git_df.index, social_df['like_count'], marker='o', color='r', label='like_count')

# reply_count 꺾은선 그래프
plt.plot(git_df.index, social_df['reply_count'], marker='o', color='orange', label='reply_count')

# quote_count 꺾은선 그래프
plt.plot(git_df.index, social_df['quote_count'], marker='o', color='purple', label='quote_count')

# follower_count 꺾은선 그래프
plt.plot(git_df.index, social_df['follower_count'], marker='o', color='magenta', label='follower_count')

# 그래프 제목과 라벨 설정
plt.title(f"{target_project} - tweet, retweet, lik, reply, quote, follower")
plt.xlabel('Month')
plt.ylabel('Count')

# 범례 추가
plt.legend()

# 그래프 표시
plt.tight_layout()
plt.show()