#!/usr/bin/env python3
"""Ghostling - a minimal terminal emulator built with libghostty-py and PyQt6.

Demonstrates how to use the libghostty-vt Python bindings to build a
functional terminal emulator with PTY management, keyboard/mouse input
encoding, and cell-level rendering via the render state API.

Usage:
    LIBGHOSTTY_VT_PATH=/path/to/libghostty-vt.so python ghostling.py

Requirements:
    pip install PyQt6 libghostty
"""

from __future__ import annotations

import fcntl
import os
import pty
import signal
import struct
import sys
import termios
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSocketNotifier, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QFontMetricsF, QKeyEvent, QPainter, QResizeEvent
from PyQt6.QtWidgets import QApplication, QWidget

from libghostty import Terminal, ffi, lib
from libghostty.errors import check_result
from libghostty.key import KeyEncoder, KeyEvent

if TYPE_CHECKING:
    from PyQt6.QtGui import QPaintEvent

# Qt key code to GhosttyKey mapping
# Each entry: (qt_key, ghostty_key, unshifted_codepoint)
# The unshifted codepoint is the character the key produces with no modifiers
# on a US layout. The Kitty keyboard protocol needs this. '\0' for keys
# without a natural codepoint (arrows, function keys, etc.).

_KEY_MAP: list[tuple[int, int, str]] = [
    (Qt.Key.Key_A, lib.GHOSTTY_KEY_A, "a"),
    (Qt.Key.Key_B, lib.GHOSTTY_KEY_B, "b"),
    (Qt.Key.Key_C, lib.GHOSTTY_KEY_C, "c"),
    (Qt.Key.Key_D, lib.GHOSTTY_KEY_D, "d"),
    (Qt.Key.Key_E, lib.GHOSTTY_KEY_E, "e"),
    (Qt.Key.Key_F, lib.GHOSTTY_KEY_F, "f"),
    (Qt.Key.Key_G, lib.GHOSTTY_KEY_G, "g"),
    (Qt.Key.Key_H, lib.GHOSTTY_KEY_H, "h"),
    (Qt.Key.Key_I, lib.GHOSTTY_KEY_I, "i"),
    (Qt.Key.Key_J, lib.GHOSTTY_KEY_J, "j"),
    (Qt.Key.Key_K, lib.GHOSTTY_KEY_K, "k"),
    (Qt.Key.Key_L, lib.GHOSTTY_KEY_L, "l"),
    (Qt.Key.Key_M, lib.GHOSTTY_KEY_M, "m"),
    (Qt.Key.Key_N, lib.GHOSTTY_KEY_N, "n"),
    (Qt.Key.Key_O, lib.GHOSTTY_KEY_O, "o"),
    (Qt.Key.Key_P, lib.GHOSTTY_KEY_P, "p"),
    (Qt.Key.Key_Q, lib.GHOSTTY_KEY_Q, "q"),
    (Qt.Key.Key_R, lib.GHOSTTY_KEY_R, "r"),
    (Qt.Key.Key_S, lib.GHOSTTY_KEY_S, "s"),
    (Qt.Key.Key_T, lib.GHOSTTY_KEY_T, "t"),
    (Qt.Key.Key_U, lib.GHOSTTY_KEY_U, "u"),
    (Qt.Key.Key_V, lib.GHOSTTY_KEY_V, "v"),
    (Qt.Key.Key_W, lib.GHOSTTY_KEY_W, "w"),
    (Qt.Key.Key_X, lib.GHOSTTY_KEY_X, "x"),
    (Qt.Key.Key_Y, lib.GHOSTTY_KEY_Y, "y"),
    (Qt.Key.Key_Z, lib.GHOSTTY_KEY_Z, "z"),
    (Qt.Key.Key_0, lib.GHOSTTY_KEY_DIGIT_0, "0"),
    (Qt.Key.Key_1, lib.GHOSTTY_KEY_DIGIT_1, "1"),
    (Qt.Key.Key_2, lib.GHOSTTY_KEY_DIGIT_2, "2"),
    (Qt.Key.Key_3, lib.GHOSTTY_KEY_DIGIT_3, "3"),
    (Qt.Key.Key_4, lib.GHOSTTY_KEY_DIGIT_4, "4"),
    (Qt.Key.Key_5, lib.GHOSTTY_KEY_DIGIT_5, "5"),
    (Qt.Key.Key_6, lib.GHOSTTY_KEY_DIGIT_6, "6"),
    (Qt.Key.Key_7, lib.GHOSTTY_KEY_DIGIT_7, "7"),
    (Qt.Key.Key_8, lib.GHOSTTY_KEY_DIGIT_8, "8"),
    (Qt.Key.Key_9, lib.GHOSTTY_KEY_DIGIT_9, "9"),
    (Qt.Key.Key_Space, lib.GHOSTTY_KEY_SPACE, " "),
    (Qt.Key.Key_Return, lib.GHOSTTY_KEY_ENTER, "\0"),
    (Qt.Key.Key_Enter, lib.GHOSTTY_KEY_NUMPAD_ENTER, "\0"),
    (Qt.Key.Key_Tab, lib.GHOSTTY_KEY_TAB, "\0"),
    (Qt.Key.Key_Backspace, lib.GHOSTTY_KEY_BACKSPACE, "\0"),
    (Qt.Key.Key_Delete, lib.GHOSTTY_KEY_DELETE, "\0"),
    (Qt.Key.Key_Escape, lib.GHOSTTY_KEY_ESCAPE, "\0"),
    (Qt.Key.Key_Up, lib.GHOSTTY_KEY_ARROW_UP, "\0"),
    (Qt.Key.Key_Down, lib.GHOSTTY_KEY_ARROW_DOWN, "\0"),
    (Qt.Key.Key_Left, lib.GHOSTTY_KEY_ARROW_LEFT, "\0"),
    (Qt.Key.Key_Right, lib.GHOSTTY_KEY_ARROW_RIGHT, "\0"),
    (Qt.Key.Key_Home, lib.GHOSTTY_KEY_HOME, "\0"),
    (Qt.Key.Key_End, lib.GHOSTTY_KEY_END, "\0"),
    (Qt.Key.Key_PageUp, lib.GHOSTTY_KEY_PAGE_UP, "\0"),
    (Qt.Key.Key_PageDown, lib.GHOSTTY_KEY_PAGE_DOWN, "\0"),
    (Qt.Key.Key_Insert, lib.GHOSTTY_KEY_INSERT, "\0"),
    (Qt.Key.Key_Minus, lib.GHOSTTY_KEY_MINUS, "-"),
    (Qt.Key.Key_Equal, lib.GHOSTTY_KEY_EQUAL, "="),
    (Qt.Key.Key_BracketLeft, lib.GHOSTTY_KEY_BRACKET_LEFT, "["),
    (Qt.Key.Key_BracketRight, lib.GHOSTTY_KEY_BRACKET_RIGHT, "]"),
    (Qt.Key.Key_Backslash, lib.GHOSTTY_KEY_BACKSLASH, "\\"),
    (Qt.Key.Key_Semicolon, lib.GHOSTTY_KEY_SEMICOLON, ";"),
    (Qt.Key.Key_Apostrophe, lib.GHOSTTY_KEY_QUOTE, "'"),
    (Qt.Key.Key_Comma, lib.GHOSTTY_KEY_COMMA, ","),
    (Qt.Key.Key_Period, lib.GHOSTTY_KEY_PERIOD, "."),
    (Qt.Key.Key_Slash, lib.GHOSTTY_KEY_SLASH, "/"),
    (Qt.Key.Key_QuoteLeft, lib.GHOSTTY_KEY_BACKQUOTE, "`"),
    (Qt.Key.Key_F1, lib.GHOSTTY_KEY_F1, "\0"),
    (Qt.Key.Key_F2, lib.GHOSTTY_KEY_F2, "\0"),
    (Qt.Key.Key_F3, lib.GHOSTTY_KEY_F3, "\0"),
    (Qt.Key.Key_F4, lib.GHOSTTY_KEY_F4, "\0"),
    (Qt.Key.Key_F5, lib.GHOSTTY_KEY_F5, "\0"),
    (Qt.Key.Key_F6, lib.GHOSTTY_KEY_F6, "\0"),
    (Qt.Key.Key_F7, lib.GHOSTTY_KEY_F7, "\0"),
    (Qt.Key.Key_F8, lib.GHOSTTY_KEY_F8, "\0"),
    (Qt.Key.Key_F9, lib.GHOSTTY_KEY_F9, "\0"),
    (Qt.Key.Key_F10, lib.GHOSTTY_KEY_F10, "\0"),
    (Qt.Key.Key_F11, lib.GHOSTTY_KEY_F11, "\0"),
    (Qt.Key.Key_F12, lib.GHOSTTY_KEY_F12, "\0"),
]

