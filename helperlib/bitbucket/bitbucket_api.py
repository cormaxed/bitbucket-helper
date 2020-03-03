import stashy


class Bitbucket:
    def __init__(self, host: str, user: str, token: str):
        self.bitbucket = stashy.connect(host, user, token)

    def repos(self):
        all_repos = []
        projects = self.bitbucket.projects.list()

        for project in projects:
            project_key = project['key']
            repos = self.bitbucket.projects[project_key].repos.list()

            all_repos = all_repos + repos

        return all_repos
