from setuptools import setup, find_packages
from typing import (
  List,
)

from aoirint_hg100rclient import __VERSION__ as VERSION

install_requires: List[str] = [
  # dependencies like requirements.txt
  'requests', # https://pypi.org/project/requests/
  'pydantic', # https://pypi.org/project/pydantic/
]

setup(
  name='aoirint_hg100rclient',
  version=VERSION, # '0.1.0-alpha', # == 0.1.0-alpha0 == 0.1.0a0
  # license='MIT',

  # packages=[ 'PACKAGE_NAME', ],
  packages=find_packages(),
  include_package_data=True,

  entry_points = {
    'console_scripts': [
      # create `main` function in PACKAGE_NAME/scripts/my_command_module.py
      'hg100r = aoirint_hg100rclient.script:main',
    ],
  },

  install_requires=install_requires,

  author='aoirint',
  author_email='aoirint@gmail.com',

  url='https://github.com/aoirint/aoirint_hg100rclient',
  description='CATV回線用モデムHUMAX HG100R-02JGをHTTP API経由で操作するための非公式パッケージ',

  long_description=open('README.md', 'r').read(),
  long_description_content_type='text/markdown',

  classifiers=[
    'Development Status :: 3 - Alpha',
    # 'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
