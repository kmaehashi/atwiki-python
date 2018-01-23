# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

try:
  # Python 3
  from urllib.request import urlopen, Request
except ImportError:
  # Python 2
  from urllib2 import urlopen, Request

import re
import time
from collections import namedtuple

import bs4
import bs4.element
from bs4 import BeautifulSoup

from .uri import AtWikiURI

class AtWikiAPI(object):
  _PAGER_PATTERN = re.compile(r'.+?(\d+).+?(\d+).+?(\d+).+?')  # "計 110 ページ / 1 から 100 を表示"

  def __init__(self, uri, **kwargs):
    self._uri = uri
    self._user_agent = kwargs.get('user_agent', 'Mozilla/5.0')
    self._sleep = kwargs.get('sleep', 1)

  def get_list(self, tag=None):
    index = 0
    while True:
      count = 0
      is_end = True
      if tag:
        soup = self._request(self._uri.tag(tag, index))
        links = soup.find('div', attrs={'class': 'cmd_tag'}).findAll('a', href=True)
        is_end = False
      else:
        soup = self._request(self._uri.list('create', index))
        links = soup.find('table', attrs={'class': 'pagelist'}).findAll('a', href=True, title=True)
        pager = soup.find('div', attrs={'class': 'pagelist'}).findAll('p')[2].text
        m = self._PAGER_PATTERN.search(pager)
        if m:
          (total, cursor_begin, cursor_end) = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
          is_end = (total == cursor_end)
        else:
          is_end = True
      for link in links:
        page_id = self._uri.get_page_id_from_uri(link.attrs['href'])
        page_name = link.text.strip()
        if page_id:
          count += 1
          yield {'id': page_id, 'name': page_name}
      if count == 0 or is_end: break
      index += 1
      time.sleep(self._sleep)

  def get_tags(self):
    index = 0
    while True:
      count = 0
      soup = self._request(self._uri.tag('', index))
      links = soup.find('div', attrs={'class': 'cmd_tag'}).findAll('a', attrs={'class': 'tag'})
      for link in links:
        tag_name = link.text
        tag_weight = 0
        for clazz in link.attrs['class']:
          if clazz.startswith('weight'):
            tag_weight = int(clazz[6:])
            break
        count += 1
        yield {'name': tag_name, 'weight': tag_weight}
      if count == 0: break
      index += 1
      time.sleep(self._sleep)

  def get_source(self, page_id, generation=0):
    soup = self._request(self._uri.backup_source(page_id, generation))
    pre = soup.find('pre', attrs={'class': 'cmd_backup'})
    if not pre:
      raise IndexError('page {0}: generation {1} out of range'.format(page_id, generation))
    return pre.text.replace('\r', '')

  def search(self, keyword, is_and=True, wiki_syntax=False, complete=True):
    soup = self._request(self._uri.search(keyword, is_and, wiki_syntax, complete))
    lis = soup.find('div', id='wikibody').findAll('li')[:-1]  # drop last item (link to https://atwiki.jp/wiki/<keyword>)
    for li in lis:
      a = li.find('a')
      if not a: continue
      name = a.text
      snippet = None
      for sib in a.next_siblings:
        if snippet is None:
          if sib.name == 'br': snippet = ''
          continue
        if isinstance(sib, bs4.element.Tag):
          snippet += sib.text
        else:
          snippet += str(sib)
      snippet = '' if snippet is None else snippet.strip()
      yield {'name': name, 'snippet': snippet}

  def _request(self, url, data=None):
    req = Request(url, headers={'User-Agent': self._user_agent}, data=data)
    return BeautifulSoup(urlopen(req).read(), 'html5lib')
