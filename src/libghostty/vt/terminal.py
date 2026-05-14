"""Pythonic Terminal wrapper for libghostty-vt."""

from __future__ import annotations

from typing import TYPE_CHECKING

from libghostty._cffi import ffi, lib
from libghostty.vt.errors import GhosttyError, check_result

if TYPE_CHECKING:
    from cffi import FFI


class Terminal:
    """A complete terminal emulator instance.

    Manages screen, scrollback, cursor, styles, modes, and VT stream processing.
    """

    def __init__(
        self,
        cols: int = 80,
        rows: int = 24,
        max_scrollback: int = 10000,
    ) -> None:
        opts = ffi.new("GhosttyTerminalOptions *")
        opts.cols = cols
        opts.rows = rows
        opts.max_scrollback = max_scrollback

        handle = ffi.new("GhosttyTerminal *")
        check_result(lib.ghostty_terminal_new(ffi.NULL, handle, opts[0]))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_terminal_free(self._handle)
            self._handle = ffi.NULL

    @property
    def handle(self) -> FFI.CData:
        """Raw CFFI handle for advanced use."""
        return self._handle

    def reset(self) -> None:
        """Full reset (RIS) of all terminal state."""
        lib.ghostty_terminal_reset(self._handle)

    def resize(
        self,
        cols: int,
        rows: int,
        cell_width_px: int = 0,
        cell_height_px: int = 0,
    ) -> None:
        """Resize the terminal to the given dimensions."""
        check_result(
            lib.ghostty_terminal_resize(self._handle, cols, rows, cell_width_px, cell_height_px)
        )

    def write(self, data: bytes | str) -> None:
        """Write VT-encoded data to the terminal for processing."""
        if isinstance(data, str):
            data = data.encode("utf-8")
        lib.ghostty_terminal_vt_write(self._handle, data, len(data))

    @property
    def cols(self) -> int:
        """Terminal width in cells."""
        out = ffi.new("uint16_t *")
        check_result(lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_COLS, out))
        return out[0]

    @property
    def rows(self) -> int:
        """Terminal height in cells."""
        out = ffi.new("uint16_t *")
        check_result(lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_ROWS, out))
        return out[0]

    @property
    def cursor_x(self) -> int:
        """Cursor column position (0-indexed)."""
        out = ffi.new("uint16_t *")
        check_result(
            lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_CURSOR_X, out)
        )
        return out[0]

    @property
    def cursor_y(self) -> int:
        """Cursor row position within the active area (0-indexed)."""
        out = ffi.new("uint16_t *")
        check_result(
            lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_CURSOR_Y, out)
        )
        return out[0]

    @property
    def cursor_visible(self) -> bool:
        """Whether the cursor is visible (DEC mode 25)."""
        out = ffi.new("bool *")
        check_result(
            lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_CURSOR_VISIBLE, out)
        )
        return bool(out[0])

    @property
    def title(self) -> str:
        """Terminal title as set by escape sequences."""
        out = ffi.new("GhosttyString *")
        check_result(lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_TITLE, out))
        if out.len == 0:
            return ""
        return ffi.buffer(out.ptr, out.len)[:].decode("utf-8")

    @property
    def active_screen(self) -> str:
        """Active screen: 'primary' or 'alternate'."""
        out = ffi.new("GhosttyTerminalScreen *")
        check_result(
            lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_ACTIVE_SCREEN, out)
        )
        if out[0] == lib.GHOSTTY_TERMINAL_SCREEN_ALTERNATE:
            return "alternate"
        return "primary"

    @property
    def total_rows(self) -> int:
        """Total rows including scrollback."""
        out = ffi.new("size_t *")
        check_result(
            lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_TOTAL_ROWS, out)
        )
        return out[0]

    @property
    def scrollback_rows(self) -> int:
        """Number of scrollback rows."""
        out = ffi.new("size_t *")
        check_result(
            lib.ghostty_terminal_get(self._handle, lib.GHOSTTY_TERMINAL_DATA_SCROLLBACK_ROWS, out)
        )
        return out[0]

    def format_screen(self, fmt: str = "plain", trim: bool = True) -> str:
        """Format the current screen contents.

        Args:
            fmt: Output format - 'plain', 'vt', or 'html'.
            trim: Whether to trim trailing whitespace.

        Returns:
            The formatted screen content as a string.
        """
        format_map = {
            "plain": lib.GHOSTTY_FORMATTER_FORMAT_PLAIN,
            "vt": lib.GHOSTTY_FORMATTER_FORMAT_VT,
            "html": lib.GHOSTTY_FORMATTER_FORMAT_HTML,
        }
        emit = format_map[fmt]

        opts = ffi.new("GhosttyFormatterTerminalOptions *")
        opts.size = ffi.sizeof("GhosttyFormatterTerminalOptions")
        opts.emit = emit
        opts.trim = trim
        opts.selection = ffi.NULL

        formatter = ffi.new("GhosttyFormatter *")
        check_result(lib.ghostty_formatter_terminal_new(ffi.NULL, formatter, self._handle, opts[0]))
        try:
            out_ptr = ffi.new("uint8_t **")
            out_len = ffi.new("size_t *")
            check_result(
                lib.ghostty_formatter_format_alloc(formatter[0], ffi.NULL, out_ptr, out_len)
            )
            try:
                return ffi.buffer(out_ptr[0], out_len[0])[:].decode("utf-8")
            finally:
                lib.ghostty_free(ffi.NULL, out_ptr[0], out_len[0])
        finally:
            lib.ghostty_formatter_free(formatter[0])

    def mode_get(self, mode: int) -> bool:
        """Get the value of a terminal mode."""
        out = ffi.new("bool *")
        check_result(lib.ghostty_terminal_mode_get(self._handle, mode, out))
        return bool(out[0])

    def mode_set(self, mode: int, value: bool) -> None:
        """Set a terminal mode value."""
        check_result(lib.ghostty_terminal_mode_set(self._handle, mode, value))

    def scroll_top(self) -> None:
        """Scroll viewport to the top of scrollback."""
        sv = ffi.new("GhosttyTerminalScrollViewport *")
        sv.tag = lib.GHOSTTY_SCROLL_VIEWPORT_TOP
        lib.ghostty_terminal_scroll_viewport(self._handle, sv[0])

    def scroll_bottom(self) -> None:
        """Scroll viewport to the bottom (active area)."""
        sv = ffi.new("GhosttyTerminalScrollViewport *")
        sv.tag = lib.GHOSTTY_SCROLL_VIEWPORT_BOTTOM
        lib.ghostty_terminal_scroll_viewport(self._handle, sv[0])

    def scroll_delta(self, delta: int) -> None:
        """Scroll viewport by a delta (negative = up, positive = down)."""
        sv = ffi.new("GhosttyTerminalScrollViewport *")
        sv.tag = lib.GHOSTTY_SCROLL_VIEWPORT_DELTA
        sv.value.delta = delta
        lib.ghostty_terminal_scroll_viewport(self._handle, sv[0])

    def get_foreground_color(self) -> tuple[int, int, int] | None:
        """Get effective foreground color as (r, g, b) or None if unset."""
        out = ffi.new("GhosttyColorRgb *")
        result = lib.ghostty_terminal_get(
            self._handle, lib.GHOSTTY_TERMINAL_DATA_COLOR_FOREGROUND, out
        )
        if result == GhosttyError.NO_VALUE:
            return None
        check_result(result)
        return (out.r, out.g, out.b)

    def get_background_color(self) -> tuple[int, int, int] | None:
        """Get effective background color as (r, g, b) or None if unset."""
        out = ffi.new("GhosttyColorRgb *")
        result = lib.ghostty_terminal_get(
            self._handle, lib.GHOSTTY_TERMINAL_DATA_COLOR_BACKGROUND, out
        )
        if result == GhosttyError.NO_VALUE:
            return None
        check_result(result)
        return (out.r, out.g, out.b)

    def set_foreground_color(self, r: int, g: int, b: int) -> None:
        """Set the default foreground color."""
        color = ffi.new("GhosttyColorRgb *", {"r": r, "g": g, "b": b})
        check_result(
            lib.ghostty_terminal_set(self._handle, lib.GHOSTTY_TERMINAL_OPT_COLOR_FOREGROUND, color)
        )

    def set_background_color(self, r: int, g: int, b: int) -> None:
        """Set the default background color."""
        color = ffi.new("GhosttyColorRgb *", {"r": r, "g": g, "b": b})
        check_result(
            lib.ghostty_terminal_set(self._handle, lib.GHOSTTY_TERMINAL_OPT_COLOR_BACKGROUND, color)
        )

    def get_kitty_image_storage_limit(self) -> int | None:
        """Get the active screen's Kitty graphics image storage limit in bytes."""
        out = ffi.new("uint64_t *")
        result = lib.ghostty_terminal_get(
            self._handle,
            lib.GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_STORAGE_LIMIT,
            out,
        )
        if result == GhosttyError.NO_VALUE:
            return None
        check_result(result)
        return int(out[0])

    @property
    def kitty_image_storage_limit(self) -> int | None:
        """Active screen's Kitty graphics image storage limit in bytes."""
        return self.get_kitty_image_storage_limit()

    @kitty_image_storage_limit.setter
    def kitty_image_storage_limit(self, limit_bytes: int) -> None:
        self.set_kitty_image_storage_limit(limit_bytes)

    def is_kitty_image_from_file_allowed(self) -> bool | None:
        """Return whether Kitty graphics may load images from regular files."""
        out = ffi.new("bool *")
        result = lib.ghostty_terminal_get(
            self._handle,
            lib.GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_FILE,
            out,
        )
        if result == GhosttyError.NO_VALUE:
            return None
        check_result(result)
        return bool(out[0])

    @property
    def kitty_image_from_file_allowed(self) -> bool | None:
        """Whether Kitty graphics may load images from regular files."""
        return self.is_kitty_image_from_file_allowed()

    @kitty_image_from_file_allowed.setter
    def kitty_image_from_file_allowed(self, allowed: bool) -> None:
        self.set_kitty_image_from_file_allowed(allowed)

    def is_kitty_image_from_temp_file_allowed(self) -> bool | None:
        """Return whether Kitty graphics may load images from temporary files."""
        out = ffi.new("bool *")
        result = lib.ghostty_terminal_get(
            self._handle,
            lib.GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_TEMP_FILE,
            out,
        )
        if result == GhosttyError.NO_VALUE:
            return None
        check_result(result)
        return bool(out[0])

    @property
    def kitty_image_from_temp_file_allowed(self) -> bool | None:
        """Whether Kitty graphics may load images from temporary files."""
        return self.is_kitty_image_from_temp_file_allowed()

    @kitty_image_from_temp_file_allowed.setter
    def kitty_image_from_temp_file_allowed(self, allowed: bool) -> None:
        self.set_kitty_image_from_temp_file_allowed(allowed)

    def is_kitty_image_from_shared_memory_allowed(self) -> bool | None:
        """Return whether Kitty graphics may load images from shared memory."""
        out = ffi.new("bool *")
        result = lib.ghostty_terminal_get(
            self._handle,
            lib.GHOSTTY_TERMINAL_DATA_KITTY_IMAGE_MEDIUM_SHARED_MEM,
            out,
        )
        if result == GhosttyError.NO_VALUE:
            return None
        check_result(result)
        return bool(out[0])

    @property
    def kitty_image_from_shared_memory_allowed(self) -> bool | None:
        """Whether Kitty graphics may load images from shared memory."""
        return self.is_kitty_image_from_shared_memory_allowed()

    @kitty_image_from_shared_memory_allowed.setter
    def kitty_image_from_shared_memory_allowed(self, allowed: bool) -> None:
        self.set_kitty_image_from_shared_memory_allowed(allowed)

    def set_kitty_image_storage_limit(self, limit_bytes: int) -> None:
        """Set the maximum bytes available for Kitty graphics image storage.

        A limit of zero disables the Kitty graphics protocol and clears stored images.
        """
        limit = ffi.new("uint64_t *", limit_bytes)
        check_result(
            lib.ghostty_terminal_set(
                self._handle,
                lib.GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_STORAGE_LIMIT,
                limit,
            )
        )

    def set_kitty_image_from_file_allowed(self, allowed: bool) -> None:
        """Enable or disable Kitty graphics image loading from regular files."""
        value = ffi.new("bool *", allowed)
        check_result(
            lib.ghostty_terminal_set(
                self._handle,
                lib.GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_FILE,
                value,
            )
        )

    def set_kitty_image_from_temp_file_allowed(self, allowed: bool) -> None:
        """Enable or disable Kitty graphics image loading from temporary files."""
        value = ffi.new("bool *", allowed)
        check_result(
            lib.ghostty_terminal_set(
                self._handle,
                lib.GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_TEMP_FILE,
                value,
            )
        )

    def set_kitty_image_from_shared_memory_allowed(self, allowed: bool) -> None:
        """Enable or disable Kitty graphics image loading from shared memory."""
        value = ffi.new("bool *", allowed)
        check_result(
            lib.ghostty_terminal_set(
                self._handle,
                lib.GHOSTTY_TERMINAL_OPT_KITTY_IMAGE_MEDIUM_SHARED_MEM,
                value,
            )
        )

    def configure_kitty_graphics(
        self,
        *,
        storage_limit_bytes: int | None = None,
        allow_file: bool | None = None,
        allow_temp_file: bool | None = None,
        allow_shared_memory: bool | None = None,
    ) -> None:
        """Configure Kitty graphics options in one call.

        Omitted options are left unchanged. Set ``storage_limit_bytes`` to zero to
        disable Kitty graphics and clear stored images.
        """
        if storage_limit_bytes is not None:
            self.set_kitty_image_storage_limit(storage_limit_bytes)
        if allow_file is not None:
            self.set_kitty_image_from_file_allowed(allow_file)
        if allow_temp_file is not None:
            self.set_kitty_image_from_temp_file_allowed(allow_temp_file)
        if allow_shared_memory is not None:
            self.set_kitty_image_from_shared_memory_allowed(allow_shared_memory)
