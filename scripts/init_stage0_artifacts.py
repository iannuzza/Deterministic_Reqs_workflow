#!/usr/bin/env python3
"""Initialize Stage 0 ontology artifacts from templates.

Creates missing Gate 0 files in artifacts/ without overwriting existing files.
"""

from pathlib import Path
import shutil
from datetime import datetime


FILES = [
    ("templates/artifacts/stage0_ontology/ontology.md", "artifacts/stage0_ontology/ontology.md"),
    ("templates/artifacts/stage0_ontology/glossary.csv", "artifacts/stage0_ontology/glossary.csv"),
    ("templates/artifacts/stage0_ontology/semantic_issues.md", "artifacts/stage0_ontology/semantic_issues.md"),
    ("templates/artifacts/stage0_ontology/uArch_analysis.agent.md", "artifacts/stage2_mirco_arc/uArch_analysis.agent.md"),
    ("templates/artifacts/stage2_mirco_arc/architecture_crosscheck_report.md", "artifacts/stage2_mirco_arc/architecture_crosscheck_report.md"),
    ("templates/artifacts/orchestrator/stage_00_report.md", "artifacts/orchestrator/stage_00_report.md"),
]


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    created = []
    skipped = []
    missing_templates = []

    for src_rel, dst_rel in FILES:
        src = repo_root / src_rel
        dst = repo_root / dst_rel

        if not src.exists():
            missing_templates.append(src_rel)
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists():
            skipped.append(dst_rel)
            continue

        shutil.copy2(src, dst)
        created.append(dst_rel)

    if missing_templates:
        print("Stage 0 init: FAIL")
        for item in missing_templates:
            print(f"- missing template: {item}")
        _append_log(repo_root, script_name, f"FAIL missing_templates={','.join(missing_templates)}")
        return 1

    print("Stage 0 init: DONE")
    if created:
        print("Created:")
        for item in created:
            print(f"- {item}")
    if skipped:
        print("Already exists (kept):")
        for item in skipped:
            print(f"- {item}")

    _append_log(repo_root, script_name, f"PASS created={len(created)} skipped={len(skipped)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

