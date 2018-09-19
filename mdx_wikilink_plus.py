# -*- coding: utf-8 -*-
'''
WikiLinkPlus Extension for Python-Markdown
===========================================

Converts [[WikiLinkPlus]] to relative links.

See <https://github.com/neurobin/WikiLinkPlusPlus> for documentation.

Copyright Md. Jahidul Hamid <https://github.com/neurobin>

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

'''

from __future__ import absolute_import
from __future__ import unicode_literals
try:
    from urllib.parse import urljoin
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
    from urllib.parse import quote_plus
except ImportError:
    from urlparse import urljoin
    from urlparse import urlparse
    from urlparse import urlunparse
    from urllib import quote_plus
import markdown
from markdown.util import etree
import re
import os

__version__ = "1.0.0"


WIKILINK_PLUS_RE = r'\[\[\s*(?P<target>[^][|]+?)(\s*\|\s*(?P<label>[^][]+))?\s*\]\]'

def build_url(target, base, end, url_whitespace):
    """ Build a valid url from the label, a base, and an end. """
    clean_target = re.sub(r'\s+', url_whitespace, target)
    url = ("%s%s%s" % (base, clean_target, end))
    if base.endswith('/'):
        url = "%s%s%s" % (base, clean_target.lstrip('/'), end)
    elif base and not clean_target.startswith('/'):
        url = "%s/%s%s" % (base, clean_target, end)
    return urlunparse(urlparse(url))

def title(subject):
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

    def __init__(self,  *args, **kwargs):
        self.config = {
            'base_url': ['', 'String to append to beginning or URL.'],
            'end_url': ['', 'String to append to end of URL.'],
            'url_whitespace': ['-', 'String to replace white space in the URL'],
            'label_case':['titlecase', "Other valid values are: capitalize and none"],
            'html_class': ['wikilink wikilinkplus', 'CSS hook. Leave blank for none.'],
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
        d = m.groupdict()
        tl = d.get('target')
        label = d.get('label')
        if tl:
            base_url, end_url, url_whitespace, label_case, html_class = self._getMeta()
            urlo = urlparse(tl)
            print(urlo)
            path = urlo.path
            clean_path = path.strip().rstrip('/')
            if not label:
                if clean_path:
                    label = re.sub(r'[_-]', ' ', os.path.basename(clean_path)).strip()
                    if label_case.lower() == 'titlecase':
                        label = title(label)
                    elif label_case.lower() == 'capitalize':
                        label = label.capitalize()
                elif urlo.netloc:
                    label = urlo.netloc
                else:
                    label = tl
            url = ''
            if urlo.netloc:
                url = urlunparse(urlo)
            if not url:
                url = build_url(path, base_url, end_url, url_whitespace)
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
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
            if 'wiki_label_case' in self.md.Meta:
                label_case = self.md.Meta['wiki_label_case'][0]
            if 'wiki_url_whitespace' in self.md.Meta:
                url_whitespace = self.md.Meta['wiki_url_whitespace'][0]
                
        return base_url, end_url, url_whitespace, label_case, html_class


def makeExtension(*args, **kwargs):  # pragma: no cover
    return WikiLinkPlusExtension(*args, **kwargs)

if __name__ == "__main__":
    text = """
wiki_base_url: /static/
wiki_label_case: capitalize
wiki_url_whitespace: _

[[wikilink]]

[[/path/to/file name]]

[[/path/to/file name/?a=b&b=c]]

[[https://www.example.com/?]]

[[https://www.example.com/example-tutorial]]

[[https://www.example.com/example-tutorial | Example Tutorial]]

    """.strip()
    from markdown.extensions.meta import MetaExtension
    md = markdown.Markdown(extensions=[WikiLinkPlusExtension(), MetaExtension()])
    print(md.convert(text))
