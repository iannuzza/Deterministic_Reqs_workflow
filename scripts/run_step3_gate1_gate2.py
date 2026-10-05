#!/usr/bin/env python3
"""Dedicated Step 3 runner: Gate 1 validation, Stage 2 generation, Gate 2 validation."""

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
    sync_cmd = [sys.executable, "scripts/sync_repo_memory_local.py", "--quiet"]
    sync_rc = subprocess.run(sync_cmd, cwd=repo_root).returncode
    if sync_rc != 0:
        print(f"Step 3: FAIL (memory sync exit={sync_rc})")
        return sync_rc

    rc = _run(repo_root, "Step 3.1 Validate Gate 1", ["scripts/validate_stage1_gate.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Step 3.2 Generate Stage 2 baseline artifacts", ["scripts/generate_stage2_specs.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Step 3.3 Specs crosscheck agent", ["scripts/run_specs_crosscheck_agent.py"])
    if rc != 0:
        return rc

    rc = _run(repo_root, "Step 3.4 Validate Gate 2", ["scripts/validate_stage2_gate.py"])
    if rc != 0:
        return rc

    print("\nStep 3: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
