.. _rconf-definitions:

************************************************************************
Definitions
************************************************************************

Restrictions
========================================================================

This package reserves JSON and TOML key ``$ref`` for references.


Configuration
========================================================================

A configuration is defined as

- a *mapping* with *string keys*
  (`JSON strings <https://datatracker.ietf.org/doc/html/rfc8259#section-7>`_ and
  `TOML strings <https://toml.io/en/v1.0.0#string>`_)
  to represent

  - `JSON objects <https://datatracker.ietf.org/doc/html/rfc8259#section-4>`_ and
  - `TOML tables <https://toml.io/en/v1.0.0#table>`_;

- an *array* to represent

  - `JSON arrays <https://datatracker.ietf.org/doc/html/rfc8259#section-5>`_ and
  - `TOML arrays <https://toml.io/en/v1.0.0#array>`_;

- or other types (*leafs*) to represent

  - number, string, false, null and true
    `JSON values <https://datatracker.ietf.org/doc/html/rfc8259#section-3>`_ and
  - string, integer, float, boolean, date-time, date and time
    `TOML values <https://toml.io/en/v1.0.0#keyvalue-pair>`_.

The mapping values and array elements are again configuration instances.

:ref:`Python implementation: rconf.Value<rconf-reference-value>`.


.. _rconf-definitions-pointer:

Pointers
========================================================================

A JSON or TOML pointer identifies a value within a JSON or TOML document
respectively.

JSON pointers
    are defined in
    `RFC 6901: JSON Pointer <https://datatracker.ietf.org/doc/html/rfc6901>`_.
