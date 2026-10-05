#!/usr/bin/env python3
"""Generate and validate the deterministic analog IPOS stage."""

from __future__ import annotations

import subprocess
import sys
import argparse
import json
from pathlib import Path

from approved_snapshot_resolver import resolve_complete_snapshot_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Analog IPOS from an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    parser.add_argument(
        "--regenerate-downstream",
        action="store_true",
        help="Explicitly refresh rendered Analog IPOS artifacts before final coherence validation.",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    snapshot_args = ["--use-latest-approved"] if args.use_latest_approved else ["--snapshot-id", args.snapshot_id]
    snapshot_id = args.snapshot_id
    if args.use_latest_approved:
        context = json.loads((root / "config" / "project_context.json").read_text(encoding="utf-8"))
        snapshot_id = resolve_complete_snapshot_id(
            root,
            project_id=str(context.get("project_name") or root.name),
        )
        if args.regenerate_downstream:
            snapshot_args = ["--snapshot-id", snapshot_id]
    commands = [
        [
            sys.executable,
            "scripts/generate_ipos_specs.py",
            "--kind",
            "analog",
            *snapshot_args,
            *( ["--regenerate-downstream"] if args.regenerate_downstream else [] ),
        ],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_descriptive_summary.py"],
        [sys.executable, "scripts/validate_ipos_gate.py", "--kind", "analog", *snapshot_args],
    ]
    for index, command in enumerate(commands):
        result = subprocess.run(command, cwd=root)
        if result.returncode:
            if index == 1:
                print(f"Analog IPOS descriptive regression tests: FAIL (exit={result.returncode})")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
