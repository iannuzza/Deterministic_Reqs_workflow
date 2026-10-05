#!/usr/bin/env python3
"""Generate and centrally validate the complete approved-snapshot SysML set."""

from __future__ import annotations

import argparse
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

    for label, command in (
        (
            "Final SysML generation",
            ["scripts/generate_architecture_sysml.py", "--snapshot-id", snapshot_id],
        ),
        (
            "Final SysML structural review",
            ["scripts/review_architecture_sysml.py", "--scope", "stage3-structural"],
        ),
        (
            "Final SysML central coherence validation",
            ["scripts/validate_downstream_coherence.py", "--snapshot-id", snapshot_id],
        ),
    ):
        if _run(root, label, command):
            return 1
    print("\nFinal SysML phase: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())