.. _rconf-reference-decode:

Decode
========================================================================

.. automodule:: rconf.decode

.. autofunction:: rconf.decode.build_decoder


BaseHandler
------------------------------------------------------------------------

.. autoclass:: rconf.decode.BaseHandler
    :members:

.. autoclass:: rconf.decode.DecoderDirector
    :members:


Language-specific handlers
------------------------------------------------------------------------

.. autoclass:: rconf.decode.JSONHandler
    :members:

.. autoclass:: rconf.decode.TOMLHandler
    :members:

.. autoclass:: rconf.decode.INIHandler
    :members:


Exceptions
------------------------------------------------------------------------

.. autoclass:: rconf.decode.DecodeError

.. autoclass:: rconf.decode.DecodeFileError

.. autoclass:: rconf.decode.DecodeStringError

.. autoclass:: rconf.decode.DecodeValueError
