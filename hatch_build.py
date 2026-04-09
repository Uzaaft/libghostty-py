"""Hatch build hook that bundles the libghostty-vt shared library into the wheel.

The library is located via (in priority order):
    1. LIBGHOSTTY_VT_PATH env var  (path to the .so/.dylib itself)
    2. pkg-config                  (installed via system package or nix)
    3. Build from source           (requires the ghostty repo + zig)

The resulting wheel is platform-specific and contains the shared library
next to the Python package so that dlopen can find it without any system
installation.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

_LIB_NAMES = {
    "Linux": "libghostty-vt.so",
    "Darwin": "libghostty-vt.dylib",
    "Windows": "ghostty-vt.dll",
}


def _lib_name() -> str:
    return _LIB_NAMES.get(platform.system(), "libghostty-vt.so")


def _find_via_env() -> Path | None:
    env = os.environ.get("LIBGHOSTTY_VT_PATH")
    if env:
        p = Path(env)
        if p.is_file():
            return p
    return None


def _find_via_pkg_config() -> Path | None:
    try:
        result = subprocess.run(
            ["pkg-config", "--variable=libdir", "libghostty-vt"],
            capture_output=True,
            text=True,
            check=True,
        )
        libdir = Path(result.stdout.strip())
        candidate = libdir / _lib_name()
        if candidate.is_file():
            return candidate
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return None


def _build_from_source() -> Path:
    """Build libghostty-vt from the ghostty repository.

    Expects GHOSTTY_SRC_DIR env var pointing to a ghostty checkout,
    or a `ghostty` directory as a sibling of this project.
    """
    src_dir = os.environ.get("GHOSTTY_SRC_DIR")
    if not src_dir:
        # Try common sibling locations
        for candidate in [
            Path(__file__).parent.parent / "ghostty",
            Path(__file__).parent.parent / "ghostty-org" / "ghostty",
        ]:
            if (candidate / "build.zig").is_file():
                src_dir = str(candidate)
                break

    if not src_dir or not Path(src_dir, "build.zig").is_file():
        raise RuntimeError(
            "Cannot find ghostty source to build libghostty-vt. "
            "Set LIBGHOSTTY_VT_PATH to a pre-built library, or "
            "set GHOSTTY_SRC_DIR to a ghostty repository checkout."
        )

    print(f"Building libghostty-vt from {src_dir}", file=sys.stderr)
    subprocess.run(
        [
            "zig",
            "build",
            "-Demit-lib-vt=true",
            "-Doptimize=ReleaseFast",
        ],
        cwd=src_dir,
        check=True,
    )

    lib_path = Path(src_dir) / "zig-out" / "lib" / _lib_name()
    if not lib_path.is_file():
        raise RuntimeError(f"Build succeeded but {lib_path} not found. Check zig build output.")
    return lib_path


def _resolve_library() -> Path:
    """Find or build the shared library, returning the path to the file."""
    path = _find_via_env()
    if path:
        return path

    path = _find_via_pkg_config()
    if path:
        return path

    return _build_from_source()


class NativeLibraryHook(BuildHookInterface):
    """Bundle libghostty-vt shared library into the wheel."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict) -> None:  # type: ignore[override]
        if self.target_name != "wheel" or version == "editable":
            return

        lib_path = _resolve_library()
        pkg_dir = Path(self.root) / "src" / "libghostty_cffi"
        lib_name = _lib_name()

        # Resolve symlinks to get the actual file
        real_path = lib_path.resolve() if lib_path.is_symlink() else lib_path

        # Copy the real file with the canonical unversioned name
        dest = pkg_dir / lib_name
        shutil.copy2(real_path, dest)
        build_data["force_include"][str(dest)] = f"libghostty_cffi/{lib_name}"

        # Mark this as a platform-specific wheel
        build_data["pure_python"] = False
        build_data["infer_tag"] = True

    def clean(self, versions: list[str]) -> None:
        # Remove any previously bundled libraries
        pkg_dir = Path(self.root) / "src" / "libghostty_cffi"
        for suffix in (".so", ".dylib", ".dll"):
            for f in pkg_dir.glob(f"*ghostty*{suffix}*"):
                f.unlink(missing_ok=True)
