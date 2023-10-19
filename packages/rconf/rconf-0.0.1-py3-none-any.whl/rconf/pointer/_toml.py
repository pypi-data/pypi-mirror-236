from __future__ import annotations

import re

from ._error import PointerValueError
from ._pointer import Key, Pointer

_BARE_KEY_RE = re.compile(r"[A-Za-z0-9_-]+")
_MUST_ESCAPE_RE = re.compile(r'[\x00-\x08\x0a-\x1f\x7f"\\]')

_DOTTED_KEYS_RE = re.compile(
    r"(?:^|(?<!^)\.)"  # start or dotted
    r"[ \t]*(?:"  # whitespace before
    r"([A-Za-z0-9_-]+)|"  # capture bare key
    r'"('
    r"(?:"
    r'\\[btnfr"\\]|'
    r"\\u[0-9a-fA-F]{4}|"
    r"\\U[0-9a-fA-F]{8}|"
    r'[^\x00-\x08\x0a-\x1f\x7f"\\]'
    r")*"
    r')"|'  # capture basic string
    r"'([^']*)'"  # capture literal string
    r")[ \t]*",  # whitespace after
)


class TOMLPointer(Pointer):
    """:class:`rconf.pointer.Pointer` to parse and serialize TOML Pointers.

    A TOML Pointer is defined as a `TOML Key <https://toml.io/en/v1.0.0#keys>`_.
    """

    @classmethod
    def parse(cls, ptr: str) -> TOMLPointer:
        """Get the keys in a TOML Pointer."""
        if not isinstance(ptr, str):
            msg = f'Invalid TOML pointer "{ptr}": it should be a string.'
            raise PointerValueError(msg)

        if len(ptr) == 0:
            return TOMLPointer()

        result: list[Key] = []
        pos: int = 0
        for key in _DOTTED_KEYS_RE.finditer(ptr):
            if key.start() != pos:
                msg = (
                    f'Invalid TOML pointer "{ptr}":'
                    f' "{ptr[pos:key.start()]}" unexpected at {pos}.'
                )
                raise PointerValueError(msg)
            pos = key.end()
            groups = key.groups()
            if groups[0] is not None:
                result.append(groups[0])
            elif groups[1] is not None:
                result.append(
                    groups[1].encode("raw_unicode_escape").decode("unicode_escape"),
                )
            elif groups[2] is not None:
                result.append(groups[2])
        if pos != len(ptr):
            # invalid end
            msg = f'Invalid TOML pointer "{ptr}": "{ptr[pos:]}" unexpected at {pos}.'
            raise PointerValueError(msg)

        return TOMLPointer(*result)

    def __str__(self) -> str:
        """Return a valid TOML Pointer."""
        return ".".join(
            str(key)
            if not isinstance(key, str)
            else key
            if _BARE_KEY_RE.fullmatch(key)
            else f"'{key}'"
            if "'" not in key
            else _MUST_ESCAPE_RE.sub(lambda c: f"\\u{ord(c[0]):04x}", key)
            for key in self.keys
        )
