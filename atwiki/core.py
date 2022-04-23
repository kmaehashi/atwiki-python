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
  _TAG_WEIGHT_PATTERN = re.compile(r'\((\d+)\)$')  # "タグ名(1)"

  def __init__(self, uri, **kwargs):
    self._uri = uri
    self._user_agent = kwargs.get('user_agent', 'Mozilla/5.0 (AtWikiPython)')
    self._sleep = kwargs.get('sleep', 10)  # in seconds
    self._last_request = 0.0  # epoch second last request has made

  def get_list(self, tag=None, _start=1):
    index = _start
    while True:
      count = 0
      if tag:
        soup = self._request(self._uri.tag(tag, index))
        links = soup.find('div', attrs={'class': 'cmd_tag'}).find('ul').select('a')
        pager = soup.find('div', attrs={'class': 'cmd_tag'}).select_one('a[href$="?&p={}"]'.format(index + 1))
      else:
        soup = self._request(self._uri.list('create', index))
        links = soup.find('table', attrs={'class': 'pagelist'}).findAll('a', href=True, title=True)
        pager = soup.find('ul', attrs={'class': 'atwiki_pagination'})
        if pager is not None:
          pager = pager.select_one('a[href$="&pp={}"]'.format(index + 1))
      is_end = (pager is None or len(links) == 0)
      for link in links:
        page_id = self._uri.get_page_id_from_uri(link.attrs['href'])
        page_name = link.text.strip()
        if page_id:
          count += 1
          yield {'id': page_id, 'name': page_name}
      if count == 0 or is_end: break
      index += 1

  def get_tags(self, sort='', _start=1):
    index = _start
    while True:
      count = 0
      soup = self._request(self._uri.tags(sort, index))
      links = soup.find('div', attrs={'class': 'cmd_tag'}).findAll('a', attrs={'class': 'tag'})
      for link in links:
        tag_name = link.text
        tag_weight = 0
        m = self._TAG_WEIGHT_PATTERN.search(link.attrs['title'])
        if m:
          tag_weight = int(m.group(1))
        count += 1
        yield {'name': tag_name, 'weight': tag_weight}
      if count == 0: break

      # Find "次の500件" link.
      pager = soup.find('div', attrs={'class': 'cmd_tag'}).select_one('a[href$="/tag/?p={}"]'.format(index + 1))
      if not pager:
        break
      index += 1

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
    sleep = self._last_request + self._sleep - time.time()
    if 0 < sleep:
      time.sleep(sleep)
    self._last_request = time.time()
    return BeautifulSoup(urlopen(req).read(), 'html5lib')
