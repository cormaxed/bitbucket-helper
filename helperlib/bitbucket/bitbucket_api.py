import datetime
import stashy
from pybitbucket37.auth import BasicAuthenticator
from pybitbucket37.bitbucket import Client
from pybitbucket37.repository import Repository, RepositoryRole
from pybitbucket37.team import Team
from pybitbucket37.pullrequest import PullRequest

XLS_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


class Repo:
    def __init__(self, project, name, clone_uri, owner):
        self.project = project
        self.name = name
        self.clone_uri = clone_uri
        self.owner = owner

    def __str__(self):
        return """{{'project': '{project}',\
                    'name': '{name}, \
                    'clone_uri': '{clone_uri}',
                    'owner:': '{owner}'}}""".format(project=self.project,
                                                    name=self.name,
                                                    clone_uri=self.clone_uri,
                                                    owner=self.owner)


class PR:
    def __init__(self, repo, title, state, author, created_date, closed_date):
        self.repo = repo
        self.title = title
        self.state = state
        self.author = author
        self.created_date = created_date
        self.closed_date = closed_date

    def __str__(self):
        return """{{'project': '{project}',\
                    'repo_name': '{repo_name}', \
                    'title': '{title}', \
                    'state': '{state}', \
                    'author': '{author}, \
                    'created_date: '{created_date}', \
                    'closed_date: '{closed_date}'}}""".format(project=self.repo.project,
                                                              repo_name=self.repo.name,
                                                              title=self.title,
                                                              state=self.state,
                                                              author=self.author,
                                                              created_date=self.created_date,
                                                              closed_date=str(self.closed_date))


class BitbucketServer:
    def __init__(self, host: str, user: str, token: str, clone_type: str, working_dir: str):
        self.bitbucket = stashy.connect(host, user, token)
        self.clone_type = clone_type
        self.working_dir = working_dir

    def projects(self):
        return self.bitbucket.projects.list()

    def repos(self):
        all_repos = []

        for project in self.projects():
            project_key = project['key']
            for repo in self.bitbucket.projects[project_key].repos.list():
                clone_links = repo['links']['clone']
                clone_uri = list(filter(lambda t: t['name'] == self.clone_type, clone_links))[
                    0]['href']

                all_repos.append(
                    Repo(project, repo['name'], clone_uri, owner=None))

        return all_repos

    def pull_requests(self, repo, state):
        pull_requests = []

        for pr in self.bitbucket.projects[repo.project['key']].repos[repo.name].pull_requests.all(
                state=state):
            closed_date = None
            if pr['state'] in ('MERGED', 'DECLINED'):
                closed_date = datetime.datetime.utcfromtimestamp(
                    pr['closedDate']/1000).strftime(XLS_DATE_FORMAT)

            created_date = datetime.datetime.utcfromtimestamp(
                pr['createdDate']/1000).strftime(XLS_DATE_FORMAT)
            pull_requests.append(PR(repo, pr['title'], pr['state'], pr['author']['user']['name'],
                                    created_date, closed_date))

        return pull_requests


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

        self.teams = []
        for team in Team.find_teams_for_role(RepositoryRole.MEMBER.value, client=self.bitbucket):
            self.teams.append(team['username'])

    def repos(self):
        all_repos = []

        for team in self.teams:
            for repo in Repository.find_repositories_by_owner_and_role(
                    owner=team, role=RepositoryRole.MEMBER.value, client=self.bitbucket):

                all_repos.append(Repo(project=repo.project, name=repo.slug,
                                      clone_uri=repo.clone[self.clone_type],
                                      owner=repo.owner['username']))

        return all_repos

    def pull_requests(self, repo, state):
        pull_requests = []

        for team in self.teams:
            url_friendly_name = ' '.join(
                repo.name.split(' - ')).replace(' ', '-')
            for pr in PullRequest.find_pullrequests_for_repository_by_state(url_friendly_name,
                                                                            state=state,
                                                                            owner=team,
                                                                            client=self.bitbucket):
                if isinstance(pr, PullRequest):
                    closed_date = None
                    if pr.state in ('MERGED', 'DECLINED'):
                        closed_date = datetime.datetime.strptime(
                            pr.updated_on, ISO_DATE_FORMAT).strftime(XLS_DATE_FORMAT)

                    created_date = datetime.datetime.strptime(
                        pr.created_on, ISO_DATE_FORMAT).strftime(XLS_DATE_FORMAT)
                    pull_requests.append(PR(repo, pr.title, pr.state, pr.author['display_name'],
                                            created_date, closed_date))

        return pull_requests
