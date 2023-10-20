from __future__ import annotations

import typing

from ._error import PointerLookupError

if typing.TYPE_CHECKING:
    from collections.abc import Iterator

    try:
        # TODO: python-3.11
        from typing import Self
    except ImportError:
        from typing_extensions import Self

    try:
        # TODO: python-3.8
        from typing import SupportsIndex
    except ImportError:
        from typing_extensions import SupportsIndex

    from rconf._value import Value


Key = typing.Union[int, str]
"""A Pointer key to index a :class:`rconf.Value` mapping or array."""


class Pointer:
    """A Pointer to a :class:`rconf.Value` fragment.

    It's a :term:`hashable`, :term:`iterable` :term:`sequence`
    of :class:`rconf.Key`.
    The slash operator can be used to create child paths.
    """

    __slots__ = ("_keys",)

    @classmethod
    def parse(cls, ptr: str) -> Pointer:
        """Pointer-specific parsing.

        :raises: :class:`PointerValueError` for invalid pointer strings.
        """
        raise NotImplementedError

    def __init__(self, *keys: Pointer | Key) -> None:
        """Build a pointer from its keys, or copy a :class:`Pointer`."""
        if len(keys) == 1 and isinstance(keys[0], Pointer):
            self._keys = keys[0].keys
        else:
            self._keys = tuple(keys)

    @property
    def keys(self) -> tuple[Key, ...]:
        """Get the internal representation of the pointer."""
        return self._keys

    def __str__(self) -> str:
        return str(self._keys)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self._keys!r}"

    def __truediv__(self, other: Key | Pointer) -> Pointer:
        if isinstance(other, Pointer):
            return self.__class__(*self._keys, *other._keys)
        return self.__class__(*self._keys, other)

    def __rtruediv__(self, other: Key | Pointer) -> Pointer:
        if isinstance(other, Pointer):
            return self.__class__(*other._keys, *self._keys)
        return self.__class__(other, *self._keys)

    def __itruediv__(self, other: Key | Pointer) -> Self:
        if isinstance(other, Pointer):
            self._keys += other._keys
        else:
            self._keys += (other,)
        return self

    # hashable
    def __eq__(self, other: Pointer) -> bool:
        return isinstance(other, Pointer) and self._keys == other._keys

    def __hash__(self) -> int:
        return hash(self._keys)

    # iterable
    def __iter__(self) -> Iterator[Key]:
        return iter(self._keys)

    # sequence
    @typing.overload
    def __getitem__(self, idx: SupportsIndex) -> Key:
        ...

    @typing.overload
    def __getitem__(self, idx: slice) -> Pointer:
        ...

    @typing.overload
    def __getitem__(self, idx: SupportsIndex | slice) -> Key | Pointer:
        ...

    def __getitem__(self, idx: SupportsIndex | slice) -> Key | Pointer:
        if isinstance(idx, slice):
            return self.__class__(*self._keys[idx])
        return self._keys[idx]

    def __len__(self) -> int:
        return len(self._keys)

    # pointer
    def resolve(
        self,
        value: Value,
        *,
        cross_ref: bool = True,
    ) -> Value:
        """Resolve the pointer in a configuration.

        :param value: The configuration.
        :param cross_ref: Allow crossing ``$ref`` instances.

        :returns: The value.

        :raises: :class:`PointerLookupError`
            if the pointer path is not present in the configuration.
        """
        _, _, value, ptr = self.reduce(
            value,
            cross_ref=cross_ref,
        )
        if ptr:
            msg = (
                f"Pointer {self} could not be reached: "
                f' "{self[-len(ptr)]}" not present in {self[:-len(ptr)]}.'
            )
            raise PointerLookupError(msg)
        return value

    def reduce(
        self,
        value: Value,
        *,
        parent: Value | None = None,
        key: Key | None = None,
        cross_ref: bool = True,
    ) -> tuple[Value | None, Key | None, Value, Pointer]:
        """Reduce the pointer by following the path as far as possible.

        :param value: The configuration.
        :param parent: The parent of the target.
        :param key: The key for the target in ``parent``.
        :param cross_ref: Allow crossing ``$ref`` instances.

        :returns: The reduced (parent, key, value, pointer) tuple.
        """
        parent_key = key

        if len(self) == 0:
            return (parent, parent_key, value, self)

        for idx, key in enumerate(self):
            if isinstance(value, dict):
                if key not in value or (not cross_ref and "$ref" in value):
                    return (parent, parent_key, value, self[idx:])
            elif isinstance(value, (list, tuple)):
                if isinstance(key, str) and key.isdecimal():
                    key = int(key)  # noqa: PLW2901
                if not (isinstance(key, int) and 0 <= key < len(value)):
                    return (parent, parent_key, value, self[idx:])
            else:
                return (parent, parent_key, value, self[idx:])
            parent = value
            parent_key = key
            value = parent[parent_key]
        return (parent, parent_key, value, self.__class__())
