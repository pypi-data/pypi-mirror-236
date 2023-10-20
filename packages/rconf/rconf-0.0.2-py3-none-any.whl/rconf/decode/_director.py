from __future__ import annotations

import typing
import urllib.parse
from mimetypes import MimeTypes

from ._error import DecodeValueError
from ._handler import BaseHandler

if typing.TYPE_CHECKING:
    from rconf._value import Value


class DecoderDirector:
    """Load configurations from string or file.

    The :class:`rconf.decode.BaseHandler` is selected
    using a configuration's media type,
    explicitly given or derived from the URL using :class:`mimetypes.MimeTypes`.
    """

    def __init__(
        self,
        *handlers: type[BaseHandler] | BaseHandler,
        fallback: type[BaseHandler] | BaseHandler | str | None = None,
        mime_types: MimeTypes | None = None,
    ) -> None:
        """Build a :class:`rconf.decode.DecoderDirector`.

        :param handlers: :class:`rconf.decode.BaseHandler` s to choose from.
        :param fallback: The fallback :class:`rconf.decode.BaseHandler`.
            If missing, the first handler will be the fallback handler.
        :param mime_types: :class:`mimetypes.MimeTypes` object used
            to guess a configuration's media type from a URL.
        """
        self.handlers: dict[str, BaseHandler] = {}
        self.fallback: BaseHandler = None
        self.mime_types: MimeTypes = mime_types or MimeTypes()

        if fallback is not None and not isinstance(fallback, str):
            self.add_handler(fallback)

        for handler in handlers:
            self.add_handler(handler)

        if isinstance(fallback, str):
            self.fallback = self.get_handler(fallback)

    def add_handler(
        self,
        handler: type[BaseHandler] | BaseHandler,
        *media_types: str | tuple[str, str] | list[str],
    ) -> BaseHandler:
        """Add a handler.

        The handler added first will be the fallback handler.

        :param media_types: Add media types by name,
            or (name, extension) :class:`tuple` for those
            not registered in :class:`mimetypes.MimeTypes`.
            If missing, those listed in the :class:`BaseHandler` are used.

        :returns: The inserted handler.

        :raises: :class:`rconf.decode.DecodeValueError`.
        """
        if isinstance(handler, type):
            if not issubclass(handler, BaseHandler):
                msg = (
                    "Director only handles valid BaseHandler classes "
                    f"or instances thereof, not {handler}."
                )
                raise DecodeValueError(msg)
            handler = handler()
        elif not isinstance(handler, BaseHandler):
            msg = (
                "Director only handles valid BaseHandler classes "
                f"or instances thereof, not {type(handler)}."
            )
            raise DecodeValueError(msg)

        for media_type in media_types or handler.media_types:
            if isinstance(media_type, (tuple, list)):
                media_type = tuple(map(str.lower, media_type))  # noqa: PLW2901
                self.mime_types.add_type(*media_type)
                media_type = media_type[0]  # noqa: PLW2901
            self.handlers[media_type] = handler

        if self.fallback is None:
            self.fallback = handler

        return handler

    def get_handler(
        self,
        media_type: str | None = None,
        url: str | None = None,
    ) -> BaseHandler:
        """Get a matching handler.

        Unknown media type or unknown URL-derived media type
        results in the fallback handler.

        :param media_type: Assumed media type, overrides URL-derived media type.
            It can also be a filename extension.
        :param url: Configuration URL.
        """
        if media_type is None and url is not None:
            media_type, _ = self.mime_types.guess_type(
                urllib.parse.urldefrag(url).url,
                strict=False,
            )
        elif isinstance(media_type, str) and "/" not in media_type:
            if media_type and media_type[0] != ".":
                media_type = "." + media_type
            media_type = media_type.lower()
            media_type = self.mime_types.types_map[1].get(
                media_type,
                None,
            ) or self.mime_types.types_map[0].get(media_type, None)
        return self.handlers.get(media_type, self.fallback)

    def load(
        self,
        fp: typing.BinaryIO,
        media_type: str | None = None,
        url: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a ``read``-supporting :term:`binary file`.

        :param fp: ``read``-supporting :term:`binary file`.
        :param media_type: Assumed media type, overrides URL-derived media type.
            It can also be a filename extension.
        :param url: Configuration URL.
        :param kwargs: Forwarded to language-specific
            :class:`rconf.decode.BaseHandler`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        return self.get_handler(media_type, url).load(fp, url, **kwargs)

    def loads(
        self,
        s: str,
        media_type: str | None = None,
        url: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document.

        :param s: Configuration document.
        :param media_type: Assumed media type, overrides URL-derived media type.
            It can also be a filename extension.
        :param url: Configuration URL.
        :param kwargs: Forwarded to language-specific
            :class:`rconf.decode.BaseHandler`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        return self.get_handler(media_type, url).loads(s, url, **kwargs)
