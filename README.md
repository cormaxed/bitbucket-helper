# bitbucket-helper

Bitbucket-helper is a command-line utility for working with lots of bitbucket server projects and repositories. This handy helper allows you to clone or pull every bitbucket repository you have access too. Repositories are pathed under their parent project, making it easy to identify the source project.

# Installation  

The utility requires python3.7.
```
pip install bitbucket-helper
```

# Setup

The first time you attempt to sync, you will get prompted to provide your bitbucket details. The tool supports both Bitbucket Server and Bitbucket Cloud.

Bitbucket Server requires a read-only personal access token. To generate goto Bitbucket -> Manage account -> Personal Access Tokens.

BitBucket Cloud requires an App Password if you use 2FA. The App needs to be granted read access.

All configuration settings get stored in `~/.bitbucket-helper.config`. To reconfigure you can delete this file. 

# Listing Repositories

To list all of the repositories, you have permission to access:

```
bitbucket-helper repo
```

The command outputs the following quoted comma-separated values:

```
"project_key","clone_uri"
```

# Synchronising 

The synchronisation function uses bitbucket APIs to get all accessible projects and repositories. 
For each project, it will create a directory using its key. For each repository, we perform a `git clone` or a  `git pull` if we already have a local copy. After the pull, we prune and delete local branches that have been merged at the origin.

Local directory structure:

- working_directory (~/bitbucket-server)
  - proj1
    - repo1
    - repo2
  - proj2
    - repo1
    - repo2

```
bitbucket-helper sync
```

## Pull requests

Bitbucket helper can list pull requests across all of your repositories. By default it returns OPEN pull requests, you can also filter for pull requests in a specific state, e.g. ALL, OPEN, MERGED, DECLINED.

```
bitbucket-helper pr --state=MERGED
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

## Create a Snyk Import File

Snyk created an [import utility](https://www.npmjs.com/package/snyk-api-import) to help import projects into BitBucket Cloud. The utility supports stable imports by pacing to avoid rate limiting and by implementing retries.

The import tool requires an import configuration file that bitbucket-helper can generate for you.

To generate an import configuration:

* orgid - Can be found in https://app.snyk.io/org/YOUR_ORG/manage/settings
* integrationid - Can be found in integrations menu for each SCM https://app.snyk.io/org/YOUR_ORG/manage/settings

```
bitbucket-helper snyk:import --owner <repositoryOwner> --orgid <snykOrganisationId> --integrationid <snykIntegrationId> --outfile /tmp/import-projects.json
```

## Find out more

You can find out more [here](http://omahony.id.au/tech/2020/05/03/Bitbucket-Helper.html) 