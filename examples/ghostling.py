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
from typing import TYPE_CHECKING, NamedTuple

from PyQt6.QtCore import QSocketNotifier, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QFontMetricsF, QImage, QKeyEvent, QPainter, QResizeEvent
from PyQt6.QtWidgets import QApplication, QWidget

from libghostty.vt import (
    Cell,
    Color,
    CursorInfo,
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
    Snapshot,
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


class TerminalGeometry(NamedTuple):
    cols: int
    rows: int
    cell_width_px: int
    cell_height_px: int


class FontSet(NamedTuple):
    normal: QFont
    bold: QFont
    italic: QFont
    bold_italic: QFont
    by_style: dict[tuple[bool, bool], QFont]
    cell_width: float
    cell_height: float

    @classmethod
    def monospace(cls, point_size: int) -> FontSet:
        normal = QFont("monospace", point_size)
        normal.setStyleHint(QFont.StyleHint.Monospace)
        bold = QFont(normal)
        bold.setBold(True)
        italic = QFont(normal)
        italic.setItalic(True)
        bold_italic = QFont(normal)
        bold_italic.setBold(True)
        bold_italic.setItalic(True)
        metrics = QFontMetricsF(normal)
        return cls(
            normal=normal,
            bold=bold,
            italic=italic,
            bold_italic=bold_italic,
            by_style={
                (False, False): normal,
                (True, False): bold,
                (False, True): italic,
                (True, True): bold_italic,
            },
            cell_width=metrics.horizontalAdvance("M"),
            cell_height=metrics.height(),
        )


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


def _set_pty_size(
    fd: int,
    geometry: TerminalGeometry,
) -> None:
    width_px = geometry.cols * geometry.cell_width_px
    height_px = geometry.rows * geometry.cell_height_px
    winsize = struct.pack("HHHH", geometry.rows, geometry.cols, width_px, height_px)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


class PtySession:
    """A shell process connected to a non-blocking PTY."""

    def __init__(self, geometry: TerminalGeometry) -> None:
        child_pid, master_fd = pty.fork()
        if child_pid == 0:
            shell = os.environ.get("SHELL", "/bin/sh")
            env = os.environ.copy()
            env["TERM"] = "xterm-256color"
            env["COLORTERM"] = "truecolor"
            os.execvpe(shell, [shell], env)

        self.fd = master_fd
        self._child_pid = child_pid
        self.resize(geometry)
        flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def read(self) -> bytes:
        return os.read(self.fd, 65536)

    def write(self, data: bytes) -> None:
        with suppress(OSError):
            os.write(self.fd, data)

    def resize(self, geometry: TerminalGeometry) -> None:
        _set_pty_size(self.fd, geometry)

    def close(self) -> None:
        with suppress(OSError):
            os.close(self.fd)
        with suppress(OSError, ChildProcessError):
            os.kill(self._child_pid, signal.SIGTERM)
            os.waitpid(self._child_pid, os.WNOHANG)


class QtKeyEncoder:
    """Encode Qt key events into terminal input bytes."""

    def __init__(self) -> None:
        self._encoder = KeyEncoder()
        self._event = KeyEvent()

    def encode(self, event: QKeyEvent, terminal: Terminal) -> bytes:
        entry = _QT_KEY_LOOKUP.get(event.key())
        if entry is None:
            return event.text().encode("utf-8")

        ghostty_key, unshifted_cp = entry
        mods = _qt_mods_to_ghostty(event.modifiers())
        self._encoder.sync_from_terminal(terminal)
        self._event.action = KeyAction.PRESS
        self._event.key = ghostty_key
        self._event.mods = mods
        self._event.consumed_mods = _consumed_mods(unshifted_cp, mods)

        if unshifted_cp != "\0":
            self._event.unshifted_codepoint = ord(unshifted_cp)

        text = event.text()
        self._event.set_utf8(text if text and ord(text[0]) >= 0x20 else "")
        return self._encoder.encode(self._event) or text.encode("utf-8")


def _consumed_mods(unshifted_cp: str, mods: int) -> int:
    if unshifted_cp != "\0" and (mods & _MODS_SHIFT):
        return _MODS_SHIFT
    return 0


@cache
def _qcolor(color: Color) -> QColor:
    return QColor(color.r, color.g, color.b)


_DEFAULT_BG = QColor(30, 30, 46)
_DEFAULT_FG = QColor(205, 214, 244)
_CURSOR_COLOR = QColor(245, 194, 231)
_FPS_COLOR = QColor(250, 250, 0)
_QIMAGE_RAW_FORMATS: dict[KittyImageFormat, tuple[int, QImage.Format]] = {
    KittyImageFormat.RGBA: (4, QImage.Format.Format_RGBA8888),
    KittyImageFormat.RGB: (3, QImage.Format.Format_RGB888),
    KittyImageFormat.GRAY: (1, QImage.Format.Format_Grayscale8),
}


def _kitty_qimage(image: KittyImage) -> QImage:
    data = image.data
    if image.compression == KittyImageCompression.ZLIB_DEFLATE:
        data = zlib.decompress(data)

    if image.format == KittyImageFormat.PNG:
        return QImage.fromData(data)

    if raw_format := _QIMAGE_RAW_FORMATS.get(image.format):
        bytes_per_pixel, qimage_format = raw_format
        return QImage(
            data,
            image.width,
            image.height,
            image.width * bytes_per_pixel,
            qimage_format,
        ).copy()

    return QImage()


class GhostlingWidget(QWidget):
    """A PyQt6 terminal emulator widget powered by libghostty-vt."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._fonts = FontSet.monospace(13)
        self._cell_width = self._fonts.cell_width
        self._cell_height = self._fonts.cell_height

        # Initial grid size
        self._grid_cols = 80
        self._grid_rows = 24

        self._terminal = self._create_terminal()

        # Render state — initial sync from terminal
        self._render = RenderState()
        self._render.update(self._terminal)

        self._key_encoder = QtKeyEncoder()

        self._pty = PtySession(self._geometry)

        self._notifier = QSocketNotifier(self._pty.fd, QSocketNotifier.Type.Read, self)
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

    @property
    def _cell_width_px(self) -> int:
        return int(self._cell_width)

    @property
    def _cell_height_px(self) -> int:
        return int(self._cell_height)

    @property
    def _geometry(self) -> TerminalGeometry:
        return TerminalGeometry(
            cols=self._grid_cols,
            rows=self._grid_rows,
            cell_width_px=self._cell_width_px,
            cell_height_px=self._cell_height_px,
        )

    def _device_attributes(self) -> DeviceAttributes:
        return DeviceAttributes()

    def _create_terminal(self) -> Terminal:
        terminal = Terminal(
            cols=self._grid_cols,
            rows=self._grid_rows,
            max_scrollback=10000,
        )
        terminal.set_background_color(_DEFAULT_BG.red(), _DEFAULT_BG.green(), _DEFAULT_BG.blue())
        terminal.set_foreground_color(_DEFAULT_FG.red(), _DEFAULT_FG.green(), _DEFAULT_FG.blue())
        terminal.set_kitty_image_storage_limit(64 * 1024 * 1024)
        terminal.resize(
            self._geometry.cols,
            self._geometry.rows,
            self._geometry.cell_width_px,
            self._geometry.cell_height_px,
        )
        terminal.set_write_pty_callback(self._write_to_pty)
        terminal.set_device_attributes_callback(self._device_attributes)
        terminal.set_size_callback(self._size_report)
        return terminal

    def _size_report(self) -> SizeReport:
        return SizeReport(
            rows=self._grid_rows,
            columns=self._grid_cols,
            cell_width=self._cell_width_px,
            cell_height=self._cell_height_px,
        )

    def _on_pty_readable(self) -> None:
        try:
            data = self._pty.read()
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
        self._pty.write(data)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if encoded := self._key_encoder.encode(event, self._terminal):
            self._write_to_pty(encoded)
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        event.accept()

    def resizeEvent(self, event: QResizeEvent) -> None:
        new_cols = max(1, int(event.size().width() / self._cell_width))
        new_rows = max(1, int(event.size().height() / self._cell_height))

        if new_cols != self._grid_cols or new_rows != self._grid_rows:
            self._grid_cols = new_cols
            self._grid_rows = new_rows
            self._terminal.resize(
                self._geometry.cols,
                self._geometry.rows,
                self._geometry.cell_width_px,
                self._geometry.cell_height_px,
            )
            self._pty.resize(self._geometry)
            self._render.update(self._terminal)

        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        self._update_fps()

        painter = QPainter(self)
        painter.setFont(self._fonts.normal)

        with self._render.update(self._terminal) as snap:
            painter.fillRect(self.rect(), _qcolor(snap.colors.background))
            self._draw_cells(painter, snap)
            self._draw_cursor(painter, snap.cursor)
            self._draw_kitty_images(painter)
            self._draw_fps(painter)

        painter.end()

    def _update_fps(self) -> None:
        now = time.monotonic()
        self._fps_frame_count += 1
        elapsed = now - self._fps_last_update
        if elapsed >= 1.0:
            self._fps = self._fps_frame_count / elapsed
            self._fps_frame_count = 0
            self._fps_last_update = now

    def _draw_cells(self, painter: QPainter, snap: Snapshot) -> None:
        foreground = snap.colors.foreground
        background = snap.colors.background
        ascent = QFontMetricsF(self._fonts.normal).ascent()

        for row_idx, row in enumerate(snap.rows()):
            y = row_idx * self._cell_height
            for col_idx, cell in enumerate(row.cells()):
                x = col_idx * self._cell_width
                cell_fg = cell.fg or foreground
                cell_bg = cell.bg or background

                if cell.style.inverse:
                    cell_fg, cell_bg = cell_bg, cell_fg

                if cell_bg != background or cell.style.inverse:
                    painter.fillRect(
                        int(x),
                        int(y),
                        self._cell_width_px + 1,
                        self._cell_height_px,
                        _qcolor(cell_bg),
                    )

                if cell.text and cell.text != " ":
                    painter.setFont(self._font_for_cell(cell))
                    painter.setPen(_qcolor(cell_fg))
                    painter.drawText(int(x), int(y + ascent), cell.text)

            row.dirty = False

    def _font_for_cell(self, cell: Cell) -> QFont:
        return self._fonts.by_style[(cell.style.bold, cell.style.italic)]

    def _draw_cursor(self, painter: QPainter, cursor: CursorInfo | None) -> None:
        if cursor is None or not cursor.visible or not self._blink_visible:
            return

        cursor_x = cursor.x * self._cell_width
        cursor_y = cursor.y * self._cell_height
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(_CURSOR_COLOR)

        if cursor.style == CursorStyle.BLOCK:
            painter.setOpacity(0.7)
            painter.drawRect(
                int(cursor_x),
                int(cursor_y),
                self._cell_width_px,
                self._cell_height_px,
            )
            painter.setOpacity(1.0)
        elif cursor.style == CursorStyle.BAR:
            painter.drawRect(int(cursor_x), int(cursor_y), 2, self._cell_height_px)
        elif cursor.style == CursorStyle.UNDERLINE:
            painter.drawRect(
                int(cursor_x),
                int(cursor_y + self._cell_height - 2),
                self._cell_width_px,
                2,
            )
        elif cursor.style == CursorStyle.BLOCK_HOLLOW:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(_CURSOR_COLOR)
            painter.drawRect(
                int(cursor_x),
                int(cursor_y),
                self._cell_width_px,
                self._cell_height_px,
            )

    def _draw_fps(self, painter: QPainter) -> None:
        painter.setFont(self._fonts.normal)
        painter.setPen(_FPS_COLOR)
        fps_text = f"{self._fps:.1f} FPS"
        metrics = QFontMetricsF(self._fonts.normal)
        fps_width = metrics.horizontalAdvance(fps_text)
        painter.drawText(int(self.width() - fps_width - 8), int(metrics.ascent()) + 8, fps_text)

    def _draw_kitty_images(self, painter: QPainter) -> None:
        for placement in self._terminal.kitty_image_placements():
            qimage = _kitty_qimage(placement.image)
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
        self._pty.close()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Ghostling")

    widget = GhostlingWidget()
    widget.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
