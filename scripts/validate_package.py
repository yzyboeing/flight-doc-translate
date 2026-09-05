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
MAX_SKILL_BYTES = 12_000
REQUIRED_EVAL_COVERAGE = {
    "no_addition",
    "example_scope",
    "modal_strength",
    "no_invented_structure",
    "no_invented_visual_semantics",
    "review_notice",
    "cjk_preflight",
    "stitched_overlap",
    "source_doubt_reporting",
    "qrh_branching",
    "document_type_routing",
    "missing_input_recovery",
    "execution_failure_recovery",
    "scope_boundary",
}
MIN_TRIGGER_CASES_PER_CLASS = 10


def reference_markdown() -> list[Path]:
    return sorted((ROOT / "references").rglob("*.md"))


def entrypoint_quality() -> list[str]:
    path = ROOT / "SKILL.md"
    size = len(path.read_bytes())
    problems: list[str] = []
    if size > MAX_SKILL_BYTES:
        problems.append(f"SKILL.md is too large for progressive disclosure: {size} > {MAX_SKILL_BYTES}")
    required_links = {
        "references/fidelity.md",
        "references/standing_decisions.md",
        "references/source_authority.md",
        "references/preflight_review.md",
        "references/docx_production.md",
        "references/terminology_maintenance.md",
    }
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        problems.append("SKILL.md must start with YAML frontmatter")
    frontmatter_match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter_match:
        problems.append("SKILL.md has invalid or unterminated YAML frontmatter")
    else:
        frontmatter = frontmatter_match.group(1)
        if not re.search(r"^name:\s+flight-doc-translate\s*$", frontmatter, re.MULTILINE):
            problems.append("SKILL.md frontmatter name must match the skill directory")
        description_match = re.search(r'^description:\s+"(.+)"\s*$', frontmatter, re.MULTILINE)
        if not description_match:
            problems.append("SKILL.md description must be a quoted single-line string")
        else:
            description = description_match.group(1)
            if len(description) > 500:
                problems.append(f"SKILL.md description is too long for discovery: {len(description)} > 500")
            if not any(cue in description for cue in ("翻一下这份", "译成中文", "做成中文版")):
                problems.append("SKILL.md description lacks a realistic positive trigger phrase")
            if "不用于" not in description:
                problems.append("SKILL.md description lacks an explicit negative boundary")
    for link in sorted(required_links):
        if link not in text:
            problems.append(f"SKILL.md does not route to required reference: {link}")
    return problems


