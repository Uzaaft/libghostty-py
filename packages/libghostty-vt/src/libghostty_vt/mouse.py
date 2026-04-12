"""Mouse event creation and encoding."""

from __future__ import annotations

from typing import TYPE_CHECKING

from libghostty_cffi import ffi, lib
from libghostty_vt.errors import check_result


if TYPE_CHECKING:
    from cffi import FFI

    from libghostty_vt.terminal import Terminal


class MouseEvent:
    """A mouse input event."""

    def __init__(self) -> None:
        handle = ffi.new("GhosttyMouseEvent *")
        check_result(lib.ghostty_mouse_event_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_mouse_event_free(self._handle)
            self._handle = ffi.NULL

    @property
    def handle(self) -> FFI.CData:
        return self._handle

    @property
    def action(self) -> int:
        return lib.ghostty_mouse_event_get_action(self._handle)

    @action.setter
    def action(self, value: int) -> None:
        lib.ghostty_mouse_event_set_action(self._handle, value)

    @property
    def mods(self) -> int:
        return lib.ghostty_mouse_event_get_mods(self._handle)

    @mods.setter
    def mods(self, value: int) -> None:
        lib.ghostty_mouse_event_set_mods(self._handle, value)

    def set_button(self, button: int) -> None:
        """Set the mouse button."""
        lib.ghostty_mouse_event_set_button(self._handle, button)

    def clear_button(self) -> None:
        """Clear the mouse button (for motion events)."""
        lib.ghostty_mouse_event_clear_button(self._handle)

    def set_position(self, x: float, y: float) -> None:
        """Set position in surface-space pixels."""
        pos = ffi.new("GhosttyMousePosition *", {"x": x, "y": y})
        lib.ghostty_mouse_event_set_position(self._handle, pos[0])

    def get_position(self) -> tuple[float, float]:
        """Get position in surface-space pixels."""
        pos = lib.ghostty_mouse_event_get_position(self._handle)
        return (pos.x, pos.y)


class MouseEncoder:
    """Encode mouse events into terminal escape sequences."""

    def __init__(self) -> None:
        handle = ffi.new("GhosttyMouseEncoder *")
        check_result(lib.ghostty_mouse_encoder_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_mouse_encoder_free(self._handle)
            self._handle = ffi.NULL

    def sync_from_terminal(self, terminal: Terminal) -> None:
        """Set encoder options from the terminal's current state."""
        lib.ghostty_mouse_encoder_setopt_from_terminal(self._handle, terminal.handle)

    def reset(self) -> None:
        """Reset internal state (clears motion deduplication)."""
        lib.ghostty_mouse_encoder_reset(self._handle)

    def encode(self, event: MouseEvent, buf_size: int = 128) -> bytes:
        """Encode a mouse event into an escape sequence.

        Returns:
            The encoded bytes (empty if the event produces no output).
        """
        buf = ffi.new("char[]", buf_size)
        out_len = ffi.new("size_t *")
        result = lib.ghostty_mouse_encoder_encode(
            self._handle, event.handle, buf, buf_size, out_len
        )
        if result == -3:  # OUT_OF_SPACE
            buf = ffi.new("char[]", out_len[0])
            check_result(
                lib.ghostty_mouse_encoder_encode(
                    self._handle, event.handle, buf, out_len[0], out_len
                )
            )
        else:
            check_result(result)
        return ffi.buffer(buf, out_len[0])[:]
