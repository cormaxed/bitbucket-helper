import re
import os
import subprocess
import shlex


class Git:
    @staticmethod
    def pull(repo_path: str):
        print('Pulling ' + repo_path)
        subprocess.call(['git', 'pull'], cwd=repo_path)

    @staticmethod
    def prune_local(repo_path: str):
        print('Pruning merged local branches ' + repo_path)
        subprocess.call(["git", "fetch", "--prune"], cwd=repo_path)
        prune_cmd = shlex.split("""git branch -r | awk '{print $1}' |
         egrep -v -f /dev/fd/0 <(git branch -vv | grep origin)
         | awk '{print $1}' | xargs git branch -d""")
        subprocess.call(prune_cmd, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, cwd=repo_path)

    @staticmethod
    def __log_filters(args):
        filter_args = []

        if args.after:
            filter_args = ['--after=' + args.after]
        elif args.from_tag and args.to_tag:
            filter_args = [args.from_tag + '..' + args.to_tag]
        elif args.from_tag:
            filter_args = [args.from_tag + '..']

        return filter_args

    def __init__(self, working_dir: str):
        self.working_dir = working_dir

    def local_repo_path(self, project_key: str, clone_link: str):
        repo = re.search('.*/(.*).git$', clone_link).group(1)
        return os.path.join(self.working_dir, project_key, repo)

    def clone(self, project_key: str, clone_link: str):
        project_path = os.path.join(self.working_dir, project_key)
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        print("Cloning " + clone_link)
        subprocess.call(
            ["git", "clone", clone_link], cwd=project_path)

    def log(self, args):
        header = "\"repo\",\"commit_hash\",\"unix_time\",\"iso_date\",\"commit_message\",\"author\""
        print(header)
        pretty_template = "--pretty=\"{project}/{repo}\",\"%C(auto)%h\","\
            + "\"%at\",\"%aI\",\"%s\",\"%ae\""""

        for project in os.listdir(self.working_dir):
            project_path = os.path.join(self.working_dir, project)

            if not os.path.isdir(project_path):
                continue

            repos = os.listdir(path=project_path)
            for repo in repos:
                repo_path = os.path.join(project_path, repo)

                if not os.path.isdir(repo_path):
                    continue

                pretty = pretty_template.format(project=project, repo=repo)
                log_cmd = ["git", "log", pretty]
                log_cmd = log_cmd + self.__log_filters(args)

                result = subprocess.run(log_cmd, check=False,
                                        capture_output=True, text=True, cwd=repo_path)

                if result.returncode == 0 and result.stdout:
                    for log_line in result.stdout.splitlines():
                        log_record = re.search('^(\".*\")', log_line)

                        if log_record:
                            print(log_record.group(1))
