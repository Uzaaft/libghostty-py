"""Test that the CFFI C definitions parse without errors."""

import importlib.util

import cffi


def _load_cdef() -> str:
    """Load CDEF string without triggering the package __init__."""
    spec = importlib.util.spec_from_file_location("_cdef", "src/libghostty/_cdef.py")
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CDEF  # type: ignore[no-any-return]


def test_cdef_parses() -> None:
    """The CDEF string must be valid CFFI input."""
    cdef = _load_cdef()
    f = cffi.FFI()
    f.cdef(cdef)
