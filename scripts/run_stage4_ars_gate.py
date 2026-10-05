#!/usr/bin/env python3
"""Run Stage 4 ARS flow through gate validation."""

from __future__ import annotations

import csv
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from approved_snapshot_resolver import resolve_authoritative_input, resolve_complete_snapshot_id


def _run(repo_root: Path, label: str, args: list[str]) -> int:
    cmd = [sys.executable, *args]
    print(f"\n{label}: START")
    print("Command:", " ".join(cmd))
    rc = subprocess.run(cmd, cwd=repo_root).returncode
    if rc != 0:
        print(f"{label}: FAIL (exit={rc})")
        return rc
    print(f"{label}: PASS")
    return 0


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


def _write_skip_reports(repo_root: Path) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_dir = repo_root / "artifacts/orchestrator"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "stage_ars_report.md").write_text(
        "# Stage ARS Report\n\n"
        f"Date: {timestamp}\n\n"
        "ARS generation status: skipped\n\n"
        "## Skip reason\n"
        "- Stage 1 requirements contain no Analog-category source requirement IDs or retained Source Function Context rows.\n",
        encoding="utf-8",
    )
    (report_dir / "stage_ars_crosscheck_report.md").write_text(
        "# Stage ARS Crosscheck Report\n\n"
        f"Date: {timestamp}\n\n"
        "Status: skipped\n\n"
        "## Skip reason\n"
        "- No Analog-category source requirement IDs or retained Source Function Context rows were selected for ARS generation.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Stage 4 ARS flow from an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent

    context = json.loads((repo_root / "config" / "project_context.json").read_text(encoding="utf-8"))
    project_id = str(context.get("project_name") or repo_root.name)
    snapshot_id = resolve_complete_snapshot_id(repo_root, project_id=project_id, snapshot_id=args.snapshot_id)
    requirement_input = resolve_authoritative_input(repo_root, "5", project_id=project_id, snapshot_id=snapshot_id)
    routing_csv = repo_root / "artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv"
    if not _has_analog_requirement_id(requirement_input.rows) and not _has_retained_context(routing_csv):
        _write_skip_reports(repo_root)
        print("Stage 4 ARS full flow: SKIPPED (no Analog-category source requirement IDs or retained Source Function Context rows)")
        return 0

    print("Stage 4 ARS full flow")
    print("This run will generate and validate:")
    print("- artifacts/stage4_ars/analog_requirements_specification.md")
    print("- artifacts/stage4_ars/analog_requirements_specification.docx")
    print("- artifacts/stage4_ars/ars_traceability_matrix.csv")
    print("- artifacts/orchestrator/stage_ars_report.md")
    print("- artifacts/orchestrator/stage_ars_crosscheck_report.md")
    print("- artifacts/orchestrator/stage_04_ars_result.md")

    generator = ["scripts/run_ars_gen_spec_agent.py"]
    generator += ["--snapshot-id", snapshot_id]
    rc = _run(repo_root, "Stage 4 ARS.1 Generate + crosscheck", generator)
    if rc != 0:
        return rc

    validator = ["scripts/validate_stage4_ars_gate.py"]
    validator += ["--snapshot-id", snapshot_id]
    rc = _run(repo_root, "Stage 4 ARS.2 Validate ARS gate", validator)
    if rc != 0:
        return rc

    print("\nStage 4 ARS full flow: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
