import stashy
from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.repository import Repository, RepositoryRole
from pybitbucket.team import Team


class Repo:
    def __init__(self, project, clone_uri):
        self.project = project
        self.clone_uri = clone_uri

    def __str__(self):
        return """{{'project': '{project}',\
                    'clone_uri': '{clone_uri}'}}""".format(project=self.project,
                                                           clone_uri=self.clone_uri)


class BitbucketServer:
    def __init__(self, host: str, user: str, token: str, clone_type: str, working_dir: str):
        self.bitbucket = stashy.connect(host, user, token)
        self.clone_type = clone_type
        self.working_dir = working_dir

    def repos(self):
        all_repos = []
        projects = self.bitbucket.projects.list()

        for project in projects:
            project_key = project['key']
            for repo in self.bitbucket.projects[project_key].repos.list():
                clone_links = repo['links']['clone']
                clone_uri = list(filter(lambda t: t['name'] == self.clone_type, clone_links))[
                    0]['href']

                all_repos.append(Repo(project, clone_uri))

        return all_repos


class BitbucketCloud:
    def __init__(self, user: str, password: str, email: str, clone_type: str, working_dir: str):
        self.user = user
        self.email = email
        self.clone_type = clone_type
        self.working_dir = working_dir

        self.bitbucket = Client(BasicAuthenticator(
            user,
            password,
            email))

    def repos(self):
        all_repos = []

        teams = Team.find_teams_for_role(
            RepositoryRole.MEMBER.value, client=self.bitbucket)

        for team in teams:
            for repo in Repository.find_repositories_by_owner_and_role(
                    owner=team.username, role=RepositoryRole.MEMBER.value, client=self.bitbucket):

                all_repos.append(Repo(project=repo.project,
                                      clone_uri=repo.clone[self.clone_type]))

        return all_repos
