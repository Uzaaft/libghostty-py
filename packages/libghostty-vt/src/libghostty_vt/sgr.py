"""SGR (Select Graphic Rendition) parser."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from libghostty_cffi import ffi, lib

from libghostty_vt.errors import check_result

if TYPE_CHECKING:
    from collections.abc import Iterator

    from cffi import FFI


class SgrAttribute(NamedTuple):
    """A parsed SGR attribute."""

    tag: int
    rgb: tuple[int, int, int] | None = None
    palette_index: int | None = None
    underline_style: int | None = None


class SgrParser:
    """Parse SGR attribute sequences.

    SGR sequences control text styling (bold, italic, colors, etc).
    """

    def __init__(self) -> None:
        handle = ffi.new("GhosttySgrParser *")
        check_result(lib.ghostty_sgr_new(ffi.NULL, handle))
        self._handle: FFI.CData = handle[0]

    def __del__(self) -> None:
        if hasattr(self, "_handle") and self._handle != ffi.NULL:
            lib.ghostty_sgr_free(self._handle)
            self._handle = ffi.NULL

    def parse(self, params: list[int], separators: bytes | None = None) -> Iterator[SgrAttribute]:
        """Parse SGR parameters and yield attributes.

        Args:
            params: SGR parameter values (e.g. [1, 31] for bold red).
            separators: Optional separator characters (';' or ':').

        Yields:
            Parsed SGR attributes.
        """
        c_params = ffi.new("uint16_t[]", params)
        c_seps = ffi.NULL
        if separators is not None:
            c_seps = ffi.new("char[]", separators)
        check_result(lib.ghostty_sgr_set_params(self._handle, c_params, c_seps, len(params)))

        attr = ffi.new("GhosttySgrAttribute *")
        while lib.ghostty_sgr_next(self._handle, attr):
            tag = attr.tag
            rgb = None
            palette_index = None
            underline_style = None

            if tag in (
                lib.GHOSTTY_SGR_ATTR_DIRECT_COLOR_FG,
                lib.GHOSTTY_SGR_ATTR_DIRECT_COLOR_BG,
                lib.GHOSTTY_SGR_ATTR_UNDERLINE_COLOR,
            ):
                if tag == lib.GHOSTTY_SGR_ATTR_DIRECT_COLOR_FG:
                    c = attr.value.direct_color_fg
                elif tag == lib.GHOSTTY_SGR_ATTR_DIRECT_COLOR_BG:
                    c = attr.value.direct_color_bg
                else:
                    c = attr.value.underline_color
                rgb = (c.r, c.g, c.b)
            elif tag in (
                lib.GHOSTTY_SGR_ATTR_FG_8,
                lib.GHOSTTY_SGR_ATTR_BG_8,
                lib.GHOSTTY_SGR_ATTR_BRIGHT_FG_8,
                lib.GHOSTTY_SGR_ATTR_BRIGHT_BG_8,
                lib.GHOSTTY_SGR_ATTR_FG_256,
                lib.GHOSTTY_SGR_ATTR_BG_256,
                lib.GHOSTTY_SGR_ATTR_UNDERLINE_COLOR_256,
            ):
                if tag == lib.GHOSTTY_SGR_ATTR_FG_8:
                    palette_index = attr.value.fg_8
                elif tag == lib.GHOSTTY_SGR_ATTR_BG_8:
                    palette_index = attr.value.bg_8
                elif tag == lib.GHOSTTY_SGR_ATTR_BRIGHT_FG_8:
                    palette_index = attr.value.bright_fg_8
                elif tag == lib.GHOSTTY_SGR_ATTR_BRIGHT_BG_8:
                    palette_index = attr.value.bright_bg_8
                elif tag == lib.GHOSTTY_SGR_ATTR_FG_256:
                    palette_index = attr.value.fg_256
                elif tag == lib.GHOSTTY_SGR_ATTR_BG_256:
                    palette_index = attr.value.bg_256
                elif tag == lib.GHOSTTY_SGR_ATTR_UNDERLINE_COLOR_256:
                    palette_index = attr.value.underline_color_256
            elif tag == lib.GHOSTTY_SGR_ATTR_UNDERLINE:
                underline_style = attr.value.underline

            yield SgrAttribute(
                tag=tag, rgb=rgb, palette_index=palette_index, underline_style=underline_style
            )
