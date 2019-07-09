#! -*- coding:utf-8 -*-

'''
Passwords
=========

We do not put passwords into source control.
But often we need them, often for third party
reasons and sometimes because we stoopid

SO this directory is tied to weaver/devtools/passwordgetter.py

'''
from weaver_exception import WeaverBaseError
from weaver_log import logging, logger
log = logger.getLogger(__name__)
ROOTDIR = '~/.mikadopasswords'

def get_password_for_file(filename):
    """Given a file name ('github.password') return the *only* text in it.


    """
    files = os.listdir(ROOTDIR)
    if filename not in files:
        raise
