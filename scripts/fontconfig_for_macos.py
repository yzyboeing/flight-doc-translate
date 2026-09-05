#!/usr/bin/env python3
"""Create a task-local fontconfig file so bundled headless LibreOffice can see macOS CJK fonts."""

from __future__ import annotations

import argparse
import subprocess
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

    # macOS 26 起，PingFang / Songti 等中日韩字体移到可下载资产目录
    # /System/Library/AssetsV2/com_apple_MobileAsset_Font*/，不在上面四个经典路径中。
    # 只列经典路径会让 LibreOffice 解析不到任何中文字体，渲染出的 PDF 里
    # 中文全部缺失——而版面、颜色、表格看起来都正常，目视很容易漏掉。
    # 因此用 fc-list 反查实际持有中文字体的目录并一并加入。
    try:
        listing = subprocess.run(
            ["fc-list", ":lang=zh", "file"],
            capture_output=True, text=True, timeout=30, check=False,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        listing = ""
    seen = {str(d) for d in directories}
    for line in listing.splitlines():
        path_text = line.split(":", 1)[0].strip()
        if not path_text:
            continue
        parent = Path(path_text).parent
        if parent.is_dir() and str(parent) not in seen:
            seen.add(str(parent))
            directories.append(parent)

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
