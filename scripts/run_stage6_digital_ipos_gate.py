#!/usr/bin/env python3
"""Generate and validate the deterministic digital IPOS stage."""

from __future__ import annotations

import subprocess
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

from validate_downstream_coherence import validate


def _activity_start(label: str) -> datetime:
    started_at = datetime.now().astimezone()
    print(
        f"[IPOS_ACTIVITY] START | {started_at.isoformat(timespec='seconds')} | {label}",
        flush=True,
    )
    return started_at


def _activity_end(label: str, started_at: datetime, outcome: str) -> None:
    finished_at = datetime.now().astimezone()
    elapsed = str(finished_at - started_at).split(".", 1)[0]
    print(
        f"[IPOS_ACTIVITY] END | {finished_at.isoformat(timespec='seconds')} | "
        f"{label} | {outcome} | elapsed={elapsed}",
        flush=True,
    )


def _run_activity(label: str, action):
    started_at = _activity_start(label)
    outcome = "exception"
    try:
        result = action()
        outcome = f"exit={result.returncode}"
        return result
    finally:
        _activity_end(label, started_at, outcome)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Digital IPOS from an approved snapshot.")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--snapshot-id")
    selector.add_argument("--use-latest-approved", action="store_true")
    parser.add_argument(
        "--regenerate-downstream",
        action="store_true",
        help="Explicitly refresh rendered Digital IPOS artifacts before final coherence validation.",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    snapshot_args = ["--use-latest-approved"] if args.use_latest_approved else ["--snapshot-id", args.snapshot_id]
    snapshot_id = args.snapshot_id
    if args.use_latest_approved:
        from approved_snapshot_resolver import resolve_complete_snapshot_id
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
            "digital",
            *snapshot_args,
            *( ["--regenerate-downstream"] if args.regenerate_downstream else [] ),
        ],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_descriptive_summary.py"],
        [sys.executable, "scripts/validate_ipos_gate.py", "--kind", "digital", *snapshot_args],
    ]
    activity_labels = (
        "Generate Digital IPOS documents",
        "Run Digital IPOS descriptive regression tests",
        "Validate Digital IPOS gate",
    )
    for index, command in enumerate(commands):
        result = _run_activity(
            activity_labels[index],
            lambda command=command: subprocess.run(command, cwd=root),
        )
        if result.returncode:
            if index == 1:
                print(f"Digital IPOS descriptive regression tests: FAIL (exit={result.returncode})")
            return 1
    if args.regenerate_downstream:
        label = "Validate downstream snapshot coherence"
        started_at = _activity_start(label)
        result = None
        try:
            result = validate(root, snapshot_id)
        finally:
            outcome = f"decision={result['decision']}" if result is not None else "exception"
            _activity_end(label, started_at, outcome)
        if result["decision"] != "PASS":
            print(f"Digital IPOS downstream coherence: {result['decision']} ({result['finding_count']} findings)")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
