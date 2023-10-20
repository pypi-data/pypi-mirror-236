from __future__ import annotations

import copy
import typing

from rconf.pointer import JSONPointer, Pointer

from ._error import (
    PatchError,
    PatchValueError,
)
from ._object import PatchOperationObject

if typing.TYPE_CHECKING:
    from rconf._value import Value

    from ._operation import PatchOperation


class Patch:
    """`JSON Patch document <https://datatracker.ietf.org/doc/html/rfc6902#section-3>`_."""

    def __init__(
        self,
        diff: list[PatchOperationObject | dict[str, Value] | list[Value]],
        pointer_type: type[Pointer] = JSONPointer,
    ) -> None:
        """Build a :class:`rconf.patch.Patch`.

        The ``diff`` consists of a list of Patch Operation Objects,
        represented as

        - a :class:`rconf.patch.PatchOperationObject`,
        - an operation :class:`dict` or,
        - a shorthand :class:`list`.
        """
        self._diff: list[PatchOperationObject] = []
        self.pointer_type = pointer_type
        try:
            for op_obj in diff:
                if isinstance(op_obj, PatchOperationObject):
                    self._diff.append(op_obj)
                elif isinstance(op_obj, dict):
                    self.add(**op_obj)
                else:
                    self.add(*op_obj)
        except TypeError as error:
            msg = "Incomplete operation."
            raise PatchValueError(msg) from error

    def add(
        self,
        op: str | PatchOperation,
        path: str | Pointer,
        value: Value | str | Pointer | None = None,
        **kwargs,
    ) -> None:
        """Add a single operation object.

        ``value`` will be interpreted as an operation's *from*
        for move and copy
        (:const:`PatchOperation.MOVE` and :const:`PatchOperation.COPY`).
        """
        self._diff.append(
            PatchOperationObject(
                op,
                path,
                value,
                pointer_type=self.pointer_type,
                **kwargs,
            ),
        )

    def apply(
        self,
        doc: Value,
        *,
        in_place: bool = False,
    ) -> Value:
        """Apply the :class:`Patch` to ``doc`` and return the patched :class:`Value`.

        :param doc: The document to patch.
        :param in_place: Apply the changes to ``doc`` instead of a copy.

        :raises: :class:`rconf.patch.PatchError` for invalid patches,
            :class:`rconf.patch.PatchTestError` for failing tests.
        """
        result = doc
        if not in_place:
            result = copy.deepcopy(result)
        for op_obj in self._diff:
            result = op_obj.apply(result)
        if in_place and id(doc) != id(result):
            msg = "Toplevel patching is not supported for in-place patching."
            raise PatchError(msg)
        return result
