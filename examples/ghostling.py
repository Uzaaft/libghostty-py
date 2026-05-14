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
import time
import zlib
from contextlib import suppress
from functools import cache
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSocketNotifier, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QFontMetricsF, QImage, QKeyEvent, QPainter, QResizeEvent
from PyQt6.QtWidgets import QApplication, QWidget

from libghostty.vt import (
    Color,
    CursorStyle,
    DeviceAttributes,
    Dirty,
    Key,
    KeyAction,
    KeyEncoder,
    KeyEvent,
    KittyImage,
    KittyImageCompression,
    KittyImageFormat,
    RenderState,
    SizeReport,
    Terminal,
)

if TYPE_CHECKING:
    from PyQt6.QtGui import QPaintEvent

# Qt key code to Ghostty key plus unshifted codepoint. The codepoint is the
# character the key produces on a US layout without modifiers, or '\0' for keys
# without a natural printable codepoint.
# Disclaimer: generated with AI to reduce LOC count as the previous table was an eyesore.
_QT_KEY_LOOKUP: dict[Qt.Key, tuple[Key, str]] = {
    **{
        getattr(Qt.Key, f"Key_{letter}"): (Key[letter], letter.lower())
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    },
    **{getattr(Qt.Key, f"Key_{digit}"): (Key[f"DIGIT_{digit}"], digit) for digit in "0123456789"},
    **{getattr(Qt.Key, f"Key_F{number}"): (Key[f"F{number}"], "\0") for number in range(1, 13)},
    Qt.Key.Key_Space: (Key.SPACE, " "),
    Qt.Key.Key_Return: (Key.ENTER, "\0"),
    Qt.Key.Key_Enter: (Key.NUMPAD_ENTER, "\0"),
    Qt.Key.Key_Tab: (Key.TAB, "\0"),
    Qt.Key.Key_Backspace: (Key.BACKSPACE, "\0"),
    Qt.Key.Key_Delete: (Key.DELETE, "\0"),
    Qt.Key.Key_Escape: (Key.ESCAPE, "\0"),
    Qt.Key.Key_Up: (Key.ARROW_UP, "\0"),
    Qt.Key.Key_Down: (Key.ARROW_DOWN, "\0"),
    Qt.Key.Key_Left: (Key.ARROW_LEFT, "\0"),
    Qt.Key.Key_Right: (Key.ARROW_RIGHT, "\0"),
    Qt.Key.Key_Home: (Key.HOME, "\0"),
    Qt.Key.Key_End: (Key.END, "\0"),
    Qt.Key.Key_PageUp: (Key.PAGE_UP, "\0"),
    Qt.Key.Key_PageDown: (Key.PAGE_DOWN, "\0"),
    Qt.Key.Key_Insert: (Key.INSERT, "\0"),
    Qt.Key.Key_Minus: (Key.MINUS, "-"),
    Qt.Key.Key_Equal: (Key.EQUAL, "="),
    Qt.Key.Key_BracketLeft: (Key.BRACKET_LEFT, "["),
    Qt.Key.Key_BracketRight: (Key.BRACKET_RIGHT, "]"),
    Qt.Key.Key_Backslash: (Key.BACKSLASH, "\\"),
    Qt.Key.Key_Semicolon: (Key.SEMICOLON, ";"),
    Qt.Key.Key_Apostrophe: (Key.QUOTE, "'"),
    Qt.Key.Key_Comma: (Key.COMMA, ","),
    Qt.Key.Key_Period: (Key.PERIOD, "."),
    Qt.Key.Key_Slash: (Key.SLASH, "/"),
    Qt.Key.Key_QuoteLeft: (Key.BACKQUOTE, "`"),
}

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


def _set_pty_size(
    fd: int,
    cols: int,
    rows: int,
    cell_width_px: int,
    cell_height_px: int,
) -> None:
    width_px = cols * cell_width_px
    height_px = rows * cell_height_px
    winsize = struct.pack("HHHH", rows, cols, width_px, height_px)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def _spawn_shell(cols: int, rows: int, cell_width_px: int, cell_height_px: int) -> tuple[int, int]:
    """Fork a child process with a PTY running the user's shell."""
    child_pid, master_fd = pty.fork()
    if child_pid == 0:
        shell = os.environ.get("SHELL", "/bin/sh")
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        env["COLORTERM"] = "truecolor"
        os.execvpe(shell, [shell], env)
    _set_pty_size(master_fd, cols, rows, cell_width_px, cell_height_px)
    return master_fd, child_pid


