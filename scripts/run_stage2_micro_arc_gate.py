#!/usr/bin/env python3
"""Run Stage 2 micro-architecture flow through gate validation."""

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

    print("Stage 2 micro-architecture full flow")
    print(f"Repo root: {repo_root.as_posix()}")
    print(f"Python executable: {sys.executable}")
    print("This run will generate and validate:")
    print("- artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv")
    print("- artifacts/stage2_mirco_arc/block_inventory.csv")
    print("- artifacts/stage2_mirco_arc/interface_catalog.csv")
    print("- artifacts/stage2_mirco_arc/interaction_matrix.csv")
    print("- artifacts/stage2_mirco_arc/function_decomposition.md")
    print("- artifacts/stage2_mirco_arc/micro_architecture_report.md")
    print("- artifacts/stage2_mirco_arc/architecture_crosscheck_report.md")
    print("- artifacts/orchestrator/stage_02_micro_arch_report.md")
    print("- artifacts/orchestrator/stage_02_micro_arch_result.md")

    rc = _run(
        repo_root,
        "Stage 2 micro-architecture.1 Generate + crosscheck",
        ["scripts/run_stage2_micro_arch_and_crosscheck.py"],
    )
    if rc != 0:
        return rc

    rc = _run(
        repo_root,
        "Stage 2 micro-architecture.2 Validate micro-architecture gate",
        ["scripts/validate_stage2_micro_arc_gate.py"],
    )
    if rc != 0:
        return rc

    print("\nStage 2 micro-architecture full flow: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
