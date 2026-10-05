#!/usr/bin/env python3
"""Run preflight crosscheck after Step 0 preflight summary generation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    summary = repo_root / "artifacts/orchestrator/preflight_experience_summary.md"
    out = repo_root / "artifacts/orchestrator/stage_preflight_crosscheck_report.md"

    status = "pass"
    findings: list[str] = []

    if not summary.exists():
        status = "fail"
        findings.append("Missing preflight summary artifact")
    else:
        text = summary.read_text(encoding="utf-8")
        if "Execution Experience" not in text and "experience" not in text.lower():
            findings.append("Summary content is present but lacks explicit execution-experience context")

    lines = [
        "# Preflight Crosscheck Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
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
        print(f"Preflight crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"Preflight crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
