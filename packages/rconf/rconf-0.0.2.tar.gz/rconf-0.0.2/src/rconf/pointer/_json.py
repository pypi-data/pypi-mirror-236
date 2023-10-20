from __future__ import annotations

from ._error import PointerValueError
from ._pointer import Pointer


class JSONPointer(Pointer):
    """:class:`rconf.pointer.Pointer` to parse and serialize JSON Pointers.

    Follows `JSON Pointer <https://datatracker.ietf.org/doc/html/rfc6901>`_.
    """

    @classmethod
    def parse(cls, ptr: str) -> JSONPointer:
        """Get the reference tokens in a JSON Pointer.

        Known issue: allows for leading zeros in pointer array indices.
        Array indices only become integers at resolution,
        and resolution is not JSON-specific.
        """
        if not isinstance(ptr, str):
            msg = f'Invalid JSON pointer "{ptr}": it should be a string.'
            raise PointerValueError(msg)

        if len(ptr) == 0:
            return JSONPointer()

        if ptr[0] != "/":
            msg = f'Invalid JSON pointer "{ptr}": it should start with "/".'
            raise PointerValueError(msg)

        return JSONPointer(
            *(key.replace("~1", "/").replace("~0", "~") for key in ptr[1:].split("/")),
        )

    def __str__(self) -> str:
        """Return a valid JSON Pointer."""
        return "/" + "/".join(
            str(key).replace("~", "~0").replace("/", "~1") for key in self.keys
        )
