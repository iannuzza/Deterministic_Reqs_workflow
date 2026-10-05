#!/usr/bin/env python3
"""Generic Stage 2 gate validator.

Checks minimum required artifacts for specification formalization.
"""

from pathlib import Path
from datetime import datetime
from validate_common_formatting import validate_stage_markdown


REQUIRED = [
    Path("artifacts/stage1_specs/specs.md"),
    Path("artifacts/stage1_specs/traceability_seed.csv"),
    Path("artifacts/stage1_specs/architecture_profile_draft.json"),
    Path("artifacts/stage1_specs/architecture_profile_approval_request.md"),
    Path("artifacts/stage1_specs/architecture_mapping_preview.csv"),
    Path("artifacts/stage1_specs/architecture_profile_requirements_summary.csv"),
    Path("artifacts/stage1_specs/architecture_profile_block_summary.csv"),
    Path("artifacts/stage1_specs/architecture_profile_traceability.csv"),
    Path("artifacts/stage1_specs/architecture_profile_ambiguity_dispositions.csv"),
    Path("artifacts/orchestrator/stage_02_report.md"),
    Path("artifacts/orchestrator/stage_02_crosscheck_report.md"),
]


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _write_result(repo_root: Path, status: str, missing: list[str]) -> None:
    result_file = repo_root / "artifacts/orchestrator/stage_02_result.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Stage 02 Result",
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
    findings: list[str] = []
    findings.extend(validate_stage_markdown(repo_root, "2"))
    crosscheck = repo_root / "artifacts/orchestrator/stage_02_crosscheck_report.md"
    if crosscheck.exists() and "status: pass" not in crosscheck.read_text(encoding="utf-8", errors="ignore").lower():
        findings.append("Stage 2 crosscheck report status is not pass")
    if missing or findings:
        print("Stage 2: FAIL")
        for item in missing:
            print(f"- missing: {item}")
        for item in findings:
            print(f"- finding: {item}")
        _write_result(repo_root, "FAIL", missing + findings)
        _append_log(repo_root, script_name, f"FAIL findings={';'.join(missing + findings)}")
        return 1
    print("Stage 2: PASS")
    _write_result(repo_root, "PASS", [])
    _append_log(repo_root, script_name, "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