# Build a fast lookup dict: Qt key code -> (ghostty_key, unshifted_codepoint)
_QT_KEY_LOOKUP: dict[int, tuple[int, str]] = {qt: (gk, ucp) for qt, gk, ucp in _KEY_MAP}

_MODS_SHIFT = 1 << 0
_MODS_CTRL = 1 << 1
_MODS_ALT = 1 << 2
_MODS_SUPER = 1 << 3


def _qt_mods_to_ghostty(qt_mods: Qt.KeyboardModifier) -> int:
    mods = 0
    if qt_mods & Qt.KeyboardModifier.ShiftModifier:
        mods |= _MODS_SHIFT
    if qt_mods & Qt.KeyboardModifier.ControlModifier:
        mods |= _MODS_CTRL
    if qt_mods & Qt.KeyboardModifier.AltModifier:
        mods |= _MODS_ALT
    if qt_mods & Qt.KeyboardModifier.MetaModifier:
        mods |= _MODS_SUPER
    return mods


# PTY helpers


def _set_pty_size(fd: int, cols: int, rows: int) -> None:
    winsize = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def _spawn_shell(cols: int, rows: int) -> tuple[int, int]:
    """Fork a child process with a PTY running the user's shell."""
    child_pid, master_fd = pty.fork()
    if child_pid == 0:
        shell = os.environ.get("SHELL", "/bin/sh")
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        env["COLORTERM"] = "truecolor"
        os.execvpe(shell, [shell], env)
    _set_pty_size(master_fd, cols, rows)
    return master_fd, child_pid


