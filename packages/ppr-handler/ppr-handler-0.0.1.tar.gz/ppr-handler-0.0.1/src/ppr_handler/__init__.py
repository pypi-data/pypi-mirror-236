""":class:`urllib.request.BaseHandler` for scheme *ppr*: Python Package Resource files.

Using `URL <https://datatracker.ietf.org/doc/html/rfc3986#section-3>`_ terminology,
the URL consists of

- a scheme: *ppr*
- an authority: module name
- a path: package resource file path

for example
``ppr://ppr_handler/py.typed``.

It also registers *ppr* with :mod:`urllib.parse`
as a scheme that uses netloc and relative URLs.
"""

import email
import mimetypes
import urllib.error
import urllib.parse
import urllib.request
import urllib.response

try:
    # TODO: python-3.9
    from importlib.resources import files as resources_files
except ImportError:
    from importlib_resources import files as resources_files

# register scheme in urllib.parse
urllib.parse.uses_relative.append("ppr")
urllib.parse.uses_netloc.append("ppr")
# urllib.parse.uses_params: doesn't use params


class PprHandler(urllib.request.BaseHandler):
    """:class:`urllib.request.BaseHandler` for ``ppr``-scheme."""

    def ppr_open(
        self,
        request: urllib.request.Request,
    ) -> urllib.response.addinfourl:
        """Open a Python package resource file.

        It follows the :class:`urllib.request.BaseHandler` naming convention.
        """
        file = resources_files(request.host).joinpath(
            urllib.request.url2pathname(request.selector[1:]),
        )

        try:
            mtype = mimetypes.guess_type(file.name)[0]
            return urllib.response.addinfourl(
                file.open("rb"),
                email.message_from_string(f"Content-type: {mtype or 'text/plain'}\n"),
                request.full_url,
            )
        except OSError as error:
            raise urllib.error.URLError(error.strerror, file.name) from error


def build_opener(
    *handlers: urllib.request.BaseHandler,
) -> urllib.request.OpenerDirector:
    """Create an opener object including the ``ppr``-scheme handler."""
    return urllib.request.build_opener(PprHandler(), *handlers)


__all__ = [
    "PprHandler",
    "build_opener",
]
