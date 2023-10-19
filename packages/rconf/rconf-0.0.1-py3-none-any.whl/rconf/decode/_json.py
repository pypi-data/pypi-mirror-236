from __future__ import annotations

import json
import typing

from rconf.pointer import JSONPointer

from ._error import DecodeFileError, DecodeStringError
from ._handler import BaseHandler

if typing.TYPE_CHECKING:
    from rconf._value import Value
    from rconf.pointer import Pointer

MEDIA_TYPES = ("application/json",)


class JSONHandler(BaseHandler):
    """Handler for `JSON <https://datatracker.ietf.org/doc/html/rfc8259>`_.

    Uses Python's :mod:`json`.
    """

    def __init__(
        self,
        *media_types: str,
        pointer_type: type[Pointer] = JSONPointer,
        **kwargs,
    ) -> None:
        """Create a JSON Handler.

        :param kwargs: Forwarded to :func:`json.load` and :func`json.loads`.
        """
        super().__init__(*(media_types or MEDIA_TYPES), pointer_type=pointer_type)
        self.kwargs = kwargs

    def load(
        self,
        fp: typing.BinaryIO,
        url: str | None = None,  # noqa: ARG002
        **kwargs,
    ) -> Value:
        """Decode a ``read``-supporting :term:`binary file`.

        Returns :func:`json.load`.

        :param fp: ``read``-supporting :term:`binary file`.
        :param kwargs: Forwarded to :func:`json.load`.
            Overrides :func:`JSONHandler.__init__` ``kwargs``.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        try:
            return json.load(fp, **{**self.kwargs, **kwargs})
        except json.JSONDecodeError as error:
            raise DecodeFileError from error

    def loads(
        self,
        s: str,
        url: str | None = None,  # noqa: ARG002
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document.

        Returns :func:`json.loads`.

        :param s: Configuration document.
        :param kwargs: Forwarded to :func:`json.load`.
            Overrides :func:`JSONHandler.__init__` ``kwargs``.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        try:
            return json.loads(s, **{**self.kwargs, **kwargs})
        except json.JSONDecodeError as error:
            raise DecodeStringError from error
