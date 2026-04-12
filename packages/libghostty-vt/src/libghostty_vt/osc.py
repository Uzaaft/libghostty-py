"""OSC (Operating System Command) parser."""

from __future__ import annotations

from typing import TYPE_CHECKING

from libghostty_cffi import ffi, lib

from libghostty_vt.errors import check_result

if TYPE_CHECKING:
    from cffi import FFI


class OscParser:
    """Parse OSC (Operating System Command) sequences.

    The parser operates in a streaming fashion, processing input byte-by-byte.
    """

    def __init__(self) -> None:
        handle = ffi.new("GhosttyOscParser *")
        check_result(lib.ghostty_osc_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_osc_free(self._handle)
            self._handle = ffi.NULL

    def reset(self) -> None:
        """Reset the parser to its initial state."""
        lib.ghostty_osc_reset(self._handle)

    def feed(self, data: bytes) -> None:
        """Feed bytes to the parser."""
        for byte in data:
            lib.ghostty_osc_next(self._handle, byte)

    def end(self, terminator: int = 0x07) -> OscCommand:
        """Finalize parsing and retrieve the parsed command.

        Args:
            terminator: The terminating byte (0x07 for BEL, 0x5C for ST).

        Returns:
            The parsed OSC command.
        """
        cmd = lib.ghostty_osc_end(self._handle, terminator)
        return OscCommand(cmd)


class OscCommand:
    """A parsed OSC command."""

    def __init__(self, handle: FFI.CData) -> None:
        self._handle: FFI.CData = handle

    @property
    def command_type(self) -> int:
        """The command type identifier."""
        return lib.ghostty_osc_command_type(self._handle)

    @property
    def is_valid(self) -> bool:
        """Whether this is a valid (non-INVALID) command."""
        return self.command_type != lib.GHOSTTY_OSC_COMMAND_INVALID

    @property
    def window_title(self) -> str | None:
        """Extract window title if this is a title change command."""
        if self.command_type != lib.GHOSTTY_OSC_COMMAND_CHANGE_WINDOW_TITLE:
            return None
        out = ffi.new("const char **")
        if lib.ghostty_osc_command_data(
            self._handle, lib.GHOSTTY_OSC_DATA_CHANGE_WINDOW_TITLE_STR, out
        ):
            return ffi.string(out[0]).decode("utf-8")
        return None
