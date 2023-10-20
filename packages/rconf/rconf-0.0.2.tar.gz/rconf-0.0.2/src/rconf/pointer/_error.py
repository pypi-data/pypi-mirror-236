from rconf._error import RConfError


class PointerError(RConfError):
    """A generic Pointer exception."""


class PointerValueError(PointerError, ValueError):
    """Raised if a pointer representation can't be parsed."""


class PointerLookupError(PointerError, LookupError):
    """Raised if a pointer can't be resolved."""
