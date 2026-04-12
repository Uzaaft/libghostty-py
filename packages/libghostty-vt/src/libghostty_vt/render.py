"""Pythonic wrapper for the libghostty-vt render state API.

Provides a framework-agnostic interface for snapshotting terminal render state
and iterating over rows and cells with resolved colors, styles, and graphemes.
"""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, NamedTuple

from libghostty_cffi import ffi, lib

from libghostty_vt.errors import check_result

if TYPE_CHECKING:
    from cffi import FFI

    from libghostty_vt.terminal import Terminal


class Dirty(enum.IntEnum):
    CLEAN = 0
    PARTIAL = 1
    FULL = 2


class CursorStyle(enum.IntEnum):
    BAR = 0
    BLOCK = 1
    UNDERLINE = 2
    BLOCK_HOLLOW = 3


class Color(NamedTuple):
    r: int
    g: int
    b: int


class Colors(NamedTuple):
    background: Color
    foreground: Color
    cursor: Color | None


class CursorInfo(NamedTuple):
    x: int
    y: int
    visible: bool
    blinking: bool
    style: CursorStyle


class CellStyle(NamedTuple):
    bold: bool
    italic: bool
    faint: bool
    inverse: bool
    strikethrough: bool
    underline: int


class Cell(NamedTuple):
    text: str
    fg: Color | None
    bg: Color | None
    style: CellStyle


