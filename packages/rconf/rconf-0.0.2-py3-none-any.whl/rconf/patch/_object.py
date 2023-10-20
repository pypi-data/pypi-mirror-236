from __future__ import annotations

import typing

from rconf.pointer import JSONPointer, Pointer, PointerValueError

from ._error import (
    PatchError,
    PatchIndexError,
    PatchKeyError,
    PatchLookupError,
    PatchTestError,
    PatchValueError,
)
from ._operation import MAY_APPEND, MUST_EXIST, REQUIRES_FROM, PatchOperation

if typing.TYPE_CHECKING:
    from rconf._value import Value


class PatchOperationObject:
    """A single patch operation object.

    The operation object is defined in
    `RFC 6902 section 4 <https://datatracker.ietf.org/doc/html/rfc6902#section-4>`_.

    *value* and *from* are merged into *value*.
    """

    __slots__ = ("op", "path", "value")

    def __init__(
        self,
        op: str | PatchOperation,
        path: str | Pointer,
        value: Value | str | Pointer | None = None,
        *,
        pointer_type: type[Pointer] = JSONPointer,
        **kwargs,
    ) -> None:
        """Build a :class:`rconf.patch.PatchOperationObject`.

        :param op: The operation to perform.
        :param path: The pointer to the target location.
        :param value: The operation-specific *value* or *from* field.
        :param pointer_type: The pointer type if path is a :class:`str`.

        ``value`` will be interpreted as an operation's *from*
        for move and copy
        (:const:`PatchOperation.MOVE` and :const:`PatchOperation.COPY`).
        If missing, it will look for an explicit *from* field in kwargs.
        """
        if isinstance(op, str):
            try:
                op = PatchOperation[op]
            except PatchKeyError as error:
                msg = f"Invalid op field: {op}."
                raise PatchValueError(msg) from error

        if isinstance(path, str):
            try:
                path = pointer_type.parse(path)
            except PointerValueError as error:
                msg = f"Invalid path: {path}."
                raise PatchValueError(msg) from error

        if op in REQUIRES_FROM:
            if value is None:
                try:
                    value = kwargs["from"]
                except KeyError as error:
                    msg = f"Missing value or from field for {op}."
                    raise PatchValueError(msg) from error
            if isinstance(value, str):
                try:
                    value = type(path).parse(value)
                except PointerValueError as error:
                    msg = f"Invalid from field: {value}."
                    raise PatchValueError(msg) from error

        self.op = op
        self.path = path
        self.value = value

    def __str__(self) -> str:
        """Return a shorthand representation of the operation object."""
        return f'["{self.op.shorthand()}", "{self.path}", "{self.value}"]'

    def apply(self, doc: Value) -> Value:
        """Apply the :class:`PatchOperationObject`.

        :param doc: The document to patch.

        :raises: :class:`rconf.patch.PatchError` for errors while patching,
            :class:`rconf.patch.PatchTestError` for failing tests.
        """
        result = [doc]
        op = self.op
        value = self.value

        parent, key, child, ptr = self.path.reduce(doc, parent=result, key=0)
        if ptr and op in MUST_EXIST:
            # remove, replace and test require existence
            msg = (
                f'Operation "{op}" cannot be applied to path "{self.path}":'
                f' the path ends at "{self.path[:-len(ptr)]}".'
            )
            raise PatchLookupError(msg)

        if len(ptr) == 1:
            # destination isn't there yet
            parent = child
            key = ptr[0]
            ptr = Pointer()

        if ptr or not isinstance(parent, (dict, list)):
            # destination's parent doesn't exist or is a leaf
            msg = (
                f'Operation "{op}" cannot be applied to path "{self.path}":'
                f' the path ends at "{self.path[:-len(ptr)]}".'
            )
            raise PatchLookupError(msg)

        if isinstance(parent, list):
            # translate sequence index
            if isinstance(key, str) and key.isdecimal():
                key = int(key)
            elif key == "-":
                key = len(parent)
            elif not isinstance(key, int):
                msg = (
                    f'Operation "{op}" cannot be applied to path "{self.path}":'
                    f' "{key}" is not a sequence index.'
                )
                raise PatchLookupError(msg)
            limit = len(parent)
            if op not in MAY_APPEND:
                limit -= 1
            if key > limit:
                msg = (
                    f'Path "{self.path}" index is out of range(0, {limit})'
                    f' for operation "{op}".'
                )
                raise PatchIndexError(msg)

        if op in REQUIRES_FROM:
            from_parent, from_key, from_value, ptr = value.reduce(doc)
            if ptr:
                msg = (
                    f'Failed to {op} from "{value}": '
                    f' "{value}" not  present in "{self.path[:-len(ptr)]}".'
                )
                raise PatchError(msg)

        # apply patch
        if op == PatchOperation.ASSIGN:
            if isinstance(parent, list) and key == len(parent):
                parent.append(value)
            else:
                parent[key] = value
        elif op == PatchOperation.REMOVE:
            del parent[key]
        elif op == PatchOperation.REPLACE:
            parent[key] = value
        elif op == PatchOperation.MOVE:
            del from_parent[from_key]
            value = from_value
            op = PatchOperation.ADD
        elif op == PatchOperation.COPY:
            value = from_value
            op = PatchOperation.ADD
        elif op == PatchOperation.TEST and parent[key] != value:
            msg = f'Failed patch test for "{self.path}".'
            raise PatchTestError(msg)

        if op == PatchOperation.ADD:
            if isinstance(parent, list):
                parent.insert(key, value)
            else:
                parent[key] = value

        return result[0]
