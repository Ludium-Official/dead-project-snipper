TRUNCATE TABLE ProjectReport,
                OnChainActivityLog,
                GithubRepoActivityLog,
                XActivityLog,
                NearAddress,
                GithubRepos,
                XAccounts,
                FundedMembers,
                Projects
                RESTART IDENTITY CASCADE;
