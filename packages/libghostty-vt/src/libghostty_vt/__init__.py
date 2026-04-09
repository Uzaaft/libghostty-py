"""Pythonic Python bindings for libghostty-vt."""

from libghostty_cffi import ffi, lib
from libghostty_vt.errors import (
    GhosttyError,
    InvalidValueError,
    NoValueError,
    OutOfMemoryError,
    OutOfSpaceError,
)
from libghostty_vt.key import KeyEncoder, KeyEvent
from libghostty_vt.mouse import MouseEncoder, MouseEvent
from libghostty_vt.osc import OscCommand, OscParser
from libghostty_vt.render import (
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
from libghostty_vt.sgr import SgrAttribute, SgrParser
from libghostty_vt.terminal import Terminal

__all__ = [
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
]
