from rconf._error import RConfError


class DecodeError(RConfError, ValueError):
    """An error raised if a document is not valid."""


class DecodeValueError(DecodeError, ValueError):
    """Raised if an argument is not valid."""


class DecodeFileError(DecodeError):
    """An error raised if a document loaded from file is not valid."""

    def __init__(self) -> None:
        super().__init__("Exception decoding from file.")


class DecodeStringError(DecodeError):
    """An error raised if a document loaded from string is not valid."""

    def __init__(self) -> None:
        super().__init__("Exception decoding from string.")
