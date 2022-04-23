# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

try:
  # Python 3
  import urllib.parse as urlparse
  from urllib.parse import quote as urlquote
except:
  # Python 2
  import urlparse
  def urlquote(s, safe=b'/'):
    import urllib
    if isinstance(s, unicode):
      s = s.encode('utf-8')
    return urllib.quote(s, safe)

import os.path
import warnings


class AtWikiURI(object):
  def __init__(self, base):
    self._base = base

  def __str__(self):
    return self._base

  ########################################
  # URI Transformations
  ########################################

  def get_page_id_from_uri(self, uri):
    p = urlparse.urlparse(self.get_absolute_uri(uri))

    # backupx
    backupx = p.path.split('/')[-3:]
    if len(backupx) == 3 and backupx[0] == 'backupx' and backupx[2] == 'list.html':
      return int(backupx[1])

    # special pages
    pageid = urlparse.parse_qs(p.query).get('pageid', [None])[0]
    if pageid is not None:
      return int(pageid)

    # standard page
    if p.path.endswith('.html'):
      return int(os.path.splitext(os.path.basename(p.path))[0])

    return None

  def get_absolute_uri(self, uripart):
    return urlparse.urljoin(self._base, uripart)

  ########################################
  # Wiki-wide APIs
  ########################################

  def search(self, keyword=None, is_and=True, wiki_syntax=False, complete=True):
    if keyword is not None:
      andor = 'and' if is_and else 'or'
      search_field = 'source' if wiki_syntax else ''
      cmpmode = 'cmp' if complete else ''
      return '{0}/?cmd=search&keyword={1}&andor={2}&search_field={3}&cmp={4}'.format(
          self._base, urlquote(keyword), andor, search_field, cmpmode)
    else:
      return '{0}/search'.format(self._base)

  def tags(self, sort='', index=1):
    return '{}/tag/?sort={}&p={}'.format(self._base, sort, index)

  def tag(self, tag_name='', index=1):
    if tag_name == '':
      warnings.warn(
        'Specifying empty string to tag_name to get URL for list of tags is deprecated.'
        ' Use .tags() instead.',
        DeprecationWarning)
    return '{0}/tag/{1}?p={2}'.format(self._base, urlquote(tag_name), index)

  def new(self):
    return '{0}/new'.format(self._base)

  def list(self, sort='update', index=1):
    """
    ``sort`` can be any of ``update``, ``create``, ``create_desc`` or ``pagename``.
    """
    return '{0}/list?sort={1}&pp={2}'.format(self._base, sort, index)

  def contact(self):
    return '{0}/contact'.format(self._base)

  ########################################
  # Backup APIs
  ########################################

  def _backup(self, action, page_id=None, generation=None):
    url = '{0}/?cmd=backup&action={1}'.format(self._base, action)
    if page_id is not None:
      url += '&pageid={0}'.format(page_id)
    if generation is not None:
      url += '&num={0}'.format(generation)
    return url

  def backup_list(self, page_id=None):
    return self._backup('list', page_id)

  def backup_source(self, page_id, generation):
    return self._backup('source', page_id, generation)

  def backup_show(self, page_id, generation):
    return self._backup('show', page_id, generation)

  def backup_diff(self, page_id, generation):
    return self._backup('diff', page_id, generation)

  def backup_nowdiff(self, page_id, generation):
    return self._backup('nowdiff', page_id, generation)

  ########################################
  # Page APIs
  ########################################

  def page(self, page_id):
    return '{0}/pages/{1}.html'.format(self._base, page_id)

  def diff(self, page_id):
    return '{0}/diffx/{1}.html'.format(self._base, page_id)

  def word(self, page_id, keyword):
    return '{0}/?cmd=word&pageid={1}&word={2}&type=normal'.format(self._base, page_id, urlquote(keyword))

  def edit(self, page_id, menu=None, mode=None):
    if menu is not None:
      warnings.warn(
        '`menu` option will be removed in the future release. Use `mode` option instead.',
        DeprecationWarning)
    else:
      menu = True

    if mode is None:
      mode = 'editx' if menu else 'editxx'

    if mode not in [
          'pedit',    # standard
          'editx',    # simple (with menu)
          'editxx',   # simple (without menu)
        ]:
      raise ValueError('invalid mode: {}'.format(mode))
    return '{0}/{1}/{2}.html'.format(self._base, mode, page_id)

  def rename(self, page_id):
    return '{0}/renamex/{1}.html'.format(self._base, page_id)

  def chmod(self, page_id):
    return '{0}/chmod/{1}.html'.format(self._base, page_id)

  def chkind(self, page_id):
    return '{0}/chkind/{1}.html'.format(self._base, page_id)

  def upload(self, page_id):
    return '{0}/upload/{1}.html'.format(self._base, page_id)
