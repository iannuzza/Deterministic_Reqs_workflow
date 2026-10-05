#!/usr/bin/env python3
"""Generic Stage 1 gate validator.

Checks minimum required artifacts for requirements extraction baseline.
"""

import csv
import json
import re
from pathlib import Path
from datetime import datetime
from validate_common_formatting import validate_stage_markdown


REQUIRED = [
    Path("artifacts/stage1_requirements/ocr_extracts/index.csv"),
    Path("artifacts/stage1_requirements/taxonomy_crosscheck.md"),
    Path("artifacts/stage1_requirements/requirements_raw.md"),
    Path("artifacts/stage1_requirements/requirements_summary.csv"),
    Path("artifacts/stage1_requirements/requirements_summary.md"),
    Path("artifacts/stage1_requirements/duplicate_source_req_ids.csv"),
    Path("artifacts/stage1_requirements/requirements_rag_crosscheck.md"),
    Path("artifacts/stage1_requirements/coverage_crosscheck.md"),
    Path("artifacts/stage1_requirements/missing_requirements_candidates.csv"),
    Path("artifacts/orchestrator/stage_01_report.md"),
]

REQUIRED_SUMMARY_COLUMNS = {
    "id",
    "source_req_id",
    "covered_source_req_id",
    "id_policy",
    "requirement_statement",
    "category",
    "source",
    "source_section_owner",
    "derivation_kind",
    "evidence_type",
    "notes",
    "rationale",
}


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _write_result(repo_root: Path, status: str, missing: list[str]) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_01_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 01 Result",
        "",
        f"- Timestamp: {timestamp}",
        f"- Status: {status}",
        "",
        "## Checked Files",
    ]
    lines.extend([f"- {path.as_posix()}" for path in REQUIRED])
    lines.append("")
    lines.append("## Missing Files")
    if missing:
        lines.extend([f"- {item}" for item in missing])
    else:
        lines.append("- None")
    result_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _validate_duplicate_source_ids(repo_root: Path) -> list[str]:
    report_path = repo_root / "artifacts/stage1_requirements/duplicate_source_req_ids.csv"
    with report_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [
        "Duplicate source requirement ID requires user resolution: "
        + (row.get("source_req_id") or "").strip()
        for row in rows
        if (row.get("source_req_id") or "").strip()
    ]


def _is_tagged_source_mode_enabled(repo_root: Path) -> bool:
    config_path = repo_root / "config/project_context.json"
    if not config_path.exists():
        return False
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(data, dict):
        return False
    rules = data.get("requirement_id_rules")
    if not isinstance(rules, dict):
        return False
    return bool(rules.get("tagged_source_mode", False))


def _validate_summary_contract(summary_csv: Path, strict_tagged_mode: bool = False) -> list[str]:
    findings: list[str] = []
    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = set(reader.fieldnames or [])
        missing_headers = sorted(REQUIRED_SUMMARY_COLUMNS - headers)
        if missing_headers:
            findings.append("requirements_summary.csv missing columns: " + ", ".join(missing_headers))
            return findings

        tagged_mismatch = 0
        generated_mismatch = 0
        generated_rows_in_tagged_mode = 0
        unknown_policy = 0
        row_count = 0

        for row in reader:
            row_count += 1
            rid = (row.get("id") or "").strip()
            source_req_id = (row.get("source_req_id") or "").strip()
            id_policy = (row.get("id_policy") or "").strip().lower()

            if id_policy == "tagged_preserve":
                if not source_req_id or rid != source_req_id:
                    tagged_mismatch += 1
            elif id_policy == "tagged_architecture":
                if not rid or source_req_id:
                    tagged_mismatch += 1
            elif id_policy == "generated_standard":
                if not rid:
                    generated_mismatch += 1
                if strict_tagged_mode:
                    generated_rows_in_tagged_mode += 1
            else:
                unknown_policy += 1

        if row_count == 0:
            findings.append("requirements_summary.csv has no rows")
        if tagged_mismatch:
            findings.append(f"tagged_preserve policy mismatches: {tagged_mismatch}")
        if generated_mismatch:
            findings.append(f"generated_standard policy mismatches: {generated_mismatch}")
        if strict_tagged_mode and generated_rows_in_tagged_mode:
            findings.append(f"strict tagged mode violation: generated_standard rows={generated_rows_in_tagged_mode}")
        if unknown_policy:
            findings.append(f"unknown id_policy rows: {unknown_policy}")

    return findings


def _validate_stage_evidence(repo_root: Path, summary_csv: Path) -> list[str]:
    findings: list[str] = []
    rag_path = repo_root / "artifacts/stage1_requirements/requirements_rag_crosscheck.md"
    coverage_path = repo_root / "artifacts/stage1_requirements/coverage_crosscheck.md"
    report_path = repo_root / "artifacts/orchestrator/stage_01_report.md"

    rag_text = rag_path.read_text(encoding="utf-8", errors="ignore")
    for label in ("RAG fail", "Rule-check fail"):
        match = re.search(rf"^- {re.escape(label)}:\s*(\d+)", rag_text, flags=re.MULTILINE | re.IGNORECASE)
        if match and int(match.group(1)) > 0:
            findings.append(f"{label} count is nonzero: {match.group(1)}")

    coverage_text = coverage_path.read_text(encoding="utf-8", errors="ignore").lower()
    if not re.search(r"status:\s*pass\b", coverage_text):
        findings.append("coverage_crosscheck.md status is not pass")

    report_text = report_path.read_text(encoding="utf-8", errors="ignore")
    if not re.search(r"^[-*]\s*Gate 1:\s*pass\s*$", report_text, flags=re.MULTILINE | re.IGNORECASE):
        findings.append("stage_01_report.md has no explicit Gate 1: pass decision")

    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    report_count = re.search(r"^- Total requirements listed:\s*(\d+)", report_text, flags=re.MULTILINE)
    if report_count and int(report_count.group(1)) != len(rows):
        findings.append(
            f"stage_01_report.md requirement count {report_count.group(1)} "
            f"does not match requirements_summary.csv rows {len(rows)}"
        )

    for row_number, row in enumerate(rows, start=2):
        notes = (row.get("notes") or "").strip()
        source = (row.get("source") or "").lower()
        if ("table" in notes.lower() or "table" in source or "figure" in notes.lower()) and "table_line_info=" not in notes:
            findings.append(f"summary row {row_number} is table/figure-derived without table_line_info")

    return findings


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, f"START cwd={Path.cwd().as_posix()}")
    missing = [str(p) for p in REQUIRED if not (repo_root / p).exists()]
    if missing:
        print("Stage 1: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        _write_result(repo_root, "FAIL", missing)
        _append_log(repo_root, script_name, f"FAIL missing={';'.join(missing)}")
        return 1

    summary_csv = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    strict_tagged_mode = _is_tagged_source_mode_enabled(repo_root)
    contract_findings = _validate_summary_contract(summary_csv, strict_tagged_mode=strict_tagged_mode)
    duplicate_findings = _validate_duplicate_source_ids(repo_root)
    evidence_findings = _validate_stage_evidence(repo_root, summary_csv)
    formatting_findings = validate_stage_markdown(repo_root, "1")
    findings = contract_findings + duplicate_findings + evidence_findings + formatting_findings
    if findings:
        print("Stage 1: FAIL")
        for finding in findings:
            print(f"- {finding}")
        _write_result(repo_root, "FAIL", findings)
        _append_log(repo_root, script_name, "FAIL findings=" + " | ".join(findings))
        return 1

    print("Stage 1: PASS")
    _write_result(repo_root, "PASS", [])
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
