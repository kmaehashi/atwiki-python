# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from atwiki.uri import AtWikiURI

from . import TEST_BASE_URI

class AtWikiURITest(TestCase):
  def test_str(self):
    base = TEST_BASE_URI
    self.assertEqual(base, str(AtWikiURI(base)))

  def test_path_input(self):
    base = TEST_BASE_URI
    uri = AtWikiURI(base)

    self.assertEqual(uri.get_page_id_from_uri('{0}/backupx/123/list.html'.format(base)), 123)
    self.assertEqual(uri.get_page_id_from_uri('{0}/?cmd=backup&action=show&pageid=456&num=1'.format(base)), 456)
    self.assertEqual(uri.get_page_id_from_uri('{0}/pages/789.html'.format(base)), 789)

  def test_path_output(self):
    base = TEST_BASE_URI
    uri = AtWikiURI(base)

    self.assertEqual(uri.search(), '{0}/search'.format(base))
    self.assertEqual(uri.search('test'), '{0}/?cmd=search&keyword=test&andor=and&search_field=&cmp=cmp'.format(base))
    self.assertEqual(uri.search('test', is_and=False), '{0}/?cmd=search&keyword=test&andor=or&search_field=&cmp=cmp'.format(base))
    self.assertEqual(uri.search('test', wiki_syntax=True), '{0}/?cmd=search&keyword=test&andor=and&search_field=source&cmp=cmp'.format(base))
    self.assertEqual(uri.search('test', complete=False), '{0}/?cmd=search&keyword=test&andor=and&search_field=&cmp='.format(base))
    self.assertEqual(uri.tags(), '{0}/tag/?sort=&p=1'.format(base))
    self.assertEqual(uri.tags('num', 2), '{0}/tag/?sort=num&p=2'.format(base))
    self.assertEqual(uri.tag(), '{0}/tag/?p=1'.format(base))  # deprecated
    self.assertEqual(uri.tag('test'), '{0}/tag/test?p=1'.format(base))
    self.assertEqual(uri.tag('test', 2), '{0}/tag/test?p=2'.format(base))
    self.assertEqual(uri.new(), '{0}/new'.format(base))
    self.assertEqual(uri.list(), '{0}/list?sort=update&pp=1'.format(base))
    self.assertEqual(uri.list('create'), '{0}/list?sort=create&pp=1'.format(base))
    self.assertEqual(uri.list('create', 2), '{0}/list?sort=create&pp=2'.format(base))
    self.assertEqual(uri.contact(), '{0}/contact'.format(base))

    self.assertEqual(uri.backup_list(), '{0}/?cmd=backup&action=list'.format(base))
    self.assertEqual(uri.backup_list(10), '{0}/?cmd=backup&action=list&pageid=10'.format(base))
    self.assertEqual(uri.backup_source(10, 1), '{0}/?cmd=backup&action=source&pageid=10&num=1'.format(base))
    self.assertEqual(uri.backup_show(10, 1), '{0}/?cmd=backup&action=show&pageid=10&num=1'.format(base))
    self.assertEqual(uri.backup_diff(10, 1), '{0}/?cmd=backup&action=diff&pageid=10&num=1'.format(base))
    self.assertEqual(uri.backup_nowdiff(10, 1), '{0}/?cmd=backup&action=nowdiff&pageid=10&num=1'.format(base))

    self.assertEqual(uri.page(10), '{0}/pages/10.html'.format(base))
    self.assertEqual(uri.diff(10), '{0}/diffx/10.html'.format(base))
    self.assertEqual(uri.word(10, 'test'), '{0}/?cmd=word&pageid=10&word=test&type=normal'.format(base))
    self.assertEqual(uri.edit(10), '{0}/editx/10.html'.format(base))
    self.assertEqual(uri.edit(10, False), '{0}/editxx/10.html'.format(base))
    self.assertEqual(uri.rename(10), '{0}/renamex/10.html'.format(base))
    self.assertEqual(uri.chmod(10), '{0}/chmod/10.html'.format(base))
    self.assertEqual(uri.chkind(10), '{0}/chkind/10.html'.format(base))
    self.assertEqual(uri.upload(10), '{0}/upload/10.html'.format(base))
