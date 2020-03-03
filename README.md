#bitbucket-helper

A command-line utility for working with lots of bitbucket server projects and repositories. 

The helper allows you to clone or pull every bitbucket repository you have access too. Repositories are pathed under their parent project, making it easy to identify the source project.

## Installation

The utility requires `python3.7`

```
pip install --user bitbucket-helper
```

## Setup

The first time you attempt to clone, you will get prompted to provide your bitbucket server hostname, username, a personal access token and a working directory where projects will get cloned.

To generate a read-only personal access token. Go to Bitbucket -> Manage account -> Personal Access Tokens.

```
bitbucket-helper sync

[Bitbucket server hostname]: myserver.domain    
[Bitbucket username]: myusername
[Personal access token]: secret
[Working directory (defaults to ~/bitbucket/)]: 
[Clone using http or ssh]: http
```

All configuration settings get stored in `~/.bitbucket-helper.config`. 

## Synchronising 

The synchronisation function uses bitbucket APIs to get all accessible projects and repositories. 
For each project, it will create a directory using its key. For each repository, we perform a `git clone` or a  `git pull` if we already have a local copy. After the pull, we prune and delete local branches that have been merged at the origin.

Local directory structure:

- working_directory (~/bitbucket)
  - proj1
    - repo1
    - repo2
  - proj2
    - repo1
    - repo2

```
bitbucket-helper sync
```

## Git log commands

Bitbucket helper makes it easy to search for commits across all of your repositories using simple filters. Log commands operate on locally synched repositories, so remember to do a `bitbucket-helper sync` first.

You can find all commits after a specified date using:
```
bitbucket-helper log --after=2020-03-02
```

To search from commits between two tags:
```
bitbucket-helper log --from_tag=1.9.0 --to_tag=1.9.1
```

The command outputs the following quoted comma-separated values:

```
"repo","commit_hash","unix_time","iso_date","commit_message","author"
```

