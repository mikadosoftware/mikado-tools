#!/bin/env python
#! -*- coding:utf-8 -*-

"""repowatch

Monitor and synchronise Github and my laptop

Usage:
  repowatch showremote
  repowatch checklocal [--projectpath=~/projects]   
  repowatch open <repo>
  repowatch show <repo>
  repowatch (-h | --help)
  repowatch --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  

"""

from github import Github
import time
import os
import pprint
import getpass
import subprocess
from docopt import docopt

'''
Repo Watch is a simple exercise to keep my local laptop 
synchronised with the ridiculous number of repos I keep creating 

use `hub` to create a new repo as in ::

  $ `repowatch` shows a repo exists but not in github
  $ cd mikado-reporting
  $ hub create mikadosoftware/mikado-reporting
  $ git push 

'''

#{ } Add pypi status check to repo watch
def check_pypi_status(package_name):
    """Check on the simple pypi server for detaisl """
    from pypi_simple import PyPISimple
    client = PyPISimple()
    packages = client.get_project_files('todoinator')
    idx = len(packages)
    print(packages[idx-1].version)
    #need to work on this idx

def showrepos():
    github_password = open('/home/pbrian/secrets/github.token.mini01').read().strip()
    
    g = Github(github_password)

    for repo in g.get_user().get_repos():

        if repo.owner.login in ("lifeisstillgood",
                                'mikadosoftware') and not repo.fork:
            print("#", repo.name)
            print("git clone %s" % repo.ssh_url)


def get_origin_url(repopath):
    """Return the url for this repo on disk """
    try:
        url = do_subprocess(['git', '-C', repopath, 'config', 'remote.origin.url'])
        #expect:git@github.com:mikadosoftware/annotate.git
        path = url.strip().split(":")[1].replace(".git","")
        newurl = "https://github.com/" + path
    except:
        newurl = 'Not Found'
    return newurl
    
def open_repo(repopath):
    """FInd the remote url for repopath and open in webbrowser """
    url = get_origin_url(repopath)
    import webbrowser
    webbrowser.open_new_tab(newurl)

def show_repo(repopath):
    """Tell me to avoid firefox weirdness """
    url = get_origin_url(repopath)
    print(url)

def monitor_all_ondisk(paths):
    """FOr all potential repo holding firs in paths, walk into each top level
    dir and check_ondisk_status """
    all_top_dirs = []
    for path in paths:
        files = os.scandir(path)
        all_top_dirs.extend([d.path for d in files if d.is_dir()])
        
    for repopath in all_top_dirs:
        check_ondisk_status(repopath)
    

def do_subprocess(cmdlist, shell=False):
    """Given a  list of cmds (or potentially a string for shell)
    run them in subprocess, and return stdout + stderr
    (since I just read whats on screen, munging stdout and stderr seems
    bearable)
    """
    capture = subprocess.run(cmdlist, capture_output=True)
    if capture.returncode == 0:
        return capture.stdout.decode('utf-8')
    else:
        return capture.stderr.decode('utf-8')
    
    
def check_ondisk_status(repopath):
    """Given a dir on disk, check if it is git, and what status is """
    ### flags
    #: not git repo?
    isGitRepo = True
    #: files been changed but not committed?
    isDirtyWorkspace = False
    #: out of sync with remote?
    isOutOfSync = False
    
    output = do_subprocess(['git', '-C', repopath, 'status'])
    
    if 'fatal: not a git repository' in output:
        isGitRepo = False
    if 'nothing to commit, working tree clean' in output:
        isDirtyWorkspace = False
    else:
        isDirtyWorkspace = True
    if '''Your branch is up-to-date ''' in output:
        isOutOfSync = False
    else:
        isOutOfSync = True
        #this not quite right as could be on other brnach ...
    
    if not isDirtyWorkspace and not isOutOfSync and isGitRepo:
        pass
    else:
        print("---", repopath, end='')
        s = ''

        if isDirtyWorkspace:
            s += " - Files to commit"
        if isOutOfSync:
            s += " - Commits to upload"
        if not isGitRepo:
            s = " - Not a Repo"
    
        print(s)
        
    
def run():
    args = docopt(__doc__)
    if args['open']:
        repopath = args['<repo>']
        repopath = os.path.abspath(repopath)
        open_repo(repopath)
    if args['show']:
        repopath = args['<repo>']
        repopath = os.path.abspath(repopath)
        show_repo(repopath)
    if args['showremote']:
        showrepos()
    if args['checklocal']:
        givenpath = args['--projectpath']
        from pathlib import Path
        if not givenpath:
            projectpaths = [Path.home() / 'projects']
        else:
            projectpaths = [givenpath,]
        monitor_all_ondisk(projectpaths)    
    
if __name__ == '__main__':
    paths = ['/home/pbrian/projects',]
    monitor_all_ondisk(paths)