TOML pointers
    are defined here as
    `TOML keys <https://toml.io/en/v1.0.0#keys>`_,
    with the addition of array indices as defined for JSON pointers
    [#array-indices]_ .

:ref:`Python implementation: rconf.pointer.Pointer<rconf-reference-pointer>`.


.. _rconf-definitions-reference:

References
========================================================================

An object or table (mapping) with a ``$ref`` key will be substituted
by the value its string value references, compatible with the
`JSON Reference draft <https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03>`_.

The reference
`JSON string <https://datatracker.ietf.org/doc/html/rfc8259#section-7>`_ or
`TOML string <https://toml.io/en/v1.0.0#string>`_ value
is a `URL <https://datatracker.ietf.org/doc/html/rfc3986>`_ with an optional
`fragment identifier <https://datatracker.ietf.org/doc/html/rfc3986#section-3.5>`_
[#url-encoding]_
that follows the representation of the referent document:
a JSON or TOML pointer.


Example
------------------------------------------------------------------------

A configuration with references to a TOML document (with TOML pointer)
and a JSON document (with JSON pointer):

.. tab-set-code::

    .. literalinclude:: ./snippets/definitions/references.toml
        :language: toml

    .. literalinclude:: ./snippets/definitions/references.json
        :language: json

    .. literalinclude:: ./snippets/definitions/references.ini
        :language: ini

or more compact with implicitly created TOML tables,

.. tab-set-code::

    .. literalinclude:: ./snippets/definitions/references-dotted.toml
        :language: toml

At the time of writing, each of these results in the following

.. tab-set-code::

    .. literalinclude:: ../_build/snippets/definitions/references.toml
        :language: toml

    .. literalinclude:: ../_build/snippets/definitions/references.json
        :language: json


.. _rconf-definitions-patch:

Patches
========================================================================

An object or table with a ``$ref`` key can contain
additional key/value pairs for patching.
In this case, the reference value is copied.

The patch operations used here are defined in
`RFC 6902: JSON Patch <https://datatracker.ietf.org/doc/html/rfc6902>`_
using *op*, *path*, *value* and *from* fields.
*Path* and *from* fields use the pointer representation
of the document being patched.

Operation *assign* has been added as a simplified *replace*,
dropping the requirement that
the target location must exist for the operation to be successful.
It also allows appending to an array with key ``-``.

Three patch notations are allowed:

An array of operation objects
    is a ``$patch`` key with array value, containing
    `JSON Patch operation objects <https://datatracker.ietf.org/doc/html/rfc6902#section-4>`_.

An array of shorthand operation arrays
    is a ``$patch`` key with array value,
    containing shorthand operation arrays.

Key/value-pair assignments
    are key/value pairs describing *path*/*value* assignments [#patch-patch]_.

Shorthand operation arrays each consist of

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

The ``$patch`` array can contain a mix of
operation objects and shorthand operation arrays.

``$patch``-array operations are applied in order of appearance,
before any key/value-pair assignment.

Failing tests will raise an exception [#patch-test]_.


Limitations
------------------------------------------------------------------------

- Patches for circular references are not allowed.
- This implementation doesn't support
  :ref:`patching reference URLs <rconf-definitions-patched_ref>`
  (the ``$ref`` value).


Example
------------------------------------------------------------------------

.. tab-set-code::

    .. literalinclude:: ./snippets/definitions/patches.toml
        :language: toml

    .. literalinclude:: ./snippets/definitions/patches.json
        :language: json

translates to

.. tab-set-code::

    .. literalinclude:: ./snippets/definitions/patches-result.toml
        :language: toml

.. dropdown:: Full translation

    .. tab-set-code::

        .. literalinclude:: ../_build/snippets/definitions/patches.toml
            :language: toml

        .. literalinclude:: ../_build/snippets/definitions/patches.json
            :language: json


Remarks
========================================================================

Definition implications
------------------------------------------------------------------------

- Circular references are allowed,
  but references cannot point to themselves.
- Key/value-pair assignments may be applied out of order
  [#key-value-order]_,
  so they shouldn't be relied upon for patches
  requiring order preservation.
- Key/value-pair assignment allows only
  one replacement per *path* [#key-value-unique]_.
- A :func:`copy.deepcopy` is applied
  for reference substitution with patches.


.. _rconf-definitions-patched_ref:

Patching reference URLs
------------------------------------------------------------------------

In this implementation,
all patches are applied after (partial) reference resolution.
As a consequence, ``$ref`` values (the URLs) cannot be patched,
even if they are references themselves.

This is not detected automatically and no warnings are raised.

.. tab-set-code::

    .. literalinclude:: ./snippets/definitions/patched-reference.toml
        :language: toml

    .. literalinclude:: ./snippets/definitions/patched-reference.json
        :language: json

Result

.. tab-set-code::

    .. literalinclude:: ../_build/snippets/definitions/patched-reference.toml
        :language: toml

    .. literalinclude:: ../_build/snippets/definitions/patched-reference.json
        :language: json


.. [#array-indices] Zero-based base-10 integers
    that give access to the corresponding array elements,
    or the single character "-"
    referencing the value past the last array element.
    The latter can be used to extend arrays.

.. [#url-encoding] URL fragments follow
    `URL encoding <https://datatracker.ietf.org/doc/html/rfc3986#section-2>`_.

.. [#patch-patch] Note that a key/value-pair assignment is impossible
    for a TOML key ``$patch``.
    This will have to be part of a ``$patch`` array instead.

.. [#patch-test] In this implementation,
    a :class:`rconf.patch.PatchTestError` is raised for failing tests.

.. [#key-value-order]
    `JSON RFC 8259 section 1 <https://datatracker.ietf.org/doc/html/rfc8259#section-1>`_
    states

        An object is an unordered collection
        of zero or more name/value pairs, ...

    `TOML v1.0.0: Table <https://toml.io/en/v1.0.0#table>`_ mentions

        Key/value pairs within tables
        are not guaranteed to be in any specific order.

.. [#key-value-unique]
    `JSON RFC 8259 section 4 <https://datatracker.ietf.org/doc/html/rfc8259#section-4>`_
    states

        The names within an object SHOULD be unique.

    `TOML v1.0.0: Keys <https://toml.io/en/v1.0.0#keys>`_ mentions

        Defining a key multiple times is invalid.
