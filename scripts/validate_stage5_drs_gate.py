#!/usr/bin/env python3
"""Gate validator for Stage 5 DRS outputs."""

from __future__ import annotations

import csv
import argparse
import json
from datetime import datetime
from pathlib import Path
import re
from validate_common_formatting import validate_stage_markdown
from workflow_routing import TOP_DIGITAL_CATEGORY_SPECS
from run_drs_gen_spec_agent import validate_drs_descriptive_artifacts
from allocation_ledger import read_csv
from requirement_allocation_policy import validate_allocation_rows
from approved_snapshot_resolver import resolve_complete_authoritative_input
from validate_downstream_coherence import DownstreamContract, resolve_downstream_contract
from stage1_descriptive_evidence import extract_stage1_descriptive_evidence, validate_stage1_descriptive_records


REQUIRED = [
    Path("artifacts/stage5_drs/digital_requirements_specification.md"),
    Path("artifacts/stage5_drs/digital_requirements_specification.docx"),
    Path("artifacts/stage5_drs/drs_traceability_matrix.csv"),
    Path("artifacts/stage5_drs/requirements_hierarchy_coverage_report.md"),
    Path("artifacts/stage5_drs/top_digital_coverage_audit.csv"),
    Path("artifacts/orchestrator/stage_drs_report.md"),
    Path("artifacts/orchestrator/stage_drs_crosscheck_report.md"),
]


def _approved_drs_provenance(contract: DownstreamContract) -> set[str]:
    approved: set[str] = set()
    for source_id in contract.source_ids_for_target("DRS"):
        approved.add(source_id)
        allocation = contract.allocation(source_id)
        for field in ("source_origin_req_ids", "hierarchy_parent_req_ids"):
            approved.update(
                item.strip()
                for item in re.split(r"[;,]", str(allocation.get(field) or ""))
                if item.strip()
            )
    return approved


