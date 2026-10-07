#!/usr/bin/env python3
"""Run ontology crosscheck for Stage 0 outputs."""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from repo_paths import resolve_repo_path


REQUIRED = [
    "artifacts/stage0_ontology/ontology.md",
    "artifacts/stage0_ontology/glossary.csv",
    "artifacts/stage0_ontology/semantic_issues.md",
    "artifacts/stage0_ontology/evidence_registry.csv",
    "artifacts/orchestrator/stage_00_report.md",
]

PLACEHOLDER_RE = re.compile(r"<[^>]+>")
TABLE_REF_RE = re.compile(r"\bTable\s+(?P<num>\d+)\b", re.IGNORECASE)
FIGURE_REF_RE = re.compile(r"\bFigure\s+(?P<num>\d+)\b", re.IGNORECASE)
IMAGE_REF_RE = re.compile(r"\bImage\s+(?P<num>\d+)\b", re.IGNORECASE)
TABLE_CAPTION_RE = re.compile(r"^\s*Table\s+(?P<num>\d+)\s*[.:\-]\s*", re.IGNORECASE)
FIGURE_CAPTION_RE = re.compile(r"^\s*Figure\s+(?P<num>\d+)\s*[.:\-]\s*", re.IGNORECASE)
IMAGE_CAPTION_RE = re.compile(r"^\s*Image\s+(?P<num>\d+)\s*[.:\-]\s*", re.IGNORECASE)


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _load_project_context(repo_root: Path) -> dict:
    ctx = repo_root / "config/project_context.json"
    if not ctx.exists():
        return {}
    try:
        data = json.loads(ctx.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _resolve_path(repo_root: Path, raw: str) -> Path:
    return resolve_repo_path(repo_root, raw)


def _collect_detected_struct_refs(repo_root: Path) -> tuple[set[str], set[str]]:
    ctx = _load_project_context(repo_root)
    idx_rel = str(ctx.get("ocr_index_path") or "").strip()
    if not idx_rel:
        return set(), set()

    idx_path = _resolve_path(repo_root, idx_rel)
    if not idx_path.exists():
        return set(), set()

    detected_tables: set[str] = set()
    detected_figures: set[str] = set()

    try:
        with idx_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except Exception:
        return set(), set()

    for row in rows:
        text_file = (row.get("text_file") or "").strip()
        if not text_file:
            continue
        txt_path = _resolve_path(repo_root, text_file)
        if not txt_path.exists():
            continue
        try:
            lines = txt_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue

        for line in lines:
            raw = line.strip()
            if not raw:
                continue
            mt = TABLE_CAPTION_RE.match(raw)
            if mt:
                detected_tables.add(f"Table {mt.group('num')}")
            mf = FIGURE_CAPTION_RE.match(raw)
            if mf:
                detected_figures.add(f"Figure {mf.group('num')}")
            mi = IMAGE_CAPTION_RE.match(raw)
            if mi:
                detected_figures.add(f"Image {mi.group('num')}")

    return detected_tables, detected_figures


def _collect_mapped_struct_refs(evidence_rows: list[dict[str, str]]) -> tuple[set[str], set[str]]:
    mapped_tables: set[str] = set()
    mapped_figures: set[str] = set()

    for row in evidence_rows:
        text = " ".join(
            [
                (row.get("source_locator") or ""),
                (row.get("caption_or_title") or ""),
                (row.get("extracted_information") or ""),
                (row.get("notes") or ""),
            ]
        )
        for m in TABLE_REF_RE.finditer(text):
            mapped_tables.add(f"Table {m.group('num')}")
        for m in FIGURE_REF_RE.finditer(text):
            mapped_figures.add(f"Figure {m.group('num')}")
        for m in IMAGE_REF_RE.finditer(text):
            mapped_figures.add(f"Image {m.group('num')}")

    return mapped_tables, mapped_figures


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    missing: list[str] = []
    for rel in REQUIRED:
        if not (repo_root / rel).exists():
            missing.append(rel)

    findings: list[str] = []
    status = "pass"

    ontology = repo_root / "artifacts/stage0_ontology/ontology.md"
    glossary = repo_root / "artifacts/stage0_ontology/glossary.csv"
    sem = repo_root / "artifacts/stage0_ontology/semantic_issues.md"
    stage0_report = repo_root / "artifacts/orchestrator/stage_00_report.md"
    evidence_registry = repo_root / "artifacts/stage0_ontology/evidence_registry.csv"
    glossary_table_rows = 0
    glossary_image_rows = 0
    glossary_table_caption_rows = 0
    glossary_image_caption_rows = 0

    concept_count = 0
    glossary_rows = 0
    req_total = 0
    req_table = 0
    req_image = 0
    req_mode = 0
    detected_table_ids_count = 0
    detected_figure_ids_count = 0
    mapped_table_ids_count = 0
    mapped_figure_ids_count = 0
    missing_table_ids: list[str] = []
    missing_figure_ids: list[str] = []

    if ontology.exists():
        ont_text = ontology.read_text(encoding="utf-8", errors="ignore")
        ont_lower = ont_text.lower()
        if PLACEHOLDER_RE.search(ont_text):
            findings.append("ontology.md still contains template placeholders")
            status = "fail"
        concept_count = len(re.findall(r"\bONT_(SYS|ANA|DIG)_\d{3}\b", ont_text))
        if concept_count < 5:
            findings.append(f"ontology.md has too few ontology IDs (found {concept_count}, expected >= 5)")
            status = "fail"
        for marker in (
            "## concept map",
            "## requirements model",
            "## formal schema",
            "## automatic checks and traceability basis",
        ):
            if marker not in ont_lower:
                findings.append(f"ontology.md is missing required ontology-study section: {marker.replace('## ', '')}")
                status = "fail"
    
    if glossary.exists():
        gloss_text = glossary.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER_RE.search(gloss_text):
            findings.append("glossary.csv still contains template placeholders")
            status = "fail"
        try:
            with glossary.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
                headers = set(reader.fieldnames or [])
            glossary_rows = len(rows)
            if glossary_rows < 5:
                findings.append(f"glossary.csv has too few data rows (found {glossary_rows}, expected >= 5)")
                status = "fail"
            required_headers = {
                "evidence_origin_type",
                "evidence_caption_or_title",
                "evidence_extracted_information",
            }
            if not required_headers.issubset(headers):
                findings.append("glossary.csv is missing structured evidence columns for ontology study")
                status = "fail"
            for row in rows:
                origin = (row.get("evidence_origin_type") or "").strip().lower()
                caption = (row.get("evidence_caption_or_title") or "").strip()
                if origin == "table":
                    glossary_table_rows += 1
                    if caption:
                        glossary_table_caption_rows += 1
                if origin == "image":
                    glossary_image_rows += 1
                    if caption:
                        glossary_image_caption_rows += 1
        except Exception:
            findings.append("glossary.csv could not be parsed as CSV")
            status = "fail"

    if evidence_registry.exists():
        try:
            with evidence_registry.open("r", encoding="utf-8", newline="") as handle:
                ev_rows = list(csv.DictReader(handle))
            if not ev_rows:
                findings.append("evidence_registry.csv is empty")
                status = "fail"
            else:
                detected_tables, detected_figures = _collect_detected_struct_refs(repo_root)
                mapped_tables, mapped_figures = _collect_mapped_struct_refs(ev_rows)

                detected_table_ids_count = len(detected_tables)
                detected_figure_ids_count = len(detected_figures)
                mapped_table_ids_count = len(mapped_tables)
                mapped_figure_ids_count = len(mapped_figures)

                missing_table_ids = sorted(detected_tables - mapped_tables)
                missing_figure_ids = sorted(detected_figures - mapped_figures)

                if missing_table_ids:
                    findings.append(
                        "Detected OCR table IDs missing ontology evidence mapping: "
                        + ", ".join(missing_table_ids[:20])
                        + (" ..." if len(missing_table_ids) > 20 else "")
                    )
                    status = "fail"
                if missing_figure_ids:
                    findings.append(
                        "Detected OCR figure/image IDs missing ontology evidence mapping: "
                        + ", ".join(missing_figure_ids[:20])
                        + (" ..." if len(missing_figure_ids) > 20 else "")
                    )
                    status = "fail"
        except Exception:
            findings.append("evidence_registry.csv could not be parsed as CSV")
            status = "fail"

    req_csv = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    if req_csv.exists():
        try:
            with req_csv.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            req_total = len(rows)
            for row in rows:
                src = (row.get("source") or "").lower()
                stmt = (row.get("requirement_statement") or "").lower()
                ev = (row.get("evidence_type") or "").lower()
                notes = (row.get("notes") or "").lower()
                if "table" in src or "table" in ev or "table" in notes:
                    req_table += 1
                if "figure" in src or "diagram" in src or "image" in ev or "diagram" in notes or "image" in notes:
                    req_image += 1
                if "mode" in stmt or "mode" in src:
                    req_mode += 1
        except Exception:
            findings.append("requirements_summary.csv could not be parsed for coverage checks")
            status = "fail"

    if req_total > 0:
        if req_table == 0:
            findings.append("No table-derived requirements detected in requirements summary")
            status = "fail"
        if req_image == 0:
            findings.append("No image/diagram-derived requirements detected in requirements summary")
            status = "fail"

    if glossary_rows > 0:
        if glossary_table_rows == 0:
            findings.append("No table-origin ontology concepts detected in glossary evidence columns")
            status = "fail"
        if glossary_image_rows == 0:
            findings.append("No image-origin ontology concepts detected in glossary evidence columns")
            status = "fail"
        if glossary_table_caption_rows == 0:
            findings.append("No table caption/title evidence captured in glossary")
            status = "fail"
        if glossary_image_caption_rows == 0:
            findings.append("No image/figure caption evidence captured in glossary")
            status = "fail"

    if sem.exists():
        sem_text = sem.read_text(encoding="utf-8", errors="ignore")
        sem_lower = sem_text.lower()
        if PLACEHOLDER_RE.search(sem_text):
            findings.append("semantic_issues.md still contains template placeholders")
            status = "fail"
        if "## critical" not in sem_lower or "## major" not in sem_lower or "## minor" not in sem_lower:
            findings.append("semantic_issues.md is missing required severity sections (Critical/Major/Minor)")
            status = "fail"
        if "critical" in sem_lower and "none" not in sem_lower:
            findings.append("Semantic issues include unresolved critical entries")
            status = "fail"

    if stage0_report.exists():
        report_text = stage0_report.read_text(encoding="utf-8", errors="ignore")
        report_lower = report_text.lower()
        if PLACEHOLDER_RE.search(report_text):
            findings.append("stage_00_report.md still contains template placeholders")
            status = "fail"
        if "gate 0" not in report_lower or "recommendation" not in report_lower:
            findings.append("stage_00_report.md does not include explicit gate decision/recommendation")
            status = "fail"

    if missing:
        status = "fail"
        findings.append("Missing required artifacts: " + ", ".join(missing))

    out = repo_root / "artifacts/orchestrator/stage_00_crosscheck_report.md"
    lines = [
        "# Stage 00 Crosscheck Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
        "",
        "## Quality Counters",
        f"- Ontology concept IDs: {concept_count}",
        f"- Glossary data rows: {glossary_rows}",
        f"- Requirements total: {req_total}",
        f"- Table-derived requirements: {req_table}",
        f"- Image/diagram-derived requirements: {req_image}",
        f"- Mode-related requirements: {req_mode}",
        f"- Glossary table-origin concepts: {glossary_table_rows}",
        f"- Glossary image-origin concepts: {glossary_image_rows}",
        f"- Glossary table captions captured: {glossary_table_caption_rows}",
        f"- Glossary image captions captured: {glossary_image_caption_rows}",
        f"- OCR-detected table IDs: {detected_table_ids_count}",
        f"- OCR-detected figure/image IDs: {detected_figure_ids_count}",
        f"- Mapped table IDs in ontology evidence: {mapped_table_ids_count}",
        f"- Mapped figure/image IDs in ontology evidence: {mapped_figure_ids_count}",
        f"- Missing table ID mappings: {len(missing_table_ids)}",
        f"- Missing figure/image ID mappings: {len(missing_figure_ids)}",
        "",
        "## Findings",
    ]
    if findings:
        lines.extend([f"- {f}" for f in findings])
    else:
        lines.append("- None")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if status != "pass":
        print(f"Ontology crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"Ontology crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
