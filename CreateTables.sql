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
    handle VARCHAR UNIQUE NOT NULL,
    account_id VARCHAR,
    Description VARCHAR,
    condition VARCHAR(20),
    created_date TIMESTAMP
);

-- Table GithubRepos
CREATE TABLE IF NOT EXISTS GithubRepos (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    github_repo_id UUID UNIQUE PRIMARY KEY,
    owner_name VARCHAR,
    repo_name VARCHAR
);

-- Table XActivityLog
CREATE TABLE IF NOT EXISTS XActivityLog (
    handle VARCHAR REFERENCES XHandles(handle),
    tweet VARCHAR,
    retweet_count INT,
    like_count INT,
    reply_count INT,
    watch_count INT,
    datetime TIMESTAMP,
    updated_datetime TIMESTAMP

    -- Unique constraint on handle and datetime --
    CONSTRAINT unique_handle_created_datetime UNIQUE (handle, datetime)
);

-- Table GithubRepoActivityLog
CREATE TABLE IF NOT EXISTS GithubRepoActivityLog (
    github_repo_id UUID REFERENCES GithubRepos(github_repo_id),
    daily_commit_count INT,
    daily_open_issue_count INT,
    daily_closed_issue_count INT,
    daily_pull_count INT,
    daily_merge_count INT,
    subscribers_count INT,
    stars_count INT,
    forks_count INT,
    datetime TIMESTAMP
);

-- Table WalletActivityLog
CREATE TABLE IF NOT EXISTS WalletActivityLog (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    trasaction_count INT,
    datetime TIMESTAMP
);

-- Table ProjectReport
CREATE TABLE IF NOT EXISTS ProjectReport (
    project_wallet_address VARCHAR REFERENCES Projects(project_wallet_address),
    report_uuid UUID Unique,
    report Json,
    score INT,
    twitter_score INT,
    github_score INT,
    near_score INT,
    dead_or_alive BOOLEAN,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    most_recent BOOLEAN
);

-- Table XHandlesDailyFollowInfo
CREATE TABLE IF NOT EXISTS XHandlesDailyFollowInfo (
    handle VARCHAR REFERENCES XHandles(handle),
    favourites_count INT,
    following_count INT,
    followers_count INT,
    listed_count INT,
    media_count INT,
    datetime TIMESTAMP
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