def _validate_authored_ids(
    repo_root: Path,
    markdown_path: Path,
    traceability_path: Path,
    contract: DownstreamContract,
) -> list[str]:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    markdown_ids = re.findall(r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", markdown_text, flags=re.M)
    authored_blocks = re.findall(
        r"^\s*\*\*\[(DRS-REQ-\d{3})\]\s+Requirement:\*\*\s*\n(.*?)(?=^\s*\*\*\[DRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
        markdown_text,
        flags=re.M | re.S,
    )
    with traceability_path.open("r", encoding="utf-8", newline="") as handle:
        trace_ids = [row.get("drs_req_id", "").strip() for row in csv.DictReader(handle)]
    findings: list[str] = []
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    if ledger_path.exists():
        findings.extend(validate_allocation_rows(read_csv(ledger_path)))
    if len(markdown_ids) != len(set(markdown_ids)):
        findings.append("DRS markdown contains duplicate DRS-REQ IDs")
    if any(not re.fullmatch(r"DRS-REQ-\d{3}", req_id) for req_id in trace_ids):
        findings.append("DRS traceability contains an invalid authored ID namespace")
    if len(trace_ids) != len(set(trace_ids)):
        findings.append("DRS traceability contains duplicate DRS-REQ IDs")
    if set(markdown_ids) - set(trace_ids):
        findings.append("DRS markdown contains authored IDs absent from DRS traceability")
    approved_provenance = _approved_drs_provenance(contract)
    missing_covers = []
    for req_id, block in authored_blocks:
        covers = [value.strip() for value in re.findall(r"^\s*Covers:\s*(.+?)\s*$", block, flags=re.M)]
        if not covers or not any(value in approved_provenance for value in covers):
            missing_covers.append(req_id)
    if missing_covers:
        findings.append("DRS markdown contains authored DRS-REQ entries without approved snapshot provenance in Covers linkage")
    return findings


def _validate_top_digital_audit(path: Path) -> list[str]:
    if not path.exists():
        return ["Missing top-digital coverage audit"]
    expected = {name for name, _terms in TOP_DIGITAL_CATEGORY_SPECS}
    allowed_scopes = {"top_digital", "integration", "architecture", "lifted_integration"}
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    findings: list[str] = []
    if len(rows) != len(expected) or {row.get("category", "").strip() for row in rows} != expected:
        findings.append("Top-digital coverage audit is incomplete or contains unexpected categories")
    for row in rows:
        statement = row.get("statement", "").strip()
        scopes = {
            item.strip().casefold()
            for item in row.get("scope", "").split(";")
            if item.strip()
        }
        source = row.get("source", "").strip()
        if row.get("status", "").strip() not in {"Covered", "Partial", "Missing"}:
            findings.append(f"Invalid top-digital coverage status: {row.get('category', '')}")
        if statement and (not scopes or not scopes.issubset(allowed_scopes) or not source):
            findings.append(f"Top-digital audit evidence lacks approved scope/provenance: {row.get('category', '')}")
        if "digital ipos" in f"{statement} {source}".casefold() or re.search(r"\bblock\s+shall\s+implement\s*:", statement, re.I):
            findings.append(f"Top-digital audit contains Digital IPOS detail: {row.get('category', '')}")
    return findings


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _write_result(repo_root: Path, status: str, missing: list[str], findings: list[str]) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_05_drs_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 05 DRS Result",
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


def _validate_srs_upstream(repo_root: Path, drs_text: str) -> list[str]:
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
    for upstream_id in re.findall(r"^\s*Covers:\s*(SRS-REQ-\d{3})\s*$", drs_text, flags=re.M):
        if upstream_id not in srs_ids:
            findings.append(f"DRS Covers references missing SRS traceability ID: {upstream_id}")
    if re.search(r"^###\s+\d+\.\d+\s+Unassigned\s*$", drs_text, flags=re.M):
        findings.append("DRS must not emit Unassigned as a project-specific block heading")
    return findings


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")
    parser = argparse.ArgumentParser(description="Validate DRS outputs against the complete approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=False)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    try:
        snapshot, selection = resolve_complete_authoritative_input(
            repo_root, "5", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=args.snapshot_id
        )
    except Exception as exc:
        print(f"Stage 5 DRS gate: FAIL (complete approved snapshot unavailable: {exc})")
        return 1
    ledger_path = repo_root / "artifacts/traceability_reports/requirement_allocation_ledger.csv"
    manifest_path = repo_root / "artifacts/traceability_reports/requirement_allocation_materialization.json"
    if not ledger_path.exists() or not manifest_path.exists():
        print("Stage 5 DRS gate: FAIL (allocation ledger materialization is missing)")
        return 1
    ledger_rows = read_csv(ledger_path)
    if any(row.get("snapshot_id") != snapshot.snapshot_id for row in ledger_rows):
        print("Stage 5 DRS gate: FAIL (allocation ledger snapshot does not match selected snapshot)")
        return 1
    findings = validate_allocation_rows(ledger_rows)
    if findings:
        print("Stage 5 DRS gate: FAIL (central allocation policy findings)")
        return 1

    missing = [str(p) for p in REQUIRED if not (repo_root / p).exists()]
    findings: list[str] = []
    findings.extend(validate_stage_markdown(repo_root, "5"))
    stage1_index = repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
    if stage1_index.exists():
        findings.extend(
            f"Stage 1 descriptive evidence: {finding}"
            for finding in validate_stage1_descriptive_records(
                extract_stage1_descriptive_evidence(stage1_index)
            )
        )
    findings.extend(_validate_top_digital_audit(repo_root / "artifacts/stage5_drs/top_digital_coverage_audit.csv"))
    findings.extend(validate_drs_descriptive_artifacts(repo_root))
    from spec_document_contract import validate_drs_document_contract
    findings.extend(validate_drs_document_contract(repo_root))

    stage_report = repo_root / "artifacts/orchestrator/stage_drs_report.md"
    if stage_report.exists():
        text = stage_report.read_text(encoding="utf-8").lower()
        if "drs generation status: pass" not in text:
            findings.append("DRS stage report status is not pass")

    srs_result = repo_root / "artifacts/orchestrator/stage_03_srs_result.md"
    if srs_result.exists():
        text = srs_result.read_text(encoding="utf-8").lower()
        if "- status: pass" not in text:
            findings.append("DRS is blocked because the current Stage 3 SRS gate is not pass")

    crosscheck_report = repo_root / "artifacts/orchestrator/stage_drs_crosscheck_report.md"
    if crosscheck_report.exists():
        text = crosscheck_report.read_text(encoding="utf-8").lower()
        if "status: pass" not in text:
            findings.append("DRS crosscheck report status is not pass")

    drs_md = repo_root / "artifacts/stage5_drs/digital_requirements_specification.md"
    if drs_md.exists():
        drs_text = drs_md.read_text(encoding="utf-8")
        has_authored_requirements = bool(re.search(
            r"^\s*\*\*\[DRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$",
            drs_text,
            flags=re.M,
        ))
        has_top_level_integration_section = bool(re.search(
            r"^##\s+9\.\s+Top-level integration requirements(?:\s+\{#[^}]+\})?\s*$",
            drs_text,
            flags=re.M,
        ))
        if not has_authored_requirements and not has_top_level_integration_section:
            findings.append("DRS markdown does not contain authored [DRS-REQ-xxx] Requirement: entries")
        if re.search(r"^\s*(?:-\s*)?Requirement ID:\s*DRS-REQ-\d{3}\b", drs_text, flags=re.M):
            findings.append("DRS markdown uses deprecated 'Requirement ID: DRS-REQ-xxx' format; expected '[DRS-REQ-xxx] Requirement:'")
        if re.search(r"^\s*####\s+DRS-REQ-\d{3}\b", drs_text, flags=re.M):
            findings.append("DRS markdown uses deprecated '#### DRS-REQ-xxx' heading format; expected '[DRS-REQ-xxx] Requirement:'")
        if re.search(
            r"^\s*####\s+DRS-REQ-\d{3}[^\n]*\n\s*-\s*Statement:\s*",
            drs_text,
            flags=re.M,
        ):
            findings.append("DRS markdown uses deprecated '- Statement:' authored field under DRS-REQ headings")
        if "Linked requirements" in drs_text:
            findings.append("DRS markdown uses deprecated 'Linked requirements' wording; expected 'Covers'")
        if re.search(r"\*\*\[DRS-REQ-\d{3}\]\s+Requirement:\*\*\s*\n\s*Statement:\s*", drs_text):
            findings.append("DRS markdown uses deprecated 'Statement:' authored field; statement must follow the requirement header directly")
        if re.search(r"^\s*\[(?!DRS-REQ-\d{3}\])[A-Z][A-Z0-9_\-]*\]\s+Requirement:?\s*$", drs_text, flags=re.M):
            findings.append("DRS markdown contains raw source requirement headers; only DRS-REQ authored headers are allowed")
        if "the following atomic functionality" in drs_text.lower():
            findings.append("DRS markdown uses deprecated filler phrase 'the following atomic functionality'")
        findings.extend(_validate_srs_upstream(repo_root, drs_text))
        downstream_contract = resolve_downstream_contract(repo_root, snapshot.snapshot_id)
        findings.extend(
            _validate_authored_ids(
                repo_root,
                drs_md,
                repo_root / "artifacts/stage5_drs/drs_traceability_matrix.csv",
                downstream_contract,
            )
        )

    status = "PASS"
    if missing or findings:
        status = "FAIL"

    _write_result(repo_root, status, missing, findings)

    if status != "PASS":
        print("Stage 5 DRS gate: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        for item in findings:
            print(f"- finding: {item}")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print("Stage 5 DRS gate: PASS")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
