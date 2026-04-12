"""Build info queries for libghostty-vt."""

from __future__ import annotations

from libghostty_cffi import ffi, lib

from libghostty_vt.errors import check_result


def check_build_info(field: int) -> bool:
    out = ffi.new("bool *")
    check_result(lib.ghostty_build_info(field, out))
    return bool(out[0])


def has_simd() -> bool:
    """Whether SIMD-accelerated code paths are enabled."""
    return check_build_info(lib.GHOSTTY_BUILD_INFO_SIMD)


def has_kitty_graphics() -> bool:
    """Whether Kitty graphics protocol support is available."""
    return check_build_info(lib.GHOSTTY_BUILD_INFO_KITTY_GRAPHICS)


def has_tmux_control_mode() -> bool:
    """Whether tmux control mode support is available."""
    return check_build_info(lib.GHOSTTY_BUILD_INFO_TMUX_CONTROL_MODE)


def version() -> str:
    """Full version string (e.g. '1.2.3' or '1.2.3-dev+abcdef')."""
    out = ffi.new("GhosttyString *")
    check_result(lib.ghostty_build_info(lib.GHOSTTY_BUILD_INFO_VERSION_STRING, out))
    return ffi.buffer(out.ptr, out.len)[:].decode("utf-8")


def version_tuple() -> tuple[int, int, int]:
    """Version as (major, minor, patch) tuple."""
    major = ffi.new("size_t *")
    minor = ffi.new("size_t *")
    patch = ffi.new("size_t *")
    check_result(lib.ghostty_build_info(lib.GHOSTTY_BUILD_INFO_VERSION_MAJOR, major))
    check_result(lib.ghostty_build_info(lib.GHOSTTY_BUILD_INFO_VERSION_MINOR, minor))
    check_result(lib.ghostty_build_info(lib.GHOSTTY_BUILD_INFO_VERSION_PATCH, patch))
    return (major[0], minor[0], patch[0])
