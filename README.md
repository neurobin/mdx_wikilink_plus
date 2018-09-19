
Converts wikilinks (`[[wikilink]]`) to relative links.

# Wikilink syntax

The geneal formats are:

1. Full: `[[ target | label ]]`
2. Without label: `[[wikilink]]`

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
                    'build_url': build_url,
                    # all of the above config params are optional
                },
             }
text = "[[wikilink]]"
md = markdown.Markdown(extensions=['mdx_wikilink_plus'], extension_configs=md_configs)
html = md.convert(text)
```

# Examples

`[[wikilink]]` will be converted to:

```html
<a class="wikilink" href="wikilink">Wikilink</a>
```


`[[/path/to/file name]]` will be converted to:

```html
<a class="wikilink" href="/path/to/file-name">File Name</a>
```


`[[/path/to/file_name]]` will be converted to:

```html
<a class="wikilink" href="/path/to/file_name">File Name</a>
```


`[[/path/to/file-name]]` will be converted to:

```html
<a class="wikilink" href="/path/to/file-name">File Name</a>
```


`[[/path/to/file name/?a=b&b=c]]` will be converted to:

```html
<a class="wikilink" href="/path/to/file-name/?a=b&amp;b=c">File Name</a>
```


`[[/path/to/file name.html]]` will be converted to:

```
<a class="wikilink" href="/path/to/file-name.html">File Name</a>
```


`[[/path/to/file name.html?a=b&b=c]]` will be converted to:

```html
<a class="wikilink" href="/path/to/file-name.html?a=b&amp;b=c">File Name</a>
```


`[[https://www.example.com/?]]` will be converted to:

```html
<a class="wikilink" href="https://www.example.com/">www.example.com</a>
```


`[[https://www.example.com/?a=b&b=c]]` will be converted to:

```html
<a class="wikilink" href="https://www.example.com/?a=b&amp;b=c">www.example.com</a>
```


`[[https://www.example.com/example-tutorial]]` will be converted to:

```html
<a class="wikilink" href="https://www.example.com/example-tutorial">Example Tutorial</a>
```


`[[https://www.example.com/example-tutorial | Example Tutorial]]` will be converted to:

```html
<a class="wikilink" href="https://www.example.com/example-tutorial">Example Tutorial</a>
```

