"""Error types for libghostty-py."""

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Never


class BaseGhosttyError(Exception):
    """Base exception for libghostty errors."""


class OutOfMemoryError(BaseGhosttyError, MemoryError):
    """Allocation failed."""


class InvalidValueError(BaseGhosttyError, ValueError):
    """Invalid argument or state."""


class OutOfSpaceError(BaseGhosttyError, MemoryError):
    """Buffer too small for the requested operation."""


class NoValueError(BaseGhosttyError, ValueError):
    """Requested data has no value."""


class GhosttyError(IntEnum):
    OUT_OF_MEMORY = -1
    INVALID_VALUE = -2
    OUT_OF_SPACE = -3
    NO_VALUE = -4

    @classmethod
    def _missing_(cls, value: int) -> Never:
        raise BaseGhosttyError(f"unknown error code: {value}")

    def raise_error(self) -> Never:
        raise {
            self.OUT_OF_MEMORY: OutOfMemoryError("out of memory"),
            self.INVALID_VALUE: InvalidValueError("invalid value"),
            self.OUT_OF_SPACE: OutOfSpaceError("out of space"),
            self.NO_VALUE: NoValueError("no value"),
        }[self.value]


def check_result(result: int) -> None:
    """Raise an appropriate exception if result is not GHOSTTY_SUCCESS (0)."""
    if result == 0:
        return
    GhosttyError(result).raise_error()