class RenderState:
    """Owns the render state handle and pre-allocated iterator pointer containers."""

    def __init__(self) -> None:
        handle = ffi.new("GhosttyRenderState *")
        check_result(lib.ghostty_render_state_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

        # Pre-allocate pointer containers for iterators. The C API writes the
        # opaque handle *through* these pointers (out-param pattern), and the
        # actual handle used for subsequent calls is container[0].
        self._row_iter_ptr: FFI.CData = ffi.new("GhosttyRenderStateRowIterator *")
        self._cells_ptr: FFI.CData = ffi.new("GhosttyRenderStateRowCells *")

        row_iter_handle = ffi.new("GhosttyRenderStateRowIterator *")
        check_result(lib.ghostty_render_state_row_iterator_new(ffi.NULL, row_iter_handle))
        self._row_iter_ptr[0] = row_iter_handle[0]

        cells_handle = ffi.new("GhosttyRenderStateRowCells *")
        check_result(lib.ghostty_render_state_row_cells_new(ffi.NULL, cells_handle))
        self._cells_ptr[0] = cells_handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_cells_ptr") and self._cells_ptr[0] != ffi.NULL:
            lib.ghostty_render_state_row_cells_free(self._cells_ptr[0])
            self._cells_ptr[0] = ffi.NULL
        if hasattr(self, "_row_iter_ptr") and self._row_iter_ptr[0] != ffi.NULL:
            lib.ghostty_render_state_row_iterator_free(self._row_iter_ptr[0])
            self._row_iter_ptr[0] = ffi.NULL
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_render_state_free(self._handle)
            self._handle = ffi.NULL

    @property
    def handle(self) -> FFI.CData:
        """Raw CFFI handle for advanced use."""
        return self._handle

    def update(self, terminal: Terminal) -> Snapshot:
        """Snapshot the terminal state. Returns a Snapshot context manager."""
        check_result(lib.ghostty_render_state_update(self._handle, terminal.handle))
        return Snapshot(self)


class Snapshot:
    """Active snapshot of terminal render state. Use as context manager to auto-clear dirty."""

    def __init__(self, state: RenderState) -> None:
        self._state = state

    def __enter__(self) -> Snapshot:
        return self

    def __exit__(self, *exc: object) -> None:
        self.dirty = Dirty.CLEAN

    @property
    def dirty(self) -> Dirty:
        out = ffi.new("GhosttyRenderStateDirty *")
        check_result(
            lib.ghostty_render_state_get(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_DIRTY, out
            )
        )
        return Dirty(out[0])

    @dirty.setter
    def dirty(self, value: Dirty) -> None:
        dirty_val = ffi.new("GhosttyRenderStateDirty *", int(value))
        check_result(
            lib.ghostty_render_state_set(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_OPTION_DIRTY, dirty_val
            )
        )

    @property
    def colors(self) -> Colors:
        out = ffi.new("GhosttyRenderStateColors *")
        out.size = ffi.sizeof("GhosttyRenderStateColors")
        check_result(lib.ghostty_render_state_colors_get(self._state._handle, out))
        cursor = Color(out.cursor.r, out.cursor.g, out.cursor.b) if out.cursor_has_value else None
        return Colors(
            background=Color(out.background.r, out.background.g, out.background.b),
            foreground=Color(out.foreground.r, out.foreground.g, out.foreground.b),
            cursor=cursor,
        )

    @property
    def cursor(self) -> CursorInfo | None:
        """Returns cursor info if viewport has value, else None."""
        has_value = ffi.new("bool *")
        result = lib.ghostty_render_state_get(
            self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_HAS_VALUE, has_value
        )
        check_result(result)
        if not has_value[0]:
            return None

        x = ffi.new("uint16_t *")
        y = ffi.new("uint16_t *")
        visible = ffi.new("bool *")
        blinking = ffi.new("bool *")
        style = ffi.new("GhosttyRenderStateCursorVisualStyle *")

        check_result(
            lib.ghostty_render_state_get(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_X, x
            )
        )
        check_result(
            lib.ghostty_render_state_get(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_Y, y
            )
        )
        check_result(
            lib.ghostty_render_state_get(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VISIBLE, visible
            )
        )
        check_result(
            lib.ghostty_render_state_get(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_BLINKING, blinking
            )
        )
        check_result(
            lib.ghostty_render_state_get(
                self._state._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VISUAL_STYLE, style
            )
        )

        return CursorInfo(
            x=x[0],
            y=y[0],
            visible=bool(visible[0]),
            blinking=bool(blinking[0]),
            style=CursorStyle(style[0]),
        )

    def rows(self) -> RowIterator:
        """Iterate rows. Populates the pre-allocated row iterator."""
        check_result(
            lib.ghostty_render_state_get(
                self._state._handle,
                lib.GHOSTTY_RENDER_STATE_DATA_ROW_ITERATOR,
                self._state._row_iter_ptr,
            )
        )
        return RowIterator(self._state)


class RowIterator:
    """Iterator over rows in the snapshot. Yields Row objects."""

    def __init__(self, state: RenderState) -> None:
        self._state = state

    def __iter__(self) -> RowIterator:
        return self

    def __next__(self) -> Row:
        if not lib.ghostty_render_state_row_iterator_next(self._state._row_iter_ptr[0]):
            raise StopIteration
        return Row(self)


class Row:
    """A single row in the snapshot. Provides cell iteration."""

    def __init__(self, row_iter: RowIterator) -> None:
        self._state = row_iter._state

    @property
    def dirty(self) -> bool:
        out = ffi.new("bool *")
        check_result(
            lib.ghostty_render_state_row_get(
                self._state._row_iter_ptr[0],
                lib.GHOSTTY_RENDER_STATE_ROW_DATA_DIRTY,
                out,
            )
        )
        return bool(out[0])

    @dirty.setter
    def dirty(self, value: bool) -> None:
        dirty_val = ffi.new("bool *", value)
        check_result(
            lib.ghostty_render_state_row_set(
                self._state._row_iter_ptr[0], lib.GHOSTTY_RENDER_STATE_ROW_OPTION_DIRTY, dirty_val
            )
        )

    def cells(self) -> CellIterator:
        """Iterate cells in this row."""
        check_result(
            lib.ghostty_render_state_row_get(
                self._state._row_iter_ptr[0],
                lib.GHOSTTY_RENDER_STATE_ROW_DATA_CELLS,
                self._state._cells_ptr,
            )
        )
        return CellIterator(self._state)


class CellIterator:
    """Iterator over cells in a row. Yields Cell dataclass objects."""

    def __init__(self, state: RenderState) -> None:
        self._state = state

    def __iter__(self) -> CellIterator:
        return self

    def __next__(self) -> Cell:
        cells_handle = self._state._cells_ptr[0]
        if not lib.ghostty_render_state_row_cells_next(cells_handle):
            raise StopIteration

        graphemes_len = ffi.new("uint32_t *")
        check_result(
            lib.ghostty_render_state_row_cells_get(
                cells_handle, lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_LEN, graphemes_len
            )
        )

        text = ""
        if graphemes_len[0] > 0:
            buf = ffi.new("uint32_t[]", graphemes_len[0])
            check_result(
                lib.ghostty_render_state_row_cells_get(
                    cells_handle, lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_BUF, buf
                )
            )
            text = "".join(chr(buf[i]) for i in range(graphemes_len[0]))

        fg_rgb = ffi.new("GhosttyColorRgb *")
        fg_result = lib.ghostty_render_state_row_cells_get(
            cells_handle, lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_FG_COLOR, fg_rgb
        )
        fg: Color | None = Color(fg_rgb.r, fg_rgb.g, fg_rgb.b) if fg_result == 0 else None

        bg_rgb = ffi.new("GhosttyColorRgb *")
        bg_result = lib.ghostty_render_state_row_cells_get(
            cells_handle, lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_BG_COLOR, bg_rgb
        )
        bg: Color | None = Color(bg_rgb.r, bg_rgb.g, bg_rgb.b) if bg_result == 0 else None

        style_out = ffi.new("GhosttyStyle *")
        style_out.size = ffi.sizeof("GhosttyStyle")
        check_result(
            lib.ghostty_render_state_row_cells_get(
                cells_handle, lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_STYLE, style_out
            )
        )

        cell_style = CellStyle(
            bold=bool(style_out.bold),
            italic=bool(style_out.italic),
            faint=bool(style_out.faint),
            inverse=bool(style_out.inverse),
            strikethrough=bool(style_out.strikethrough),
            underline=int(style_out.underline),
        )

        return Cell(text=text, fg=fg, bg=bg, style=cell_style)
