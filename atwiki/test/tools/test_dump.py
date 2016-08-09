# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from atwiki.tools.dump import AtWikiDump

from .. import TEST_BASE_URI

class AtWikiDumpTest(TestCase):
  def test_simple(self):
    self.assertRaises(IOError, AtWikiDump.start, ['-o', '/tmp/non/existing/directory', TEST_BASE_URI])
