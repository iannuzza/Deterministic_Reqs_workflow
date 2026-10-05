#!/usr/bin/env python3
"""Run SRS LaTeX crosscheck for combined TeX output."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


REQUIRED = [
    "artifacts/stage3_srs/stage2_srs_combined.tex",
    "artifacts/stage3_srs/system_requirements_specification.md",
]


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

    missing = [rel for rel in REQUIRED if not (repo_root / rel).exists()]
    tex = repo_root / "artifacts/stage3_srs/stage2_srs_combined.tex"

    status = "pass"
    findings: list[str] = []

    if missing:
        status = "fail"
        findings.append("Missing required artifacts: " + ", ".join(missing))

    if tex.exists():
        content = tex.read_text(encoding="utf-8")
        if "\\documentclass" not in content or "\\end{document}" not in content:
            status = "fail"
            findings.append("Combined TeX missing required LaTeX document boundaries")

    out = repo_root / "artifacts/orchestrator/stage_srs_latex_crosscheck_report.md"
    lines = [
        "# Stage SRS LaTeX Crosscheck Report",
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
        print(f"SRS LaTeX crosscheck: FAIL ({out})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"SRS LaTeX crosscheck: PASS ({out})")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
