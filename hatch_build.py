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
import subprocess as sp
import sys
from contextlib import suppress
from pathlib import Path
from typing import Any, final

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

REPO_PARENT = Path(__file__).parents[1]

LIB_NAME = {
    "Linux": "libghostty-vt.so",
    "Darwin": "libghostty-vt.dylib",
    "Windows": "ghostty-vt.dll",
}.get(platform.system(), "libghostty-vt.so")


def _find_via_env() -> Path | None:
    if (env := os.getenv("LIBGHOSTTY_VT_PATH")) and (path := Path(env)).is_file():
        return path
    return None


def _find_via_pkg_config() -> Path | None:
    with suppress(sp.CalledProcessError, FileNotFoundError):
        result = sp.run(
            ("pkg-config", "--variable=libdir", "libghostty-vt"),
            capture_output=True,
            text=True,
            check=True,
        )
        libdir = Path(result.stdout.strip())
        candidate = libdir / LIB_NAME
        if candidate.is_file():
            return candidate
    return None


def _build_from_source() -> Path:
    """Build libghostty-vt from the ghostty repository.

    Expects GHOSTTY_SRC_DIR env var pointing to a ghostty checkout,
    or a `ghostty` directory as a sibling of this project.
    """
    if not (src_dir := os.getenv("GHOSTTY_SRC_DIR")):
        # Try common sibling locations
        for candidate in (REPO_PARENT / "ghostty", REPO_PARENT / "ghostty-org" / "ghostty"):
            if (candidate / "build.zig").is_file():
                src_dir = str(candidate)
                break

    if not (src_dir and Path(src_dir, "build.zig").is_file()):
        msg = (
            "Cannot find ghostty source to build libghostty-vt. "
            "Set LIBGHOSTTY_VT_PATH to a pre-built library, or "
            "set GHOSTTY_SRC_DIR to a ghostty repository checkout."
        )
        raise RuntimeError(msg)

    print(f"Building libghostty-vt from {src_dir}", file=sys.stderr)
    _ = sp.run(
        ("zig", "build", "-Demit-lib-vt=true", "-Doptimize=ReleaseFast"), cwd=src_dir, check=True
    )

    lib_path = Path(src_dir) / "zig-out" / "lib" / LIB_NAME
    if not lib_path.is_file():
        msg = f"Build succeeded but {lib_path} not found. Check zig build output."
        raise RuntimeError(msg)
    return lib_path


def _resolve_library() -> Path:
    """Find or build the shared library, returning the path to the file."""
    if path := _find_via_env():
        return path
    if path := _find_via_pkg_config():
        return path
    return _build_from_source()


@final
class NativeLibraryHook(BuildHookInterface[Any]):
    """Bundle libghostty-vt shared library into the wheel."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if self.target_name != "wheel" or version == "editable":
            return

        lib_path = _resolve_library()
        pkg_dir = Path(self.root) / "src" / "libghostty_cffi"

        # Resolve symlinks to get the actual file
        real_path = lib_path.resolve() if lib_path.is_symlink() else lib_path

        # Copy the real file with the canonical unversioned name
        dest = pkg_dir / LIB_NAME
        _ = shutil.copy2(real_path, dest)
        build_data["force_include"][str(dest)] = f"libghostty_cffi/{LIB_NAME}"

        # Mark this as a platform-specific wheel
        build_data["pure_python"] = False
        build_data["infer_tag"] = True

    def clean(self, versions: list[str]) -> None:
        # Remove any previously bundled libraries
        pkg_dir = Path(self.root) / "src" / "libghostty_cffi"
        for suffix in (".so", ".dylib", ".dll"):
            for file in pkg_dir.glob(f"*ghostty*{suffix}*"):
                file.unlink(missing_ok=True)
