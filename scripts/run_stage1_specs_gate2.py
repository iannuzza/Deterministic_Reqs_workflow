#!/usr/bin/env python3
"""Run Stage 1 specs workflow through Gate 2 validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


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
    repo_root = Path(__file__).resolve().parent.parent

    print("Stage 1 specs (Gate 2) full flow")
    print("This run will generate and validate:")
    print("- artifacts/stage1_specs/specs.md")
    print("- artifacts/stage1_specs/traceability_seed.csv")
    print("- artifacts/stage1_specs/architecture_profile_draft.json")
    print("- artifacts/stage1_specs/architecture_profile_approval_request.md")
    print("- artifacts/stage1_specs/architecture_mapping_preview.csv")
    print("- artifacts/stage1_specs/architecture_profile_requirements_summary.csv")
    print("- artifacts/stage1_specs/architecture_profile_block_summary.csv")
    print("- artifacts/stage1_specs/architecture_profile_traceability.csv")
    print("- artifacts/stage1_specs/architecture_profile_ambiguity_dispositions.csv")
    print("- artifacts/orchestrator/stage_02_report.md")
    print("- artifacts/orchestrator/stage_02_crosscheck_report.md")
    print("- artifacts/orchestrator/stage_02_result.md")

    sync_cmd = [sys.executable, "scripts/sync_repo_memory_local.py", "--quiet"]
    sync_rc = subprocess.run(sync_cmd, cwd=repo_root).returncode
    if sync_rc != 0:
        print(f"Stage 1 specs runner: FAIL (memory sync exit={sync_rc})")
        return sync_rc

    rc = _run(repo_root, "Stage 1 specs.1 Generate Stage 1 specs baseline", ["scripts/generate_stage2_specs.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Stage 1 specs.2 Specs crosscheck agent", ["scripts/run_specs_crosscheck_agent.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Stage 1 specs.3 Validate Gate 2", ["scripts/validate_stage2_gate.py"])
    if rc != 0:
        return rc

    print("\nStage 1 specs runner: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
