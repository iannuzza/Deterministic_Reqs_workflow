#!/usr/bin/env python3
"""Run Stage 1 requirements workflow through Gate 1 validation.

This dedicated runner executes:
1) OCR extraction
2) Taxonomy cross-check/update
3) RAG index build
4) Stage 1 requirements generation
5) RAG crosscheck of requirements
6) Requirements coverage crosscheck agent
7) Gate 1 validation
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class CmdStep:
    name: str
    args: List[str]


def _run(repo_root: Path, step: CmdStep) -> int:
    cmd = [sys.executable, *step.args]
    print(f"\n{step.name}: START")
    print("Command:", " ".join(cmd))
    rc = subprocess.run(cmd, cwd=repo_root).returncode
    if rc != 0:
        print(f"{step.name}: FAIL (exit={rc})")
        return rc
    print(f"{step.name}: PASS")
    return 0


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    print("Stage 1 requirements full flow")
    print("This run will generate and validate:")
    print("- artifacts/stage1_requirements/ocr_extracts/index.csv")
    print("- artifacts/stage1_requirements/taxonomy_crosscheck.md")
    print("- artifacts/stage1_requirements/requirements_raw.md")
    print("- artifacts/stage1_requirements/requirements_summary.csv")
    print("- artifacts/stage1_requirements/requirements_summary.md")
    print("- artifacts/stage1_requirements/duplicate_source_req_ids.csv")
    print("- artifacts/stage1_requirements/requirements_rag_crosscheck.md")
    print("- artifacts/stage1_requirements/coverage_crosscheck.md")
    print("- artifacts/stage1_requirements/missing_requirements_candidates.csv")
    print("- artifacts/orchestrator/stage_01_report.md")
    print("- artifacts/orchestrator/stage_01_result.md")

    sync_cmd = [sys.executable, "scripts/sync_repo_memory_local.py", "--quiet"]
    sync_rc = subprocess.run(sync_cmd, cwd=repo_root).returncode
    if sync_rc != 0:
        print(f"Stage 1 runner: FAIL (memory sync exit={sync_rc})")
        return sync_rc

    steps = [
        CmdStep("Stage 1.1 OCR extraction", ["scripts/extract_requirements_ocr.py", "--spec-folder", "specs"]),
        CmdStep(
            "Stage 1.2 Taxonomy crosscheck/update",
            ["scripts/run_taxonomy_crosscheck_update.py", "--index-csv", "artifacts/stage1_requirements/ocr_extracts/index.csv"],
        ),
        CmdStep("Stage 1.3 Build RAG index", ["scripts/build_rag_index.py"]),
        CmdStep(
            "Stage 1.4 Generate Stage 1 requirements",
            [
                "scripts/generate_stage1_requirements.py",
                "--index",
                "artifacts/stage1_requirements/ocr_extracts/index.csv",
                "--raw",
                "artifacts/stage1_requirements/requirements_raw.md",
                "--summary-csv",
                "artifacts/stage1_requirements/requirements_summary.csv",
                "--summary-md",
                "artifacts/stage1_requirements/requirements_summary.md",
                "--stage-report",
                "artifacts/orchestrator/stage_01_report.md",
                "--min-target",
                "100",
            ],
        ),
        CmdStep(
            "Stage 1.5 Crosscheck requirements vs RAG",
            [
                "scripts/crosscheck_stage1_requirements_rag.py",
                "--summary-csv",
                "artifacts/stage1_requirements/requirements_summary.csv",
                "--index-csv",
                "artifacts/stage1_requirements/ocr_extracts/index.csv",
                "--summary-md",
                "artifacts/stage1_requirements/requirements_summary.md",
                "--raw-md",
                "artifacts/stage1_requirements/requirements_raw.md",
                "--stage-report",
                "artifacts/orchestrator/stage_01_report.md",
                "--crosscheck-report",
                "artifacts/stage1_requirements/requirements_rag_crosscheck.md",
            ],
        ),
        CmdStep(
            "Stage 1.6 Requirements coverage crosscheck agent",
            ["scripts/run_requirements_coverage_crosscheck_agent.py"],
        ),
        CmdStep("Stage 1.7 Validate Gate 1", ["scripts/validate_stage1_gate.py"]),
    ]

    for step in steps:
        rc = _run(repo_root, step)
        if rc != 0:
            return rc

    print("\nStage 1 runner: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
