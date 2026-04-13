"""Test that the CFFI C definitions parse without errors."""

from pathlib import Path

import cffi


def test_cdef_parses() -> None:
    """The CDEF string must be valid CFFI input."""
    cdef_path = Path(__file__).parents[1] / "src" / "libghostty" / "_cffi" / "cdef.h"
    f = cffi.FFI()
    f.cdef(cdef_path.read_text())
