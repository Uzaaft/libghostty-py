#!/usr/bin/env python3
"""Fetch and flatten the libghostty-vt C headers for CFFI.

The upstream public header, `ghostty/vt.h`, includes the per-module headers
that contain the actual declarations. CFFI consumes a single declaration string,
so this script downloads the stable include order and writes one flattened
`cdef.h` file for the package.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PINNED_GHOSTTY_COMMIT = "b0f8276658fbcc75318d2125d40146074a3fc505"
RAW_BASE_URL = "https://raw.githubusercontent.com/ghostty-org/ghostty/{ref}/include/{path}"


class HeaderPackage(NamedTuple):
    name: str
    include_header: str
    include_prefix: str
    default_output: Path
    header_paths: tuple[str, ...]
    expected_symbols: tuple[str, ...]


VT_PACKAGE = HeaderPackage(
    name="vt",
    include_header="ghostty/vt.h",
    include_prefix="ghostty/vt/",
    default_output=Path("src/libghostty/_cffi/cdef.h"),
    header_paths=(
        "ghostty/vt/types.h",
        "ghostty/vt/allocator.h",
        "ghostty/vt/build_info.h",
        "ghostty/vt/color.h",
        "ghostty/vt/device.h",
        "ghostty/vt/modes.h",
        "ghostty/vt/size_report.h",
        "ghostty/vt/screen.h",
        "ghostty/vt/point.h",
        "ghostty/vt/focus.h",
        "ghostty/vt/style.h",
        "ghostty/vt/grid_ref.h",
        "ghostty/vt/selection.h",
        "ghostty/vt/kitty_graphics.h",
        "ghostty/vt/terminal.h",
        "ghostty/vt/formatter.h",
        "ghostty/vt/render.h",
        "ghostty/vt/osc.h",
        "ghostty/vt/sgr.h",
        "ghostty/vt/sys.h",
        "ghostty/vt/key/event.h",
        "ghostty/vt/key/encoder.h",
        "ghostty/vt/key.h",
        "ghostty/vt/mouse/event.h",
        "ghostty/vt/mouse/encoder.h",
        "ghostty/vt/mouse.h",
        "ghostty/vt/paste.h",
    ),
    expected_symbols=("GhosttyResult", "ghostty_terminal_new"),
)
HEADER_PACKAGES = {VT_PACKAGE.name: VT_PACKAGE}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument(
        "package",
        nargs="?",
        choices=tuple(HEADER_PACKAGES),
        default=VT_PACKAGE.name,
        help="Header package to fetch. Defaults to %(default)s.",
    )
    _ = parser.add_argument(
        "--ref",
        default=PINNED_GHOSTTY_COMMIT,
        help=(
            "Ghostty git ref to fetch from. Defaults to the pinned commit in "
            "PINNED_GHOSTTY_COMMIT."
        ),
    )
    _ = parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to write the flattened CFFI header. Defaults to the package output path.",
    )
    return parser.parse_args()


def fetch_header(package: HeaderPackage, ref: str, path: str) -> str:
    if not ref.strip():
        msg = "ref must not be empty"
        raise ValueError(msg)
    if path != package.include_header and not path.startswith(package.include_prefix):
        msg = f"refusing to fetch unexpected header path: {path}"
        raise ValueError(msg)

    url = RAW_BASE_URL.format(ref=ref, path=path)
    request = Request(url, headers={"User-Agent": "libghostty-py-fetch-cdef"})
    try:
        with urlopen(request, timeout=30) as response:
            data: bytes = response.read()
            content = data.decode("utf-8")
    except (HTTPError, URLError, TimeoutError) as error:
        msg = f"failed to fetch {url}: {error}"
        raise RuntimeError(msg) from error

    if not content.strip():
        msg = f"fetched empty header: {url}"
        raise RuntimeError(msg)
    return content


def strip_for_cffi(content: str) -> str:
    lines: list[str] = []
    skipping_extern_block = False
    skipping_directive_continuation = False
    skipping_static_inline = False

    for line in content.splitlines():
        stripped = line.strip()
        if skipping_static_inline:
            if stripped == "}":
                skipping_static_inline = False
            continue
        if skipping_directive_continuation:
            skipping_directive_continuation = stripped.endswith("\\")
            continue
        if stripped.startswith("#"):
            skipping_directive_continuation = stripped.endswith("\\")
            continue
        if stripped.startswith("static inline "):
            skipping_static_inline = not stripped.endswith("}")
            continue
        if "= GHOSTTY_ENUM_MAX_VALUE" in stripped:
            continue

        line = line.replace("GHOSTTY_API ", "")
        line = line.replace(" GHOSTTY_API", "")
        line = line.replace(" GHOSTTY_ENUM_TYPED", "")

        if stripped == "extern \"C\" {":
            skipping_extern_block = True
            continue
        if skipping_extern_block and stripped == "}":
            skipping_extern_block = False
            continue
        lines.append(line)

    stripped_content = "\n".join(lines).strip()
    if not stripped_content:
        msg = "header became empty after preprocessing"
        raise RuntimeError(msg)
    return stripped_content


def build_cdef(package: HeaderPackage, ref: str) -> str:
    parts = [
        "/* This file is generated by scripts/fetch_cdef.py. */",
        f"/* Source: ghostty-org/ghostty {ref} include/{package.include_header} */",
    ]

    for header_path in package.header_paths:
        header = strip_for_cffi(fetch_header(package, ref, header_path))
        parts.append(f"// {header_path}\n\n{header}")

    cdef = "\n\n".join(parts) + "\n"
    missing_symbols = [symbol for symbol in package.expected_symbols if symbol not in cdef]
    if missing_symbols:
        missing = ", ".join(missing_symbols)
        msg = f"flattened {package.name} header is missing expected declarations: {missing}"
        raise RuntimeError(msg)
    return cdef


def write_text_atomic(path: Path, content: str) -> None:
    if not content.strip():
        msg = "refusing to write empty content"
        raise ValueError(msg)

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as file:
        temp_path = Path(file.name)
        _ = file.write(content)
    temp_path.replace(path)


def main() -> int:
    args = parse_args()
    package = HEADER_PACKAGES[args.package]
    output = args.output if args.output is not None else package.default_output
    cdef = build_cdef(package, args.ref)
    write_text_atomic(output, cdef)
    print(f"wrote {output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
