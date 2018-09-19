# -*- coding: utf-8 -*-
'''
WikiLinkPlus Extension for Python-Markdown
===========================================

Converts [[WikiLinks]] to relative links.

See <https://github.com/neurobin/mdx_wikilink_plus> for documentation.

Copyright Md. Jahidul Hamid <jahidulhamid@yahoo.com>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

'''

from __future__ import absolute_import
from __future__ import unicode_literals
try:
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
except ImportError:
    from urlparse import urlparse
    from urlparse import urlunparse
import markdown
from markdown.util import etree
import re
import os
from . import version

__version__ = version.__version__


WIKILINK_PLUS_RE = r'\[\[\s*(?P<target>[^][|]+?)(\s*\|\s*(?P<label>[^][]+))?\s*\]\]'

def build_url(urlo, base, end, url_whitespace):
    """ Build and return a valid url.
        
    Parameters
    ----------
    
    urlo            A ParseResult object returned by urlparse
    
    base            base_url from config
    
    end             end_url from config
    
    url_whitespace  url_whitespace from config
    
    Returns
    -------
    
    URL string
    
    """
    if not urlo.netloc:
        if not end:
            clean_target = re.sub(r'\s+', url_whitespace, urlo.path)
        else:
            clean_target = re.sub(r'\s+', url_whitespace, urlo.path.rstrip('/'))
            if clean_target.endswith(end):
                end = ''
        if base.endswith('/'):
            path = "%s%s%s" % (base, clean_target.lstrip('/'), end)
        elif base and not clean_target.startswith('/'):
            path = "%s/%s%s" % (base, clean_target, end)
        else:
            path = "%s%s%s" % (base, clean_target, end)
        urlo = urlo._replace(path=path)
    return urlunparse(urlo)
        

def title(subject):
    """Return title cased version of the given subject string"""
    exceptions = ['a', 'an', 'the', 'v', 'vs', 'am', 'at', 'and', 'as', 'but','by', 'en', 'for', 'if', 'be', 'in', 'of', 'on', 'or', 'to', 'via',]
    slst = list(filter(None, re.split(r'[ \t]+', subject)))
    res = []
    c = 0
    for s in slst:
        if re.match(r'^[^a-z]+$', s) or (s in exceptions and c != 0):
            res.append(s)
        else:
            res.append(s.title())
        c = c + 1
    return ' '.join(res)

class WikiLinkPlusExtension(markdown.Extension):
    """WikiLinkPlus Extension class for markdown"""

    def __init__(self,  *args, **kwargs):
        self.config = {
            'base_url': ['', 'String to append to beginning or URL.'],
            'end_url': ['', 'String to append to end of URL.'],
            'url_whitespace': ['-', 'String to replace white space in the URL'],
            'label_case':['titlecase', "Other valid values are: capitalize and none"],
            'html_class': ['wikilink', 'CSS hook. Leave blank for none.'],
            'build_url': [build_url, 'Callable formats URL from label.'],
        }
        super(WikiLinkPlusExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        ext = WikiLinkPlusPattern(self.config, md)
        md.inlinePatterns.add('wikilink_plus', ext, "<not_strong")


class WikiLinkPlusPattern(markdown.inlinepatterns.Pattern):
    def __init__(self, config, md=None):
        markdown.inlinepatterns.Pattern.__init__(self, '', md)
        self.compiled_re = re.compile("^(.*?)%s(.*?)$" % (WIKILINK_PLUS_RE,), re.DOTALL | re.X)
        self.config = config
        self.md = md

    def getCompiledRegExp(self):
        return self.compiled_re

    def handleMatch(self, m):
        """Return an a element if regex matched"""
        d = m.groupdict()
        tl = d.get('target')
        label = d.get('label')
        if tl:
            base_url, end_url, url_whitespace, label_case, html_class = self._getMeta()
            urlo = urlparse(tl)
            clean_path = urlo.path.rstrip('/')
            if not label:
                if clean_path:
                    label = re.sub(r'[\s_-]+', ' ', re.sub(r'\..*$', r'', os.path.basename(clean_path))).strip()
                    if label_case.lower() == 'titlecase':
                        label = title(label)
                    elif label_case.lower() == 'capitalize':
                        label = label.capitalize()
                elif urlo.netloc:
                    label = urlo.netloc
                else:
                    label = tl
            url = self.config['build_url'][0](urlo, base_url, end_url, url_whitespace)
            a = etree.Element('a')
            a.text = label
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        else:
            a = ''
        return a

    def _getMeta(self):
        """ Return meta data or config data. """
        base_url = self.config['base_url'][0]
        end_url = self.config['end_url'][0]
        url_whitespace = self.config['url_whitespace'][0]
        label_case = self.config['label_case'][0]
        html_class = self.config['html_class'][0]
        if hasattr(self.md, 'Meta'):
            if 'wiki_base_url' in self.md.Meta:
                base_url = self.md.Meta['wiki_base_url'][0]
            if 'wiki_end_url' in self.md.Meta:
                end_url = self.md.Meta['wiki_end_url'][0]
            if 'wiki_url_whitespace' in self.md.Meta:
                url_whitespace = self.md.Meta['wiki_url_whitespace'][0]
            if 'wiki_label_case' in self.md.Meta:
                label_case = self.md.Meta['wiki_label_case'][0]
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
        return base_url, end_url, url_whitespace, label_case, html_class


def makeExtension(*args, **kwargs):  # pragma: no cover
    return WikiLinkPlusExtension(*args, **kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
