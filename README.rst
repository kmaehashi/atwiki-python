|Travis|_ |Coveralls|_ |PyPi|_

.. |Travis| image:: https://api.travis-ci.org/kmaehashi/atwiki-python.svg?branch=master
.. _Travis: https://travis-ci.org/kmaehashi/atwiki-python

.. |Coveralls| image:: https://coveralls.io/repos/kmaehashi/atwiki-python/badge.svg?branch=master&service=github
.. _Coveralls: https://coveralls.io/r/kmaehashi/atwiki-python

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

* Python 2.7, 3.3, 3.4, 3.5 or 3.6.

Usage
-----

``atwiki-dump`` Tool
~~~~~~~~~~~~~~~~~~~~

Dump source and page name for each page in the wiki site.

::

  atwiki-dump -o /tmp/dump_dir https://www65.atwiki.jp/python-client/

Python API
~~~~~~~~~~

Python API provides access to @wiki features.

.. code:: python

  from atwiki import *

  api = AtWikiAPI(AtWikiURI('https://www65.atwiki.jp/python-client/'))

  # Show list of tags.
  for page in api.get_tags():
    print(page['name'])

  # Show list of pages.
  for page in api.get_list():
    print(page['name'])

  # Show list of pages tagged with 'tag01'.
  for page in api.get_list('tag01'):
    print(page['name'])

  # Show source of page ID 14.
  print(api.get_source(14))

  # Show results of wiki search.
  for result in api.search('test'):
    print(result)

License
-------

MIT License
