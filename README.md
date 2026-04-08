# libghostty-py

Python bindings for [libghostty-vt](https://ghostty.org), the virtual terminal emulator library extracted from Ghostty.

## Overview

libghostty-py provides a Pythonic interface to the libghostty-vt C library via CFFI. It exposes:

- **Terminal** - Complete terminal emulator state (screen, scrollback, cursor, modes, VT stream processing)
- **OSC Parser** - Parse OSC (Operating System Command) sequences
- **SGR Parser** - Parse SGR (Select Graphic Rendition) sequences for text styling
- **Key Encoder** - Encode keyboard events into terminal escape sequences
- **Mouse Encoder** - Encode mouse events into terminal escape sequences
- **Formatter** - Format terminal content as plain text, VT sequences, or HTML

## Installation

The wheel bundles the `libghostty-vt` shared library so no system-level
install is required.

### From a pre-built wheel

```bash
pip install libghostty            # once published to PyPI
```

### Building a wheel locally

The build hook finds `libghostty-vt` via (in priority order):

1. `LIBGHOSTTY_VT_PATH` env var pointing to the `.so`/`.dylib`
2. `pkg-config` (e.g. from `nix develop`)
3. Building from source via `zig build` (set `GHOSTTY_SRC_DIR` to a
   Ghostty checkout, or place the repo as a sibling directory)

```bash
# Option A: nix dev shell (provides the library automatically)
nix develop
uv build

# Option B: explicit path to a pre-built library
LIBGHOSTTY_VT_PATH=/path/to/libghostty-vt.so uv build

# Option C: build from ghostty source
GHOSTTY_SRC_DIR=../ghostty uv build
```

### Standalone library builds

```bash
nix build .#libghostty-vt          # ReleaseFast (default)
nix build .#libghostty-vt-debug    # Debug
```

## Examples

### Ghostling

A minimal terminal emulator built with PyQt6 and libghostty-vt. Spawns a
PTY, renders cells via the render state API, and encodes keyboard input
through the key encoder.

```bash
uv sync --extra examples
LIBGHOSTTY_VT_PATH=/path/to/libghostty-vt.so uv run python examples/ghostling.py
```

## Development

```bash
# Enter the dev shell
nix develop

# Sync dependencies
uv sync

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy src/
```
