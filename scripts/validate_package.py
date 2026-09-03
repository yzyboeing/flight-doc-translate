#!/usr/bin/env python3
"""Validate public-package safety and terminology-table consistency."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {".pdf", ".docx", ".zip", ".txt", ".jsonl", ".png", ".jpg", ".jpeg"}
ABSOLUTE_LOCAL_PATH = re.compile(r"/(?:Users|home)/[^\s`\"']+")
INTERNAL_DOC_ID = re.compile(r"\b(?:D\d|[A-Z]{2,5})-\d[A-Z0-9-]{2,}\b")
AIRCRAFT_REGISTRY = re.compile(r"\bB-\d{4}\b")
SHA256_VALUE = re.compile(r"\b[0-9a-fA-F]{64}\b")
PERSONAL_BYLINE = re.compile(
    r"Translated\s+by|Proofread\s+by|Verified\s+by|编译\s*[/：:]|校对\s*[/：:]|审核\s*[/：:]",
    re.IGNORECASE,
)
EXPECTED_TOPIC_MODULES = {
    "chapter_1_general_information.md": 45,
    "chapter_2_ground_operations.md": 40,
    "chapter_3_takeoff_initial_climb.md": 50,
    "chapter_4_climb_cruise_descent_holding.md": 45,
    "chapter_5_approach_missed_approach.md": 60,
    "chapter_6_landing.md": 120,
    "chapter_7_maneuvers.md": 50,
    "chapter_8_non_normal_operations.md": 70,
}
EXPECTED_QRH_MODULES = {
    "checklist_structure.md": 30,
    "airframe_air_anti_ice_communications.md": 18,
    "electrical_engines_apu_fire.md": 18,
    "flight_controls_instruments_navigation.md": 14,
    "fuel_hydraulics_landing_gear_warnings.md": 18,
    "performance_and_maneuvers.md": 14,
}
ALLOWED_STATUS = {"已对齐", "等义对照", "风格候选", "冲突", "废弃"}
ALLOWED_CONFIDENCE = {"高", "中", "低", "语境相关"}


def reference_markdown() -> list[Path]:
    return sorted((ROOT / "references").rglob("*.md"))


def terminology_sources() -> list[Path]:
    return [
        ROOT / "references" / "glossary.md",
        ROOT / "references" / "fctm_zh_usage.md",
        *sorted((ROOT / "references" / "fctm_topics").glob("*.md")),
        ROOT / "references" / "qrh_zh_usage.md",
        ROOT / "references" / "operator_zh_style.md",
        *sorted((ROOT / "references" / "qrh_topics").glob("*.md")),
    ]


def topic_module_completeness() -> list[str]:
    problems: list[str] = []
    topic_dir = ROOT / "references" / "fctm_topics"
    actual = {path.name for path in topic_dir.glob("*.md")}
    expected = set(EXPECTED_TOPIC_MODULES)
    for name in sorted(expected - actual):
        problems.append(f"missing FCTM topic module: {name}")
    for name in sorted(actual - expected):
        problems.append(f"unexpected FCTM topic module: {name}")
    for name, minimum_rows in EXPECTED_TOPIC_MODULES.items():
        path = topic_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for heading in ("## 适用场景", "## 高复用句式框架", "## 易混边界"):
            if heading not in text:
                problems.append(f"missing section in {name}: {heading}")
        row_count = len(table_rows(path))
        if row_count < minimum_rows:
            problems.append(f"too few terminology rows in {name}: {row_count} < {minimum_rows}")
    return problems


def qrh_module_completeness() -> list[str]:
    problems: list[str] = []
    topic_dir = ROOT / "references" / "qrh_topics"
    actual = {path.name for path in topic_dir.glob("*.md")}
    expected = set(EXPECTED_QRH_MODULES)
    for name in sorted(expected - actual):
        problems.append(f"missing QRH topic module: {name}")
    for name in sorted(actual - expected):
        problems.append(f"unexpected QRH topic module: {name}")
    for name, minimum_rows in EXPECTED_QRH_MODULES.items():
        path = topic_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for heading in ("## 适用场景", "## 高复用术语与搭配", "## 易混边界"):
            if heading not in text:
                problems.append(f"missing section in {name}: {heading}")
        if "## 高复用句式框架" not in text and "## 动作与状态框架" not in text:
            problems.append(f"missing pattern section in {name}")
        row_count = len(table_rows(path))
        if row_count < minimum_rows:
            problems.append(f"too few terminology rows in {name}: {row_count} < {minimum_rows}")
    return problems


def markdown_links() -> list[str]:
    problems: list[str] = []
    for source in [ROOT / "README.md", ROOT / "SKILL.md", *reference_markdown()]:
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
        internal_id = INTERNAL_DOC_ID.search(text)
        if internal_id:
            problems.append(f"internal document id in {path.relative_to(ROOT)}: {internal_id.group(0)}")
        registry = AIRCRAFT_REGISTRY.search(text)
        if registry:
            problems.append(f"aircraft registry in {path.relative_to(ROOT)}: {registry.group(0)}")
        digest = SHA256_VALUE.search(text)
        if digest:
            problems.append(f"file hash in {path.relative_to(ROOT)}: {digest.group(0)}")
        byline = PERSONAL_BYLINE.search(text)
        if byline:
            problems.append(f"personal byline in {path.relative_to(ROOT)}: {byline.group(0)}")
    return problems


def structured_table_schema() -> list[str]:
    problems: list[str] = []
    candidates = [
        ROOT / "references" / "operator_zh_style.md",
        *sorted((ROOT / "references" / "qrh_topics").glob("*.md")),
    ]
    for path in candidates:
        if not path.exists():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells[0].lower() in {"english", "english cue"} or not cells[0] or set(cells[0]) <= {"-", ":"}:
                continue
            if len(cells) == 3:
                continue
            if len(cells) != 10:
                problems.append(
                    f"structured row must have 10 columns: {path.relative_to(ROOT)}:{line_number}"
                )
                continue
            if cells[8] not in ALLOWED_STATUS:
                problems.append(
                    f"invalid status {cells[8]!r}: {path.relative_to(ROOT)}:{line_number}"
                )
            if cells[9] not in ALLOWED_CONFIDENCE:
                problems.append(
                    f"invalid confidence {cells[9]!r}: {path.relative_to(ROOT)}:{line_number}"
                )
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


def terminology_family(path: Path) -> str:
    if path.name == "operator_zh_style.md" or "qrh_topics" in path.parts or path.name == "qrh_zh_usage.md":
        return "qrh"
    return "fctm-general"


def terminology_conflicts() -> list[str]:
    sources = terminology_sources()
    index: dict[tuple[str, str], list[tuple[str, str, int]]] = defaultdict(list)
    for source in sources:
        for key, chinese, line in table_rows(source):
            index[(terminology_family(source), key)].append(
                (str(source.relative_to(ROOT)), chinese, line)
            )

    problems: list[str] = []
    for (family, key), values in sorted(index.items()):
        if len(values) > 1 and len({value[1] for value in values}) > 1:
            locations = ", ".join(f"{source}:{line}={chinese}" for source, chinese, line in values)
            problems.append(f"conflicting term {key!r} in {family}: {locations}")
    return problems


def eval_schema() -> list[str]:
    path = ROOT / "evals" / "translation_cases.yaml"
    if not path.exists():
        return ["missing behavior evals: evals/translation_cases.yaml"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"invalid behavior eval file: {exc}"]
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 10:
        return ["behavior evals must contain at least 10 cases"]
    problems: list[str] = []
    required_types = {"FCTM", "QRH", "mixed", "revision"}
    found_types: set[str] = set()
    ids: set[str] = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            problems.append(f"behavior eval {index} is not an object")
            continue
        missing = {"id", "document_type", "source", "expected", "forbidden"} - set(case)
        if missing:
            problems.append(f"behavior eval {index} missing: {', '.join(sorted(missing))}")
            continue
        case_id = case["id"]
        if case_id in ids:
            problems.append(f"duplicate behavior eval id: {case_id}")
        ids.add(case_id)
        found_types.add(case["document_type"])
        if not case["expected"] or not isinstance(case["expected"], list):
            problems.append(f"behavior eval {case_id} has no expected checks")
        if not isinstance(case["forbidden"], list):
            problems.append(f"behavior eval {case_id} has invalid forbidden checks")
    missing_types = required_types - found_types
    if missing_types:
        problems.append(f"behavior evals missing document types: {', '.join(sorted(missing_types))}")
    return problems


def semantic_distinctions() -> list[str]:
    sources = terminology_sources()
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
    problems = (
        topic_module_completeness()
        + qrh_module_completeness()
        + markdown_links()
        + public_content()
        + structured_table_schema()
        + terminology_conflicts()
        + semantic_distinctions()
        + eval_schema()
    )
    if problems:
        raise SystemExit("\n".join(problems))
    count = sum(
        len(table_rows(path))
        for path in terminology_sources()
    )
    print(f"package validation passed; terminology rows: {count}")


if __name__ == "__main__":
    main()
