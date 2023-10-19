from requests import get
from .terminal import *

__title__ = 'custom'
__author__ = 'cxstles'
__version__ = '1.0.1'

VERSION = get('https://pypi.org/pypi/custerm/json').json()['info']['version']
if VERSION != __version__:
    Terminal.print(
        '**custerm** | New Version | pip install -U custerm',
        markdown=True
    )
