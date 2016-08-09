atwiki-python
=============

``atwiki-python`` is a client library to access [@wiki](https://atwiki.jp) from Python.

Install
-------

..

  pip install .

Requirements
------------

* Python 2.6, 2.7, 3.3, 3.4 or 3.5.

Usage
-----

.. code:: python

  from atwiki import *

  api = AtWikiAPI(AtWikiURI('http://www65.atwiki.jp/python-client/'))

  # List of pages.
  for page in api.get_list():
    print(page['name'])

  # List of pages tagged with 'tag01'.
  for page in api.get_list('tag01'):
    print(page['name'])

  # Source of page ID 14
  print(api.get_source(14))

License
-------

MIT License
