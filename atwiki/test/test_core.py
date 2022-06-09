# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import re
from unittest import TestCase

from atwiki.core import AtWikiAPI
from atwiki.uri import AtWikiURI

from . import TEST_BASE_URI

class AtWikiAPITest(TestCase):
  def setUp(self):
    self._api = AtWikiAPI(AtWikiURI(TEST_BASE_URI))

  def test_get_list(self):
    results = list(self._api.get_list())
    self.assertEqual(len(results), 19)

  def test_get_list_tag(self):
    results = list(self._api.get_list('tag01'))
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0]['id'], 18)
    self.assertEqual(results[0]['name'], 'Test_atwiki.test.test_core:AtWikiAPITest:test_get_list_tag')

  def test_get_tags(self):
    results = list(self._api.get_tags())
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0]['name'], 'tag01')
    self.assertEqual(results[0]['weight'], 1)

  def test_get_source(self):
    self.assertEqual(self._api.get_source(14, 0),
                     'テスト1\nテスト2\n\nテスト3\nテスト4\n\n\nテスト5')
    self.assertEqual(self._api.get_source(14, 1),
                     'テスト1\nテスト2\n\nテスト3\nテスト4')

  def test_get_source_special(self):
    self.assertEqual(self._api.get_source(15, 0),
                     '"テスト1"<br>&\n"テスト2"<br>&')

  def test_get_source_invalid(self):
    self.assertRaises(IndexError, self._api.get_source, 15, 100000)

  def test_search(self):
    results = list(self._api.search('SearchKeyword01 SearchKeyword02'))
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0]['name'], 'Test_atwiki.test.test_core:AtWikiAPITest:test_search')
    self.assertEqual(results[0]['snippet'], 'SearchKeyword01  SearchKeyword02')

  def test_search_or(self):
    results = list(self._api.search('SearchKeyword01 SearchKeyword02', False))
    self.assertEqual(len(results), 2)
    self.assertEqual(results[0]['name'], 'Test_atwiki.test.test_core:AtWikiAPITest:test_search')
    self.assertEqual(results[0]['snippet'], 'SearchKeyword01  SearchKeyword02')
    self.assertEqual(results[1]['name'], 'Test_atwiki.test.test_core:AtWikiAPITest:test_search_or')
    self.assertEqual(results[1]['snippet'], 'SearchKeyword02')

  def test_search_none(self):
    results = list(self._api.search('no_result_expected_for_this'))
    self.assertEqual(len(results), 0)


class PagerizeTest(TestCase):
    def setUp(self):
        self._uri = AtWikiURI('https://w.atwiki.jp/hmiku')
        self._api = AtWikiAPI(self._uri)

    def test_get_list(self):
        top_page = next(self._api.get_list())
        assert top_page == {'id': 1, 'name': 'トップページ'}

        soup = self._api._request(self._uri.list(sort='create', index=1))
        text = soup.find('div', class_='pagelist').text
        m = re.search(r'計 (\d+) ページ / 1 から 100 を表示', text)
        assert m is not None
        count = int(m.group(1))
        assert 45000 < count < 90000
        last_index = math.ceil(count / 100)

        # Get list from the last page.
        # N.B. The page counter is not updated immediately.
        pages = list(self._api.get_list(_start=last_index))
        expected = (count % 100)
        assert max(0, (expected - 50)) < len(pages) < min(100, (expected + 50))

        top_page = next(self._api.get_list(_start=last_index + 1))
        assert top_page == {'id': 1, 'name': 'トップページ'}

    def test_get_list_tag(self):
        soup = self._api._request(self._uri.tag('曲', index=1))
        last_index = 1
        for link in soup.find('div', class_='cmd_tag').find_all('a'):
            if not link.attrs['href'].endswith('&p={}'.format(last_index + 1)):
                break
            last_index += 1
        pages = list(self._api.get_list('曲', _start=last_index))
        assert 1 <= len(pages) <= 50

        pages = list(self._api.get_list('曲', _start=last_index + 1))
        assert len(pages) == 0

    def test_get_tags(self):
        song = next(self._api.get_tags('num'))
        assert song['name'] == '曲'
        assert 35000 < song['weight'] < 70000

        not_song = next(self._api.get_tags('num', _start=2))
        assert not_song['name'] != '曲'
