#!/usr/bin/python3
import datetime
import os
import threading
import configparser
import json

# Backs up github code by clone & pull
# 
# 9.11.2022 
#
# Henry Palonen / PalonenLABS Oy


def read_config():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config = configparser.ConfigParser()
    config.read(os.path.join(__location__, 'conf.ini'))
    return config

# thread function for each repository
def handle_repo(repo,org,repodir):
    
    repopath = os.path.join(repodir, org + "/" + repo)

    if (os.path.exists(repopath)):
        print("{} - fetch".format(repopath))
        #stream = os.popen('cd ' + repopath  + ' && git pull --all')
        stream = os.popen('cd ' + repopath  + ' && git fetch --update-head-ok')
        output = stream.read()
        if (output != ""):
            print("{} : {}".format(repopath,output))
    else:
        print("{} - clone".format(repopath))
        stream = os.popen('git clone --mirror git@github.com:'+ org + '/' + repo + '.git ' + repopath)
        output = stream.read()
        print("{} : {}".format(repopath,output))
        #stream = os.popen('cd ' + repopath  + ' && git config --bool core.bare false')
        #output = stream.read()
        #print("{} : {}".format(repopath,output))


# main program
if __name__ == "__main__":

    config = read_config()

    threads = list()
    now = datetime.datetime.now()
    print ("---------------------")
    print ("Start ... {}".format(now.strftime("%Y-%m-%d %H:%M:%S")))

    # if login is necessary, uncomment 2 following lines and create token.txt
    #print("Login with gh")
    #os.system(ghcommand + " auth login --with-token < token.txt > ghlog.txt 2>&1 ")
    # for threading to work ?

    os.system("ulimit -n 8000")

    # for each organization output repository list
    for org in json.loads(config['Settings']['orgs']):

        repodir = config['Settings']['repodir']
        repofile = os.path.join(repodir, org + "/" + org + "_repos.txt")
        ghcommand = config['Settings']['ghcommand']

        stream = os.popen('mkdir -p ' + repodir + '/' + org)

        print("Outputting repos to {}".format(repofile))

        os.system(ghcommand + " repo list " + org + " -L200 --json name --jq '.[].name' > " + repofile)

        file1 = open(repofile, 'r')

        repos = file1.readlines()

        # for each repository in this organization, create an separate thread for
        # cloning or pulling repository
        # mac can't handle threads correctly, oserror.too many files open
        # ulimit -n 2048 for example could help
        for repo in repos:
            repo = repo.strip()

#### THREADING START        

            # without threading use this            
            #handle_repo(repo,org,repodir)

            # create and call thread for one repository
            x = threading.Thread(target=handle_repo, args=(repo,org,repodir,))
            threads.append(x)
            x.start()

    # wait for each thread to end executing
    for index, thread in enumerate(threads):
        thread.join()

#### THREADING END

    now = datetime.datetime.now()
    print ("End {}".format(now.strftime("%Y-%m-%d %H:%M:%S")))
