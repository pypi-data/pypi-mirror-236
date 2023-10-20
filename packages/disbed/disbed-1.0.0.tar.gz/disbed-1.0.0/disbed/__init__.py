from custerm import Terminal
from .embed import Embed
from requests import get

__title__ = 'disbed'
__author__ = 'cxstles'
__version__ = '1.0.0'

VERSION = get('https://pypi.org/pypi/disbed/json').json()['info']['version']
if VERSION != __version__:
    Terminal.print(
        '**disbed ** | New Version | pip install -U disbed',
        markdown=True
    )