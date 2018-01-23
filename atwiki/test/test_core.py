# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from atwiki.core import AtWikiAPI
from atwiki.uri import AtWikiURI

from . import TEST_BASE_URI

class AtWikiAPITest(TestCase):
  def setUp(self):
    self._api = AtWikiAPI(AtWikiURI(TEST_BASE_URI))

  def test_get_list(self):
    results = list(self._api.get_list())
    self.assertTrue(1 < len(results))

  def test_get_list_tag(self):
    results = list(self._api.get_list('tag01'))
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0]['id'], 18)
    self.assertEqual(results[0]['name'], 'Test_atwiki.test.test_core:AtWikiAPITest:test_get_list_tag')

  def test_get_tags(self):
    results = list(self._api.get_tags())
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0]['name'], 'tag01')
    self.assertEqual(results[0]['weight'], 3)

  def test_get_source(self):
    self.assertEqual(self._api.get_source(14, 0),
                     'テスト1\nテスト2\n\nテスト3\nテスト4\n\n\nテスト5')
    self.assertEqual(self._api.get_source(14, 1),
                     'テスト1\nテスト2\n\nテスト3\nテスト4')

  def test_get_source_special(self):
    self.assertEqual(self._api.get_source(15, 0),
                     '"テスト1"<br>&\n"テスト2"<br>&')

  def test_get_source_invalid(self):
    self.assertRaises(IndexError, self._api.get_source, 15, -1)

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
