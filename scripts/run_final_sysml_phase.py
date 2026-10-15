#!/usr/bin/env python3
"""Generate and centrally validate the complete approved-snapshot SysML set."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from approved_snapshot_resolver import resolve_complete_snapshot_id


def _run(root: Path, label: str, command: list[str]) -> int:
    print(f"\n{label}: START")
    print("Command:", " ".join(command))
    result = subprocess.run([sys.executable, *command], cwd=root)
    if result.returncode:
        print(f"{label}: FAIL (exit={result.returncode})")
        return result.returncode
    print(f"{label}: PASS")
    return 0


def _log_readiness_reports(root: Path, assessment: dict) -> None:
    from validate_downstream_coherence import readiness_model_report_path

    directory = root / "artifacts/validation/readiness_checklists"
    summary_json = directory / "readiness_summary.json"
    summary_excel = directory / "readiness_summary.xlsx"
    if summary_json.is_file() and summary_excel.is_file():
        print("[SYSML_READINESS] " + json.dumps({
            "snapshot_id": assessment["binding"]["snapshot_id"],
            "summary_json_sha256": hashlib.sha256(summary_json.read_bytes()).hexdigest(),
            "summary_excel_sha256": hashlib.sha256(summary_excel.read_bytes()).hexdigest(),
        }, sort_keys=True))
    print("[REPORT] Central SysML checklist: " + assessment["status"] + "; publication: " + assessment["publication_status"])
    print("[REPORT] Open SysML readiness Excel: " + str((root / "artifacts/validation/readiness_checklists/readiness_summary.xlsx").resolve()))
    for key, model in assessment["models"].items():
        print("[REPORT] " + model["block_name"] + ": " + model["status"])
        print("[REPORT] Open SysML readiness Excel: " + str(readiness_model_report_path(root, key).with_suffix(".xlsx").resolve()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the final snapshot-bound SysML generation and validation phase.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    project_id = root.name
    context_path = root / "config/project_context.json"
    if context_path.exists():
        import json
        project_id = str(json.loads(context_path.read_text(encoding="utf-8")).get("project_name") or project_id)
    snapshot_id = resolve_complete_snapshot_id(root, project_id=project_id, snapshot_id=args.snapshot_id)
    from readiness_checklist import sync_checklist_from_excel

    try:
        if sync_checklist_from_excel():
            print("Checklist reference: config/readiness_checklist.xlsx; saved rule edits synchronized to JSON.")
    except (ValueError, OSError) as error:
        print("Readiness checklist synchronization blocked: " + str(error))
        return 1
    from validate_downstream_coherence import assess_final_readiness, stamp_final_readiness, write_readiness_reports

    for label, command in (
        (
            "Final SysML generation",
            ["scripts/generate_architecture_sysml.py", "--snapshot-id", snapshot_id],
        ),
        (
            "Final SysML structural review",
            ["scripts/review_architecture_sysml.py", "--scope", "stage3-structural", "--snapshot-id", snapshot_id],
        ),
        (
            "Final SysML central coherence validation",
            ["scripts/validate_downstream_coherence.py", "--snapshot-id", snapshot_id],
        ),
    ):
        if label == "Final SysML central coherence validation":
            assessment = assess_final_readiness(root, snapshot_id)
            stamp_final_readiness(root, assessment)
            _log_readiness_reports(root, assessment)
        code = _run(root, label, command)
        if label == "Final SysML generation" or code:
            try:
                print("\nCentral readiness checklist: automatic assessment after " + label)
                if code:
                    print("Generation/validation failed; reports assess available official artifacts, not a successful new model set.")
                assessment = assess_final_readiness(root, snapshot_id)
                write_readiness_reports(root, assessment)
                _log_readiness_reports(root, assessment)
            except (ValueError, OSError, KeyError) as error:
                print("Readiness diagnostic unavailable: " + str(error))
                return 1
        if code:
            return 1
    import json
    if _run(root, "Final SysML readiness declaration validation",
            ["scripts/validate_downstream_coherence.py", "--snapshot-id", snapshot_id]):
        return 1
    print("\nFinal SysML phase: PASS; implementation readiness: " + assessment["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())