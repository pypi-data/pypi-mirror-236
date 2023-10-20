from __future__ import annotations

import copy
import pathlib
import re
import typing
import urllib.error
import urllib.parse
import uuid
from collections import deque

from .decode import BaseHandler, DecodeError, DecoderDirector
from .patch import Patch
from .pointer import Key, Pointer, traverse

if typing.TYPE_CHECKING:
    from collections.abc import Iterator
    from urllib.request import OpenerDirector

    from ._value import Value

# `RFC 3986 section 3.1 <https://datatracker.ietf.org/doc/html/rfc3986#section-3.1>`_,
_URL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+\-.]+:")


def _guess_url(locator: str | pathlib.Path | None = None) -> str:
    """Create a URL given a locator that can be a URL or a file path."""
    if locator is None:
        locator = f"./{uuid.uuid4()}"
    if isinstance(locator, str):
        if _URL_SCHEME_RE.match(locator):
            # an actual URL
            return locator
        # as_uri() drops trailing slash, so keep track of it
        is_folder = locator and locator[-1] in r"\/"
        locator = pathlib.Path(locator)
    else:
        is_folder = False
    locator = locator.expanduser().resolve().as_uri()
    return locator + "/" if is_folder else locator


def _url_ptr(url: str, ptr: str | None = None) -> str:
    """Add a URL fragment if ptr is not None."""
    if ptr is None:
        return url
    return f"{urllib.parse.urldefrag(url).url}#{urllib.parse.quote(ptr)}"


