"""Load libghostty-vt shared library via CFFI.

Library search order:
    1. LIBGHOSTTY_VT_PATH env var
    2. Bundled library shipped inside the wheel (same directory as this file)
    3. System library via OS loader (LD_LIBRARY_PATH, etc.)
"""

from __future__ import annotations

import os
import platform
from pathlib import Path

import cffi

ffi = cffi.FFI()
ffi.cdef((Path(__file__).parent / "cdef.h").read_text())

LIB_NAME = {
    "Linux": "libghostty-vt.so",
    "Darwin": "libghostty-vt.dylib",
    "Windows": "ghostty-vt.dll",
}.get(platform.system(), "libghostty-vt.so")

_LIB_ENV = "LIBGHOSTTY_VT_PATH"


def _find_library() -> str:
    # 1. Explicit env var
    env_path = os.getenv(_LIB_ENV)
    if env_path and Path(env_path).is_file():
        return env_path

    # 2. Bundled alongside this package (installed via wheel)
    bundled = Path(__file__).parent / LIB_NAME
    if bundled.is_file():
        return str(bundled)

    # 3. Let the OS loader find it (LD_LIBRARY_PATH, system paths, etc.)
    #    ffi.dlopen with just the name will use dlopen(3) search semantics.
    return env_path or LIB_NAME


lib = ffi.dlopen(_find_library())