@cache
def _qcolor(color: Color) -> QColor:
    return QColor(color.r, color.g, color.b)


_DEFAULT_BG = QColor(30, 30, 46)
_DEFAULT_FG = QColor(205, 214, 244)
_CURSOR_COLOR = QColor(245, 194, 231)
_FPS_COLOR = QColor(250, 250, 0)


class GhostlingWidget(QWidget):
    """A PyQt6 terminal emulator widget powered by libghostty-vt."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Font setup
        self._font = QFont("monospace", 13)
        self._font.setStyleHint(QFont.StyleHint.Monospace)
        self._font_bold = QFont(self._font)
        self._font_bold.setBold(True)
        self._font_italic = QFont(self._font)
        self._font_italic.setItalic(True)
        self._font_bold_italic = QFont(self._font)
        self._font_bold_italic.setBold(True)
        self._font_bold_italic.setItalic(True)
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
        self._terminal.set_kitty_image_storage_limit(64 * 1024 * 1024)

        # Set cell pixel dimensions so size reports work correctly
        self._terminal.resize(
            self._grid_cols,
            self._grid_rows,
            int(self._cell_width),
            int(self._cell_height),
        )

        self._terminal.set_write_pty_callback(self._write_to_pty)
        self._terminal.set_device_attributes_callback(self._device_attributes)
        self._terminal.set_size_callback(self._size_report)

        # Render state — initial sync from terminal
        self._render = RenderState()
        self._render.update(self._terminal)

        # Key encoder
        self._key_encoder = KeyEncoder()
        self._key_event = KeyEvent()

        # PTY
        cell_w = int(self._cell_width)
        cell_h = int(self._cell_height)
        self._master_fd, self._child_pid = _spawn_shell(
            self._grid_cols,
            self._grid_rows,
            cell_w,
            cell_h,
        )
        flags = fcntl.fcntl(self._master_fd, fcntl.F_GETFL)
        fcntl.fcntl(self._master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        self._notifier = QSocketNotifier(self._master_fd, QSocketNotifier.Type.Read, self)
        self._notifier.activated.connect(self._on_pty_readable)

        # Blink timer
        self._blink_visible = True
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._on_blink)
        self._blink_timer.start(530)

        # FPS counter state. The timer keeps the overlay fresh even when the
        # terminal contents are otherwise idle.
        self._fps_frame_count = 0
        self._fps_last_update = time.monotonic()
        self._fps = 0.0
        self._fps_timer = QTimer(self)
        self._fps_timer.timeout.connect(self.update)
        self._fps_timer.start(250)

        # Widget config
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(400, 200)
        self._update_window_size()
        self._update_title()

    def _device_attributes(self) -> DeviceAttributes:
        return DeviceAttributes()

    def _size_report(self) -> SizeReport:
        return SizeReport(
            rows=self._grid_rows,
            columns=self._grid_cols,
            cell_width=int(self._cell_width),
            cell_height=int(self._cell_height),
        )

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
        snap = self._render.update(self._terminal)

        if snap.dirty != Dirty.CLEAN:
            self.update()

        self._update_title()

    def _write_to_pty(self, data: bytes) -> None:
        with suppress(OSError):
            os.write(self._master_fd, data)

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

        self._key_event.action = KeyAction.PRESS
        self._key_event.key = ghostty_key
        self._key_event.mods = mods

        self._key_event.consumed_mods = consumed

        # Set unshifted codepoint for Kitty keyboard protocol
        if unshifted_cp != "\0":
            self._key_event.unshifted_codepoint = ord(unshifted_cp)

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
            _set_pty_size(self._master_fd, new_cols, new_rows, cell_w, cell_h)
            self._render.update(self._terminal)

        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        now = time.monotonic()
        self._fps_frame_count += 1
        elapsed = now - self._fps_last_update
        if elapsed >= 1.0:
            self._fps = self._fps_frame_count / elapsed
            self._fps_frame_count = 0
            self._fps_last_update = now

        painter = QPainter(self)
        painter.setFont(self._font)

        with self._render.update(self._terminal) as snap:
            colors = snap.colors
            bg_color = colors.background
            fg_color = colors.foreground
            painter.fillRect(self.rect(), _qcolor(bg_color))

            cw = self._cell_width
            ch = self._cell_height
            ascent = QFontMetricsF(self._font).ascent()

            for row_idx, row in enumerate(snap.rows()):
                y = row_idx * ch
                for col_idx, cell in enumerate(row.cells()):
                    x = col_idx * cw

                    cell_fg = cell.fg or fg_color
                    cell_bg = cell.bg or bg_color

                    if cell.style.inverse:
                        cell_fg, cell_bg = cell_bg, cell_fg

                    if cell_bg != bg_color or cell.style.inverse:
                        painter.fillRect(
                            int(x), int(y), int(cw) + 1, int(ch), _qcolor(cell_bg)
                        )

                    if cell.text and cell.text != " ":
                        font = self._font
                        if cell.style.bold and cell.style.italic:
                            font = self._font_bold_italic
                        elif cell.style.bold:
                            font = self._font_bold
                        elif cell.style.italic:
                            font = self._font_italic
                        painter.setFont(font)
                        painter.setPen(_qcolor(cell_fg))
                        painter.drawText(int(x), int(y + ascent), cell.text)

                row.dirty = False

            cursor = snap.cursor
            if cursor is not None and cursor.visible and self._blink_visible:
                cursor_x = cursor.x * cw
                cursor_y = cursor.y * ch
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(_CURSOR_COLOR)

                if cursor.style == CursorStyle.BLOCK:
                    painter.setOpacity(0.7)
                    painter.drawRect(int(cursor_x), int(cursor_y), int(cw), int(ch))
                    painter.setOpacity(1.0)
                elif cursor.style == CursorStyle.BAR:
                    painter.drawRect(int(cursor_x), int(cursor_y), 2, int(ch))
                elif cursor.style == CursorStyle.UNDERLINE:
                    painter.drawRect(int(cursor_x), int(cursor_y + ch - 2), int(cw), 2)
                elif cursor.style == CursorStyle.BLOCK_HOLLOW:
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.setPen(_CURSOR_COLOR)
                    painter.drawRect(int(cursor_x), int(cursor_y), int(cw), int(ch))

            self._draw_kitty_images(painter)

            painter.setFont(self._font)
            painter.setPen(_FPS_COLOR)
            fps_text = f"{self._fps:.1f} FPS"
            fps_width = QFontMetricsF(self._font).horizontalAdvance(fps_text)
            painter.drawText(int(self.width() - fps_width - 8), int(ascent) + 8, fps_text)

        painter.end()

    def _draw_kitty_images(self, painter: QPainter) -> None:
        for placement in self._terminal.kitty_image_placements():
            qimage = self._kitty_qimage(placement.image)
            if qimage.isNull():
                continue

            source = qimage.copy(
                placement.source_x,
                placement.source_y,
                placement.source_width,
                placement.source_height,
            )
            painter.drawImage(
                int(placement.viewport_col * self._cell_width),
                int(placement.viewport_row * self._cell_height),
                source.scaled(
                    placement.pixel_width,
                    placement.pixel_height,
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                ),
            )

    def _kitty_qimage(self, image: KittyImage) -> QImage:
        data = image.data
        if image.compression == KittyImageCompression.ZLIB_DEFLATE:
            data = zlib.decompress(data)

        if image.format == KittyImageFormat.PNG:
            return QImage.fromData(data)
        if image.format == KittyImageFormat.RGBA:
            return QImage(
                data,
                image.width,
                image.height,
                image.width * 4,
                QImage.Format.Format_RGBA8888,
            ).copy()
        if image.format == KittyImageFormat.RGB:
            return QImage(
                data,
                image.width,
                image.height,
                image.width * 3,
                QImage.Format.Format_RGB888,
            ).copy()
        if image.format == KittyImageFormat.GRAY:
            return QImage(
                data,
                image.width,
                image.height,
                image.width,
                QImage.Format.Format_Grayscale8,
            ).copy()
        return QImage()

    def _on_blink(self) -> None:
        self._blink_visible = not self._blink_visible
        snap = self._render.update(self._terminal)
        if snap.cursor is not None and snap.cursor.visible:
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
        with suppress(OSError):
            os.close(self._master_fd)
        with suppress(OSError, ChildProcessError):
            os.kill(self._child_pid, signal.SIGTERM)
            os.waitpid(self._child_pid, os.WNOHANG)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Ghostling")

    widget = GhostlingWidget()
    widget.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