class Loader:
    """Load configurations, replace references and apply patches.

    Uses

    - an :class:`urllib.request.OpenerDirector` and
    - a :class:`rconf.decode.DecoderDirector`.
    """

    def __init__(
        self,
        opener: OpenerDirector | None = None,
        decoder: DecoderDirector | None = None,
    ) -> None:
        """Build a :class:`rconf.Loader`.

        :param opener: The :class:`urllib.request.OpenerDirector`.
        :param decoder: The :class:`rconf.decode.DecoderDirector`.
        """
        self.opener = opener
        self.decoder = decoder

    def load(
        self,
        fp: typing.BinaryIO,
        media_type: str | None = None,
        url: str | pathlib.Path | None = None,
        *,
        ptr: str | None = None,
        check_circular: bool = True,
        **kwargs,
    ) -> Value:
        """Decode a ``read``-supporting :term:`binary file` with references and patches.

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
        url = _url_ptr(_guess_url(url), ptr)
        handler = self.decoder.get_handler(media_type, url)
        init = handler.load(fp, url, **kwargs)
        return self._load(init, url, handler, check_circular=check_circular, **kwargs)

    def loads(
        self,
        s: str,
        media_type: str | None = None,
        url: str | pathlib.Path | None = None,
        *,
        ptr: str | None = None,
        check_circular: bool = True,
        **kwargs,
    ) -> Value:
        """Decode a :class:`str` configuration document with references and patches.

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
        url = _url_ptr(_guess_url(url), ptr)
        handler = self.decoder.get_handler(media_type, url)
        init = handler.loads(s, url, **kwargs)
        return self._load(init, url, handler, check_circular=check_circular, **kwargs)

    def loadc(
        self,
        config: Value,
        media_type: str | None = None,
        url: str | pathlib.Path | None = None,
        *,
        ptr: str | None = None,
        check_circular: bool = True,
        **kwargs,
    ) -> Value:
        """Decode a configuration document with references and patches.

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
        url = _url_ptr(_guess_url(url), ptr)
        handler = self.decoder.get_handler(media_type, url)
        return self._load(
            copy.deepcopy(config),
            url,
            handler,
            check_circular=check_circular,
            **kwargs,
        )

    def loadu(
        self,
        url: str | pathlib.Path,
        media_type: str | None = None,
        *,
        base_url: str | pathlib.Path | None = None,
        ptr: str | None = None,
        check_circular: bool = True,
        **kwargs,
    ) -> Value:
        """Decode a configuration document at a URL or path with references and patches.

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
        url = _guess_url(url)
        handler, init = self._open(url, media_type)

        if base_url is None:
            url = _url_ptr(url, ptr)
        else:
            if ptr is None:
                ptr = urllib.parse.unquote(urllib.parse.urldefrag(url).fragment)
            url = _url_ptr(_guess_url(base_url), ptr)

        return self._load(init, url, handler, check_circular=check_circular, **kwargs)

    def _load(
        self,
        init: Value,
        url: str,
        handler: BaseHandler,
        *,
        check_circular: bool = True,
        **kwargs,
    ) -> Value:
        """Decode a configuration document at a URL with references and patches.

        :param init: Configuration :class:`rconf.Value`.
        :param url: Assumed document URL
            for fragment and relative reference resolution.
        :param handler: The :class:`BaseHandler` of the initial document.
        :param check_circular: Verify that no circular references are patched.
        :param kwargs: Forwarded to :class:`rconf.decode.DecoderDirector`.

        :raises: :class:`rconf.decode.DecodeError` in case of decode errors,
            :class:`rconf.patch.PatchError` for patch errors.
        """
        # keep track of loaded documents
        url_handler_value: dict[str, tuple[BaseHandler, Value]] = {
            urllib.parse.urldefrag(url).url: (handler, init),
        }

        # embedded in a list to always have a parent
        result: Value = [{"$ref": url}]

        # traversal stack
        url_handler_items: deque[
            tuple[str, BaseHandler, Iterator[tuple[Pointer, Value | None, Key, Value]]]
        ] = deque(
            [
                (
                    "",
                    handler,
                    iter(
                        traverse(
                            result[0],
                            leafs=False,
                            lists=False,
                            parent=result,
                            key=0,
                            pointer_type=handler.pointer_type,
                        ),
                    ),
                ),
            ],
        )

        # avoid processing duplicates
        duplicate_id: set[int] = set()

        # iterate over dicts, looking for references
        while url_handler_items:
            src_url, src_handler, src_items = url_handler_items[-1]
            try:
                src_ptr, src_parent, src_key, src_value = next(src_items)

                if "$ref" not in src_value or id(src_value) in duplicate_id:
                    continue
                # id is added below if the reference is not replaceable yet

                if not isinstance(src_value["$ref"], str):
                    msg = (
                        f'Error loading "{src_url}": {src_ptr/"$ref"} is not a string.'
                    )
                    raise DecodeError(msg)

                # parse URL
                target_url, target_fragment = urllib.parse.urldefrag(
                    urllib.parse.urljoin(src_url, src_value["$ref"]),
                )

                # load document if needed
                if target_url not in url_handler_value:
                    target_handler, target_value = self._open(target_url, **kwargs)
                    url_handler_value[target_url] = (target_handler, target_value)
                else:
                    target_handler, target_value = url_handler_value[target_url]

                # reduce ptr and insert
                # don't resolve because you might miss patches in target document
                ptr = target_handler.pointer_type.parse(
                    urllib.parse.unquote(target_fragment),
                )
                _, _, target_value, target_ptr = ptr.reduce(
                    target_value,
                    cross_ref=False,
                )
                if id(target_value) == id(src_value):
                    msg = f"A reference cannot point to itself ({target_url}#{ptr})."
                    raise DecodeError(msg)

                if not target_ptr and len(src_value) == 1:
                    src_parent[src_key] = target_value
                    traverse_parent = src_parent
                    traverse_key = src_key
                else:
                    # list to traverse and apply potential patches in target
                    traverse_parent = src_value["$ref"] = [
                        src_handler,
                        target_value,
                        target_ptr,
                    ]
                    traverse_key = 1
                    duplicate_id.add(id(src_value))

                # referenced content should also be processed
                if id(target_value) not in duplicate_id:
                    url_handler_items.append(
                        (
                            target_url,
                            target_handler,
                            iter(
                                traverse(
                                    target_value,
                                    leafs=False,
                                    lists=False,
                                    parent=traverse_parent,
                                    key=traverse_key,
                                    pointer_type=target_handler.pointer_type,
                                ),
                            ),
                        ),
                    )
            except StopIteration:
                url_handler_items.pop()

        # replace references and patch if needed
        for ptr, parent, key, value in traverse(
            result[0],
            leafs=False,
            lists=False,
            parent=result,
            key=0,
            pointer_type=handler.pointer_type,
        ):
            if "$ref" in value:
                src_handler: BaseHandler
                src_value: Value
                src_ptr: Pointer
                src_handler, src_value, src_ptr = value["$ref"]
                replacement = src_ptr.resolve(src_value)
                if len(value) > 1:
                    # avoid circular reference patching
                    if check_circular and any(
                        "$ref" in child
                        for _, _, _, child in traverse(
                            replacement,
                            leafs=False,
                            lists=False,
                        )
                    ):
                        msg = f"A circular reference cannot be patched ({ptr})."
                        raise DecodeError(msg)
                    patch = Patch(
                        value["$patch"] if "$patch" in value else [],
                        src_handler.pointer_type,
                    )
                    del value["$ref"]
                    if "$patch" in value:
                        del value["$patch"]
                    for patch_key, patch_value in value.items():
                        patch.add("=", patch_key, patch_value)
                    replacement = patch.apply(replacement)
                    # prepare patched value for other references
                    value.clear()
                    value["$ref"] = [
                        src_handler,
                        replacement,
                        src_handler.pointer_type(),
                    ]
                parent[key] = replacement

        return result[0]

    def _open(
        self,
        url: str,
        media_type: str | None = None,
        **kwargs,
    ) -> tuple[BaseHandler, Value]:
        try:
            with self.opener.open(url) as fp:
                if media_type is None and "content-type" in fp.headers:
                    media_type = fp.headers["content-type"]
                    if media_type not in self.decoder.handlers:
                        media_type = None
                handler = self.decoder.get_handler(media_type, url)
                return (handler, handler.load(fp, url, **kwargs))
        except urllib.error.URLError as error:
            msg = f'Error loading "{url}".'
            raise DecodeError(msg) from error
