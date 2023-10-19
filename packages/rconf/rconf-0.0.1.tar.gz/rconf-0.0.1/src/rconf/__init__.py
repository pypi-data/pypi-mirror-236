"""Extensible Python package to resolve references and apply patches in
`JSON <https://datatracker.ietf.org/doc/html/rfc8259>`_ and
`TOML <https://toml.io/en/v1.0.0>`_ configurations.

It uses :mod:`json` and :mod:`tomllib` to decode,
handles local and remote reference URLs using :mod:`urllib`,
and resolves document fragments specified through pointers,
optionally applying patches.

- References follow the
  `JSON Reference draft <https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03>`_.
- Reference patches are based on
  `RFC 6902 <https://datatracker.ietf.org/doc/html/rfc6902>`_,
  extended with shorthand notations and an *assign* operation.
- JSON pointers follow
  `RFC 6901 <https://datatracker.ietf.org/doc/html/rfc6901>`_.
- TOML pointers are
  `TOML keys <https://toml.io/en/v1.0.0#keys>`_
  extended with array indices.
"""  # noqa: D205
from __future__ import annotations

import typing
from urllib.request import BaseHandler as UrlHandler
from urllib.request import OpenerDirector, build_opener

from . import decode, patch, pointer
from ._error import RConfError
from ._load import Loader
from ._value import Leaf, Value
from .decode import (
    BaseHandler,
    DecodeError,
    DecodeFileError,
    DecoderDirector,
    DecodeStringError,
    DecodeValueError,
    INIHandler,
    JSONHandler,
    TOMLHandler,
    build_decoder,
)
from .patch import (
    Patch,
    PatchError,
    PatchIndexError,
    PatchKeyError,
    PatchLookupError,
    PatchOperation,
    PatchOperationObject,
    PatchTestError,
    PatchValueError,
)
from .pointer import (
    JSONPointer,
    Key,
    Pointer,
    PointerError,
    PointerLookupError,
    PointerValueError,
    TOMLPointer,
)

if typing.TYPE_CHECKING:
    import pathlib
    from mimetypes import MimeTypes

_loader: Loader | None = None


def build_loader(
    *handlers: type[BaseHandler | UrlHandler] | BaseHandler | UrlHandler,
    fallback: type[BaseHandler] | BaseHandler | str | None = None,
    mime_types: MimeTypes | None = None,
    opener: OpenerDirector | None = None,
    decoder: DecoderDirector | None = None,
) -> Loader:
    """Build a :class:`rconf.Loader`.

    :param handlers: :class:`rconf.decode.BaseHandler` s and
        :class:`urllib.request.UrlHandler` s to choose from.
    :param fallback: The fallback :class:`rconf.decode.BaseHandler`.
        If missing, :class:`rconf.decode.JSONHandler` will be the fallback handler.
    :param mime_types: :class:`mimetypes.MimeTypes` object used
        to guess a configuration's media type from a URL.
    :param opener: The :class:`urllib.request.OpenerDirector`.  Overrides ``handlers``.
    :param decoder: The :class:`rconf.decode.DecoderDirector`.  Overrides ``handlers``.
    """
    if opener is None:
        opener = build_opener(
            *(
                handler
                for handler in handlers
                if (
                    isinstance(handler, UrlHandler)
                    or (isinstance(handler, type) and issubclass(handler, UrlHandler))
                )
            ),
        )
    if decoder is None:
        decoder = build_decoder(
            *(
                handler
                for handler in handlers
                if (
                    isinstance(handler, BaseHandler)
                    or (isinstance(handler, type) and issubclass(handler, BaseHandler))
                )
            ),
            fallback=fallback,
            mime_types=mime_types,
        )
    return Loader(opener, decoder)


def install_loader(loader: Loader) -> None:
    """Install a default :class:`rconf.Loader`.

    This loader is used by

    - :func:`rconf.load`,
    - :func:`rconf.loads`,
    - :func:`rconf.loadc` and
    - :func:`rconf.loadu`.
    """
    global _loader  # noqa: PLW0603
    _loader = loader


def _get_loader() -> Loader:
    global _loader  # noqa: PLW0603
    if _loader is None:
        _loader = build_loader(build_opener(), build_decoder())
    return _loader


