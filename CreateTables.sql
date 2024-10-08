-- Table: Projects
CREATE TABLE Projects (
    project_id UUID PRIMARY KEY,
    project_name VARCHAR,
    project_url VARCHAR,
    created_date TIMESTAMP,
    recent_action_date TIMESTAMP
);

-- Table: FundedMembers
CREATE TABLE FundedMembers (
    project_id UUID REFERENCES Projects(project_id),
    name VARCHAR
);

-- Table: XAccounts
CREATE TABLE XAccounts (
    project_id UUID REFERENCES Projects(project_id),
    account_id VARCHAR UNIQUE
);

-- Table: GithubRepos
CREATE TABLE GithubRepos (
    project_id UUID REFERENCES Projects(project_id),
    github_repo_id UUID UNIQUE,
    owner_name VARCHAR,
    github_repo VARCHAR
);

-- Table: NearAddress
CREATE TABLE NearAddress (
    project_id UUID REFERENCES Projects(project_id),
    near_address VARCHAR UNIQUE
);

-- Table: XActivityLog
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

-- Table: GithubRepoActivityLog
CREATE TABLE GithubRepoActivityLog (
    github_repo_id UUID REFERENCES GithubRepos(github_repo_id),
    daily_commit_count INT,
    daily_open_issue_count INT,
    daily_closed_issue_count INT,
    daily_pull_count INT,
    daily_merge_count INT,
    watchers_count INT,
    stars_count INT,
    forks_count INT,
    datetime TIMESTAMP
);

-- Table: OnChainActivityLog
CREATE TABLE OnChainActivityLog (
    near_address VARCHAR REFERENCES NearAddress(near_address),
    activity_log VARCHAR
);

-- Table: ProjectReport
CREATE TABLE ProjectReport (
    project_id UUID REFERENCES Projects(project_id),
    report VARCHAR,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    most_recent BOOLEAN
);
