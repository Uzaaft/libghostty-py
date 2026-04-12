"""Paste validation and encoding utilities."""

from __future__ import annotations

from libghostty_cffi import ffi, lib

from libghostty_vt.errors import check_result


def is_safe(data: bytes | str) -> bool:
    """Check if paste data is safe to send to the terminal.

    Data is considered unsafe if it contains newlines or the bracketed paste
    end sequence, which could inject commands.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return bool(lib.ghostty_paste_is_safe(data, len(data)))


def encode(data: bytes | str, bracketed: bool = False) -> bytes:
    """Encode paste data for writing to the terminal pty.

    Strips unsafe control bytes and optionally wraps in bracketed paste
    sequences.

    Args:
        data: The paste data to encode.
        bracketed: Whether bracketed paste mode is active.

    Returns:
        Encoded paste data ready for the pty.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    # Make a mutable copy since the C function modifies in place
    buf_in = ffi.new("char[]", data)
    out_written = ffi.new("size_t *")

    # Query required size
    result = lib.ghostty_paste_encode(buf_in, len(data), bracketed, ffi.NULL, 0, out_written)
    if result == 0 and out_written[0] == 0:
        return b""

    required = out_written[0]
    buf_out = ffi.new("char[]", required)
    # Re-create input since the first call may have modified it
    buf_in = ffi.new("char[]", data)
    check_result(
        lib.ghostty_paste_encode(buf_in, len(data), bracketed, buf_out, required, out_written)
    )
    return ffi.buffer(buf_out, out_written[0])[:]
