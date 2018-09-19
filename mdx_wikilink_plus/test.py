# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import markdown
from markdown.extensions.meta import MetaExtension
from mdx_wikilink_plus.mdx_wikilink_plus import WikiLinkPlusExtension

def build_url(urlo, base, end, url_whitespace):
    return "https://dummy"

meta_text = """
wiki_base_url: /static/
wiki_end_url: 
wiki_url_whitespace: _
wiki_label_case: capitalize
wiki_html_class: wikilink
""".strip()

text = """
[[wikilink]]    `[[wikilink]]`

[[/path/to/file name]]

[[/path/to/file_name]]

[[/path/to/file-name]]

[[/path/to/file name/?a=b&b=c]]

[[/path/to/file name.html]]

[[/path/to/file name.html?a=b&b=c]]

[[https://www.example.com/?]]

[[https://www.example.com/?a=b&b=c]]

[[https://www.example.com/example-tutorial]]

[[https://www.example.com/example-tutorial | Example Tutorial]]
    """.strip()

md_configs1 = {
                'mdx_wikilink_plus': {
                    'base_url': '/static',
                    'end_url': '.html',
                    'url_whitespace': '-',
                    'label_case': 'titlecase',
                    'html_class': 'a-custom-class',
                },
             }


md_configs2 = {
                'mdx_wikilink_plus': {
                    'base_url': '/static',
                    'end_url': '.html',
                    'url_whitespace': '-',
                    'label_case': 'titlecase',
                    'html_class': 'a-custom-class',
                    'build_url': build_url,
                },
             }

def test_without_config():
    output = """
<p><a class="wikilink" href="wikilink">Wikilink</a>    <code>[[wikilink]]</code></p>
<p><a class="wikilink" href="/path/to/file-name">File Name</a></p>
<p><a class="wikilink" href="/path/to/file_name">File Name</a></p>
<p><a class="wikilink" href="/path/to/file-name">File Name</a></p>
<p><a class="wikilink" href="/path/to/file-name/?a=b&amp;b=c">File Name</a></p>
<p><a class="wikilink" href="/path/to/file-name.html">File Name</a></p>
<p><a class="wikilink" href="/path/to/file-name.html?a=b&amp;b=c">File Name</a></p>
<p><a class="wikilink" href="https://www.example.com/">www.example.com</a></p>
<p><a class="wikilink" href="https://www.example.com/?a=b&amp;b=c">www.example.com</a></p>
<p><a class="wikilink" href="https://www.example.com/example-tutorial">Example Tutorial</a></p>
<p><a class="wikilink" href="https://www.example.com/example-tutorial">Example Tutorial</a></p>
""".strip()
    md = markdown.Markdown(extensions=[WikiLinkPlusExtension()])
    html = md.convert(text)
    # ~ print(html)
    assert(html == output)

def test_with_config1():
    output = """
<p><a class="a-custom-class" href="/static/wikilink.html">Wikilink</a>    <code>[[wikilink]]</code></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file_name.html">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html?a=b&amp;b=c">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html?a=b&amp;b=c">File Name</a></p>
<p><a class="a-custom-class" href="https://www.example.com/">www.example.com</a></p>
<p><a class="a-custom-class" href="https://www.example.com/?a=b&amp;b=c">www.example.com</a></p>
<p><a class="a-custom-class" href="https://www.example.com/example-tutorial">Example Tutorial</a></p>
<p><a class="a-custom-class" href="https://www.example.com/example-tutorial">Example Tutorial</a></p>
    """.strip()
    md2 = markdown.Markdown(extensions=[WikiLinkPlusExtension(md_configs1['mdx_wikilink_plus'])]) 
    html = md2.convert(text)
    assert(html == output)

def test_with_config2():
    output = """
<p><a class="a-custom-class" href="https://dummy">Wikilink</a>    <code>[[wikilink]]</code></p>
<p><a class="a-custom-class" href="https://dummy">File Name</a></p>
<p><a class="a-custom-class" href="https://dummy">File Name</a></p>
<p><a class="a-custom-class" href="https://dummy">File Name</a></p>
<p><a class="a-custom-class" href="https://dummy">File Name</a></p>
<p><a class="a-custom-class" href="https://dummy">File Name</a></p>
<p><a class="a-custom-class" href="https://dummy">File Name</a></p>
<p><a class="a-custom-class" href="https://dummy">www.example.com</a></p>
<p><a class="a-custom-class" href="https://dummy">www.example.com</a></p>
<p><a class="a-custom-class" href="https://dummy">Example Tutorial</a></p>
<p><a class="a-custom-class" href="https://dummy">Example Tutorial</a></p>
    """.strip()
    md2 = markdown.Markdown(extensions=[WikiLinkPlusExtension(md_configs2['mdx_wikilink_plus'])]) 
    html = md2.convert(text)
    # ~ print(html)
    assert(html == output)


def test_with_meta():
    output = """
<p><a class="wikilink" href="/static/wikilink">Wikilink</a>    <code>[[wikilink]]</code></p>
<p><a class="wikilink" href="/static/path/to/file_name">File name</a></p>
<p><a class="wikilink" href="/static/path/to/file_name">File name</a></p>
<p><a class="wikilink" href="/static/path/to/file-name">File name</a></p>
<p><a class="wikilink" href="/static/path/to/file_name/?a=b&amp;b=c">File name</a></p>
<p><a class="wikilink" href="/static/path/to/file_name.html">File name</a></p>
<p><a class="wikilink" href="/static/path/to/file_name.html?a=b&amp;b=c">File name</a></p>
<p><a class="wikilink" href="https://www.example.com/">www.example.com</a></p>
<p><a class="wikilink" href="https://www.example.com/?a=b&amp;b=c">www.example.com</a></p>
<p><a class="wikilink" href="https://www.example.com/example-tutorial">Example tutorial</a></p>
<p><a class="wikilink" href="https://www.example.com/example-tutorial">Example Tutorial</a></p>
    """.strip()
    md2 = markdown.Markdown(extensions=[WikiLinkPlusExtension(), MetaExtension()]) 
    html = md2.convert(meta_text+"\n\n"+text)
    # ~ print(html)
    assert(html == output)

if __name__ == "__main__":
    test_without_config()
    test_with_config1()
    test_with_config2()
    test_with_meta()
