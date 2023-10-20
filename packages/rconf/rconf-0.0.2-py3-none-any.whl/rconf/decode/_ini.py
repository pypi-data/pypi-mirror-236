from __future__ import annotations

import configparser
import inspect
import typing

from rconf.pointer import TOMLPointer

from ._error import DecodeStringError
from ._handler import BaseHandler

if typing.TYPE_CHECKING:
    from rconf._value import Value
    from rconf.pointer import Pointer

MEDIA_TYPES = ()

KWARGS_KEYS = {
    param.name
    for param in inspect.signature(
        configparser.ConfigParser.__init__,
    ).parameters.values()
    if param.default != inspect.Parameter.empty
}


class INIHandler(BaseHandler):
    """Handler for :mod:`configparser`.

    All :mod:`configparser` keyword arguments are forwarded
    to support the same configuration language dialects.
    """

    def __init__(
        self,
        *media_types: str,
        encoding: str = "utf-8",
        errors: str = "strict",
        pointer_type: type[Pointer] = TOMLPointer,
        **kwargs,
    ) -> None:
        """Create a :mod:`configparser` Handler.

        Only valid :func:`configparser.ConfigParser`
        keyword arguments are forwarded.

        :param encoding: Forwarded to :func:`bytes.decode`.
        :param errors: Forwarded to :func:`bytes.decode`.
        :param kwargs: Forwarded to :class:`configparser.ConfigParser`.
        """
        super().__init__(*(media_types or MEDIA_TYPES), pointer_type=pointer_type)
        self.kwargs = kwargs
        self._encoding = encoding
        self._errors = errors

    def load(
        self,
        fp: typing.BinaryIO,
        url: str | None = None,
        *,
        encoding: str | None = None,
        errors: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a ``read``-supporting :term:`binary file`.

        Uses :func:`configparser.ConfigParser.read_string`
        and translates the result to a :class:`rconf.Value`.

        Only valid :func:`configparser.ConfigParser`
        keyword arguments are forwarded.

        :param fp: ``read``-supporting :term:`binary file`.
        :param encoding: Forwarded to :func:`bytes.decode`.
            Overrides :func:`INIHandler.__init__` ``encoding``.
        :param errors: Forwarded to :func:`bytes.decode`.
            Overrides :func:`INIHandler.__init__` ``errors``.
        :param kwargs: Forwarded to :class:`configparser.ConfigParser`.
            Overrides :func:`INIHandler.__init__` ``kwargs``.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        return self.loads(
            fp.read().decode(
                self._encoding if encoding is None else encoding,
                self._errors if errors is None else errors,
            ),
            url,
            **kwargs,
        )

    def loads(
        self,
        s: str,
        url: str | None = None,
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document.

        Uses :func:`configparser.ConfigParser.read_string`
        and translates the result to a :class:`rconf.Value`.

        Only valid :func:`configparser.ConfigParser`
        keyword arguments are forwarded.

        :param s: Configuration document.
        :param kwargs: Forwarded to :class:`configparser.ConfigParser`.
            Overrides :func:`INIHandler.__init__` ``kwargs``.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        try:
            kwargs = {
                key: value
                for key, value in {**self.kwargs, **kwargs}.items()
                if key in KWARGS_KEYS
            }
            parser = configparser.ConfigParser(**kwargs)
            parser.read_string(s, url)
            return {
                label: dict(section.items())
                for label, section in parser.items()
                if label != parser.default_section
            }
        except configparser.Error as error:
            raise DecodeStringError from error
