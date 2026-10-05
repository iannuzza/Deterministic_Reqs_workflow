#!/usr/bin/env python3
"""Gate validator for Stage 3 SRS outputs."""

from __future__ import annotations

import csv
import argparse
import json
from datetime import datetime
from pathlib import Path
import re
from validate_common_formatting import validate_stage_markdown
from workflow_routing import read_retained_rows, source_parent_title, validate_srs_system_overview
from requirement_corpus import CorpusResolutionError
from approved_snapshot_resolver import resolve_complete_authoritative_input
from run_srs_crosscheck_agent import _validate_srs_allocation_scope
from validate_downstream_coherence import resolve_downstream_contract
from stage1_descriptive_evidence import extract_stage1_descriptive_evidence, validate_stage1_descriptive_records


REQUIRED = [
    Path("artifacts/stage3_srs/system_requirements_specification.md"),
    Path("artifacts/stage3_srs/system_requirements_specification.docx"),
    Path("artifacts/stage3_srs/srs_traceability_matrix.csv"),
    Path("artifacts/stage3_srs/stage2_srs_combined.tex"),
    Path("artifacts/orchestrator/stage_srs_report.md"),
    Path("artifacts/orchestrator/stage_srs_crosscheck_report.md"),
    Path("artifacts/orchestrator/stage_srs_latex_crosscheck_report.md"),
]


