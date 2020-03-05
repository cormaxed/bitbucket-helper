#bitbucket-helper

A command-line utility for working with lots of bitbucket server projects and repositories. 

The helper allows you to clone or pull every bitbucket repository you have access too. Repositories are pathed under their parent project, making it easy to identify the source project.

## Installation

The utility requires `python3.7`

```
pip install bitbucket-helper
```

## Setup

The first time you attempt to sync, you will get prompted to provide your bitbucket details. The tool supports both Bitbucket server and Bitbucket cloud.

Bitbucket server requires a read-only personal access token. To generate go to Bitbucket -> Manage account -> Personal Access Tokens.

Bickbucket cloud requires an App Password if you use 2FA. The App must be granted `Team Membership -> Read, Projects -> Read`

All configuration settings get stored in `~/.bitbucket-helper.config`. To reconfigure you can delete this file. 

## Listing Repositories

You can list all of the repositories you have permission to access with:

```
bitbucket-helper list
```

The command outputs the following quoted comma-separated values:

```
"project_key","clone_uri"
```

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