def load(
    fp: typing.BinaryIO,
    media_type: str | None = None,
    url: str | pathlib.Path | None = None,
    *,
    ptr: str | None = None,
    check_circular: bool = True,
    **kwargs,
) -> Value:
    """Decode a ``read``-supporting :term:`binary file` with references and patches.

    This uses the default :class:`rconf.Loader`.

    :param fp: ``read``-supporting :term:`binary file`.
    :param media_type: Assumed media type, overrides URL-derived media type.
        It can also be a filename extension.
    :param url: Assumed document URL or path
        for media type, fragment and relative reference resolution.
    :param ptr: Fragment pointer, overrides URL fragment.
    :param check_circular: Verify that no circular references are patched.
    :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

    :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
        :class:`rconf.patch.PatchError` for patch errors.
    """
    return _get_loader().load(
        fp,
        media_type,
        url,
        ptr=ptr,
        check_circular=check_circular,
        **kwargs,
    )


def loads(
    s: str,
    media_type: str | None = None,
    url: str | pathlib.Path | None = None,
    *,
    ptr: str | None = None,
    check_circular: bool = True,
    **kwargs,
) -> Value:
    """Decode a :class:`str` configuration document with references and patches.

    This uses the default :class:`rconf.Loader`.

    :param s: Configuration document.
    :param media_type: Assumed media type, overrides URL-derived media type.
        It can also be a filename extension.
    :param url: Assumed document URL or path
        for media type, fragment and relative reference resolution.
    :param ptr: Fragment pointer, overrides URL fragment.
    :param check_circular: Verify that no circular references are patched.
    :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

    :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
        :class:`rconf.patch.PatchError` for patch errors.
    """
    return _get_loader().loads(
        s,
        media_type,
        url,
        ptr=ptr,
        check_circular=check_circular,
        **kwargs,
    )


def loadc(
    config: Value,
    media_type: str | None = None,
    url: str | pathlib.Path | None = None,
    *,
    ptr: str | None = None,
    check_circular: bool = True,
    **kwargs,
) -> Value:
    """Decode a configuration document with references and patches.

    This uses the default :class:`rconf.Loader`.

    :param config: Configuration :class:`rconf.Value`.
    :param media_type: Assumed media type, overrides URL-derived media type.
        It can also be a filename extension.
    :param url: Assumed document URL or path
        for media type, fragment and relative reference resolution.
    :param ptr: Fragment pointer, overrides URL fragment.
    :param check_circular: Verify that no circular references are patched.
    :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

    :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
        :class:`rconf.patch.PatchError` for patch errors.
    """
    return _get_loader().loadc(
        config,
        media_type,
        url,
        ptr=ptr,
        check_circular=check_circular,
        **kwargs,
    )


def loadu(
    url: str | pathlib.Path,
    media_type: str | None = None,
    *,
    base_url: str | pathlib.Path | None = None,
    ptr: str | None = None,
    check_circular: bool = True,
    **kwargs,
) -> Value:
    """Decode a configuration document at a URL or path with references and patches.

    This uses the default :class:`rconf.Loader`.

    :param url: Document URL or path,
        optionally with a language-specific pointer as URL fragment.
    :param media_type: Assumed media type, overrides URL-derived media type
        and content-type from :func:`urllib.request.OpenerDirector.open`.
        It can also be a filename extension.
    :param base_url: Assumed document URL or path
        for relative reference resolution, overrides URL base.
    :param ptr: Fragment pointer, overrides URL fragment.
    :param check_circular: Verify that no circular references are patched.
    :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

    :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
        :class:`rconf.patch.PatchError` for patch errors.
    """
    return _get_loader().loadu(
        url,
        media_type,
        base_url=base_url,
        ptr=ptr,
        check_circular=check_circular,
        **kwargs,
    )


RConfError.__module__ = __name__
Loader.__module__ = __name__

__all__ = [
    "Leaf",
    "Value",
    "RConfError",
    # Decode
    "decode",
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
    # Pointer
    "pointer",
    "PointerError",
    "PointerLookupError",
    "PointerValueError",
    "Key",
    "Pointer",
    "JSONPointer",
    "TOMLPointer",
    # Patch
    "patch",
    "PatchError",
    "PatchIndexError",
    "PatchKeyError",
    "PatchLookupError",
    "PatchTestError",
    "PatchValueError",
    "PatchOperationObject",
    "PatchOperation",
    "Patch",
    # Loader
    "Loader",
    # Convenience
    "build_loader",
    "install_loader",
    "load",
    "loads",
    "loadc",
    "loadu",
]
