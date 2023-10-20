.. _rconf-remarks:

************************************************************************
Remarks
************************************************************************

Remarks
========================================================================


Partial reference loading
------------------------------------------------------------------------

Using a fragment in a ``url`` or a ``ptr``
in :func:`rconf.load`, :func:`rconf.loads` or :func:`rconf.loadu`
is more efficient than resolving in a following step
when there are irrelevant references elsewhere in the document.

In the following snippet,
you'll notice there is no attempt to download the invalid URL
in the first :func:`rconf.loads`.

.. literalinclude:: ./snippets/remarks/partial.py
  :language: python

results in

.. literalinclude:: ../_build/snippets/remarks/partial.py.stdout


Circular references without patches
------------------------------------------------------------------------

Circular references are allowed,
but :func:`json.dumps` and `tomli_w.dumps <https://github.com/hukkin/tomli-w>`_
won't be able to dump them:

.. literalinclude:: ./snippets/remarks/circular.py
  :language: python

results in

.. literalinclude:: ../_build/snippets/remarks/circular.py.stdout


Circular reference with patches
------------------------------------------------------------------------

As mentioned in :ref:`rconf-definitions`,
patching a circular reference is not allowed:

.. literalinclude:: ./snippets/remarks/circular-patch.py
  :language: python

results in

.. literalinclude:: ../_build/snippets/remarks/circular-patch.py.stdout


Known issues
========================================================================

JSON Pointer: leading zeros
------------------------------------------------------------------------

This implementation allows for leading zeros in array indices.

*Reason: pointer resolution is common for JSON and TOML,
and keys only become indices upon resolution.*
