from __future__ import annotations

import inspect
import typing

try:
    # TODO: python-3.11
    import tomllib as toml
except ModuleNotFoundError:
    import tomli as toml

from rconf.pointer import TOMLPointer

from ._error import DecodeFileError, DecodeStringError
from ._handler import BaseHandler

if typing.TYPE_CHECKING:
    from rconf._value import Value
    from rconf.pointer import Pointer

MEDIA_TYPES = (("application/toml", ".toml"),)

LOAD_KWARGS_KEYS = {
    param.name
    for param in inspect.signature(toml.load).parameters.values()
    if param.default != inspect.Parameter.empty
}

LOADS_KWARGS_KEYS = {
    param.name
    for param in inspect.signature(toml.loads).parameters.values()
    if param.default != inspect.Parameter.empty
}


class TOMLHandler(BaseHandler):
    """Handler for `TOML <https://toml.io/en/v1.0.0>`_.

    Uses Python's :mod:`tomllib` for Python>=3.11,
    or :mod:`tomli` (`github <https://github.com/hukkin/tomli>`_) below.
    """

    def __init__(
        self,
        *media_types: str,
        pointer_type: type[Pointer] = TOMLPointer,
        **kwargs,
    ) -> None:
        """Create a TOML Handler.

        Only valid :func:`tomllib.load` and :func:`tomllib.loads`
        keyword arguments are forwarded.

        :param kwargs: Forwarded to :func:`tomllib.load` and :func`tomllib.loads`.
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

        Returns :func:`tomllib.load`.

        Only valid :func:`tomllib.load` keyword arguments are forwarded.

        :param fp: ``read``-supporting :term:`binary file`.
        :param kwargs: Forwarded to :func:`tomllib.load`.
            Overrides :func:`TOMLHandler.__init__` ``kwargs``.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        kwargs = {
            key: value
            for key, value in {**self.kwargs, **kwargs}.items()
            if key in LOAD_KWARGS_KEYS
        }

        try:
            return toml.load(fp, **kwargs)
        except toml.TOMLDecodeError as error:
            raise DecodeFileError from error

    def loads(
        self,
        s: str,
        url: str | None = None,  # noqa: ARG002
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document.

        Returns :func:`tomllib.loads`.

        Only valid :func:`tomllib.loads` keyword arguments are forwarded.

        :param s: Configuration document.
        :param kwargs: Forwarded to :func:`tomllib.loads`.
            Overrides :func:`TOMLHandler.__init__` ``kwargs``.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors.
        """
        kwargs = {
            key: value
            for key, value in {**self.kwargs, **kwargs}.items()
            if key in LOADS_KWARGS_KEYS
        }

        try:
            return toml.loads(s, **kwargs)
        except toml.TOMLDecodeError as error:
            raise DecodeStringError from error
