"""Pythonic Python bindings for libghostty-vt."""

from libghostty_cffi import ffi, lib

from .errors import (
    GhosttyError,
    InvalidValueError,
    NoValueError,
    OutOfMemoryError,
    OutOfSpaceError,
)
from .key import KeyEncoder, KeyEvent
from .mouse import MouseEncoder, MouseEvent
from .osc import OscCommand, OscParser
from .render import (
    Cell,
    CellStyle,
    Color,
    Colors,
    CursorInfo,
    CursorStyle,
    Dirty,
    RenderState,
    Snapshot,
)
from .sgr import SgrAttribute, SgrParser
from .terminal import Terminal

__all__ = (
    "Cell",
    "CellStyle",
    "Color",
    "Colors",
    "CursorInfo",
    "CursorStyle",
    "Dirty",
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
    "RenderState",
    "SgrAttribute",
    "SgrParser",
    "Snapshot",
    "Terminal",
    "ffi",
    "lib",
)
