# GITHUB BACKUP
Github automatic clone and pull to local machine

Preparations

0) Install github cli, eg. gh-command
1) Authenticate gh-cli: https://cli.github.com/manual/gh_auth_login
   Create an personal access token (old style) and use that to authenticate
   gh command

2) Make an backup directory and modify conf.ini to match that directory

3) Modify conf.ini organizations to match your username and possible organizations

Example configuration conf-example.ini should be copied to conf.ini


This script does following:

1) lists repositories from user/organization and outputs them to file
2) parses that file and for each repository a separate thread is launced which
   a) sees if repository directory exists, if not, creates is by clone
   b) if it exists, issues an pull


Crontab entry for cloning repositories at the end of day:

55 16 * * * /home/user/bin/github-backup/github-backup.py >> /a/git/github-backup/runlog.log


Normal first run

`./github-backup.py`
```
Start ... 2022-11-09 17:14:58
Printing repos to /a/git/github-backup/ORG1_repos.txt
ORG1_repo1- clone
ORG1_repo2- clone
Cloning into 'ORG1_repo1
Cloning into 'ORG1_repo2
USER1_repo1 - clone
USER1_repo2 - clone
remote: Enumerating objects: 778, done.
remote: Enumerating objects: 71, done.
...
...
End 2022-11-09 17:18:17
```

And then subsequent runs should either pull or report up to date

`./github-backup.py`
```
Start ... 2022-11-09 18:14:58
...
USER1_repo1 - pull
USER1_repo1 : Already up to date.
...

End 2022-11-09 17:18:17
```
