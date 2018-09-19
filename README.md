
Converts wikilinks (`[[wikilink]]`) to relative links. Absolute links are kept as is.

# Wikilink syntax

The geneal formats are:

1. With explicit label: `[[ target | label ]]`
2. Without explicit label: `[[wikilink]]`

# Usage

```python
text = "[[wikilink]]"
md = markdown.Markdown(extensions=['mdx_wikilink_plus'])
html = md.convert(text)
```

## Configuration

```python
md_configs = {
                'mdx_wikilink_plus': {
                    'base_url': '/static',
                    'end_url': '.html',
                    'url_whitespace': '-',
                    'label_case': 'titlecase',
                    'html_class': 'a-custom-class',
                    'build_url': build_url, # A callable
                    # all of the above config params are optional
                },
             }
text = "[[wikilink]]"
md = markdown.Markdown(extensions=['mdx_wikilink_plus'], extension_configs=md_configs)
html = md.convert(text)
```

### An example with the above configuration:

For the markdown:

```md
[[/path/to/file-name]]

[[/path/to/file name/?a=b&b=c]]
```

the output will be:

```html
<p><a class="a-custom-class" href="/static/path/to/file-name.html">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html?a=b&amp;b=c">File Name</a></p>
```

!!! info
    `end_url` is added at the end of the file-path part in the URL.


# Examples

Our test markdown:

```md
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
```

## Output without any config

```html
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
```

## With a config

With the configuration

```python
'mdx_wikilink_plus': {
    'base_url': '/static',
    'end_url': '.html',
    'url_whitespace': '-',
    'label_case': 'titlecase',
    'html_class': 'a-custom-class',
},
```

the output will be:

```html
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
```

## With meta (`markdown.extensions.meta`)

With the following meta added to the markdown:

```md
wiki_base_url: /static/
wiki_end_url: 
wiki_url_whitespace: _
wiki_label_case: capitalize
wiki_html_class: wikilink
```

the output will be:

```html
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
```


# The build_url callable:

The default `build_url` function is defined as:

```python
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
        
```
