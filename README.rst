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

Install
-------

::

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
