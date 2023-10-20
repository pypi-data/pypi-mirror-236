"""The core types of :mod:`rconf`.

A configuration :class:`rconf.Value` is defined as

- a :class:`dict` with :class:`str` keys as a :term:`mapping` to represent a *mapping*,
- a :class:`list` or :class:`tuple` as a :term:`sequence` to represent an *array* and
- other types listed below as *leafs*.

The mapping values and sequence elements can in turn be
any valid :class:`rconf.Value` instance.

This definition allows :mod:`rconf` to be a drop-in replacement for
:func:`json.load`, :func:`json.loads`, :func:`tomllib.load` and :func:`tomllib.loads`.
"""

import typing
from datetime import date, datetime, time

Leaf = typing.Union[
    # JSON / TOML
    str,
    int,
    float,
    bool,
    # JSON null
    None,
    # TOML Date, Date-Time, Time
    date,
    datetime,
    time,
    # other
    bytes,
    bytearray,
    memoryview,
]

Value = typing.Union[
    # JSON object, TOML table
    typing.Dict[str, "Value"],
    # JSON array / TOML array
    typing.List["Value"],
    typing.Tuple["Value", ...],
    # Leaf
    Leaf,
]
