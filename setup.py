#! -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import glob

# get version data
with open("VERSION") as fo:
    version = fo.read()

setup(
     name='mikado.tools',
     version=version,
     description='A Description to change',
     author='author',
     packages=find_packages(exclude=('tests')),
     #Make any (python/bash) scripts found here executable in PATH
     scripts=glob.glob('bin/*'),
     install_requires = [
        line.strip() for line in open('requirements.txt')
     ],
)
