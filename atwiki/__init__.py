from ._version import VERSION

from .core import AtWikiAPI
from .uri import AtWikiURI

__version__ = '.'.join(map(str, VERSION))

__all__ = ['AtWikiAPI', 'AtWikiURI']
