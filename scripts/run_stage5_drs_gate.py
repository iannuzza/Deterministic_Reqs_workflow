#!/usr/bin/env python3
"""Run the complete Stage 5 DRS flow through crosscheck and gate validation.

Flow:
1) Generate DRS artifacts and run DRS crosscheck.
2) Run Stage 5 DRS gate validator.

Primary generated artifacts:
- artifacts/stage5_drs/digital_requirements_specification.md
- artifacts/stage5_drs/digital_requirements_specification.docx (optional when pandoc is available)
- artifacts/stage5_drs/drs_traceability_matrix.csv
- artifacts/stage5_drs/requirements_hierarchy_coverage_report.md
- artifacts/orchestrator/stage_drs_report.md
- artifacts/orchestrator/stage_drs_crosscheck_report.md
- artifacts/orchestrator/stage_05_drs_result.md
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from approved_snapshot_resolver import resolve_complete_snapshot_id


def _run(repo_root: Path, label: str, args: list[str]) -> int:
    cmd = [sys.executable, *args]
    print(f"\n{label}: START", flush=True)
    print("Command:", " ".join(cmd), flush=True)
    rc = subprocess.run(cmd, cwd=repo_root).returncode
    if rc != 0:
        print(f"{label}: FAIL (exit={rc})", flush=True)
        return rc
    print(f"{label}: PASS", flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run Stage 5 DRS full flow. Optional requirements-only mode supports running "
            "Stage 5 directly after Stage 2A without Stage 3/4 generation."
        )
    )
    parser.add_argument(
        "--requirements-only",
        action="store_true",
        help="Generate DRS from Stage 1 + Stage 2A artifacts and omit Stage 4 ARS references.",
    )
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

    print("Stage 5 DRS full flow", flush=True)
    print("This run will generate and validate:", flush=True)
    print("- artifacts/stage5_drs/digital_requirements_specification.md", flush=True)
    print("- artifacts/stage5_drs/digital_requirements_specification.docx", flush=True)
    print("- artifacts/stage5_drs/drs_traceability_matrix.csv", flush=True)
    print("- artifacts/stage5_drs/requirements_hierarchy_coverage_report.md", flush=True)
    print("- artifacts/orchestrator/stage_drs_report.md", flush=True)
    print("- artifacts/orchestrator/stage_drs_crosscheck_report.md", flush=True)
    print("- artifacts/orchestrator/stage_05_drs_result.md", flush=True)

    # Step 1 generates DRS markdown/CSV/stage report and runs the DRS crosscheck.
    drs_gen_cmd = ["scripts/run_drs_gen_spec_agent.py"]
    if args.requirements_only:
        drs_gen_cmd.append("--requirements-only")
    drs_gen_cmd += ["--snapshot-id", snapshot_id]

    rc = _run(repo_root, "Stage 5 DRS.1 Generate + crosscheck", drs_gen_cmd)
    if rc != 0:
        return rc

    # Step 2 validates required Stage 5 outputs and writes stage_05_drs_result.md.
    validator = ["scripts/validate_stage5_drs_gate.py"]
    validator += ["--snapshot-id", snapshot_id]
    rc = _run(repo_root, "Stage 5 DRS.2 Validate DRS gate", validator)
    if rc != 0:
        return rc

    print("\nStage 5 DRS full flow: PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
