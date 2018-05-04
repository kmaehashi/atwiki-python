# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import time
import optparse
import json

from ..core import AtWikiAPI
from ..uri import AtWikiURI

class AtWikiDump(object):
  """
  ``atwiki-dump`` is a simple tool to dump every Wiki source.

  Restrictions:
    - Contents other than Wiki source, page number and page name will not be dumped.
      This means that followings are not included in the dump:
        - WYSIWYG mode (i.e., syntax of the source)
        - history backup
        - tags
        - ACLs
    - No consistency between pages.
  """

  @classmethod
  def start(cls, args):
    USAGE = 'atwiki-dump [--output-dir OUTPUT_DIR] WIKI_URI'

    parser = optparse.OptionParser(description='@wiki Dump Tool', usage=USAGE)
    parser.add_option('--output-dir', '-o', type='string', default='.',
                      help='directory to output Wiki source')

    (parsed, target) = parser.parse_args(args)
    if len(target) != 1:
      parser.error('A single WIKI_URI must be specified')

    output_dir = parsed.output_dir
    target_site = target[0]

    api = AtWikiAPI(AtWikiURI(target_site))
    page_meta = {'version': 1, 'meta': {}}

    for page in api.get_list():
      page_id = page['id']
      page_name = page['name']
      page_meta['meta'][page_id] = {'name': page_name}
      path = '{0}/{1}.wiki'.format(output_dir, page_id)

      print('dumping: page {0} ({1}) to {2}'.format(page_id, page_name, path))
      page_src = api.get_source(page_id)
      with open(path, 'w') as f:
        f.write(page_src)
      time.sleep(10)

    path = '{0}/meta.json'.format(output_dir)
    print('dumping: meta data to {0}'.format(path))
    with open(path, 'w') as f:
      json.dump(page_meta, f)
    print('done!')

    return 0

def main():
  sys.exit(AtWikiDump.start(sys.argv[1:]))
