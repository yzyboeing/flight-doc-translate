#!/usr/bin/env python3
"""Validate public-package safety and terminology-table consistency."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".pdf", ".docx", ".zip"}
ABSOLUTE_LOCAL_PATH = re.compile(r"/(?:Users|home)/[^\s`\"']+")


def markdown_links() -> list[str]:
    problems: list[str] = []
    for source in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]:
        text = source.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", text):
            if not (source.parent / link).resolve().exists():
                problems.append(f"broken link: {source.relative_to(ROOT)} -> {link}")
    return problems


def public_content() -> list[str]:
    problems: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"forbidden artifact: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = ABSOLUTE_LOCAL_PATH.search(text)
        if match:
            problems.append(f"local path in {path.relative_to(ROOT)}: {match.group(0)}")
    return problems


def table_rows(path: Path) -> list[tuple[str, str, int]]:
    rows: list[tuple[str, str, int]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2 or cells[0].lower() in {"english", "english pattern"}:
            continue
        if not cells[0] or set(cells[0]) <= {"-", ":"}:
            continue
        key = re.sub(r"\s+", " ", cells[0].lower())
        rows.append((key, cells[1], line_number))
    return rows


def terminology_conflicts() -> list[str]:
    sources = [ROOT / "references" / "glossary.md", ROOT / "references" / "fctm_zh_usage.md"]
    index: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
    for source in sources:
        for key, chinese, line in table_rows(source):
            index[key].append((source.name, chinese, line))

    problems: list[str] = []
    for key, values in sorted(index.items()):
        if len(values) > 1 and len({value[1] for value in values}) > 1:
            locations = ", ".join(f"{source}:{line}={chinese}" for source, chinese, line in values)
            problems.append(f"conflicting term {key!r}: {locations}")
    return problems


def semantic_distinctions() -> list[str]:
    sources = [ROOT / "references" / "glossary.md", ROOT / "references" / "fctm_zh_usage.md"]
    translations: dict[str, str] = {}
    for source in sources:
        for key, chinese, _ in table_rows(source):
            translations[key] = chinese

    groups = (
        ("firm touchdown", "hard landing", "bounced landing"),
        ("landing distance", "stopping distance"),
        ("braking action", "braking capability", "braking force"),
        ("reverse thrust", "thrust reverser", "reverse idle"),
        ("wet runway", "slippery runway", "contaminated runway"),
        ("main landing gear", "main gear touchdown"),
        ("engine failure", "engine inoperative"),
        ("speedbrake", "spoiler", "ground spoiler"),
        ("upset recovery", "stall recovery"),
        ("de-crab", "sideslip technique"),
    )
    problems: list[str] = []
    for group in groups:
        missing = [key for key in group if key not in translations]
        if missing:
            problems.append(f"missing semantic-boundary term(s): {', '.join(missing)}")
            continue
        values = [translations[key] for key in group]
        if len(set(values)) != len(values):
            problems.append(f"collapsed semantic boundary: {group} -> {values}")
    return problems


def main() -> None:
    problems = markdown_links() + public_content() + terminology_conflicts() + semantic_distinctions()
    if problems:
        raise SystemExit("\n".join(problems))
    count = sum(
        len(table_rows(path))
        for path in (ROOT / "references" / "glossary.md", ROOT / "references" / "fctm_zh_usage.md")
    )
    print(f"package validation passed; terminology rows: {count}")


if __name__ == "__main__":
    main()
