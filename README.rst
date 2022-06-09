|GitHubActions|_ |CodeCov|_ |PyPi|_

.. |GitHubActions| image:: https://github.com/kmaehashi/atwiki-python/actions/workflows/test.yml/badge.svg?branch=master
.. _GitHubActions: https://github.com/kmaehashi/atwiki-python/actions/workflows/test.yml

.. |CodeCov| image:: https://codecov.io/gh/kmaehashi/atwiki-python/branch/master/graph/badge.svg
.. _CodeCov: https://codecov.io/gh/kmaehashi/atwiki-python

.. |PyPi| image:: https://badge.fury.io/py/atwiki-python.svg
.. _PyPi: https://badge.fury.io/py/atwiki-python

atwiki-python
=============

``atwiki-python`` is a client library to access `@wiki <https://atwiki.jp/>`_ from Python.

This package also includes ``atwiki-dump`` command to dump source from @wiki wiki site.

Install
-------

::

  pip install atwiki-python

Requirements
------------

* Python 2.7 / 3.7 / 3.8 / 3.9 / 3.10

Usage
-----

``atwiki-dump`` Command
~~~~~~~~~~~~~~~~~~~~~~~

Dump source and page name for each page in the wiki site.

::

  atwiki-dump -o /tmp/dump_dir https://w.atwiki.jp/python-client/

Python API
~~~~~~~~~~

Python API provides access to @wiki features.

.. code:: python

  from atwiki import *

  api = AtWikiAPI(AtWikiURI('https://w.atwiki.jp/python-client/'))

  # Show list of tags.
  for tag in api.get_tags():
    print(tag)

  # Show list of pages.
  for page in api.get_list():
    print(page)

  # Show list of pages tagged with 'tag01'.
  for page in api.get_list('tag01'):
    print(page)

  # Show source of page ID 14.
  print(api.get_source(14))

  # Show results of wiki search.
  for result in api.search('test'):
    print(result)

Hints
-----

* Always use an appropraite interval between requests, or your IP address may get banned.
  Empirically, 10 seconds of sleep between API call is sufficient.
* Your application must expect that entries returned from APIs may be duplicate/missing when pages/tags are added/removed during API call.
  This is because listing requests are internally pagerized and it is costly to guarantee consistency.
* AtWiki's specification may change anytime.
  If you are going to build an automated system, it is encouraged to run test suites included with the installation of this library (``python -m unittest discover atwiki``) everytime before running your application.

License
-------

MIT License
