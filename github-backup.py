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
    config = configparser.ConfigParser()
    config.read('conf.ini')
    return config

# thread function for each repository
def handle_repo(repo,org,repodir):
    
    repopath = repodir + "/" + org + "_" + repo

    if (os.path.exists(repopath)):
        print("{} - pull".format(repopath))
        stream = os.popen('cd ' + repopath  + ' && git pull')
        output = stream.read()
        print("{} : {}".format(repopath,output))
    else:
        print("{} - clone".format(repopath))
        stream = os.popen('git clone git@github.com:'+ org + '/' + repo + '.git ' + repopath)
        output = stream.read()
        print("{} : {}".format(repopath,output))


# main program
if __name__ == "__main__":

    config = read_config()

    threads = list()
    now = datetime.datetime.now()
    print ("---------------------")
    print ("Start ... {}".format(now.strftime("%Y-%m-%d %H:%M:%S")))


    # for each organization output repository list
    for org in json.loads(config['Settings']['orgs']):

        repodir = config['Settings']['repodir']
        repofile = repodir + "/" + org + "_repos.txt"
        
        print("Outputting repos to {}".format(repofile))

        os.system("gh repo list " + org + " -L200 --json name --jq '.[].name' > " + repofile)

        file1 = open(repofile, 'r')

        repos = file1.readlines()

        # for each repository in this organization, create an separate thread for
        # cloning or pulling repository
        for repo in repos:
            repo = repo.strip()
            # create and call thread for one repository
            x = threading.Thread(target=handle_repo, args=(repo,org,repodir,))
            threads.append(x)
            x.start()

    # wait for each thread to end executing
    for index, thread in enumerate(threads):
        thread.join()

    now = datetime.datetime.now()
    print ("End {}".format(now.strftime("%Y-%m-%d %H:%M:%S")))