def workflow_invariants() -> list[str]:
    required_markers = {
        "SKILL.md": (
            "不在启动时完整读取",
            "原文疑点清单",
            "Markdown／纯文本",
            "## 异常与失败",
            "不得声称成功",
            "一次只问一个最关键问题",
            "## 做完汇报",
        ),
        "references/fidelity.md": (
            "当前只有 SD-4 覆盖第 6 条的纸面部分",
            "照译 + 报告",
            "SD-2 取消了原有交付控制信息例外",
        ),
        "references/standing_decisions.md": (
            "非术语长期决策的唯一记录",
            "单次任务答复不得自动提升为长期决策",
        ),
        "references/preflight_review.md": (
            "CJK 字体",
            "拼接截图",
            "对话中的独立“交付说明”",
        ),
        "references/docx_production.md": (
            "单页烟雾测试",
            "覆盖图层",
            "逐页内容连续性检查",
        ),
        "references/revising_existing_translation.md": (
            "正文照译且不加译注",
            "原文疑点清单",
        ),
    }
    problems: list[str] = []
    for relative, markers in required_markers.items():
        path = ROOT / relative
        if not path.exists():
            problems.append(f"missing workflow reference: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                problems.append(f"missing workflow invariant in {relative}: {marker}")
    return problems


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
    if payload.get("schema_version") != 2:
        return ["behavior evals must use semantic schema_version 2"]
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 18:
        return ["behavior evals must contain at least 18 cases"]
    problems: list[str] = []
    required_types = {"FCTM", "QRH", "mixed", "revision", "layout"}
    found_types: set[str] = set()
    found_coverage: set[str] = set()
    ids: set[str] = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            problems.append(f"behavior eval {index} is not an object")
            continue
        missing = {
            "id",
            "document_type",
            "coverage",
            "prompt",
            "source",
            "pass_criteria",
            "failure_conditions",
        } - set(case)
        if missing:
            problems.append(f"behavior eval {index} missing: {', '.join(sorted(missing))}")
            continue
        if "expected" in case or "forbidden" in case:
            problems.append(f"behavior eval {index} uses deprecated exact-match fields")
        case_id = case["id"]
        if case_id in ids:
            problems.append(f"duplicate behavior eval id: {case_id}")
        ids.add(case_id)
        found_types.add(case["document_type"])
        coverage = case["coverage"]
        if not isinstance(coverage, list) or not coverage or not all(isinstance(x, str) and x for x in coverage):
            problems.append(f"behavior eval {case_id} has invalid coverage")
        else:
            found_coverage.update(coverage)
        if not isinstance(case["pass_criteria"], list) or not case["pass_criteria"]:
            problems.append(f"behavior eval {case_id} has no semantic pass criteria")
        if not isinstance(case["failure_conditions"], list) or not case["failure_conditions"]:
            problems.append(f"behavior eval {case_id} has no failure conditions")
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            problems.append(f"behavior eval {case_id} has no prompt")
        if not isinstance(case["source"], str) or not case["source"].strip():
            problems.append(f"behavior eval {case_id} has no source")
    missing_types = required_types - found_types
    if missing_types:
        problems.append(f"behavior evals missing document types: {', '.join(sorted(missing_types))}")
    missing_coverage = REQUIRED_EVAL_COVERAGE - found_coverage
    if missing_coverage:
        problems.append(f"behavior evals missing coverage: {', '.join(sorted(missing_coverage))}")
    return problems


def trigger_eval_schema() -> list[str]:
    path = ROOT / "evals" / "trigger_cases.yaml"
    if not path.exists():
        return ["missing trigger evals: evals/trigger_cases.yaml"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"invalid trigger eval file: {exc}"]
    if payload.get("schema_version") != 1:
        return ["trigger evals must use schema_version 1"]
    cases = payload.get("cases")
    if not isinstance(cases, list):
        return ["trigger evals cases must be a list"]
    problems: list[str] = []
    ids: set[str] = set()
    class_counts = {True: 0, False: 0}
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            problems.append(f"trigger eval {index} is not an object")
            continue
        missing = {"id", "prompt", "should_trigger", "reason"} - set(case)
        if missing:
            problems.append(f"trigger eval {index} missing: {', '.join(sorted(missing))}")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            problems.append(f"trigger eval {index} has invalid id")
        elif case_id in ids:
            problems.append(f"duplicate trigger eval id: {case_id}")
        ids.add(case_id)
        expected = case["should_trigger"]
        if not isinstance(expected, bool):
            problems.append(f"trigger eval {case_id} should_trigger must be boolean")
        else:
            class_counts[expected] += 1
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            problems.append(f"trigger eval {case_id} has no prompt")
        if not isinstance(case["reason"], str) or not case["reason"].strip():
            problems.append(f"trigger eval {case_id} has no reason")
    for expected, label in ((True, "positive"), (False, "negative")):
        if class_counts[expected] < MIN_TRIGGER_CASES_PER_CLASS:
            problems.append(
                f"trigger evals need at least {MIN_TRIGGER_CASES_PER_CLASS} {label} cases; "
                f"found {class_counts[expected]}"
            )
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
        entrypoint_quality()
        + workflow_invariants()
        + topic_module_completeness()
        + qrh_module_completeness()
        + markdown_links()
        + public_content()
        + structured_table_schema()
        + terminology_conflicts()
        + semantic_distinctions()
        + eval_schema()
        + trigger_eval_schema()
    )
    if problems:
        raise SystemExit("\n".join(problems))
    count = sum(
        len(table_rows(path))
        for path in terminology_sources()
    )
    behavior_cases = len(json.loads((ROOT / "evals" / "translation_cases.yaml").read_text())["cases"])
    trigger_cases = len(json.loads((ROOT / "evals" / "trigger_cases.yaml").read_text())["cases"])
    print(
        "package validation passed; "
        f"terminology rows: {count}; behavior evals: {behavior_cases}; trigger evals: {trigger_cases}"
    )


if __name__ == "__main__":
    main()
