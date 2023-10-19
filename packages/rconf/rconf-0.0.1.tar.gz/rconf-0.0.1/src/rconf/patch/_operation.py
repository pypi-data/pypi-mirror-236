from __future__ import annotations

import enum

from ._error import PatchKeyError


class PatchOperationMeta(enum.EnumMeta):
    """:class:`enum.EnumMeta` for :class:`rconf.patch.PatchOperation`."""

    SHORTHAND = "+-@<$?="

    def __getitem__(self, name: str) -> PatchOperation:
        """Lower case and shorthand indexing for PatchOperation."""
        try:
            if len(name) == 1:
                return PatchOperation(PatchOperationMeta.SHORTHAND.index(name))
            return super().__getitem__(name.upper())
        except (
            ValueError,  # index
            AttributeError,  # upper
            KeyError,  # __getitem__
        ) as error:
            msg = (
                f'Invalid operation "{name}".'
                f" Choose from {', '.join(map(str, PatchOperation))}"
                f" or {', '.join(PatchOperationMeta.SHORTHAND)}."
            )
            raise PatchKeyError(msg) from error


class PatchOperation(enum.Enum, metaclass=PatchOperationMeta):
    """Patch operations.

    Follows the definitions in
    `RFC 6902 section 4 <https://datatracker.ietf.org/doc/html/rfc6902#section-4>`_.
    Operation *assign* is added for convenience.

    :class:`rconf.patch.PatchOperation` can be indexed with a full or shorthand name.
    """

    ADD = 0  #: add, shorthand ``+``
    REMOVE = 1  #: remove, shorthand ``-``
    REPLACE = 2  #: replace, shorthand ``@``
    MOVE = 3  #: move, shorthand ``<``
    COPY = 4  #: copy, shorthand ``$``
    TEST = 5  #: test, shorthand ``?``
    ASSIGN = 6  #: assign, shorthand ``=``

    def __str__(self) -> str:
        """Return a lower case string representation of the operation."""
        return self.name.lower()

    def shorthand(self) -> str:
        """Get shorthand name for an operation."""
        return PatchOperationMeta.SHORTHAND[self.value]


MUST_EXIST = (
    PatchOperation.REMOVE,
    PatchOperation.REPLACE,
    PatchOperation.TEST,
)

MAY_APPEND = (
    PatchOperation.ASSIGN,
    PatchOperation.ADD,
    PatchOperation.MOVE,
    PatchOperation.COPY,
)

REQUIRES_FROM = (
    PatchOperation.MOVE,
    PatchOperation.COPY,
)