class RenderState:
    """Manages the libghostty render state for efficient screen painting."""

    def __init__(self) -> None:
        handle = ffi.new("GhosttyRenderState *")
        check_result(lib.ghostty_render_state_new(ffi.NULL, handle))
        self._handle = handle[0]

        # Keep row iterator and cells handles in pointer containers so
        # we can pass their address to C functions that write through
        # the pointer (ghostty_render_state_get with ROW_ITERATOR,
        # ghostty_render_state_row_get with CELLS).
        self._row_iter_ptr = ffi.new("GhosttyRenderStateRowIterator *")
        check_result(lib.ghostty_render_state_row_iterator_new(ffi.NULL, self._row_iter_ptr))

        self._cells_ptr = ffi.new("GhosttyRenderStateRowCells *")
        check_result(lib.ghostty_render_state_row_cells_new(ffi.NULL, self._cells_ptr))

    def __del__(self) -> None:
        if hasattr(self, "_cells_ptr") and self._cells_ptr[0] != ffi.NULL:
            lib.ghostty_render_state_row_cells_free(self._cells_ptr[0])
        if hasattr(self, "_row_iter_ptr") and self._row_iter_ptr[0] != ffi.NULL:
            lib.ghostty_render_state_row_iterator_free(self._row_iter_ptr[0])
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_render_state_free(self._handle)

    def update(self, terminal: Terminal) -> None:
        check_result(lib.ghostty_render_state_update(self._handle, terminal.handle))

    @property
    def dirty(self) -> int:
        out = ffi.new("GhosttyRenderStateDirty *")
        check_result(
            lib.ghostty_render_state_get(self._handle, lib.GHOSTTY_RENDER_STATE_DATA_DIRTY, out)
        )
        return out[0]

    def clear_dirty(self) -> None:
        val = ffi.new("GhosttyRenderStateDirty *", lib.GHOSTTY_RENDER_STATE_DIRTY_FALSE)
        lib.ghostty_render_state_set(self._handle, lib.GHOSTTY_RENDER_STATE_OPTION_DIRTY, val)

    def get_colors(self) -> tuple[QColor, QColor]:
        """Return (background, foreground) as QColors."""
        colors = ffi.new("GhosttyRenderStateColors *")
        colors.size = ffi.sizeof("GhosttyRenderStateColors")
        check_result(lib.ghostty_render_state_colors_get(self._handle, colors))
        bg = QColor(colors.background.r, colors.background.g, colors.background.b)
        fg = QColor(colors.foreground.r, colors.foreground.g, colors.foreground.b)
        return bg, fg

    def get_cursor_pos(self) -> tuple[int, int] | None:
        has = ffi.new("bool *")
        check_result(
            lib.ghostty_render_state_get(
                self._handle,
                lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_HAS_VALUE,
                has,
            )
        )
        if not has[0]:
            return None
        cx = ffi.new("uint16_t *")
        cy = ffi.new("uint16_t *")
        check_result(
            lib.ghostty_render_state_get(
                self._handle,
                lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_X,
                cx,
            )
        )
        check_result(
            lib.ghostty_render_state_get(
                self._handle,
                lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VIEWPORT_Y,
                cy,
            )
        )
        return (cx[0], cy[0])

    def get_cursor_visible(self) -> bool:
        out = ffi.new("bool *")
        check_result(
            lib.ghostty_render_state_get(
                self._handle, lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VISIBLE, out
            )
        )
        return bool(out[0])

    def get_cursor_style(self) -> int:
        out = ffi.new("GhosttyRenderStateCursorVisualStyle *")
        check_result(
            lib.ghostty_render_state_get(
                self._handle,
                lib.GHOSTTY_RENDER_STATE_DATA_CURSOR_VISUAL_STYLE,
                out,
            )
        )
        return out[0]

    def iter_rows_and_cells(
        self,
        default_bg: QColor,
        default_fg: QColor,
    ) -> list[list[tuple[str, QColor, QColor, bool, bool, bool]]]:
        """Iterate all rows and cells, returning a grid of render data.

        Each cell is (text, fg_color, bg_color, bold, italic, inverse).
        """
        # Populate row iterator from render state. The C function
        # writes through the pointer, so pass the pointer container.
        result = lib.ghostty_render_state_get(
            self._handle,
            lib.GHOSTTY_RENDER_STATE_DATA_ROW_ITERATOR,
            self._row_iter_ptr,
        )
        if result != 0:
            return []

        row_it = self._row_iter_ptr[0]
        rows: list[list[tuple[str, QColor, QColor, bool, bool, bool]]] = []
        while lib.ghostty_render_state_row_iterator_next(row_it):
            # Populate cell iterator — same pointer-to-handle pattern
            check_result(
                lib.ghostty_render_state_row_get(
                    row_it,
                    lib.GHOSTTY_RENDER_STATE_ROW_DATA_CELLS,
                    self._cells_ptr,
                )
            )

            cells = self._cells_ptr[0]
            row: list[tuple[str, QColor, QColor, bool, bool, bool]] = []
            while lib.ghostty_render_state_row_cells_next(cells):
                # Grapheme text
                glyph_len = ffi.new("uint32_t *")
                lib.ghostty_render_state_row_cells_get(
                    cells,
                    lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_LEN,
                    glyph_len,
                )
                text = ""
                if glyph_len[0] > 0:
                    buf = ffi.new("uint32_t[]", glyph_len[0])
                    lib.ghostty_render_state_row_cells_get(
                        cells,
                        lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_GRAPHEMES_BUF,
                        buf,
                    )
                    text = "".join(chr(buf[i]) for i in range(glyph_len[0]))

                # Foreground color
                fg_rgb = ffi.new("GhosttyColorRgb *")
                fg_result = lib.ghostty_render_state_row_cells_get(
                    cells,
                    lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_FG_COLOR,
                    fg_rgb,
                )
                fg = QColor(fg_rgb.r, fg_rgb.g, fg_rgb.b) if fg_result == 0 else default_fg

                # Background color
                bg_rgb = ffi.new("GhosttyColorRgb *")
                bg_result = lib.ghostty_render_state_row_cells_get(
                    cells,
                    lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_BG_COLOR,
                    bg_rgb,
                )
                bg = QColor(bg_rgb.r, bg_rgb.g, bg_rgb.b) if bg_result == 0 else default_bg

                # Style flags
                style = ffi.new("GhosttyStyle *")
                style.size = ffi.sizeof("GhosttyStyle")
                style_result = lib.ghostty_render_state_row_cells_get(
                    cells,
                    lib.GHOSTTY_RENDER_STATE_ROW_CELLS_DATA_STYLE,
                    style,
                )
                bold = bool(style.bold) if style_result == 0 else False
                italic = bool(style.italic) if style_result == 0 else False
                inverse = bool(style.inverse) if style_result == 0 else False

                row.append((text, fg, bg, bold, italic, inverse))

            # Clear per-row dirty flag
            false_val = ffi.new("bool *", False)
            lib.ghostty_render_state_row_set(
                row_it,
                lib.GHOSTTY_RENDER_STATE_ROW_OPTION_DIRTY,
                false_val,
            )
            rows.append(row)

        return rows


