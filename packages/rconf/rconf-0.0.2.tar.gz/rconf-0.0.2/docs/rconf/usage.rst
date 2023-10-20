.. _rconf-usage:

************************************************************************
Usage
************************************************************************

:mod:`rconf` offers
a :func:`rconf.load` and a :func:`rconf.loads` function
in line with :mod:`json` and :mod:`tomllib`,
as well as a :func:`rconf.loadu` function (URLs and local paths)
and a :func:`rconf.loadc` function (:class:`rconf.Value`).

They all decode documents applying references and patches.

They are convenience methods for a globally installed :class:`rconf.Loader`,
and the same functions exist as :class:`rconf.Loader` member methods.

The default global :class:`rconf.Loader` includes

- JSON and TOML configuration language handlers
  (:class:`rconf.decode.BaseHandler`) and
- the default URL handlers that come with :mod:`urllib.request`
  (:class:`urllib.request.BaseHandler`
  for scheme ``file``, ``http``, ``https``, ``ftp`` and ``data``).

Depending on the scheme, the language is defined based on
the `Media Type <https://datatracker.ietf.org/doc/html/rfc6838>`_
or the file extension [#json-default]_.

The architecture is inspired by :mod:`urllib`,
and its :class:`urllib.request.BaseHandler`
and :class:`urllib.request.OpenerDirector`.


Load URL
========================================================================

:func:`rconf.loadu` is the easiest to use, and takes

- a file path [#local-path]_ or URL,
  optionally with a language-specific pointer as fragment.

The URL components can be overridden with

- an optional explicit ``media_type`` or file extension,
- an optional ``base_url`` to resolve relative references,
- an optional fragment pointer ``ptr`` to replace the URL fragment.

``kwargs`` are forwarded to :func:`json.load`
or :func:`tomllib.load` if relevant.


Example
------------------------------------------------------------------------

.. literalinclude:: ./snippets/usage/loadu.py
  :language: python
  :caption: Example :func:`rconf.loadu` usage.

results in

.. literalinclude:: ../_build/snippets/usage/loadu.py.stdout
  :language: json


Load file or string
========================================================================

:func:`rconf.load` and :func:`rconf.loads` load a configuration document
from a :term:`binary file` or string respectively.

An additional optional argument ``url`` can set
either an assumed URL or a ``base_url`` for the document,
and the same ``media_type`` and ``ptr`` as for :func:`rconf.loadu`
are available.


Example
------------------------------------------------------------------------

.. literalinclude:: ./snippets/usage/loads.py
  :language: python
  :caption: Example :func:`rconf.loads` usage.

results in

.. literalinclude:: ../_build/snippets/usage/loads.py.stdout
  :language: json


Additional configuration languages and URL handlers
========================================================================

To create a :class:`rconf.Loader` with these and other handlers,
:func:`rconf.build_loader` can be used.
To use a loader globally, pass it to :func:`rconf.install_loader`.

:func:`rconf.build_loader` takes

- one or more
  :class:`rconf.decode.BaseHandler` or
  :class:`urllib.request.BaseHandler` arguments
- explicit ``opener`` (:class:`urllib.request.OpenerDirector`)
  and/or ``decoder`` (:class:`rconf.decode.DecoderDirector`) arguments.


Example
------------------------------------------------------------------------

.. literalinclude:: ./snippets/usage/build_loader.py
  :language: python
  :caption: Adding a :class:`rconf.decode.BaseHandler` for INI files,
    and a :class:`urllib.request.BaseHandler` for scheme ``ppr``
    (`PprHandler`_).

results in

.. literalinclude:: ../_build/snippets/usage/build_loader.py.stdout
  :language: json


Command Line Interface
========================================================================

:ref:`rconf_cli` is added as a CLI tool
to translate JSON and TOML files with (or without) references and patches,
and works with URLs or file paths.

``rconf dump`` behavior can be modified with a configuration file.
``rconf config`` can show or create an example.

Those using bash/zsh can activate auto completion,
provided by `argcomplete`_.

.. code-block:: console
  :caption: `argcomplete`_ for the impatient.

    $ pip install rconf[sh]
    $ activate-global-python-argcomplete --user


Example
------------------------------------------------------------------------

.. literalinclude:: ./snippets/usage/cli.sh
  :language: sh
  :caption: Example :ref:`rconf_cli` usage.

results in

.. literalinclude:: ../_build/snippets/usage/cli.sh.stdout


Example with configuration file
------------------------------------------------------------------------

In the same way additional handlers can be loaded in an :class:`rconf.Loader`,
:ref:`rconf_cli` supports listing handlers in a configuration file.

The following configuration file

- sets the fallback media type to INI files,
- adds a :class:`rconf.decode.BaseHandler` for INI files with TOML pointers,
- adds a :class:`urllib.request.BaseHandler`
  for scheme ``ppr`` (`PprHandler`_) and
- enables dumping to TOML using `tomli_w <https://github.com/hukkin/tomli-w>`_.

.. literalinclude:: ./snippets/usage/config.toml
  :language: toml
  :caption: Example :ref:`rconf_cli` configuration file.

It can then be used to get ``config.dump``
from an inline INI file:

.. literalinclude:: ./snippets/usage/cli-config.sh
  :language: sh
  :caption: Example :ref:`rconf_cli` using a configuration file.

which results in

.. literalinclude:: ../_build/snippets/usage/cli-config.sh.stdout


.. [#json-default] JSON is used by default
  (no media type specified or unknown extension)
  for the default global :class:`rconf.Loader`
  because of its ubiquity and because TOML is
  *a config file format for humans*,
  who tend to use file extensions.

.. [#local-path] While `rconf.loadu()` allows for local files,
  references should always be valid
  `local file <https://datatracker.ietf.org/doc/html/rfc8089>`_
  `URLs <https://datatracker.ietf.org/doc/html/rfc3986>`_
  or, likely more common,
  `relative references <https://datatracker.ietf.org/doc/html/rfc3986#section-4.2>`_.

.. _PprHandler: https://github.com/fthyssen/ppr-handler
.. _argcomplete: https://kislyuk.github.io/argcomplete
