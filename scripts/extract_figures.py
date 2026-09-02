#!/usr/bin/env python3
"""Render PDF pages, crop normalized figure regions, trim white margins, and build a contact sheet."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Crop:
    page: int
    box: tuple[float, float, float, float]
    name: str


def page_count(pdf: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        result = subprocess.run([pdfinfo, str(pdf)], check=True, capture_output=True, text=True)
        match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, flags=re.MULTILINE)
        if match:
            return int(match.group(1))
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf)).pages)
    except Exception as exc:  # pragma: no cover - fallback message is environment-specific
        raise RuntimeError("Cannot determine page count; install pdfinfo or pypdf") from exc


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    pages: set[int] = set()
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            start, end = int(start_s), int(end_s)
            if end < start:
                raise ValueError(f"Invalid page range: {token}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(token))
    if not pages or min(pages) < 1 or max(pages) > total:
        raise ValueError(f"Pages must be within 1-{total}")
    return sorted(pages)


def parse_crop(spec: str) -> Crop:
    parts = spec.split(":", 2)
    if len(parts) < 2:
        raise argparse.ArgumentTypeError("Crop must be PAGE:X0,Y0,X1,Y1[:NAME]")
    page = int(parts[0])
    coords = tuple(float(value) for value in parts[1].split(","))
    if len(coords) != 4:
        raise argparse.ArgumentTypeError("Crop requires four normalized coordinates")
    x0, y0, x1, y1 = coords
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise argparse.ArgumentTypeError("Crop coordinates must satisfy 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1")
    name = parts[2].strip() if len(parts) == 3 else ""
    return Crop(page=page, box=(x0, y0, x1, y1), name=name)


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return value.strip("-._") or "figure"


def render_page(pdftoppm: str, pdf: Path, page: int, dpi: int, temp_dir: Path) -> Path:
    prefix = temp_dir / f"page-{page:03d}"
    subprocess.run(
        [pdftoppm, "-f", str(page), "-l", str(page), "-singlefile", "-png", "-r", str(dpi), str(pdf), str(prefix)],
        check=True,
        capture_output=True,
        text=True,
    )
    output = prefix.with_suffix(".png")
    if not output.exists():
        raise RuntimeError(f"pdftoppm did not produce {output}")
    return output


def trim_white(image: Image.Image, threshold: int, padding: int) -> Image.Image:
    rgb = image.convert("RGB")
    ink = rgb.convert("L").point(lambda value: 255 if value < threshold else 0)
    bbox = ink.getbbox()
    if not bbox:
        return rgb
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(rgb.width, right + padding)
    bottom = min(rgb.height, bottom + padding)
    return rgb.crop((left, top, right, bottom))


def crop_image(page_image: Image.Image, crop: Crop, threshold: int, padding: int) -> Image.Image:
    x0, y0, x1, y1 = crop.box
    pixels = (
        round(x0 * page_image.width),
        round(y0 * page_image.height),
        round(x1 * page_image.width),
        round(y1 * page_image.height),
    )
    return trim_white(page_image.crop(pixels), threshold, padding)


def contact_sheet(images: list[tuple[str, Path]], output: Path, thumb_width: int = 700) -> None:
    if not images:
        return
    prepared: list[tuple[str, Image.Image]] = []
    for label, path in images:
        image = Image.open(path).convert("RGB")
        scale = min(1.0, thumb_width / image.width)
        image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
        prepared.append((label, image))

    columns = 2 if len(prepared) > 1 else 1
    cell_width = thumb_width + 40
    label_height = 34
    row_heights: list[int] = []
    for start in range(0, len(prepared), columns):
        row_heights.append(max(image.height for _, image in prepared[start : start + columns]) + label_height + 30)
    canvas = Image.new("RGB", (cell_width * columns, sum(row_heights) + 20), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    y = 10
    for row_index, start in enumerate(range(0, len(prepared), columns)):
        for column, (label, image) in enumerate(prepared[start : start + columns]):
            x = column * cell_width + 20
            draw.text((x, y), label, fill="black", font=font)
            canvas.paste(image, (x, y + label_height))
        y += row_heights[row_index]
    canvas.save(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("outdir", type=Path)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--pages", help="Pages to render, e.g. 1-4,7")
    parser.add_argument("--crop", action="append", type=parse_crop, default=[], help="PAGE:X0,Y0,X1,Y1[:NAME]; repeatable")
    parser.add_argument("--threshold", type=int, default=248, help="Pixels darker than this count as content")
    parser.add_argument("--padding", type=int, default=12, help="White-margin padding retained after trimming")
    parser.add_argument("--no-contact-sheet", action="store_true")
    args = parser.parse_args()

    pdf = args.pdf.expanduser().resolve()
    if not pdf.is_file():
        parser.error(f"PDF not found: {pdf}")
    if args.dpi < 72:
        parser.error("--dpi must be at least 72")
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        parser.error("pdftoppm was not found; load the bundled workspace dependencies or install Poppler")

    total = page_count(pdf)
    if args.crop:
        invalid = [crop.page for crop in args.crop if not 1 <= crop.page <= total]
        if invalid:
            parser.error(f"Crop pages outside 1-{total}: {invalid}")
        pages = sorted({crop.page for crop in args.crop})
        if args.pages:
            selected = set(parse_pages(args.pages, total))
            if not set(pages).issubset(selected):
                parser.error("Every crop page must also be included by --pages")
    else:
        pages = parse_pages(args.pages, total)

    outdir = args.outdir.expanduser().resolve()
    pages_dir = outdir / "pages"
    figures_dir = outdir / "figures"
    pages_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    contact_items: list[tuple[str, Path]] = []
    with tempfile.TemporaryDirectory(prefix="flight-doc-figures-") as temp:
        temp_dir = Path(temp)
        rendered: dict[int, Path] = {}
        for page in pages:
            temp_path = render_page(pdftoppm, pdf, page, args.dpi, temp_dir)
            page_output = pages_dir / f"page-{page:03d}.png"
            shutil.copy2(temp_path, page_output)
            rendered[page] = page_output

        if args.crop:
            per_page_index: dict[int, int] = {}
            for crop in args.crop:
                per_page_index[crop.page] = per_page_index.get(crop.page, 0) + 1
                suffix = safe_name(crop.name) if crop.name else f"{per_page_index[crop.page]:02d}"
                output = figures_dir / f"figure-p{crop.page:03d}-{suffix}.png"
                with Image.open(rendered[crop.page]) as page_image:
                    crop_image(page_image, crop, args.threshold, args.padding).save(output)
                contact_items.append((output.stem, output))
        else:
            contact_items.extend((path.stem, path) for path in rendered.values())

    if not args.no_contact_sheet:
        contact_sheet(contact_items, outdir / "contact-sheet.png")

    print(f"Rendered pages: {len(pages)}")
    print(f"Cropped figures: {len(args.crop)}")
    print(f"Output: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
