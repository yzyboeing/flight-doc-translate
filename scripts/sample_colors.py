#!/usr/bin/env python3
"""Sample prominent source colors from a PDF or raster image without inventing a palette."""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from PIL import Image


def pdf_page_count(pdf: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        result = subprocess.run([pdfinfo, str(pdf)], check=True, capture_output=True, text=True)
        match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, flags=re.MULTILINE)
        if match:
            return int(match.group(1))
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf)).pages)
    except Exception as exc:
        raise RuntimeError("Cannot determine PDF page count; install pdfinfo or pypdf") from exc


def parse_pages(spec: str | None, total: int, maximum: int) -> list[int]:
    if not spec:
        if total <= maximum:
            return list(range(1, total + 1))
        step = (total - 1) / (maximum - 1)
        return sorted({1 + round(index * step) for index in range(maximum)})
    pages: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if "-" in token:
            start, end = (int(value) for value in token.split("-", 1))
            pages.update(range(start, end + 1))
        elif token:
            pages.add(int(token))
    if not pages or min(pages) < 1 or max(pages) > total:
        raise ValueError(f"Pages must be within 1-{total}")
    return sorted(pages)


def render_pdf(pdf: Path, pages: list[int], dpi: int, directory: Path) -> list[Path]:
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm was not found; load bundled workspace dependencies or install Poppler")
    outputs: list[Path] = []
    for page in pages:
        prefix = directory / f"sample-{page:03d}"
        subprocess.run(
            [pdftoppm, "-f", str(page), "-l", str(page), "-singlefile", "-png", "-r", str(dpi), str(pdf), str(prefix)],
            check=True,
            capture_output=True,
            text=True,
        )
        output = prefix.with_suffix(".png")
        if not output.exists():
            raise RuntimeError(f"pdftoppm did not produce {output}")
        outputs.append(output)
    return outputs


def color_stats(paths: list[Path], quantize_colors: int) -> Counter[tuple[int, int, int]]:
    counts: Counter[tuple[int, int, int]] = Counter()
    for path in paths:
        with Image.open(path) as source:
            image = source.convert("RGB")
            image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
            quantized = image.quantize(colors=quantize_colors, method=Image.Quantize.MEDIANCUT).convert("RGB")
            for count, rgb in quantized.getcolors(maxcolors=quantized.width * quantized.height) or []:
                counts[rgb] += count
    return counts


def saturation(rgb: tuple[int, int, int]) -> float:
    r, g, b = (channel / 255 for channel in rgb)
    return colorsys.rgb_to_hsv(r, g, b)[1]


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def distance(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def prominent_colors(
    counts: Counter[tuple[int, int, int]],
    number: int,
    min_saturation: float,
    include_neutral: bool,
) -> list[dict[str, object]]:
    eligible = []
    for rgb, count in counts.most_common():
        lum = luminance(rgb)
        if lum > 245 or lum < 18:
            continue
        if not include_neutral and saturation(rgb) < min_saturation:
            continue
        eligible.append((rgb, count))

    selected: list[tuple[tuple[int, int, int], int]] = []
    for rgb, count in eligible:
        if all(distance(rgb, existing) >= 34 for existing, _ in selected):
            selected.append((rgb, count))
        if len(selected) >= number:
            break

    total = sum(count for _, count in eligible) or 1
    return [
        {
            "hex": "#%02X%02X%02X" % rgb,
            "rgb": list(rgb),
            "share_of_eligible_pixels": round(count / total, 4),
        }
        for rgb, count in selected
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--pages", help="PDF pages to sample, e.g. 1-4,8")
    parser.add_argument("--max-pages", type=int, default=12, help="Evenly sample at most this many pages when --pages is omitted")
    parser.add_argument("--dpi", type=int, default=110)
    parser.add_argument("--colors", type=int, default=5)
    parser.add_argument("--quantize-colors", type=int, default=64)
    parser.add_argument("--min-saturation", type=float, default=0.18)
    parser.add_argument("--include-neutral", action="store_true")
    parser.add_argument("--json", dest="json_path", type=Path, help="Also save the result as JSON")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        parser.error(f"Source not found: {source}")
    if args.colors < 1 or args.max_pages < 1:
        parser.error("--colors and --max-pages must be positive")

    sampled_pages: list[int] | None = None
    with tempfile.TemporaryDirectory(prefix="flight-doc-colors-") as temp:
        if source.suffix.lower() == ".pdf":
            total = pdf_page_count(source)
            sampled_pages = parse_pages(args.pages, total, args.max_pages)
            paths = render_pdf(source, sampled_pages, args.dpi, Path(temp))
        else:
            paths = [source]
        counts = color_stats(paths, args.quantize_colors)
        colors = prominent_colors(counts, args.colors, args.min_saturation, args.include_neutral)

    result = {
        "source": str(source),
        "sampled_pages": sampled_pages,
        "colors": colors,
        "note": "Candidates only. Visually confirm each color against the source before configuring style_boeing.js.",
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.json_path:
        destination = args.json_path.expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
