from __future__ import annotations

import typing

from rconf.pointer import JSONPointer

if typing.TYPE_CHECKING:
    from rconf._value import Value
    from rconf.pointer import Pointer


class BaseHandler:
    """Base class for a configuration language decoder.

    Holds the media types used for registration
    and the :class:`rconf.pointer.Pointer` type.
    """

    def __init__(
        self,
        *media_types: str | tuple[str, str] | list[str],
        pointer_type: type[Pointer] = JSONPointer,
    ) -> None:
        """Build a :class:`rconf.decode.BaseHandler`.

        :param media_types: The media type name,
            or (name, extension) :class:`tuple` for those
            not registered in :class:`mimetypes.MimeTypes`.
        :param pointer_type: The decoder-specific :class:`Pointer` type.
        """
        self.media_types = tuple(media_types)
        self.pointer_type = pointer_type

    def load(
        self,
        fp: typing.BinaryIO,
        url: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a ``read``-supporting :term:`binary file`.

        :param fp: ``read``-supporting :term:`binary file`.
        :param url: Configuration URL.
        :param kwargs: The decoder-specific keyword arguments.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        raise NotImplementedError

    def loads(
        self,
        s: str,
        url: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document.

        :param s: Configuration document.
        :param url: Configuration URL.
        :param kwargs: The decoder-specific keyword arguments.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        raise NotImplementedError
