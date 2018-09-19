
Converts wikilinks (`[[wikilink]]`) to relative links. Absolute links are kept as is.

**You should not use markdown.extensions.wikilinks along with this one. This extension is designed to provide the functionalities of markdown.extensions.wikilinks along with some extra features. Choose either one.**

# Install

```bash
pip install mdx_wikilink_plus
```

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

The configuration options are:

Config param | Details
------------ | -------
base_url | Prepended to the file_path part of the URL. A `/` at the end of the base_url will be handled intelligently.
end_url | Appended to the file_path part of the URL. If end_url is given (non-empty), then any `/` at the end of the file_path part in the URL is removed. If the end_url matches the extension of the file_path part, it will be ignored, for example, if end_url is `.html` and the wikilink provided is `[[/path/to/myfile.html]]`, then the URL will be `/path/to/myfile.html` not `/path/to/myfile.html.html`.
url_whitespace | Replace all whitespace in the file_path path with this character (string) when building the URL.
label_case | Choose case of the label. Available options: titlecase, capitalize, none. Capitalize will capitalize the first character only.
html_class | Set custom HTML classes on the anchor tag. It does not add classes rather it resets any previously set value.
build_url | A callable that returns the URL string. [Default build_url callable](#the-build_url-callable)

**None of the configs apply on absolute URLs except html_class and build_url. (Yes, label_case won't work either)**

### Configuration through meta data

Configuration can also be passed through metadata (markdown.extensions.meta).

We recognize the following template:

```md
wiki_base_url: /static/
wiki_end_url: 
wiki_url_whitespace: _
wiki_label_case: capitalize
wiki_html_class: wikilink

The first line of the document
```


### An example with configuration:


```python
md_configs = {
                'mdx_wikilink_plus': {
                    'base_url': '/static',
                    'end_url': '.html',
                    'url_whitespace': '-',
                    'label_case': 'titlecase',
                    'html_class': 'a-custom-class',
                    #'build_url': build_url, # A callable
                    # all of the above config params are optional
                },
             }


text = """
[[/path/to/file-name]]

[[/path/to/file name/?a=b&b=c]]
"""


md = markdown.Markdown(extensions=['mdx_wikilink_plus'], extension_configs=md_configs)
print(md.convert(text))
```

The output will be:

```html
<p><a class="a-custom-class" href="/static/path/to/file-name.html">File Name</a></p>
<p><a class="a-custom-class" href="/static/path/to/file-name.html?a=b&amp;b=c">File Name</a></p>
```

!!! info
    `end_url` is added at the end of the file-path part in the URL.


# More examples

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


# The build_url callable

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
