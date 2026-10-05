#!/usr/bin/env python3
"""Run specs crosscheck for Stage 2 formalization outputs."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _count_rows(csv_path: Path) -> int:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return sum(1 for _ in reader)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    specs_md = repo_root / "artifacts/stage1_specs/specs.md"
    trace_seed = repo_root / "artifacts/stage1_specs/traceability_seed.csv"
    stage_report = repo_root / "artifacts/orchestrator/stage_02_report.md"
    out = repo_root / "artifacts/orchestrator/stage_02_crosscheck_report.md"

    findings: list[str] = []
    status = "pass"

    if not specs_md.exists():
        findings.append("Missing specs.md")
        status = "fail"

    if not trace_seed.exists():
        findings.append("Missing traceability_seed.csv")
        status = "fail"
        row_count = 0
    else:
        row_count = _count_rows(trace_seed)
        if row_count == 0:
            findings.append("traceability_seed.csv has zero rows")
            status = "fail"

    if not stage_report.exists():
        findings.append("Missing stage_02_report.md")
        status = "fail"

    lines = [
        "# Stage 02 Crosscheck Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
        "",
        "## Summary",
        f"- Traceability seed rows: {row_count}",
        "",
        "## Findings",
    ]
    if findings:
        lines.extend([f"- {f}" for f in findings])
    else:
        lines.append("- None")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\\n".join(lines) + "\\n", encoding="utf-8")

    if status != "pass":
        print(f"Specs crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"Specs crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, f"PASS rows={row_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
