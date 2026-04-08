"""Error types for libghostty-py."""

from __future__ import annotations


class GhosttyError(Exception):
    """Base exception for libghostty errors."""


class OutOfMemoryError(GhosttyError):
    """Allocation failed."""


class InvalidValueError(GhosttyError):
    """Invalid argument or state."""


class OutOfSpaceError(GhosttyError):
    """Buffer too small for the requested operation."""


class NoValueError(GhosttyError):
    """Requested data has no value."""


def check_result(result: int) -> None:
    """Raise an appropriate exception if result is not GHOSTTY_SUCCESS (0)."""
    if result == 0:
        return
    if result == -1:
        raise OutOfMemoryError("out of memory")
    if result == -2:
        raise InvalidValueError("invalid value")
    if result == -3:
        raise OutOfSpaceError("out of space")
    if result == -4:
        raise NoValueError("no value")
    raise GhosttyError(f"unknown error code: {result}")
