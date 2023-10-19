.. _rconf-reference-pointer:

Pointer
========================================================================

.. automodule:: rconf.pointer

.. autoclass:: rconf.pointer.Key

.. autoclass:: rconf.pointer.Pointer
    :members:
    :special-members: __str__

.. autofunction:: rconf.pointer.traverse


Language-specific pointers
------------------------------------------------------------------------

.. autoclass:: rconf.pointer.JSONPointer

.. autoclass:: rconf.pointer.TOMLPointer


Exceptions
------------------------------------------------------------------------

.. autoclass:: rconf.pointer.PointerError

.. autoclass:: rconf.pointer.PointerValueError

.. autoclass:: rconf.pointer.PointerLookupError
