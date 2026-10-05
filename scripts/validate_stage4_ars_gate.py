#!/usr/bin/env python3
"""Gate validator for Stage 4 ARS outputs."""

from __future__ import annotations

import csv
import argparse
import json
from datetime import datetime
from pathlib import Path
import re
from validate_common_formatting import validate_stage_markdown
from approved_snapshot_resolver import resolve_complete_authoritative_input
from traceability_rules import is_valid_upstream_reference
from allocation_ledger import read_csv
from requirement_allocation_policy import validate_allocation_rows


REQUIRED = [
    Path("artifacts/stage4_ars/analog_requirements_specification.md"),
    Path("artifacts/stage4_ars/analog_requirements_specification.docx"),
    Path("artifacts/stage4_ars/ars_traceability_matrix.csv"),
    Path("artifacts/orchestrator/stage_ars_report.md"),
    Path("artifacts/orchestrator/stage_ars_crosscheck_report.md"),
]


def _validate_authored_ids(repo_root: Path, markdown_path: Path, traceability_path: Path) -> list[str]:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    markdown_ids = re.findall(r"^\s*\*\*\[(ARS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", markdown_text, flags=re.M)
    with traceability_path.open("r", encoding="utf-8", newline="") as handle:
        trace_ids = [row.get("ars_req_id", "").strip() for row in csv.DictReader(handle)]
    findings: list[str] = []
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    if ledger_path.exists():
        findings.extend(validate_allocation_rows(read_csv(ledger_path)))
    if len(markdown_ids) != len(set(markdown_ids)):
        findings.append("ARS markdown contains duplicate ARS-REQ IDs")
    if any(not re.fullmatch(r"ARS-REQ-\d{3}", req_id) for req_id in trace_ids):
        findings.append("ARS traceability contains an invalid authored ID namespace")
    if len(trace_ids) != len(set(trace_ids)):
        findings.append("ARS traceability contains duplicate ARS-REQ IDs")
    if set(markdown_ids) - set(trace_ids):
        findings.append("ARS markdown contains authored IDs absent from ARS traceability")
    return findings


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _write_result(repo_root: Path, status: str, missing: list[str], findings: list[str]) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_04_ars_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 04 ARS Result",
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
    lines.append("")
    lines.append("## Findings")
    if findings:
        lines.extend([f"- {item}" for item in findings])
    else:
        lines.append("- None")
    result_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _validate_srs_upstream(repo_root: Path, ars_text: str) -> list[str]:
    srs_trace = repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv"
    if not srs_trace.exists():
        return []
    with srs_trace.open("r", encoding="utf-8", newline="") as handle:
        srs_ids = {
            (row.get("srs_req_id") or "").strip()
            for row in csv.DictReader(handle)
            if (row.get("srs_req_id") or "").strip()
        }
    findings: list[str] = []
    for upstream_id in re.findall(r"^\s*Covers:\s*(SRS-REQ-\d{3})\s*$", ars_text, flags=re.M):
        if upstream_id not in srs_ids:
            findings.append(f"ARS Covers references missing SRS traceability ID: {upstream_id}")
    if re.search(r"^###\s+\d+\.\d+\s+Unassigned\s*$", ars_text, flags=re.M):
        findings.append("ARS must not emit Unassigned as a project-specific block heading")
    return findings


def _has_analog_requirement_id(rows) -> bool:
    for row in rows:
        category = (row.get("category") or row.get("approved_classification") or "").strip().lower()
        req_id = (row.get("source_req_id") or row.get("id") or "").strip()
        if category == "analog" and req_id:
            return True
    return False


