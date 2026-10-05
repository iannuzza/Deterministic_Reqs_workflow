#!/usr/bin/env python3
"""Hard guard: Stage 2+ scripts must not read the initial source specification directly.

This check enforces that only Stage 1 can read specs/*.pdf (or use --initial-spec).
Stage 2+ must consume Stage 1 artifacts instead.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
from typing import List, Tuple


TARGET_SCRIPTS = [
    "scripts/generate_stage2_specs.py",
    "scripts/run_specs_crosscheck_agent.py",
    "scripts/validate_stage2_gate.py",
    "scripts/run_stage2_micro_arch_and_crosscheck.py",
    "scripts/validate_stage2_micro_arc_gate.py",
    "scripts/run_srs_gen_spec_agent.py",
    "scripts/run_srs_crosscheck_agent.py",
    "scripts/run_srs_latex_crosscheck_agent.py",
    "scripts/validate_stage3_srs_gate.py",
    "scripts/run_ars_gen_spec_agent.py",
    "scripts/run_ars_crosscheck_agent.py",
    "scripts/validate_stage4_ars_gate.py",
    "scripts/run_drs_gen_spec_agent.py",
    "scripts/run_drs_crosscheck_agent.py",
    "scripts/validate_stage5_drs_gate.py",
]

FORBIDDEN_PATTERNS: List[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bPdfReader\s*\("), "Direct PDF parsing is forbidden in Stage 2+"),
    (re.compile(r"\bfrom\s+pypdf\s+import\s+PdfReader\b"), "pypdf PdfReader import is forbidden in Stage 2+"),
    (re.compile(r"--initial-spec\b"), "--initial-spec usage is forbidden in Stage 2+"),
    (re.compile(r"--initial-pdf\b"), "--initial-pdf usage is forbidden in Stage 2+"),
    (re.compile(r"source_spec_path"), "source_spec_path dependency is forbidden in Stage 2+"),
    (re.compile(r"specs[\\/][^\n\r\"']*\.pdf", flags=re.IGNORECASE), "Direct specs/*.pdf path usage is forbidden in Stage 2+"),
]


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\\n")


def _scan_file(path: Path) -> List[str]:
    findings: List[str] = []
    if not path.exists():
        findings.append(f"Missing required script for guard scope: {path.as_posix()}")
        return findings

    text = path.read_text(encoding="utf-8", errors="ignore")
    for pattern, reason in FORBIDDEN_PATTERNS:
        for match in pattern.finditer(text):
            line_no = text.count("\n", 0, match.start()) + 1
            findings.append(f"{path.as_posix()}:{line_no}: {reason}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Enforce Stage 2+ independence from initial source spec")
    parser.add_argument("--quiet", action="store_true", help="Print only failures")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name

    findings: List[str] = []
    for rel in TARGET_SCRIPTS:
        findings.extend(_scan_file((repo_root / rel).resolve()))

    if findings:
        if not args.quiet:
            print("Stage 2+ source-spec independence guard: FAIL")
        for item in findings:
            print(f"- {item}")
        _append_log(repo_root, script_name, f"FAIL findings={len(findings)}")
        return 1

    if not args.quiet:
        print("Stage 2+ source-spec independence guard: PASS")
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