def _validate_authored_ids(markdown_path: Path, traceability_path: Path, *, enforce_srs_content: bool) -> list[str]:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    markdown_ids = re.findall(r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*$", markdown_text, flags=re.M)
    authored_blocks = re.findall(
        r"^\s*\*\*\[(SRS-REQ-\d{3})\]\s+Requirement:\*\*\s*\n(.*?)(?=^\s*\*\*\[SRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$|\Z)",
        markdown_text,
        flags=re.M | re.S,
    )
    with traceability_path.open("r", encoding="utf-8", newline="") as handle:
        trace_ids = [row.get("srs_req_id", "").strip() for row in csv.DictReader(handle)]
    findings: list[str] = []
    if len(markdown_ids) != len(set(markdown_ids)):
        findings.append("SRS markdown contains duplicate SRS-REQ IDs")
    if any(not re.fullmatch(r"SRS-REQ-\d{3}", req_id) for req_id in trace_ids):
        findings.append("SRS traceability contains an invalid authored ID namespace")
    if len(trace_ids) != len(set(trace_ids)):
        findings.append("SRS traceability contains duplicate SRS-REQ IDs")
    if enforce_srs_content and set(markdown_ids) - set(trace_ids):
        findings.append("SRS markdown contains authored IDs absent from SRS traceability")
    for _req_id, block in authored_blocks:
        statement_text = re.split(r"^\s*Covers:\s*", block, maxsplit=1, flags=re.M)[0]
        if re.search(r"\b(?:DDS_[A-Z0-9_]+|(?:SYS|ANA|DIG|XDN)-RQ-\d+)\b", statement_text):
            findings.append("SRS authored statement contains an upstream requirement ID outside Covers")
            break
        if re.search(r"DCC\s+IP\s+00\s+25nA\s+01\s+50nA", statement_text):
            findings.append("SRS authored statement contains an unrewritten DCC table fragment")
            break
    return findings


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _write_result(repo_root: Path, status: str, missing: list[str], findings: list[str]) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_03_srs_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 03 SRS Result",
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


def _validate_retained_context(repo_root: Path, srs_text: str, requirement_input, srs_source_ids: set[str]) -> list[str]:
    routing_path = repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv"
    if not routing_path.exists():
        return []
    requirement_ids: set[str] = set()
    requirement_ids = {
        (row.get("source_req_id") or row.get("id") or "").strip()
        for row in requirement_input.rows
        if (row.get("source_req_id") or row.get("id") or "").strip()
    }
    rows = read_retained_rows(routing_path, requirement_ids)
    matrix_ids: set[str] = set()
    matrix_path = repo_root / "artifacts/stage2_mirco_arc/interaction_matrix.csv"
    if matrix_path.exists():
        with matrix_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                for value in (row.get("Requirement IDs") or "").split(";"):
                    normalized = re.sub(r"\s+", "", value)
                    if normalized:
                        matrix_ids.add(normalized)
    findings: list[str] = []
    for row in rows:
        source_id = re.sub(r"\s+", "", (row.get("Requirement ID") or "").strip())
        if source_id not in srs_source_ids:
            continue
        if source_id in matrix_ids:
            continue
        statement = row.get("Requirement Statement") or ""
        evidence = " ".join(
            [
                row.get("Source Paragraph") or "",
                statement,
            ]
        )
        # Address/register-map rows are reference evidence, not normative SRS entries.
        if re.search(r"register\s+map|register\s+address|memory\s+map", evidence, flags=re.IGNORECASE):
            if not re.search(r"\b(?:shall|must|required|requirement)\b", statement, flags=re.IGNORECASE):
                continue
        if not re.search(r"\b(?:shall|must|required)\b", statement, flags=re.IGNORECASE):
            continue
        covers_count = len(re.findall(rf"^\s*Covers:\s*{re.escape(source_id)}\s*$", srs_text, flags=re.M))
        if covers_count != 1:
            findings.append(f"Retained source ID must appear exactly once in SRS Covers: {source_id}")
        context = source_parent_title(row.get("Non-Block Function Context") or row.get("Source Paragraph") or "")
        if context and context not in srs_text:
            findings.append(f"Retained source-parent context is missing from SRS: {source_id}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SRS outputs against an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    try:
        requirement_input, selection = resolve_complete_authoritative_input(
            repo_root, "3", project_id=str(context.get("project_name") or repo_root.name), snapshot_id=args.snapshot_id
        )
        downstream_contract = resolve_downstream_contract(repo_root, str(selection["selected_snapshot_id"]))
        srs_source_ids = downstream_contract.source_ids_for_target("SRS")
        _append_log(repo_root, Path(__file__).name, f"AUTHORITATIVE_SNAPSHOT snapshot_id={selection['selected_snapshot_id']}")
    except Exception as exc:
        print(f"Stage 3 SRS gate: FAIL (complete approved snapshot unavailable: {exc})")
        return 1
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    missing = [str(p) for p in REQUIRED if not (repo_root / p).exists()]
    findings: list[str] = []
    findings.extend(validate_stage_markdown(repo_root, "3"))
    stage1_index = repo_root / "artifacts/stage1_requirements/ocr_extracts/index.csv"
    if stage1_index.exists():
        findings.extend(
            f"Stage 1 descriptive evidence: {finding}"
            for finding in validate_stage1_descriptive_records(
                extract_stage1_descriptive_evidence(stage1_index)
            )
        )

    stage_report = repo_root / "artifacts/orchestrator/stage_srs_report.md"
    if stage_report.exists():
        text = stage_report.read_text(encoding="utf-8").lower()
        if srs_source_ids and "srs generation status: pass" not in text:
            findings.append("SRS stage report status is not pass")

    for rel in [
        Path("artifacts/orchestrator/stage_srs_crosscheck_report.md"),
        Path("artifacts/orchestrator/stage_srs_latex_crosscheck_report.md"),
    ]:
        p = repo_root / rel
        if p.exists():
            text = p.read_text(encoding="utf-8").lower()
            if "status: pass" not in text:
                findings.append(f"Crosscheck report not pass: {rel.as_posix()}")

    srs_md = repo_root / "artifacts/stage3_srs/system_requirements_specification.md"
    findings.extend(f"SRS overview: {finding}" for finding in validate_srs_system_overview(srs_md))
    traceability_path = repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv"
    selected_ids = {
        (row.get("source_req_id") or row.get("canonical_id") or row.get("id") or "").strip()
        for row in requirement_input.rows
        if (row.get("source_req_id") or row.get("canonical_id") or row.get("id") or "").strip()
    }
    trace_source_ids: list[str] = []
    if traceability_path.exists():
        with traceability_path.open("r", encoding="utf-8", newline="") as handle:
            trace_source_ids = [
                (row.get("source_req_id") or "").strip()
                for row in csv.DictReader(handle)
            ]
    findings.extend(
        _validate_srs_allocation_scope(
            repo_root,
            project_id=str(context.get("project_name") or repo_root.name),
            snapshot_id=str(selection["selected_snapshot_id"]),
            snapshot_ids=selected_ids,
            trace_source_ids=trace_source_ids,
        )
    )
    if srs_md.exists():
        srs_text = srs_md.read_text(encoding="utf-8")
        if srs_source_ids and not re.search(r"^\s*\*\*\[SRS-REQ-\d{3}\]\s+Requirement:\*\*\s*$", srs_text, flags=re.M):
            findings.append("SRS markdown does not contain authored [SRS-REQ-xxx] Requirement: entries")
        if re.search(r"^\s*(?:-\s*)?Requirement ID:\s*SRS-REQ-\d{3}\b", srs_text, flags=re.M):
            findings.append("SRS markdown uses deprecated 'Requirement ID: SRS-REQ-xxx' format; expected '[SRS-REQ-xxx] Requirement:'")
        if re.search(r"^\s*####\s+SRS-REQ-\d{3}\b", srs_text, flags=re.M):
            findings.append("SRS markdown uses deprecated '#### SRS-REQ-xxx' heading format; expected '[SRS-REQ-xxx] Requirement:'")
        if re.search(
            r"^\s*####\s+SRS-REQ-\d{3}[^\n]*\n\s*-\s*Statement:\s*",
            srs_text,
            flags=re.M,
        ):
            findings.append("SRS markdown uses deprecated '- Statement:' authored field under SRS-REQ headings")
        if "Linked requirements" in srs_text:
            findings.append("SRS markdown uses deprecated 'Linked requirements' wording; expected 'Covers'")
        if re.search(r"\*\*\[SRS-REQ-\d{3}\]\s+Requirement:\*\*\s*\n\s*Statement:\s*", srs_text):
            findings.append("SRS markdown uses deprecated 'Statement:' authored field; statement must follow the requirement header directly")
        findings.extend(
            _validate_authored_ids(
                srs_md,
                repo_root / "artifacts/stage3_srs/srs_traceability_matrix.csv",
                enforce_srs_content=bool(srs_source_ids),
            )
        )
        findings.extend(
            [resolver_error]
            if requirement_input is None
            else _validate_retained_context(repo_root, srs_text, requirement_input, srs_source_ids)
        )

    status = "PASS"
    if missing or findings:
        status = "FAIL"

    _write_result(repo_root, status, missing, findings)

    if status != "PASS":
        print("Stage 3 SRS gate: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        for item in findings:
            print(f"- finding: {item}")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print("Stage 3 SRS gate: PASS")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
