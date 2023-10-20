r"""Patch configuration documents.

Follows the description in
`RFC 6902: JSON Patch <https://datatracker.ietf.org/doc/html/rfc6902>`_.

Operation *assign* has been added as a simplified *replace*,
dropping the requirement that
the target location must exist for the operation to be successful.
It also allows appending to an array with key ``-``.

A shorthand notation is also supported,
using an array (:class:`list`) instead of an object (:class:`dict`) per operation.

A shorthand :class:`list` consists of

- a shorthand *op* (``+-@<$?=``),
- a *path* and
- a *from* or *value* field if relevant, depending on the operation.

========== ========= =============
 Operation Shorthand Third element
========== ========= =============
      add   ``+``     *value*
   remove   ``-``     \-
  replace   ``@``     *value*
     move   ``<``     *from*
     copy   ``$``     *from*
     test   ``?``     *value*
   assign   ``=``     *value*
========== ========= =============

Operations are applied in order of appearance.

Toplevel patching is not supported for in-place patching.

.. code-block:: json
    :caption: Example from
        `RFC 6902 section 3 <https://datatracker.ietf.org/doc/html/rfc6902#section-3>`_.

    [
        { "op": "test", "path": "/a/b/c", "value": "foo" },
        { "op": "remove", "path": "/a/b/c" },
        { "op": "add", "path": "/a/b/c", "value": [ "foo", "bar" ] },
        { "op": "replace", "path": "/a/b/c", "value": 42 },
        { "op": "move", "from": "/a/b/c", "path": "/a/b/d" },
        { "op": "copy", "from": "/a/b/d", "path": "/a/b/e" }
    ]

.. code-block:: json
    :caption: Shorthand equivalent.

    [
        [ "?", "/a/b/c", "foo" ],
        [ "-", "/a/b/c" ],
        [ "+", "/a/b/c", [ "foo", "bar" ] ],
        [ "@", "/a/b/c", 42 ],
        [ "<", "/a/b/d", "/a/b/c" ],
        [ "$", "/a/b/e", "/a/b/d" ]
    ]
"""


from ._error import (
    PatchError,
    PatchIndexError,
    PatchKeyError,
    PatchLookupError,
    PatchTestError,
    PatchValueError,
)
from ._object import PatchOperationObject
from ._operation import PatchOperation
from ._patch import Patch

PatchError.__module__ = __name__
PatchIndexError.__module__ = __name__
PatchKeyError.__module__ = __name__
PatchLookupError.__module__ = __name__
PatchTestError.__module__ = __name__
PatchValueError.__module__ = __name__

PatchOperationObject.__module__ = __name__
PatchOperation.__module__ = __name__
Patch.__module__ = __name__

__all__ = [
    "PatchError",
    "PatchIndexError",
    "PatchKeyError",
    "PatchLookupError",
    "PatchTestError",
    "PatchValueError",
    "PatchOperationObject",
    "PatchOperation",
    "Patch",
]