_DEFAULT_BG = QColor(30, 30, 46)
_DEFAULT_FG = QColor(205, 214, 244)
_CURSOR_COLOR = QColor(245, 194, 231)


class GhostlingWidget(QWidget):
    """A PyQt6 terminal emulator widget powered by libghostty-vt."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Font setup
        self._font = QFont("monospace", 13)
        self._font.setStyleHint(QFont.StyleHint.Monospace)
        metrics = QFontMetricsF(self._font)
        self._cell_width = metrics.horizontalAdvance("M")
        self._cell_height = metrics.height()

        # Initial grid size
        self._grid_cols = 80
        self._grid_rows = 24

        # Terminal
        self._terminal = Terminal(
            cols=self._grid_cols,
            rows=self._grid_rows,
            max_scrollback=10000,
        )
        self._terminal.set_background_color(
            _DEFAULT_BG.red(), _DEFAULT_BG.green(), _DEFAULT_BG.blue()
        )
        self._terminal.set_foreground_color(
            _DEFAULT_FG.red(), _DEFAULT_FG.green(), _DEFAULT_FG.blue()
        )

        # Set cell pixel dimensions so size reports work correctly
        self._terminal.resize(
            self._grid_cols,
            self._grid_rows,
            int(self._cell_width),
            int(self._cell_height),
        )

        # Install terminal effects so VT query responses flow back
        self._write_pty_cb = ffi.callback("GhosttyTerminalWritePtyFn", self._on_write_pty)
        check_result(
            lib.ghostty_terminal_set(
                self._terminal.handle,
                lib.GHOSTTY_TERMINAL_OPT_WRITE_PTY,
                self._write_pty_cb,
            )
        )

        # Device attributes callback (DA1/DA2/DA3)
        self._da_cb = ffi.callback("GhosttyTerminalDeviceAttributesFn", self._on_device_attributes)
        check_result(
            lib.ghostty_terminal_set(
                self._terminal.handle,
                lib.GHOSTTY_TERMINAL_OPT_DEVICE_ATTRIBUTES,
                self._da_cb,
            )
        )

        # Size callback (XTWINOPS CSI 14/16/18 t)
        self._size_cb = ffi.callback("GhosttyTerminalSizeFn", self._on_size_query)
        check_result(
            lib.ghostty_terminal_set(
                self._terminal.handle,
                lib.GHOSTTY_TERMINAL_OPT_SIZE,
                self._size_cb,
            )
        )

        # Render state — initial sync from terminal
        self._render = RenderState()
        self._render.update(self._terminal)

        # Key encoder
        self._key_encoder = KeyEncoder()
        self._key_event = KeyEvent()

        # PTY
        self._master_fd, self._child_pid = _spawn_shell(self._grid_cols, self._grid_rows)
        flags = fcntl.fcntl(self._master_fd, fcntl.F_GETFL)
        fcntl.fcntl(self._master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        self._notifier = QSocketNotifier(self._master_fd, QSocketNotifier.Type.Read, self)
        self._notifier.activated.connect(self._on_pty_readable)

        # Blink timer
        self._blink_visible = True
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._on_blink)
        self._blink_timer.start(530)

        # Widget config
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(400, 200)
        self._update_window_size()
        self._update_title()

    def _on_write_pty(
        self, _terminal: object, _userdata: object, data: object, length: int
    ) -> None:
        buf = ffi.buffer(data, length)[:]
        self._write_to_pty(buf)

    def _on_device_attributes(
        self, _terminal: object, _userdata: object, out_attrs: object
    ) -> bool:
        # DA1: VT220-level with common features
        out_attrs.primary.conformance_level = 62  # VT220
        out_attrs.primary.features[0] = 1  # COLUMNS_132
        out_attrs.primary.features[1] = 6  # SELECTIVE_ERASE
        out_attrs.primary.features[2] = 22  # ANSI_COLOR
        out_attrs.primary.num_features = 3
        # DA2: VT220, version 1
        out_attrs.secondary.device_type = 1  # VT220
        out_attrs.secondary.firmware_version = 1
        out_attrs.secondary.rom_cartridge = 0
        # DA3: default unit id
        out_attrs.tertiary.unit_id = 0
        return True

    def _on_size_query(self, _terminal: object, _userdata: object, out_size: object) -> bool:
        out_size.rows = self._grid_rows
        out_size.columns = self._grid_cols
        out_size.cell_width = int(self._cell_width)
        out_size.cell_height = int(self._cell_height)
        return True

    def _on_pty_readable(self) -> None:
        try:
            data = os.read(self._master_fd, 65536)
        except OSError:
            self._notifier.setEnabled(False)
            self.close()
            return
        if not data:
            self._notifier.setEnabled(False)
            self.close()
            return

        self._terminal.write(data)
        self._render.update(self._terminal)

        if self._render.dirty != lib.GHOSTTY_RENDER_STATE_DIRTY_FALSE:
            self.update()

        self._update_title()

    def _write_to_pty(self, data: bytes) -> None:
        try:
            os.write(self._master_fd, data)
        except OSError:
            pass

    def keyPressEvent(self, event: QKeyEvent) -> None:
        qt_key = event.key()
        entry = _QT_KEY_LOOKUP.get(qt_key)

        if entry is None:
            # Key not in our map — send raw text as fallback
            text = event.text()
            if text:
                self._write_to_pty(text.encode("utf-8"))
            return

        ghostty_key, unshifted_cp = entry
        mods = _qt_mods_to_ghostty(event.modifiers())

        # Consumed mods: for printable keys, shift is consumed by the
        # platform's text input (it turns 'a' into 'A')
        consumed = 0
        if unshifted_cp != "\0" and (mods & _MODS_SHIFT):
            consumed |= _MODS_SHIFT

        # Sync encoder with current terminal modes
        self._key_encoder.sync_from_terminal(self._terminal)

        self._key_event.action = lib.GHOSTTY_KEY_ACTION_PRESS
        self._key_event.key = ghostty_key
        self._key_event.mods = mods

        # Set consumed mods
        lib.ghostty_key_event_set_consumed_mods(self._key_event.handle, consumed)

        # Set unshifted codepoint for Kitty keyboard protocol
        if unshifted_cp != "\0":
            lib.ghostty_key_event_set_unshifted_codepoint(self._key_event.handle, ord(unshifted_cp))

        # Attach UTF-8 text from Qt (the character after platform processing)
        text = event.text()
        if text and ord(text[0]) >= 0x20:
            self._key_event.set_utf8(text)
        else:
            self._key_event.set_utf8("")

        encoded = self._key_encoder.encode(self._key_event)
        if encoded:
            self._write_to_pty(encoded)
        elif text:
            # Fallback: encoder produced nothing, send raw text
            self._write_to_pty(text.encode("utf-8"))

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        event.accept()

    def resizeEvent(self, event: QResizeEvent) -> None:
        new_cols = max(1, int(event.size().width() / self._cell_width))
        new_rows = max(1, int(event.size().height() / self._cell_height))

        if new_cols != self._grid_cols or new_rows != self._grid_rows:
            self._grid_cols = new_cols
            self._grid_rows = new_rows
            cell_w = int(self._cell_width)
            cell_h = int(self._cell_height)
            self._terminal.resize(new_cols, new_rows, cell_w, cell_h)
            _set_pty_size(self._master_fd, new_cols, new_rows)
            self._render.update(self._terminal)

        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setFont(self._font)

        bg_color, fg_color = self._render.get_colors()
        painter.fillRect(self.rect(), bg_color)

        grid = self._render.iter_rows_and_cells(bg_color, fg_color)
        cw = self._cell_width
        ch = self._cell_height
        ascent = QFontMetricsF(self._font).ascent()

        for row_idx, row in enumerate(grid):
            y = row_idx * ch
            for col_idx, (text, fg, bg, bold, italic, inverse) in enumerate(row):
                x = col_idx * cw

                # Handle inverse (reverse video)
                if inverse:
                    fg, bg = bg, fg

                # Draw cell background if different from terminal background
                if bg != bg_color or inverse:
                    painter.fillRect(int(x), int(y), int(cw) + 1, int(ch), bg)

                # Draw text
                if text and text != " ":
                    font = QFont(self._font)
                    if bold:
                        font.setBold(True)
                    if italic:
                        font.setItalic(True)
                    painter.setFont(font)
                    painter.setPen(fg)
                    painter.drawText(int(x), int(y + ascent), text)
                    if bold or italic:
                        painter.setFont(self._font)

        # Draw cursor
        if self._render.get_cursor_visible():
            cursor_pos = self._render.get_cursor_pos()
            if cursor_pos is not None and self._blink_visible:
                cx, cy = cursor_pos
                cursor_x = cx * cw
                cursor_y = cy * ch
                style = self._render.get_cursor_style()
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(_CURSOR_COLOR)

                if style == lib.GHOSTTY_RENDER_STATE_CURSOR_VISUAL_STYLE_BLOCK:
                    painter.setOpacity(0.7)
                    painter.drawRect(int(cursor_x), int(cursor_y), int(cw), int(ch))
                    painter.setOpacity(1.0)
                elif style == lib.GHOSTTY_RENDER_STATE_CURSOR_VISUAL_STYLE_BAR:
                    painter.drawRect(int(cursor_x), int(cursor_y), 2, int(ch))
                elif style == lib.GHOSTTY_RENDER_STATE_CURSOR_VISUAL_STYLE_UNDERLINE:
                    painter.drawRect(int(cursor_x), int(cursor_y + ch - 2), int(cw), 2)
                elif style == lib.GHOSTTY_RENDER_STATE_CURSOR_VISUAL_STYLE_BLOCK_HOLLOW:
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.setPen(_CURSOR_COLOR)
                    painter.drawRect(int(cursor_x), int(cursor_y), int(cw), int(ch))

        # Reset dirty state after full paint
        self._render.clear_dirty()
        painter.end()

    def _on_blink(self) -> None:
        self._blink_visible = not self._blink_visible
        if self._render.get_cursor_visible():
            self.update()

    def _update_title(self) -> None:
        title = self._terminal.title
        self.window().setWindowTitle(title if title else "Ghostling")

    def _update_window_size(self) -> None:
        w = int(self._grid_cols * self._cell_width)
        h = int(self._grid_rows * self._cell_height)
        self.resize(w, h)

    def closeEvent(self, event: object) -> None:
        self._notifier.setEnabled(False)
        try:
            os.close(self._master_fd)
        except OSError:
            pass
        try:
            os.kill(self._child_pid, signal.SIGTERM)
            os.waitpid(self._child_pid, os.WNOHANG)
        except (OSError, ChildProcessError):
            pass


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Ghostling")

    widget = GhostlingWidget()
    widget.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
