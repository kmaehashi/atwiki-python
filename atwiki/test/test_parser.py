# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from unittest import TestCase

from atwiki.parser import AtWikiStripper

INPUT = r"""
// This is a comment.

&nivocideo(url) &color(#ffffff){white} and black

[[Link1]] / [[Link2>URL]]
Styles: ''bold'' '''italic''' %%del%% ''bold'' 
Special: '' A ✔︎ ( ) { } \ / ! '' 


#right(aaa){inline} 
#comment() 
#region
+item 1
++item 2
-item 1
--item 2
-+item 3
*head 1
**head 2
>quote 1
>>quote 2
 pre
---- 
#exk(xxx){{{
block 1
}}}
#exk(){{{{{
block 2
}}}}}
"""

OUTPUT = r"""

white and black

Link1 / Link2
Styles: bold italic del bold 
Special:  A ✔︎ ( ) { } \ / !  


inline


item 1
item 2
item 1
item 2
+item 3
head 1
head 2
quote 1
quote 2
pre

block 1
block 2"""

class AtWikiStripperTest(TestCase):
  def test_doc(self):
    stripper = AtWikiStripper(INPUT)
    self.assertEqual(OUTPUT, stripper.text())

  def test_single(self):
    stripper = AtWikiStripper('[[Test]]')
    self.assertEqual('Test', stripper.text())
