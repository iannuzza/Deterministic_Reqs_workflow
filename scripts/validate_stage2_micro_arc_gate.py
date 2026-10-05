#!/usr/bin/env python3
"""Gate validator for Stage 2 micro-architecture outputs."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys
from validate_common_formatting import validate_stage_markdown
from validate_stage2_profile import validate_approval_evidence


REQUIRED = [
    Path("artifacts/stage0_ontology/ontology_requirement_links.csv"),
    Path("artifacts/stage1_requirements/source_matrix_edges.csv"),
    Path("artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv"),
    Path("artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv"),
    Path("artifacts/stage2_mirco_arc/block_inventory.csv"),
    Path("artifacts/stage2_mirco_arc/interface_catalog.csv"),
    Path("artifacts/stage2_mirco_arc/interaction_matrix.csv"),
    Path("artifacts/stage2_mirco_arc/function_decomposition.md"),
    Path("artifacts/stage2_mirco_arc/micro_architecture_report.md"),
    Path("artifacts/stage2_mirco_arc/architecture_crosscheck_report.md"),
    Path("artifacts/stage2_mirco_arc/stage2_mapping_crosscheck_report.md"),
    Path("artifacts/orchestrator/stage_02_micro_arch_report.md"),
]


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _write_result(
    repo_root: Path,
    status: str,
    missing: list[str],
    findings: list[str],
    approval_status: str,
) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_02_micro_arch_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 02 Micro-Architecture Result",
        "",
        f"- Timestamp: {timestamp}",
        f"- Status: {status}",
        f"- S2A Approval Evidence: {approval_status}",
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


def _validate_routing(path: Path) -> list[str]:
    required = {
        "Requirement ID",
        "Source Paragraph",
        "Requirement Statement",
        "Identified Block Mapping",
        "Non-Block Function Context",
        "Routing Status",
    }
    findings: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not required.issubset(set(reader.fieldnames or [])):
            return ["Stage 2A routing CSV is missing required context columns"]
        seen: set[str] = set()
        for row in reader:
            req_id = (row.get("Requirement ID") or "").strip()
            if not req_id:
                findings.append("Stage 2A routing contains a row without Requirement ID")
                continue
            if req_id in seen:
                findings.append(f"Stage 2A routing contains duplicate Requirement ID: {req_id}")
            seen.add(req_id)
            mapping = (row.get("Identified Block Mapping") or "").strip()
            status = (row.get("Routing Status") or "").strip()
            context = (row.get("Non-Block Function Context") or "").strip()
            if status == "retained_as_non_block_function_context":
                if mapping != "Unassigned":
                    findings.append(f"Retained routing is not Unassigned: {req_id}")
                if not context:
                    findings.append(f"Retained routing has no source-function context: {req_id}")
            elif status and status != "assigned_to_block":
                findings.append(f"Unknown Stage 2A routing status for {req_id}: {status}")
            if context and not re.search(r"\S", context):
                findings.append(f"Stage 2A source-function context is blank: {req_id}")
    return findings


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    missing = [str(p) for p in REQUIRED if not (repo_root / p).exists()]
    findings: list[str] = []
    findings.extend(validate_stage_markdown(repo_root, "2a"))
    approval_findings = validate_approval_evidence(
        repo_root / "config/stage2_mirco_arc_profile.json",
        repo_root / "artifacts/stage1_specs/architecture_profile_draft.json",
        repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv",
    )
    findings.extend(approval_findings)
    profile_checker = repo_root / "scripts/validate_stage2_profile.py"
    if profile_checker.exists() and not missing:
        result = subprocess.run([sys.executable, str(profile_checker)], cwd=repo_root)
        if result.returncode != 0:
            findings.append("Stage 2A profile crosscheck failed")
    mapping_checker = repo_root / "scripts/validate_stage2_mapping.py"
    if mapping_checker.exists() and not missing:
        result = subprocess.run([sys.executable, str(mapping_checker)], cwd=repo_root)
        if result.returncode != 0:
            findings.append("Stage 2A post-mapping semantic crosscheck failed")
    routing_path = repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv"
    if routing_path.exists():
        findings.extend(_validate_routing(routing_path))

    report_path = repo_root / "artifacts/orchestrator/stage_02_micro_arch_report.md"
    if report_path.exists():
        report_text = report_path.read_text(encoding="utf-8").lower()
        if "stage 2 micro-architecture gate: pass" not in report_text:
            findings.append("Stage report does not confirm pass decision")

    crosscheck_path = repo_root / "artifacts/stage2_mirco_arc/architecture_crosscheck_report.md"
    if crosscheck_path.exists():
        crosscheck_text = crosscheck_path.read_text(encoding="utf-8", errors="ignore").lower()
        if "status: pass" not in crosscheck_text and "decision: go" not in crosscheck_text:
            findings.append("Architecture crosscheck report does not confirm a go/pass decision")

    status = "PASS"
    if missing or findings:
        status = "FAIL"

    _write_result(
        repo_root,
        status,
        missing,
        findings,
        "FAIL" if approval_findings else "PASS",
    )

    if status != "PASS":
        print("Stage 2 micro-architecture gate: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        for item in findings:
            print(f"- finding: {item}")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print("Stage 2 micro-architecture gate: PASS")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
