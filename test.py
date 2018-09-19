# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import markdown


text = """

[[wikilink]]

[[/path/to/file name]]

[[https://www.example.com/example-tutorial

"""

md = markdown.Markdown(extensions=['markdown.extensions.mdx_wikilink_plus'])
print(md.convert(text))
