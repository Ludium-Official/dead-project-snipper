CREATE TABLE Projects (
  project_id UUID PRIMARY KEY,
  project_name VARCHAR,
  created_date TIMESTAMP,
  recent_action_date TIMESTAMP
);

CREATE TABLE FundedMembers (
  project_id UUID REFERENCES Projects(project_id),
  name VARCHAR
);

CREATE TABLE XAccounts (
  project_id UUID REFERENCES Projects(project_id),
  account_id VARCHAR UNIQUE
);

CREATE TABLE GithubRepos (
  project_id UUID REFERENCES Projects(project_id),
  github_repo_id UUID UNIQUE,
  owner_name VARCHAR,
  github_repo VARCHAR
);

CREATE TABLE NearAddress (
  project_id UUID REFERENCES Projects(project_id),
  near_address VARCHAR UNIQUE
);

CREATE TABLE XActivityLog (
  account_id VARCHAR REFERENCES XAccounts(account_id),
  tweet VARCHAR,
  retweet_count INT,
  like_count INT,
  reply_count INT,
  quote_count INT,
  follower_count INT,
  datetime TIMESTAMP
);

CREATE TABLE GithubRepoActivityLog (
  github_repo_id UUID REFERENCES GithubRepos(github_repo_id),
  commit_count INT,
  issue_count INT,
  PR_count INT,
  watcher_count INT,
  datetime TIMESTAMP
);

CREATE TABLE OnChainActivityLog (
  near_address VARCHAR REFERENCES NearAddress(near_address),
  Activity_log VARCHAR
);
