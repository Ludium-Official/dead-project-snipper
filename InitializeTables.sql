TRUNCATE TABLE ProjectReport,
                WalletActivityLog,
                GithubRepoActivityLog,
                XActivityLog,
                XHandlesDailyFollowInfo,
                GithubRepos,
                XHandles,
                AllUsers,
                Projects
                RESTART IDENTITY CASCADE;