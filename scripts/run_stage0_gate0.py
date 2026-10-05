#!/usr/bin/env python3
"""Dedicated Stage 0 runner: initialize ontology artifacts and validate Gate 0."""

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

    print("Stage 0 full flow")
    print("This run will generate and validate:")
    print("- artifacts/stage0_ontology/ontology.md")
    print("- artifacts/stage0_ontology/glossary.csv")
    print("- artifacts/stage0_ontology/semantic_issues.md")
    print("- artifacts/orchestrator/stage_00_report.md")
    print("- artifacts/orchestrator/stage_00_result.md")

    sync_cmd = [sys.executable, "scripts/sync_repo_memory_local.py", "--quiet"]
    sync_rc = subprocess.run(sync_cmd, cwd=repo_root).returncode
    if sync_rc != 0:
        print(f"Stage 0 runner: FAIL (memory sync exit={sync_rc})")
        return sync_rc

    rc = _run(repo_root, "Stage 0.1 Initialize Stage 0 artifacts", ["scripts/init_stage0_artifacts.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Stage 0.2 Generate ontology artifacts", ["scripts/generate_stage0_ontology_outputs.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Stage 0.3 Generate ontology analysis report", ["scripts/generate_stage0_ontology_report.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Stage 0.4 Ontology crosscheck agent", ["scripts/run_ontology_crosscheck_agent.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Stage 0.5 Validate Gate 0", ["scripts/validate_stage0_gate.py"])
    if rc != 0:
        return rc

    print("\nStage 0 runner: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
