#!/usr/bin/env python3
"""Create a task-local fontconfig file so bundled headless LibreOffice can see macOS CJK fonts."""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cache-dir", type=Path)
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    cache = (args.cache_dir or output.parent / "font-cache").expanduser().resolve()
    candidates = [
        Path("/System/Library/Fonts"),
        Path("/System/Library/Fonts/Supplemental"),
        Path("/Library/Fonts"),
        Path.home() / "Library/Fonts",
    ]
    directories = [path.resolve() for path in candidates if path.is_dir()]
    if not directories:
        parser.error("No macOS font directories were found")

    output.parent.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)
    lines = [
        '<?xml version="1.0"?>',
        '<!DOCTYPE fontconfig SYSTEM "fonts.dtd">',
        '<fontconfig>',
        *[f"  <dir>{escape(str(path))}</dir>" for path in directories],
        f"  <cachedir>{escape(str(cache))}</cachedir>",
        '</fontconfig>',
        '',
    ]
    output.write_text("\n".join(lines), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
