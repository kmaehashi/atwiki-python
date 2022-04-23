#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def _read(filename):
  with open(filename) as f:
    return f.read()

# Load package version.
exec(_read('atwiki/_version.py'))

setup(name='atwiki-python',
      version='.'.join(str(x) for x in VERSION),
      description='Atwiki Client Library',
      long_description=_read('README.rst'),
      url='https://github.com/kmaehashi/atwiki-python',
      author='Kenichi Maehashi',
      author_email='webmaster@kenichimaehashi.com',
      license='MIT',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
      packages=find_packages(),
      test_suite = 'atwiki.test',
      entry_points={
          'console_scripts': ['atwiki-dump=atwiki.tools.dump:main'],
      },
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*,!=3.6.*',
      install_requires=[
          'BeautifulSoup4',
          'html5lib',
      ],
)
