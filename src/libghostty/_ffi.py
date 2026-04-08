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
from typing import TYPE_CHECKING

import cffi

from libghostty._cdef import CDEF

if TYPE_CHECKING:
    from cffi import FFI as FFIType

ffi: FFIType = cffi.FFI()
ffi.cdef(CDEF)

_LIB_NAMES = {
    "Linux": "libghostty-vt.so",
    "Darwin": "libghostty-vt.dylib",
    "Windows": "ghostty-vt.dll",
}

_LIB_ENV = "LIBGHOSTTY_VT_PATH"


def _find_library() -> str:
    # 1. Explicit env var
    env_path = os.environ.get(_LIB_ENV)
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2. Bundled alongside this package (installed via wheel)
    lib_name = _LIB_NAMES.get(platform.system(), "libghostty-vt.so")
    bundled = Path(__file__).parent / lib_name
    if bundled.is_file():
        return str(bundled)

    # 3. Let the OS loader find it (LD_LIBRARY_PATH, system paths, etc.)
    #    ffi.dlopen with just the name will use dlopen(3) search semantics.
    if env_path:
        return env_path
    return lib_name


lib = ffi.dlopen(_find_library())
