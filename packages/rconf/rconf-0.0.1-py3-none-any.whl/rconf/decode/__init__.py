"""RConf decoding module.

:class:`rconf.decode.BaseHandler` implements a decoder for a specific language,
and :class:`rconf.decode.DecoderDirector` decides
which :class:`rconf.decode.BaseHandler` to use
based on the `Media Type <https://datatracker.ietf.org/doc/html/rfc6838>`_ or URL.
"""
from __future__ import annotations

import typing

from ._director import DecoderDirector
from ._error import DecodeError, DecodeFileError, DecodeStringError, DecodeValueError
from ._handler import BaseHandler
from ._ini import INIHandler
from ._json import JSONHandler
from ._toml import TOMLHandler

if typing.TYPE_CHECKING:
    from mimetypes import MimeTypes

# INIHandler is not included because of the many INI format variants.
DEFAULT_HANDLERS = (
    JSONHandler,  # fallback
    TOMLHandler,
)


def build_decoder(
    *handlers: type[BaseHandler] | BaseHandler,
    fallback: type[BaseHandler] | BaseHandler | str | None = None,
    mime_types: MimeTypes | None = None,
) -> DecoderDirector:
    """Build a :class:`rconf.decode.DecoderDirector` with default handlers.

    :class:`rconf.decode.JSONHandler` is chosen as the default fallback
    (no media type specified or unknown extension)
    because of its ubiquity and because TOML is
    *a config file format for humans*,
    who tend to use file extensions.

    :param handlers: :class:`rconf.decode.BaseHandler` s to choose from.
    :param fallback: The fallback :class:`rconf.decode.BaseHandler`.
        If missing, :class:`rconf.decode.JSONHandler` will be the fallback handler.
    :param mime_types: :class:`mimetypes.MimeTypes` object used to guess
        a configuration's media type from a URL.
    """
    return DecoderDirector(
        *DEFAULT_HANDLERS,
        *handlers,
        fallback=fallback,
        mime_types=mime_types,
    )


DecodeError.__module__ = __name__
DecodeFileError.__module__ = __name__
DecodeStringError.__module__ = __name__
DecodeValueError.__module__ = __name__

BaseHandler.__module__ = __name__
DecoderDirector.__module__ = __name__
INIHandler.__module__ = __name__
JSONHandler.__module__ = __name__
TOMLHandler.__module__ = __name__

__all__ = [
    "DecodeError",
    "DecodeFileError",
    "DecodeStringError",
    "DecodeValueError",
    "BaseHandler",
    "DecoderDirector",
    "INIHandler",
    "JSONHandler",
    "TOMLHandler",
    "build_decoder",
]