def _has_retained_context(routing_csv: Path) -> bool:
    if not routing_csv.exists():
        return False
    with routing_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        return any(
            (row.get("Requirement ID") or "").strip()
            and (row.get("Routing Status") or "").strip() == "retained_as_non_block_function_context"
            for row in csv.DictReader(handle)
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ARS outputs against an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")
    try:
        requirement_input, _selection = resolve_complete_authoritative_input(
            repo_root, "5", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=args.snapshot_id
        )
    except Exception as exc:
        print(f"Stage 4 ARS gate: FAIL (complete approved snapshot unavailable: {exc})")
        return 1

    stage_report = repo_root / "artifacts/orchestrator/stage_ars_report.md"
    if stage_report.exists() and "ars generation status: skipped" in stage_report.read_text(encoding="utf-8").lower():
        findings = []
        requirement_input, _selection = resolve_complete_authoritative_input(
            repo_root, "5", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=args.snapshot_id
        )
        if _has_analog_requirement_id(requirement_input.rows):
            findings.append("ARS is marked skipped but Stage 1 contains Analog-category source requirement IDs")
        if _has_retained_context(repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv"):
            findings.append("ARS is marked skipped but retained Source Function Context rows require authored ARS requirements")
        status = "FAIL" if findings else "PASS"
        _write_result(repo_root, status, [], findings)
        if findings:
            print("Stage 4 ARS gate: FAIL")
            for item in findings:
                print(f"- finding: {item}")
            _append_log(repo_root, script_name, "FAIL invalid_skip")
            return 1
        print("Stage 4 ARS gate: PASS (skipped; no Analog-category source requirement IDs or retained Source Function Context rows)")
        _append_log(repo_root, script_name, "PASS skipped_no_analog_requirements")
        return 0

    missing = [str(p) for p in REQUIRED if not (repo_root / p).exists()]
    findings: list[str] = []
    findings.extend(validate_stage_markdown(repo_root, "4"))

    if stage_report.exists():
        text = stage_report.read_text(encoding="utf-8").lower()
        if "ars generation status: pass" not in text:
            findings.append("ARS stage report status is not pass")

    srs_result = repo_root / "artifacts/orchestrator/stage_03_srs_result.md"
    if srs_result.exists():
        text = srs_result.read_text(encoding="utf-8").lower()
        if "- status: pass" not in text:
            findings.append("ARS is blocked because the current Stage 3 SRS gate is not pass")

    crosscheck_report = repo_root / "artifacts/orchestrator/stage_ars_crosscheck_report.md"
    if crosscheck_report.exists():
        text = crosscheck_report.read_text(encoding="utf-8").lower()
        if "status: pass" not in text:
            findings.append("ARS crosscheck report status is not pass")

    ars_md = repo_root / "artifacts/stage4_ars/analog_requirements_specification.md"
    ars_traceability = repo_root / "artifacts/stage4_ars/ars_traceability_matrix.csv"
    if ars_md.exists():
        ars_text = ars_md.read_text(encoding="utf-8")
        traceability_rows = 0
        if ars_traceability.exists():
            with ars_traceability.open("r", encoding="utf-8", newline="") as handle:
                traceability_rows = sum(1 for _ in csv.DictReader(handle))
        if traceability_rows and not re.search(r"^\s*\*\*\[ARS-REQ-\d{3}\]\s+Requirement:\*\*\s*$", ars_text, flags=re.M):
            findings.append("ARS markdown does not contain authored [ARS-REQ-xxx] Requirement: entries")
        if re.search(r"^\s*(?:-\s*)?Requirement ID:\s*ARS-REQ-\d{3}\b", ars_text, flags=re.M):
            findings.append("ARS markdown uses deprecated 'Requirement ID: ARS-REQ-xxx' format; expected '[ARS-REQ-xxx] Requirement:'")
        if re.search(r"^\s*####\s+ARS-REQ-\d{3}\b", ars_text, flags=re.M):
            findings.append("ARS markdown uses deprecated '#### ARS-REQ-xxx' heading format; expected '[ARS-REQ-xxx] Requirement:'")
        if re.search(
            r"^\s*####\s+ARS-REQ-\d{3}[^\n]*\n\s*-\s*Statement:\s*",
            ars_text,
            flags=re.M,
        ):
            findings.append("ARS markdown uses deprecated '- Statement:' authored field under ARS-REQ headings")
        if "Linked requirements" in ars_text:
            findings.append("ARS markdown uses deprecated 'Linked requirements' wording; expected 'Covers'")
        if re.search(r"\*\*\[ARS-REQ-\d{3}\]\s+Requirement:\*\*\s*\n\s*Statement:\s*", ars_text):
            findings.append("ARS markdown uses deprecated 'Statement:' authored field; statement must follow the requirement header directly")
        invalid_covers = re.findall(r"^\s*(?:-\s*)?Covers:\s*(.+?)\s*$", ars_text, flags=re.M)
        if any(not is_valid_upstream_reference(value.strip()) for value in invalid_covers):
            findings.append("ARS markdown Covers entries must reference an SRS requirement or supplementary source requirement")
        if "Mapped requirements by analog block" in ars_text:
            findings.append("ARS markdown includes redundant mapped-summary subsection; project-specific analog sub-block requirement paragraphs must be the single source")
        findings.extend(_validate_srs_upstream(repo_root, ars_text))
        if ars_traceability.exists():
            findings.extend(_validate_authored_ids(repo_root, ars_md, ars_traceability))

    status = "PASS"
    if missing or findings:
        status = "FAIL"

    _write_result(repo_root, status, missing, findings)

    if status != "PASS":
        print("Stage 4 ARS gate: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        for item in findings:
            print(f"- finding: {item}")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print("Stage 4 ARS gate: PASS")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
