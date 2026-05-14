"""Key event creation and encoding."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from libghostty_vt._cffi import ffi, lib
from libghostty_vt.errors import GhosttyError, check_result

if TYPE_CHECKING:
    from cffi import FFI

    from libghostty_vt.terminal import Terminal


class KittyKeyFlags(enum.IntFlag):
    """Kitty keyboard protocol flags used by the key encoder."""

    DISABLED = 0x00
    DISAMBIGUATE = 0x01
    REPORT_EVENTS = 0x02
    REPORT_ALTERNATES = 0x04
    REPORT_ALL = 0x08
    REPORT_ASSOCIATED = 0x10
    ALL = 0x1F


class KeyAction(enum.IntEnum):
    """Keyboard event action values."""

    PRESS = lib.GHOSTTY_KEY_ACTION_PRESS
    RELEASE = lib.GHOSTTY_KEY_ACTION_RELEASE
    REPEAT = lib.GHOSTTY_KEY_ACTION_REPEAT


class Key(enum.IntEnum):
    """Keyboard keys understood by libghostty-vt."""

    A = lib.GHOSTTY_KEY_A
    ALT_LEFT = lib.GHOSTTY_KEY_ALT_LEFT
    ALT_RIGHT = lib.GHOSTTY_KEY_ALT_RIGHT
    ARROW_DOWN = lib.GHOSTTY_KEY_ARROW_DOWN
    ARROW_LEFT = lib.GHOSTTY_KEY_ARROW_LEFT
    ARROW_RIGHT = lib.GHOSTTY_KEY_ARROW_RIGHT
    ARROW_UP = lib.GHOSTTY_KEY_ARROW_UP
    B = lib.GHOSTTY_KEY_B
    BACKQUOTE = lib.GHOSTTY_KEY_BACKQUOTE
    BACKSLASH = lib.GHOSTTY_KEY_BACKSLASH
    BACKSPACE = lib.GHOSTTY_KEY_BACKSPACE
    BRACKET_LEFT = lib.GHOSTTY_KEY_BRACKET_LEFT
    BRACKET_RIGHT = lib.GHOSTTY_KEY_BRACKET_RIGHT
    C = lib.GHOSTTY_KEY_C
    CAPS_LOCK = lib.GHOSTTY_KEY_CAPS_LOCK
    COMMA = lib.GHOSTTY_KEY_COMMA
    CONTEXT_MENU = lib.GHOSTTY_KEY_CONTEXT_MENU
    CONTROL_LEFT = lib.GHOSTTY_KEY_CONTROL_LEFT
    CONTROL_RIGHT = lib.GHOSTTY_KEY_CONTROL_RIGHT
    CONVERT = lib.GHOSTTY_KEY_CONVERT
    D = lib.GHOSTTY_KEY_D
    DELETE = lib.GHOSTTY_KEY_DELETE
    DIGIT_0 = lib.GHOSTTY_KEY_DIGIT_0
    DIGIT_1 = lib.GHOSTTY_KEY_DIGIT_1
    DIGIT_2 = lib.GHOSTTY_KEY_DIGIT_2
    DIGIT_3 = lib.GHOSTTY_KEY_DIGIT_3
    DIGIT_4 = lib.GHOSTTY_KEY_DIGIT_4
    DIGIT_5 = lib.GHOSTTY_KEY_DIGIT_5
    DIGIT_6 = lib.GHOSTTY_KEY_DIGIT_6
    DIGIT_7 = lib.GHOSTTY_KEY_DIGIT_7
    DIGIT_8 = lib.GHOSTTY_KEY_DIGIT_8
    DIGIT_9 = lib.GHOSTTY_KEY_DIGIT_9
    E = lib.GHOSTTY_KEY_E
    END = lib.GHOSTTY_KEY_END
    ENTER = lib.GHOSTTY_KEY_ENTER
    EQUAL = lib.GHOSTTY_KEY_EQUAL
    ESCAPE = lib.GHOSTTY_KEY_ESCAPE
    F = lib.GHOSTTY_KEY_F
    F1 = lib.GHOSTTY_KEY_F1
    F10 = lib.GHOSTTY_KEY_F10
    F11 = lib.GHOSTTY_KEY_F11
    F12 = lib.GHOSTTY_KEY_F12
    F2 = lib.GHOSTTY_KEY_F2
    F3 = lib.GHOSTTY_KEY_F3
    F4 = lib.GHOSTTY_KEY_F4
    F5 = lib.GHOSTTY_KEY_F5
    F6 = lib.GHOSTTY_KEY_F6
    F7 = lib.GHOSTTY_KEY_F7
    F8 = lib.GHOSTTY_KEY_F8
    F9 = lib.GHOSTTY_KEY_F9
    G = lib.GHOSTTY_KEY_G
    H = lib.GHOSTTY_KEY_H
    HELP = lib.GHOSTTY_KEY_HELP
    HOME = lib.GHOSTTY_KEY_HOME
    I = lib.GHOSTTY_KEY_I  # noqa: E741
    INSERT = lib.GHOSTTY_KEY_INSERT
    INTL_BACKSLASH = lib.GHOSTTY_KEY_INTL_BACKSLASH
    INTL_RO = lib.GHOSTTY_KEY_INTL_RO
    INTL_YEN = lib.GHOSTTY_KEY_INTL_YEN
    J = lib.GHOSTTY_KEY_J
    K = lib.GHOSTTY_KEY_K
    KANA_MODE = lib.GHOSTTY_KEY_KANA_MODE
    L = lib.GHOSTTY_KEY_L
    M = lib.GHOSTTY_KEY_M
    META_LEFT = lib.GHOSTTY_KEY_META_LEFT
    META_RIGHT = lib.GHOSTTY_KEY_META_RIGHT
    MINUS = lib.GHOSTTY_KEY_MINUS
    N = lib.GHOSTTY_KEY_N
    NON_CONVERT = lib.GHOSTTY_KEY_NON_CONVERT
    NUMPAD_0 = lib.GHOSTTY_KEY_NUMPAD_0
    NUMPAD_1 = lib.GHOSTTY_KEY_NUMPAD_1
    NUMPAD_2 = lib.GHOSTTY_KEY_NUMPAD_2
    NUMPAD_3 = lib.GHOSTTY_KEY_NUMPAD_3
    NUMPAD_4 = lib.GHOSTTY_KEY_NUMPAD_4
    NUMPAD_5 = lib.GHOSTTY_KEY_NUMPAD_5
    NUMPAD_6 = lib.GHOSTTY_KEY_NUMPAD_6
    NUMPAD_7 = lib.GHOSTTY_KEY_NUMPAD_7
    NUMPAD_8 = lib.GHOSTTY_KEY_NUMPAD_8
    NUMPAD_9 = lib.GHOSTTY_KEY_NUMPAD_9
    NUMPAD_ADD = lib.GHOSTTY_KEY_NUMPAD_ADD
    NUMPAD_BACKSPACE = lib.GHOSTTY_KEY_NUMPAD_BACKSPACE
    NUMPAD_BEGIN = lib.GHOSTTY_KEY_NUMPAD_BEGIN
    NUMPAD_CLEAR = lib.GHOSTTY_KEY_NUMPAD_CLEAR
    NUMPAD_CLEAR_ENTRY = lib.GHOSTTY_KEY_NUMPAD_CLEAR_ENTRY
    NUMPAD_COMMA = lib.GHOSTTY_KEY_NUMPAD_COMMA
    NUMPAD_DECIMAL = lib.GHOSTTY_KEY_NUMPAD_DECIMAL
    NUMPAD_DELETE = lib.GHOSTTY_KEY_NUMPAD_DELETE
    NUMPAD_DIVIDE = lib.GHOSTTY_KEY_NUMPAD_DIVIDE
    NUMPAD_DOWN = lib.GHOSTTY_KEY_NUMPAD_DOWN
    NUMPAD_END = lib.GHOSTTY_KEY_NUMPAD_END
    NUMPAD_ENTER = lib.GHOSTTY_KEY_NUMPAD_ENTER
    NUMPAD_EQUAL = lib.GHOSTTY_KEY_NUMPAD_EQUAL
    NUMPAD_HOME = lib.GHOSTTY_KEY_NUMPAD_HOME
    NUMPAD_INSERT = lib.GHOSTTY_KEY_NUMPAD_INSERT
    NUMPAD_LEFT = lib.GHOSTTY_KEY_NUMPAD_LEFT
    NUMPAD_MEMORY_ADD = lib.GHOSTTY_KEY_NUMPAD_MEMORY_ADD
    NUMPAD_MEMORY_CLEAR = lib.GHOSTTY_KEY_NUMPAD_MEMORY_CLEAR
    NUMPAD_MEMORY_RECALL = lib.GHOSTTY_KEY_NUMPAD_MEMORY_RECALL
    NUMPAD_MEMORY_STORE = lib.GHOSTTY_KEY_NUMPAD_MEMORY_STORE
    NUMPAD_MEMORY_SUBTRACT = lib.GHOSTTY_KEY_NUMPAD_MEMORY_SUBTRACT
    NUMPAD_MULTIPLY = lib.GHOSTTY_KEY_NUMPAD_MULTIPLY
    NUMPAD_PAGE_DOWN = lib.GHOSTTY_KEY_NUMPAD_PAGE_DOWN
    NUMPAD_PAGE_UP = lib.GHOSTTY_KEY_NUMPAD_PAGE_UP
    NUMPAD_PAREN_LEFT = lib.GHOSTTY_KEY_NUMPAD_PAREN_LEFT
    NUMPAD_PAREN_RIGHT = lib.GHOSTTY_KEY_NUMPAD_PAREN_RIGHT
    NUMPAD_RIGHT = lib.GHOSTTY_KEY_NUMPAD_RIGHT
    NUMPAD_SEPARATOR = lib.GHOSTTY_KEY_NUMPAD_SEPARATOR
    NUMPAD_SUBTRACT = lib.GHOSTTY_KEY_NUMPAD_SUBTRACT
    NUMPAD_UP = lib.GHOSTTY_KEY_NUMPAD_UP
    NUM_LOCK = lib.GHOSTTY_KEY_NUM_LOCK
    O = lib.GHOSTTY_KEY_O  # noqa: E741
    P = lib.GHOSTTY_KEY_P
    PAGE_DOWN = lib.GHOSTTY_KEY_PAGE_DOWN
    PAGE_UP = lib.GHOSTTY_KEY_PAGE_UP
    PERIOD = lib.GHOSTTY_KEY_PERIOD
    Q = lib.GHOSTTY_KEY_Q
    QUOTE = lib.GHOSTTY_KEY_QUOTE
    R = lib.GHOSTTY_KEY_R
    S = lib.GHOSTTY_KEY_S
    SEMICOLON = lib.GHOSTTY_KEY_SEMICOLON
    SHIFT_LEFT = lib.GHOSTTY_KEY_SHIFT_LEFT
    SHIFT_RIGHT = lib.GHOSTTY_KEY_SHIFT_RIGHT
    SLASH = lib.GHOSTTY_KEY_SLASH
    SPACE = lib.GHOSTTY_KEY_SPACE
    T = lib.GHOSTTY_KEY_T
    TAB = lib.GHOSTTY_KEY_TAB
    U = lib.GHOSTTY_KEY_U
    UNIDENTIFIED = lib.GHOSTTY_KEY_UNIDENTIFIED
    V = lib.GHOSTTY_KEY_V
    W = lib.GHOSTTY_KEY_W
    X = lib.GHOSTTY_KEY_X
    Y = lib.GHOSTTY_KEY_Y
    Z = lib.GHOSTTY_KEY_Z


class KeyEvent:
    """A keyboard input event."""

    def __init__(self) -> None:
        handle = ffi.new("GhosttyKeyEvent *")
        check_result(lib.ghostty_key_event_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_key_event_free(self._handle)
            self._handle = ffi.NULL

    @property
    def handle(self) -> FFI.CData:
        return self._handle

    @property
    def action(self) -> KeyAction:
        return KeyAction(lib.ghostty_key_event_get_action(self._handle))

    @action.setter
    def action(self, value: KeyAction) -> None:
        lib.ghostty_key_event_set_action(self._handle, int(value))

    @property
    def key(self) -> Key:
        return Key(lib.ghostty_key_event_get_key(self._handle))

    @key.setter
    def key(self, value: Key) -> None:
        lib.ghostty_key_event_set_key(self._handle, int(value))

    @property
    def mods(self) -> int:
        return int(lib.ghostty_key_event_get_mods(self._handle))

    @mods.setter
    def mods(self, value: int) -> None:
        lib.ghostty_key_event_set_mods(self._handle, value)

    @property
    def consumed_mods(self) -> int:
        return int(lib.ghostty_key_event_get_consumed_mods(self._handle))

    @consumed_mods.setter
    def consumed_mods(self, value: int) -> None:
        lib.ghostty_key_event_set_consumed_mods(self._handle, value)

    @property
    def composing(self) -> bool:
        return bool(lib.ghostty_key_event_get_composing(self._handle))

    @composing.setter
    def composing(self, value: bool) -> None:
        lib.ghostty_key_event_set_composing(self._handle, value)

    @property
    def unshifted_codepoint(self) -> int:
        return int(lib.ghostty_key_event_get_unshifted_codepoint(self._handle))

    @unshifted_codepoint.setter
    def unshifted_codepoint(self, value: int) -> None:
        lib.ghostty_key_event_set_unshifted_codepoint(self._handle, value)

    def set_utf8(self, text: str | None) -> None:
        """Set the UTF-8 text generated by this key event.

        The caller must keep the KeyEvent alive while the text is needed.
        """
        if text is None:
            self._utf8_buf = ffi.NULL
            lib.ghostty_key_event_set_utf8(self._handle, ffi.NULL, 0)
            return

        encoded = text.encode("utf-8")
        # Store reference to prevent GC of the buffer
        self._utf8_buf = ffi.new("char[]", encoded)
        lib.ghostty_key_event_set_utf8(self._handle, self._utf8_buf, len(encoded))

    def get_utf8(self) -> str:
        """Return the UTF-8 text stored on this key event."""
        out_len = ffi.new("size_t *")
        buf = lib.ghostty_key_event_get_utf8(self._handle, out_len)
        if buf == ffi.NULL:
            return ""
        return bytes(ffi.buffer(buf, out_len[0])).decode("utf-8")


class KeyEncoder:
    """Encode key events into terminal escape sequences."""

    def __init__(self) -> None:
        handle = ffi.new("GhosttyKeyEncoder *")
        check_result(lib.ghostty_key_encoder_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_key_encoder_free(self._handle)
            self._handle = ffi.NULL

    def sync_from_terminal(self, terminal: Terminal) -> None:
        """Set encoder options from the terminal's current state."""
        lib.ghostty_key_encoder_setopt_from_terminal(self._handle, terminal.handle)

    def set_kitty_flags(self, flags: KittyKeyFlags) -> None:
        """Set Kitty keyboard protocol flags for subsequent key encoding."""
        value = ffi.new("GhosttyKittyKeyFlags *", int(flags))
        lib.ghostty_key_encoder_setopt(
            self._handle,
            lib.GHOSTTY_KEY_ENCODER_OPT_KITTY_FLAGS,
            value,
        )

    def encode(self, event: KeyEvent, buf_size: int = 128) -> bytes:
        """Encode a key event into an escape sequence.

        Returns:
            The encoded bytes (empty if the event produces no output).
        """
        buf = ffi.new("char[]", buf_size)
        out_len = ffi.new("size_t *")
        result = lib.ghostty_key_encoder_encode(self._handle, event.handle, buf, buf_size, out_len)
        if result == GhosttyError.OUT_OF_SPACE:
            buf = ffi.new("char[]", out_len[0])
            check_result(
                lib.ghostty_key_encoder_encode(self._handle, event.handle, buf, out_len[0], out_len)
            )
        else:
            check_result(result)
        return bytes(ffi.buffer(buf, out_len[0]))
