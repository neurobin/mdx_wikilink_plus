# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import markdown
from markdown.extensions.meta import MetaExtension
from mdx_wikilink_plus.mdx_wikilink_plus import WikiLinkPlusExtension

unittest.TestLoader.sortTestMethodsUsing = None

def build_url(urlo, base, end, url_whitespace, url_case):
    return "https://dummy"

meta_text = """
wiki_base_url: /local
wiki_url_whitespace: _
wiki_url_case: lowercase
wiki_label_case: capitalize
wiki_html_class: wiki-lnk
wiki_image_class: wiki-img
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

[[wikilink.png]]

[[/path/to/file name.jpg?a=b&b=c]]

[[https://example.jpeg?a=b&b=c]]

[[https://www.example.com/example-tutorial.jpeg]]

[[https://example.com/example-tutorial.gif | Example Tutorial]]

[[example tutorial.jpg | Example-Tutorial| alt= better example |alt=Alternate example]]
    """.strip()

md_configs1 = {
                'mdx_wikilink_plus': {
                    'base_url': '/static',
                    'end_url': '.html',
                    'url_case': 'lowercase',
                    'html_class': 'a-custom-class',
                },
             }


md_configs2 = {
                'mdx_wikilink_plus': {
                    'base_url': '/static',
                    'end_url': '.html',
                    'url_whitespace': '-',
                    'url_case': 'uppercase',
                    'label_case': 'titlecase',
                    'image_class': 'wikilink',
                    'build_url': build_url,
                },
             }

class TestMethods(unittest.TestCase):
    
    def test_without_config(self):
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
<p><img class="wikilink-image" src="wikilink.png" /></p>
<p><img class="wikilink-image" src="/path/to/file-name.jpg?a=b&amp;b=c" /></p>
<p><img class="wikilink-image" src="https://example.jpeg?a=b&amp;b=c" /></p>
<p><img class="wikilink-image" src="https://www.example.com/example-tutorial.jpeg" /></p>
<p><img class="wikilink-image" src="https://example.com/example-tutorial.gif" /></p>
<p><img alt="better example" class="wikilink-image" src="example-tutorial.jpg" /></p>
    """.strip()
        md = markdown.Markdown(extensions=[WikiLinkPlusExtension()])
        html = md.convert(text)
        # ~ print(html)
        self.assertEqual(html, output)

    def test_with_config1(self):
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
<p><img class="wikilink-image" src="/static/wikilink.png" /></p>
<p><img class="wikilink-image" src="/static/path/to/file-name.jpg?a=b&amp;b=c" /></p>
<p><img class="wikilink-image" src="https://example.jpeg?a=b&amp;b=c" /></p>
<p><img class="wikilink-image" src="https://www.example.com/example-tutorial.jpeg" /></p>
<p><img class="wikilink-image" src="https://example.com/example-tutorial.gif" /></p>
<p><img alt="better example" class="wikilink-image" src="/static/example-tutorial.jpg" /></p>
        """.strip()
        md2 = markdown.Markdown(extensions=[WikiLinkPlusExtension(md_configs1['mdx_wikilink_plus'])]) 
        html = md2.convert(text)
        # ~ print(html)
        self.assertEqual(html, output)

    def test_with_config2(self):
        output = """
<p><a class="wikilink" href="https://dummy">Wikilink</a>    <code>[[wikilink]]</code></p>
<p><a class="wikilink" href="https://dummy">File Name</a></p>
<p><a class="wikilink" href="https://dummy">File Name</a></p>
<p><a class="wikilink" href="https://dummy">File Name</a></p>
<p><a class="wikilink" href="https://dummy">File Name</a></p>
<p><a class="wikilink" href="https://dummy">File Name</a></p>
<p><a class="wikilink" href="https://dummy">File Name</a></p>
<p><a class="wikilink" href="https://dummy">www.example.com</a></p>
<p><a class="wikilink" href="https://dummy">www.example.com</a></p>
<p><a class="wikilink" href="https://dummy">Example Tutorial</a></p>
<p><a class="wikilink" href="https://dummy">Example Tutorial</a></p>
<p><img class="wikilink" src="https://dummy" /></p>
<p><img class="wikilink" src="https://dummy" /></p>
<p><img class="wikilink" src="https://dummy" /></p>
<p><img class="wikilink" src="https://dummy" /></p>
<p><img class="wikilink" src="https://dummy" /></p>
<p><img alt="better example" class="wikilink" src="https://dummy" /></p>
        """.strip()
        md2 = markdown.Markdown(extensions=[WikiLinkPlusExtension(md_configs2['mdx_wikilink_plus'])]) 
        html = md2.convert(text)
        # ~ print(html)
        self.assertEqual(html, output)


    def test_with_meta(self):
        output = """
<p><a class="wiki-lnk" href="/local/wikilink">Wikilink</a>    <code>[[wikilink]]</code></p>
<p><a class="wiki-lnk" href="/local/path/to/file_name">File name</a></p>
<p><a class="wiki-lnk" href="/local/path/to/file_name">File name</a></p>
<p><a class="wiki-lnk" href="/local/path/to/file-name">File name</a></p>
<p><a class="wiki-lnk" href="/local/path/to/file_name/?a=b&amp;b=c">File name</a></p>
<p><a class="wiki-lnk" href="/local/path/to/file_name.html">File name</a></p>
<p><a class="wiki-lnk" href="/local/path/to/file_name.html?a=b&amp;b=c">File name</a></p>
<p><a class="wiki-lnk" href="https://www.example.com/">www.example.com</a></p>
<p><a class="wiki-lnk" href="https://www.example.com/?a=b&amp;b=c">www.example.com</a></p>
<p><a class="wiki-lnk" href="https://www.example.com/example-tutorial">Example tutorial</a></p>
<p><a class="wiki-lnk" href="https://www.example.com/example-tutorial">Example Tutorial</a></p>
<p><img class="wiki-img" src="/local/wikilink.png" /></p>
<p><img class="wiki-img" src="/local/path/to/file_name.jpg?a=b&amp;b=c" /></p>
<p><img class="wiki-img" src="https://example.jpeg?a=b&amp;b=c" /></p>
<p><img class="wiki-img" src="https://www.example.com/example-tutorial.jpeg" /></p>
<p><img class="wiki-img" src="https://example.com/example-tutorial.gif" /></p>
<p><img alt="better example" class="wiki-img" src="/local/example_tutorial.jpg" /></p>
        """.strip()
        md2 = markdown.Markdown(extensions=[WikiLinkPlusExtension(), MetaExtension()]) 
        html = md2.convert(meta_text+"\n\n"+text)
        # ~ print(html)
        self.assertEqual(html, output)

if __name__ == "__main__":
    unittest.main()
