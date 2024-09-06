from SQLScript import SQL_tools as SSS

class SocialMediaScore:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_id = SSS.pick_project_to_db(project_name)

    def read_df(self):
        return SSS.read_X_data(self.project_id)

    def frequency_of_posts(self):
        df = self.read_df()
        # Logic for frequency of posts

    def engagement_rates(self):
        df = self.read_df()
        # Logic for engagement rates

    def growth_decline_followers(self):
        df = self.read_df()
        # Logic for growth/decline in followers

class GithubScore:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_id = SSS.pick_project_to_db(project_name)

    def read_df(self):
        return SSS.read_git_data(self.project_id)

    def frequency_of_commit(self):
        df = self.read_df()
        # Logic for frequency of commits

    def number_of_active_contributors(self):
        df = self.read_df()
        # Logic for number of active contributors

    def issues_pull_request(self):
        df = self.read_df()
        # Logic for issues and pull requests

class OnchainActivityScore:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_id = SSS.pick_project_to_db(project_name)

    def read_df(self):
        return SSS.read_chain_data(self.project_id)

    def transaction(self):
        df = self.read_df()
        # Logic for transactions

    def unique_active_addresses(self):
        df = self.read_df()
        # Logic for unique active addresses

    def smart_contract_interactions(self):
        df = self.read_df()
        # Logic for smart contract interactions

