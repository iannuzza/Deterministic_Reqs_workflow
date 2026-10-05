#!/usr/bin/env python3
"""Generic Stage 0 gate validator.

Checks minimum required artifacts for ontology baseline.
"""

from pathlib import Path
import re
from datetime import datetime
from validate_common_formatting import validate_stage_markdown


REQUIRED = [
    Path("artifacts/stage0_ontology/ontology.md"),
    Path("artifacts/stage0_ontology/glossary.csv"),
    Path("artifacts/stage0_ontology/semantic_issues.md"),
    Path("artifacts/stage2_mirco_arc/uArch_analysis.agent.md"),
    Path("artifacts/orchestrator/stage_00_report.md"),
    Path("artifacts/orchestrator/stage_00_crosscheck_report.md"),
]

PLACEHOLDER_RE = re.compile(r"<[^>]+>")


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _write_result(repo_root: Path, status: str, missing: list[str]) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_00_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 00 Result",
        "",
        f"- Timestamp: {timestamp}",
        f"- Status: {status}",
        "",
        "## Checked Files",
    ]
    lines.extend([f"- {path.as_posix()}" for path in REQUIRED])
    lines.append("")
    lines.append("## Missing Files")
    if missing:
        lines.extend([f"- {item}" for item in missing])
    else:
        lines.append("- None")
    result_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, f"START cwd={Path.cwd().as_posix()}")
    missing = [str(p) for p in REQUIRED if not (repo_root / p).exists()]
    quality_issues: list[str] = []
    quality_issues.extend(validate_stage_markdown(repo_root, "0"))

    ontology = repo_root / "artifacts/stage0_ontology/ontology.md"
    glossary = repo_root / "artifacts/stage0_ontology/glossary.csv"
    semantic = repo_root / "artifacts/stage0_ontology/semantic_issues.md"
    report = repo_root / "artifacts/orchestrator/stage_00_report.md"

    if ontology.exists():
        text = ontology.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER_RE.search(text):
            quality_issues.append("ontology.md contains template placeholders")
        if len(re.findall(r"\bONT_(SYS|ANA|DIG)_\d{3}\b", text)) < 5:
            quality_issues.append("ontology.md does not contain enough ontology concepts")

    if glossary.exists():
        text = glossary.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER_RE.search(text):
            quality_issues.append("glossary.csv contains template placeholders")
        if len([ln for ln in text.splitlines() if ln.strip()]) < 6:
            quality_issues.append("glossary.csv has too few populated rows")

    if semantic.exists():
        text = semantic.read_text(encoding="utf-8", errors="ignore").lower()
        if "## critical" not in text or "## major" not in text or "## minor" not in text:
            quality_issues.append("semantic_issues.md missing required severity sections")

    if report.exists():
        text = report.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER_RE.search(text):
            quality_issues.append("stage_00_report.md contains template placeholders")

    if missing:
        print("Stage 0: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        _write_result(repo_root, "FAIL", missing)
        _append_log(repo_root, script_name, f"FAIL missing={';'.join(missing)}")
        return 1

    if quality_issues:
        print("Stage 0: FAIL")
        for item in quality_issues:
            print(f"- quality: {item}")
        _write_result(repo_root, "FAIL", quality_issues)
        _append_log(repo_root, script_name, f"FAIL quality={';'.join(quality_issues)}")
        return 1

    print("Stage 0: PASS")
    _write_result(repo_root, "PASS", [])
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

