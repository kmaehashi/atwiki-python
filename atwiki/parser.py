# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import re

class AtWikiStripper(object):
  # Comment: `// comment`
  COMMENT = re.compile(r'^//')

  # Inline annotation: `&color(#999999){text}`, `&nicovideo(url)`
  INLINE_ANN = re.compile(r'&[a-z_]+\(([^()]*?)\)({([^{}]+?)})?'), 3

  # Inline links: `[[page]]`, `[[alias>URL]]`
  INLINE_LINK = re.compile(r'\[\[(.+?)((>|>>)(.+?))?\]\]'), 1

  # Inline italic: `'''text'''`
  INLINE_ITALIC = re.compile(r'\'\'\'(.+?)\'\'\''), 1

  # Inline bold: `''text''`
  INLINE_BOLD = re.compile(r'\'\'(.+?)\'\''), 1

  # Inline del: `%%text%%`
  INLINE_DEL = re.compile(r'%%(.+?)%%'), 1

  # Line annotation: `#right(){text}`, `#comment()`, `#region`
  LINE_ANN = re.compile(r'^#[a-z_]+(\(([^()]*?)\)({([^{}]+?)})?)?\s*$'), 4

  # Line horizontal line: `----`
  LINE_HR = re.compile(r'^----\s*()$'), 1

  # Line item list and heading: `+foo`, `-foo`, `*foo`
  LINE_ITEMLIST = re.compile(r'^(\*+|\++|-+)(.+)$'), 2

  # Line quote: `>text`
  LINE_QUOTE = re.compile(r'^>+(.+)$'), 1

  # Line formatted: ` text`
  LINE_PRE = re.compile(r'^ (.+)$'), 1

  # Block annotation: `#exk(){{{` ... `}}}`
  BLOCK_BEGIN_ANN = re.compile(r'^#[a-z_]+\(([^{}()]*?)\)({+)\s*$')
  BLOCK_END_ANN = re.compile(r'^(}+)\s*$')

  def __init__(self, source):
    self._source = source

  def _inline_strip(self, line, pattern, group):
    while True:
      prev = line
      # Note: prior to Python 3.5, use of backreference of nonmatching group
      # in replacement string raises exception.
      line = pattern.sub(lambda m: m.group(group), line)
      if prev == line: return line

  def _line_process(self, buf, line, pattern, group):
    prev = line
    line = pattern.sub(lambda m: m.group(group), line)
    if prev == line: return False
    buf.append(line)
    return True

  def text(self):
    ret = []
    lines = self._source.splitlines()
    block_level = 0
    for line in lines:
      if self.COMMENT.match(line): continue
      line = self._inline_strip(line, *self.INLINE_ANN)
      line = self._inline_strip(line, *self.INLINE_LINK)
      line = self._inline_strip(line, *self.INLINE_ITALIC)
      line = self._inline_strip(line, *self.INLINE_BOLD)
      line = self._inline_strip(line, *self.INLINE_DEL)
      if self._line_process(ret, line, *self.LINE_ANN): continue
      if self._line_process(ret, line, *self.LINE_HR): continue
      if self._line_process(ret, line, *self.LINE_ITEMLIST): continue
      if self._line_process(ret, line, *self.LINE_QUOTE): continue
      if self._line_process(ret, line, *self.LINE_PRE): continue
      if block_level == 0:
        m = self.BLOCK_BEGIN_ANN.match(line)
        if m:
          block_level = len(m.group(2))
          continue
      else:
        m = self.BLOCK_END_ANN.match(line)
        if m and len(m.group(1)) == block_level:
          block_level = 0
          continue
      ret.append(line)
    return '\n'.join(ret)
