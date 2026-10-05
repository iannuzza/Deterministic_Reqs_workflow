#!/usr/bin/env python3
"""Dedicated Step 0 runner: preflight experience summary."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    sync_cmd = [sys.executable, "scripts/sync_repo_memory_local.py", "--quiet"]
    sync_rc = subprocess.run(sync_cmd, cwd=repo_root).returncode
    if sync_rc != 0:
        print(f"Step 0: FAIL (memory sync exit={sync_rc})")
        return sync_rc

    cmd = [
        sys.executable,
        "scripts/preflight_experience.py",
        "--experience-file",
        "docs/execution-experience-log.md",
        "--keywords",
        "stage1,rag,pypdf,pandoc,ssl,path",
        "--summary-out",
        "artifacts/orchestrator/preflight_experience_summary.md",
    ]

    print("Step 0: START")
    print("Command:", " ".join(cmd))
    rc = subprocess.run(cmd, cwd=repo_root).returncode
    if rc != 0:
        print(f"Step 0: FAIL (exit={rc})")
        return rc

    crosscheck_cmd = [sys.executable, "scripts/run_preflight_crosscheck_agent.py"]
    crosscheck_rc = subprocess.run(crosscheck_cmd, cwd=repo_root).returncode
    if crosscheck_rc != 0:
        print(f"Step 0: FAIL (preflight crosscheck exit={crosscheck_rc})")
        return crosscheck_rc

    print("Step 0: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
