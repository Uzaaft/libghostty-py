"""Python bindings for libghostty-vt."""

from libghostty._ffi import ffi, lib
from libghostty.errors import (
    GhosttyError,
    InvalidValueError,
    NoValueError,
    OutOfMemoryError,
    OutOfSpaceError,
)
from libghostty.key import KeyEncoder, KeyEvent
from libghostty.mouse import MouseEncoder, MouseEvent
from libghostty.osc import OscCommand, OscParser
from libghostty.sgr import SgrAttribute, SgrParser
from libghostty.terminal import Terminal

__all__ = [
    "GhosttyError",
    "InvalidValueError",
    "KeyEncoder",
    "KeyEvent",
    "MouseEncoder",
    "MouseEvent",
    "NoValueError",
    "OscCommand",
    "OscParser",
    "OutOfMemoryError",
    "OutOfSpaceError",
    "SgrAttribute",
    "SgrParser",
    "Terminal",
    "ffi",
    "lib",
]
