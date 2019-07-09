#!/bin/env python
#! -*- coding:utf-8 -*-

"""repowatch

Monitor and synchronise Github and my laptop

Usage:
  repowatch show          
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

'''
Repo Watch is a simple exercise to keep my local laptop 
synchronised with the ridiculous number of repos I keep creating 
'''

def showrepos():
    github_password = open('/home/pbrian/secure/github').read()
    g = Github(github_password)

    for repo in g.get_user().get_repos():

        if repo.owner.login in ("lifeisstillgood",
                                'mikadosoftware') and not repo.fork:
            print("#", repo.name)
            print("git clone %s" % repo.ssh_url)

def main():
    args = docopt(__doc__)
    if args['show']:
        showrepos()

if __name__ == '__main__':
    showrepos()
