-- Table AllUsers
CREATE TABLE IF NOT EXISTS AllUsers (
    id VARCHAR PRIMARY KEY,
    total_donations_in_usd FLOAT,
    total_donations_out_usd FLOAT,
    total_matching_pool_allocations_usd FLOAT,
    donors_count INT,
    near_social_profile_data JSON
);

-- Table Projects
CREATE TABLE IF NOT EXISTS Projects (
    project_wallet_address VARCHAR PRIMARY KEY,
    project_potlock_url VARCHAR,
    project_official_website_url VARCHAR,
    created_date TIMESTAMP
);

-- Table XHandles
CREATE TABLE IF NOT EXISTS XHandles (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    handle VARCHAR UNIQUE,
    account_id VARCHAR,
    Description VARCHAR,
    created_date TIMESTAMP,
    PRIMARY KEY (project_wallet_address, handle)
);

-- Table GithubRepos
CREATE TABLE IF NOT EXISTS GithubRepos (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    github_repo_id UUID UNIQUE PRIMARY KEY,
    owner_name VARCHAR,
    github_repo VARCHAR
);

-- Table XActivityLog
CREATE TABLE IF NOT EXISTS XActivityLog (
    handle VARCHAR REFERENCES XHandles(handle),
    tweet VARCHAR,
    retweet_count INT,
    like_count INT,
    reply_count INT,
    quote_count INT,
    follower_count INT,
    datetime TIMESTAMP
);

-- Table GithubRepoActivityLog
CREATE TABLE IF NOT EXISTS GithubRepoActivityLog (
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

-- Table WalletActivityLog
CREATE TABLE IF NOT EXISTS WalletActivityLog (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    sent_count INT,
    received_count INT
);

-- Table ProjectReport
CREATE TABLE IF NOT EXISTS ProjectReport (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    report VARCHAR,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    most_recent BOOLEAN
);

-- Table XHandlesDailyFollowInfo
CREATE TABLE IF NOT EXISTS XHandlesDailyFollowInfo (
    handle VARCHAR REFERENCES XHandles(handle),
    following_count INT,
    follower_count INT
);

-- Foreign Key Constraints (already defined within tables)
ALTER TABLE IF EXISTS XHandles
    ADD CONSTRAINT fk_xhandles_project FOREIGN KEY (project_wallet_address)
    REFERENCES Projects (project_wallet_address);

ALTER TABLE IF EXISTS GithubRepos
    ADD CONSTRAINT fk_githubrepos_project FOREIGN KEY (project_wallet_address)
    REFERENCES Projects (project_wallet_address);

ALTER TABLE IF EXISTS GithubRepoActivityLog
    ADD CONSTRAINT fk_githubrepoactivitylog_repo FOREIGN KEY (github_repo_id)
    REFERENCES GithubRepos (github_repo_id);

ALTER TABLE IF EXISTS XActivityLog
    ADD CONSTRAINT fk_xactivitylog_handle FOREIGN KEY (handle)
    REFERENCES XHandles (handle);

ALTER TABLE IF EXISTS XHandlesDailyFollowInfo
    ADD CONSTRAINT fk_xhandlesdailyfollowinfo_handle FOREIGN KEY (handle)
    REFERENCES XHandles (handle);

ALTER TABLE IF EXISTS WalletActivityLog
    ADD CONSTRAINT fk_walletactivitylog_project FOREIGN KEY (project_wallet_address)
    REFERENCES Projects (project_wallet_address);

ALTER TABLE IF EXISTS ProjectReport
    ADD CONSTRAINT fk_projectreport_project FOREIGN KEY (project_wallet_address)
    REFERENCES Projects (project_wallet_address);
