# GITHUB BACKUP
Github automatic backup. Does it by 1st cloning a mirror repo and then fetching updates to it

This scripts automates querying and backing up repositories from
multiple users or organizations. It makes following directory structure

```
github-backup/ORG1/repo1
github-backup/ORG1/repo2
github-backup/USER1/repo1
github-backup/USER1/repo2
```

where each repository is either cloned with --mirror (1st time) or fetched updates to.
This is meant to be used as a daily crontab job as a simple backup for
all the organization source codes to local servers.

## Preparations

- Install github cli, eg. gh-command
- Authenticate gh-cli: https://cli.github.com/manual/gh_auth_login
   Create an personal access token (old style) and use that to authenticate
   gh command
- Make an backup directory and modify conf.ini to match that directory

- Modify conf.ini organizations to match your username and possible organizations

Example configuration conf-example.ini should be copied to conf.ini

If you want token auth before script run, put your token in "token.txt" and
uncomment following lines:

//  # if login is necessary, uncomment 2 following lines and create token.txt

// #print("Login with gh")

//  #os.system(ghcommand + " auth login --with-token < token.txt > ghlog.txt 2>&1 ")

Normally script runs in threading mode.
If you want, you can use threading by uncommenting lines between THREADING START and THREADING END. 
one repository at a time sequentially. 

This seems to work ok in Mac OS with ulimit -n 2048. With threading, you need to maybe increase simultaneous files open limit if you have big repositories and/or many repositories. Increase can be done with increasing ulimit
command number in github-backup.py.
Alternatively you can commend block between THREADING START and THREADING END and use without threading.

This script does following:

- Lists repositories from user/organization and outputs them to file
- parses that file and for each repository a separate thread is launced which
  - sees if repository directory exists, if not, creates is by clone
  - if it exists, issues an pull

Crontab entry for cloning repositories at the end of day:

`55 16 * * * /home/user/bin/github-backup/github-backup.py >> /a/git/github-backup/runlog.log`


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
