from setuptools import setup
import sys
from os import system, path

if __name__ == "__main__":
   setup()

   if sys.platform == 'win32':
      system('mkdir C:\\runnr')
      system('copy .\\runnr.conf C:\\runnr')
   elif sys.platform in ['darwin', 'linux']:
      path = path.expanduser('~')
      system(f'cp runnr.conf {path}/.config')