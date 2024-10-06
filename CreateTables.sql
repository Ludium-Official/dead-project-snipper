CREATE TABLE Projects (
  project_id UUID PRIMARY KEY,
  project_name VARCHAR,
  created_date VARCHAR,
  recent_action_date TIMESTAMP
);

CREATE TABLE XAccounts (
  project_id UUID REFERENCES Projects(project_id),
  user_id INT PRIMARY KEY,
  user_name VARCHAR
);

CREATE TABLE XFollowers (
  followers_id VARCHAR PRIMARY KEY,
  user_id INT REFERENCES XAccounts(user_id)
)


CREATE TABLE XActivityLog (
  tweet_id INT PRIMARY KEY,
  account_id INT REFERENCES XAccounts(user_id),
  like_count INT,
  reply_count INT,
  retweet_count INT,
  views INT,
  tweet VARCHAR,
  timeparsed VARCHAR
);

CREATE TABLE GithubRepos (
  project_id UUID REFERENCES Projects(project_id),
  project_id INT,
  user_id INT,
  repo_id INT PRIMARY KEY
);

CREATE TABLE GithuCommitLog (
  github_repo_id UUID REFERENCES GithubRepos(github_repo_id),
  commit_count INT,
  issue_count INT,
  PR_count INT,
  watcher_count INT,
  datetime TIMESTAMP
);

CREATE TABLE NearAddress (
  project_id UUID REFERENCES Projects(project_id),
  near_address VARCHAR UNIQUE
);

CREATE TABLE FundedMembers (
  project_id UUID REFERENCES Projects(project_id),
  name VARCHAR
);

CREATE TABLE OnChainActivityLog (
  near_address VARCHAR REFERENCES NearAddress(near_address),
  Activity_log VARCHAR
);
