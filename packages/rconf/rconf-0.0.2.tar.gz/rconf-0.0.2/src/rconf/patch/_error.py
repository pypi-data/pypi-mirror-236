from rconf._error import RConfError


class PatchError(RConfError):
    """A generic Patch exception."""


class PatchTestError(PatchError, AssertionError):
    """Raised if a patch document test fails."""


class PatchValueError(PatchError, ValueError):
    """Raised if a patch document is not valid."""


class PatchLookupError(PatchError, LookupError):
    """Raised if a path in a patch can't be resolved."""


class PatchIndexError(PatchLookupError, IndexError):
    """Raised when a sequence subscript is out of range."""


class PatchKeyError(PatchLookupError, KeyError):
    """Raised when a mapping (dictionary) key is not found."""
