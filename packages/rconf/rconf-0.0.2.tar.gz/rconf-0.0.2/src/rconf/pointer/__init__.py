"""RConf pointer module.

:class:`rconf.pointer.Pointer` can be implemented for different pointer types,
with type-specific

- class method :func:`rconf.pointer.Pointer.parse` and
- method :func:`rconf.pointer.Pointer.__str__`.

A :class:`rconf.pointer.Pointer` can be fully resolved
for a :class:`rconf.Value` (:func:`rconf.pointer.Pointer.resolve`),
or as far as possible (:func:`rconf.pointer.Pointer.reduce`).
The keys in a reference object (containing ``$ref``)
can be ignored by setting ``cross_ref=False``.

:func:`rconf.pointer.traverse` implements post-order depth-first traversal
of a :class:`rconf.Value`.
"""
from __future__ import annotations

import typing
from collections import deque

from ._error import PointerError, PointerLookupError, PointerValueError
from ._json import JSONPointer
from ._pointer import Key, Pointer
from ._toml import TOMLPointer

if typing.TYPE_CHECKING:
    from collections.abc import Iterator

    from rconf._value import Value


def traverse(
    value: Value,
    *,
    leafs: bool = True,
    dicts: bool = True,
    lists: bool = True,
    parent: Value | None = None,
    key: Key | None = None,
    pointer_type: type[Pointer] = Pointer,
) -> Iterator[tuple[Pointer, Value | None, Key | None, Value]]:
    """Post-order depth-first traversal of a configuration.

    Iterates over (pointer, parent, key, value) :class:`tuple` s.

    :param value: The configuration to traverse.
    :param leafs: Include :class:`rconf.Leaf` s.
    :param dicts: Include :class:`dict` s.
    :param lists: Include :class:`list` s.
    :param parent: The parent of ``value``.
    :param key: The key for ``value`` in ``parent``.
    :param pointer_type: :class:`Pointer` subclass to use.
    """
    # traversal stack
    ptr_parent_items: deque[
        tuple[pointer_type, Value | None, Iterator[tuple[Key | None, Value]]]
    ] = deque([(pointer_type(), parent, iter([(key, value)]))])

    # avoid circular references
    circular_id: deque[int] = deque((id(parent),))

    while ptr_parent_items:
        ptr, parent, items = ptr_parent_items[-1]
        try:
            key, value = next(items)
            ptr = ptr / key

            if isinstance(value, (dict, list, tuple)):
                # start with the children
                if id(value) in circular_id:
                    continue
                circular_id.append(id(value))

                ptr_parent_items.append(
                    (
                        ptr,
                        value,
                        iter(
                            value.items()
                            if isinstance(value, dict)
                            else enumerate(value),
                        ),
                    ),
                )
            elif leafs:
                yield (ptr[1:], parent, key, value)
        except StopIteration:
            # end with the parents
            if not ptr:
                return
            if (
                dicts
                and (isinstance(parent, dict))
                or (lists and isinstance(parent, (list, tuple)))
            ):
                value = parent
                key = ptr[-1]
                parent = ptr_parent_items[-2][1]
                if isinstance(parent, (list, tuple)):
                    key = int(key)
                yield (ptr[1:], parent, key, value)
            ptr_parent_items.pop()
            circular_id.pop()


PointerError.__module__ = __name__
PointerLookupError.__module__ = __name__
PointerValueError.__module__ = __name__

Pointer.__module__ = __name__
JSONPointer.__module__ = __name__
TOMLPointer.__module__ = __name__


__all__ = [
    "PointerError",
    "PointerLookupError",
    "PointerValueError",
    "Key",
    "Pointer",
    "JSONPointer",
    "TOMLPointer",
    "traverse",
]
