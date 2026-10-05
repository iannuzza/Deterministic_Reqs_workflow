#!/usr/bin/env python3
"""Generate a readable Stage 0 ontology analysis report.

This script synthesizes ontology baseline artifacts and Stage 1 extracted
requirements into a human-readable Stage 0 report used for Gate 0 review.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


PLACEHOLDER_RE = re.compile(r"<[^>]+>")


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def _contains_placeholders(text: str) -> bool:
    return bool(PLACEHOLDER_RE.search(text))


def _load_requirements(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _severity_counts(semantic_text: str) -> Dict[str, int]:
    def section_lines(title: str) -> List[str]:
        m = re.search(rf"^##\s+{title}\s*$", semantic_text, flags=re.IGNORECASE | re.MULTILINE)
        if not m:
            return []
        start = m.end()
        nxt = re.search(r"^##\s+", semantic_text[start:], flags=re.MULTILINE)
        block = semantic_text[start : start + nxt.start()] if nxt else semantic_text[start:]
        return [ln.strip() for ln in block.splitlines() if ln.strip().startswith("-")]

    counts: Dict[str, int] = {}
    for sev in ("Critical", "Major", "Minor"):
        lines = section_lines(sev)
        counts[sev.lower()] = 0 if not lines or lines == ["- None"] else len(lines)
    return counts


def _extract_page(source: str) -> int:
    m = re.search(r"\(page\s+(\d+)\)", source, flags=re.IGNORECASE)
    return int(m.group(1)) if m else -1


def _summarize_requirements(rows: List[Dict[str, str]]) -> Dict[str, object]:
    category_counts: Counter = Counter()
    class_counts: Counter = Counter()
    type_counts: Counter = Counter()
    evidence_counts: Counter = Counter()
    pages: set[int] = set()
    category_samples: Dict[str, List[Tuple[str, str]]] = {"System": [], "Analog": [], "Digital": []}

    for row in rows:
        category = (row.get("category") or "").strip() or "Unknown"
        content_class = (row.get("content_class") or "").strip() or "Unknown"
        req_type = (row.get("requirement_type") or "").strip() or "Unknown"
        evidence = (row.get("evidence_type") or "").strip() or "Unknown"
        req_id = (row.get("id") or "").strip()
        stmt = (row.get("requirement_statement") or "").strip()
        source = (row.get("source") or "").strip()

        category_counts[category] += 1
        class_counts[content_class] += 1
        type_counts[req_type] += 1
        evidence_counts[evidence] += 1

        pg = _extract_page(source)
        if pg > 0:
            pages.add(pg)

        if category in category_samples and req_id and stmt and len(category_samples[category]) < 3:
            short_stmt = re.sub(r"\s+", " ", stmt)
            if len(short_stmt) > 140:
                short_stmt = short_stmt[:137] + "..."
            category_samples[category].append((req_id, short_stmt))

    return {
        "total": len(rows),
        "category_counts": category_counts,
        "class_counts": class_counts,
        "type_counts": type_counts,
        "evidence_counts": evidence_counts,
        "page_count": len(pages),
        "category_samples": category_samples,
    }


def _top_counter_lines(counter: Counter, max_items: int = 6) -> List[str]:
    if not counter:
        return ["- None"]
    lines: List[str] = []
    for key, value in counter.most_common(max_items):
        label = key if key else "Unknown"
        lines.append(f"- {label}: {value}")
    return lines


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    context_path = repo_root / "config/project_context.json"
    ontology_path = repo_root / "artifacts/stage0_ontology/ontology.md"
    glossary_path = repo_root / "artifacts/stage0_ontology/glossary.csv"
    semantic_path = repo_root / "artifacts/stage0_ontology/semantic_issues.md"
    req_csv_path = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    out_path = repo_root / "artifacts/orchestrator/stage_00_report.md"

    context = {}
    if context_path.exists():
        try:
            context = json.loads(context_path.read_text(encoding="utf-8"))
        except Exception:
            context = {}

    source_spec = str(context.get("source_spec_path") or "unknown")
    source_type = Path(source_spec).suffix.lower().lstrip(".") or "unknown"
    ocr_index = str(context.get("ocr_index_path") or "artifacts/stage1_requirements/ocr_extracts/index.csv")

    ontology_text = _read_text(ontology_path)
    semantic_text = _read_text(semantic_path)
    glossary_text = _read_text(glossary_path)
    requirements = _load_requirements(req_csv_path)
    req_summary = _summarize_requirements(requirements)

    glossary_rows = 0
    if glossary_text:
        glossary_rows = max(0, len([ln for ln in glossary_text.splitlines() if ln.strip()]) - 1)

    sev = _severity_counts(semantic_text)
    ontology_is_template = _contains_placeholders(ontology_text)
    glossary_is_template = _contains_placeholders(glossary_text)

    ontology_lower = ontology_text.lower()
    has_concept_map = "## concept map" in ontology_lower
    has_requirements_model = "## requirements model" in ontology_lower
    has_formal_schema = "## formal schema" in ontology_lower
    has_auto_checks_basis = "## automatic checks and traceability basis" in ontology_lower

    gate_recommendation = "go" if sev["critical"] == 0 else "no-go"
    gate_status = "pass" if gate_recommendation == "go" else "fail"

    lines: List[str] = [
        "# Stage 00 Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Executive Summary",
        "- Ontology study definition: identifying and formalizing key concepts, properties, and relationships so the system is unambiguous and consistently modeled.",
        f"- Source specification: {source_spec}",
        f"- Source type: {source_type}",
        f"- OCR provenance index: {ocr_index}",
        f"- Requirements analyzed (from Stage 1 summary): {req_summary['total']}",
        f"- Category coverage: System={req_summary['category_counts'].get('System', 0)}, Analog={req_summary['category_counts'].get('Analog', 0)}, Digital={req_summary['category_counts'].get('Digital', 0)}",
        f"- Semantic issues: critical={sev['critical']}, major={sev['major']}, minor={sev['minor']}",
        f"- Gate 0 recommendation: {gate_recommendation}",
        "",
        "## Stage 0 Artifacts Health",
        f"- ontology.md exists: {'yes' if ontology_path.exists() else 'no'}",
        f"- glossary.csv exists: {'yes' if glossary_path.exists() else 'no'}",
        f"- semantic_issues.md exists: {'yes' if semantic_path.exists() else 'no'}",
        f"- ontology.md contains template placeholders: {'yes' if ontology_is_template else 'no'}",
        f"- glossary.csv contains template placeholders: {'yes' if glossary_is_template else 'no'}",
        f"- Glossary entries (excluding header): {glossary_rows}",
        "",
        "## Ontology-Study Deliverables",
        f"- Glossary of terms: {'yes' if glossary_rows > 0 else 'no'}",
        f"- Concept map: {'yes' if has_concept_map else 'no'}",
        f"- Requirements model: {'yes' if has_requirements_model else 'no'}",
        f"- Formal schema: {'yes' if has_formal_schema else 'no'}",
        f"- Automatic checks and traceability basis: {'yes' if has_auto_checks_basis else 'no'}",
        "",
        "## System / Analog / Digital Analysis",
        f"- System requirements count: {req_summary['category_counts'].get('System', 0)}",
        f"- Analog requirements count: {req_summary['category_counts'].get('Analog', 0)}",
        f"- Digital requirements count: {req_summary['category_counts'].get('Digital', 0)}",
        f"- Distinct source pages represented: {req_summary['page_count']}",
        "",
        "### Sample Requirements By Category",
        "- System:",
    ]

    system_samples = req_summary["category_samples"].get("System", [])
    if system_samples:
        lines.extend([f"  - {req_id}: {stmt}" for req_id, stmt in system_samples])
    else:
        lines.append("  - None")

    lines.append("- Analog:")
    analog_samples = req_summary["category_samples"].get("Analog", [])
    if analog_samples:
        lines.extend([f"  - {req_id}: {stmt}" for req_id, stmt in analog_samples])
    else:
        lines.append("  - None")

    lines.append("- Digital:")
    digital_samples = req_summary["category_samples"].get("Digital", [])
    if digital_samples:
        lines.extend([f"  - {req_id}: {stmt}" for req_id, stmt in digital_samples])
    else:
        lines.append("  - None")

    lines.extend(
        [
            "",
            "## Classification Summary",
            "### Content Class",
            *_top_counter_lines(req_summary["class_counts"]),
            "",
            "### Requirement Type",
            *_top_counter_lines(req_summary["type_counts"]),
            "",
            "### Evidence Type",
            *_top_counter_lines(req_summary["evidence_counts"]),
            "",
            "## Semantic Issues And Blockers",
            f"- Critical: {sev['critical']}",
            f"- Major: {sev['major']}",
            f"- Minor: {sev['minor']}",
            f"- Stage 1 handoff impact: {'blocked' if sev['critical'] > 0 else 'not blocked'}",
            "",
            "## Notes",
            "- This report is generated automatically from current Stage 0/Stage 1 artifacts.",
            "- If ontology/glossary placeholders are still present, run the ontology authoring step before Gate 0 sign-off.",
            "",
            "## Status",
            f"- Gate 0: {gate_status}",
            f"- Stage 1 handoff recommendation: {gate_recommendation}",
        ]
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Stage 0 ontology report: GENERATED ({out_path})")
    _append_log(
        repo_root,
        script_name,
        (
            f"PASS requirements={req_summary['total']} "
            f"system={req_summary['category_counts'].get('System', 0)} "
            f"analog={req_summary['category_counts'].get('Analog', 0)} "
            f"digital={req_summary['category_counts'].get('Digital', 0)} "
            f"critical={sev['critical']} recommendation={gate_recommendation}"
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
