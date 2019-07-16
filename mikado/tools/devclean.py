#!/bin/env python
"""devclean

Usage:
  devclean <rootpath> [--show]
  devclean (-h | --help)
  devclean --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --show        Only show dont kill files

"""
import os, sys
from fnmatch import fnmatch
from docopt import docopt



crap_matcher = ['*~',
                '*.*~',
                '*.pyc',
                '#*#']
ignore_dirs  = ['.git', '__pycache__']




def killfiles(kill_list,
              flag=False):
    '''
    '''
    for fn in kill_list:
        if flag:
            try:
                os.remove(fn)
                print("[x] ", fn)
            except Exception as e:
                print("[FAILED] %s because: %s" % (fn, e))
        else:
            print("[ ] ", fn)

def clean_tree(cwd=None,
               killflag=False):
    '''walk eveything below me, delete all the crap
    '''
    rdir = cwd or os.getcwd()
    kill_list = []
    for root, dirs, files in os.walk(rdir):
        #do we have dirs to ignore in next depth??
        for _dir in dirs:
            if _dir in ignore_dirs:
                dirs.remove(_dir)
        # now for each file, remove the crap, use globbing 
        for file in files:
            for pattern in crap_matcher:
                if fnmatch(file, pattern):
                    kill_list.append(os.path.join(root, file))
    killfiles(kill_list, killflag)

#entrypoint 
def main():
    """ """
    args = docopt(__doc__)
    killflag = bool(not args['--show'])
    rootpath = args['<rootpath>']
    clean_tree(cwd=rootpath,
               killflag=killflag)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
