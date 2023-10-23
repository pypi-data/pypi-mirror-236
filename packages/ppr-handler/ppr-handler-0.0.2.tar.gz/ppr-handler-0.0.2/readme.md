# PprHandler

[`urllib.request.BaseHandler`](https://docs.python.org/3/library/urllib.request.html#urllib.request.BaseHandler)
for URLs with scheme *ppr*,
pointing to Python Package Resource files.

Using [URL](https://datatracker.ietf.org/doc/html/rfc3986#section-3) terminology,
the URL consists of

- a scheme: *ppr*
- an authority: module name
- a path: package resource file path

for example
`ppr://ppr_handler/py.typed`.

It also registers *ppr* with [`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html)
as a scheme that uses netloc and relative URLs.

## Installation

```sh
pip install ppr-handler
```

## Usage

```py
import ppr_handler
from urllib.request import build_opener

opener = build_opener(ppr_handler.PprHandler())
# or: opener = ppr_handler.build_opener()

with opener.open("ppr://ppr_handler/py.typed") as file:
    print(file.read())
    # b'# Marker file for PEP 561.\n'
```

or, for global use with `urllib.request`,

```py
import ppr_handler
from urllib.request import build_opener, install_opener, urlopen

install_opener(build_opener(ppr_handler.PprHandler()))

with urlopen("ppr://ppr_handler/py.typed") as file:
    print(file.read())
    # b'# Marker file for PEP 561.\n' 
```
