#!/usr/bin/env python3
"""Run the workflow from preflight through Step 3 (first three gates).

Step mapping used by this script:
- Step 0: scripts/run_step0_preflight.py
- Step 1: scripts/run_stage1_requirements_gate1.py
- Step 2: scripts/run_stage0_gate0.py
- Step 3: scripts/run_step3_gate1_gate2.py

The script stops at the first failing command and returns that exit code.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class CmdStep:
    name: str
    args: List[str]


def _run_step(repo_root: Path, step: CmdStep) -> int:
    print(f"\n=== {step.name} ===")
    cmd = [sys.executable, *step.args]
    print("Command:", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=repo_root)
    if completed.returncode != 0:
        print(f"FAILED: {step.name} (exit={completed.returncode})")
        return completed.returncode
    print(f"DONE: {step.name}")
    return 0


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    steps = [
        CmdStep(
            name="Step 0 - Dedicated runner",
            args=["scripts/run_step0_preflight.py"],
        ),
        CmdStep(
            name="Step 1 - Dedicated runner",
            args=["scripts/run_stage1_requirements_gate1.py"],
        ),
        CmdStep(
            name="Step 2 - Dedicated runner",
            args=["scripts/run_stage0_gate0.py"],
        ),
        CmdStep(
            name="Step 3 - Dedicated runner",
            args=["scripts/run_step3_gate1_gate2.py"],
        ),
    ]

    print("Running workflow until Step 3 (first three gates)")
    print(f"Repository root: {repo_root}")

    for step in steps:
        rc = _run_step(repo_root, step)
        if rc != 0:
            return rc

    print("\nWorkflow completed through Step 3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
