#!/usr/bin/env python3
"""Run Stage 3 SRS flow through gate validation."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from approved_snapshot_resolver import resolve_complete_snapshot_id


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Stage 3 SRS flow from an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    project_id = repo_root.name
    context_path = repo_root / "config/project_context.json"
    if context_path.exists():
        import json
        project_id = str(json.loads(context_path.read_text(encoding="utf-8")).get("project_name") or project_id)
    snapshot_id = resolve_complete_snapshot_id(repo_root, project_id=project_id, snapshot_id=args.snapshot_id)

    review_path = repo_root / "artifacts/stage2_mirco_arc/stbio_architecture_model_review.md"
    if not review_path.exists():
        print("Stage 2 SysML review artifact: not present (non-blocking derived-artifact diagnostic).")
    elif "- Status: approved" not in review_path.read_text(encoding="utf-8"):
        print("Stage 2 SysML review artifact is not approved; continuing because it is derived and non-authoritative.")
        print("Architectural authority remains the approved mapping and snapshot materialization.")

    print("Stage 3 SRS full flow")
    print("This run will generate and validate:")
    print("- artifacts/stage3_srs/system_requirements_specification.md")
    print("- artifacts/stage3_srs/system_requirements_specification.docx")
    print("- artifacts/stage3_srs/srs_traceability_matrix.csv")
    print("- artifacts/stage3_srs/stage2_srs_combined.tex")
    print("- artifacts/orchestrator/stage_srs_report.md")
    print("- artifacts/orchestrator/stage_srs_crosscheck_report.md")
    print("- artifacts/orchestrator/stage_srs_latex_crosscheck_report.md")
    print("- artifacts/orchestrator/stage_03_srs_result.md")

    generator = ["scripts/run_srs_gen_spec_agent.py"]
    generator += ["--snapshot-id", snapshot_id]
    rc = _run(repo_root, "Stage 3 SRS.1 Generate + crosschecks", generator)
    if rc != 0:
        return rc

    validator = ["scripts/validate_stage3_srs_gate.py"]
    validator += ["--snapshot-id", snapshot_id]
    rc = _run(repo_root, "Stage 3 SRS.2 Validate SRS gate", validator)
    if rc != 0:
        return rc

    print("\nStage 3 SRS full flow: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
