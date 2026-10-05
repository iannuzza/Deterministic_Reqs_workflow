#!/usr/bin/env python3
"""Run requirements coverage crosscheck for Stage 1 outputs."""

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


def _read_ids(summary_csv: Path) -> list[str]:
    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        ids = []
        for row in reader:
            req_id = (row.get("id") or "").strip()
            if req_id:
                ids.append(req_id)
    return ids


def _read_policy_stats(summary_csv: Path) -> dict[str, int]:
    stats = {
        "total": 0,
        "tagged_preserve": 0,
        "tagged_architecture": 0,
        "generated_standard": 0,
        "unknown_policy": 0,
        "tagged_mismatch": 0,
    }
    with summary_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            stats["total"] += 1
            rid = (row.get("id") or "").strip()
            source_req_id = (row.get("source_req_id") or "").strip()
            id_policy = (row.get("id_policy") or "").strip().lower()
            if id_policy == "tagged_preserve":
                stats["tagged_preserve"] += 1
                if not source_req_id or rid != source_req_id:
                    stats["tagged_mismatch"] += 1
            elif id_policy == "tagged_architecture":
                stats["tagged_architecture"] += 1
                if not rid or source_req_id:
                    stats["tagged_mismatch"] += 1
            elif id_policy == "generated_standard":
                stats["generated_standard"] += 1
            else:
                stats["unknown_policy"] += 1
    return stats


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    summary_csv = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    rag_crosscheck = repo_root / "artifacts/stage1_requirements/requirements_rag_crosscheck.md"
    out_report = repo_root / "artifacts/stage1_requirements/coverage_crosscheck.md"
    out_missing = repo_root / "artifacts/stage1_requirements/missing_requirements_candidates.csv"

    findings: list[str] = []
    status = "pass"

    if not summary_csv.exists():
        findings.append("Missing requirements_summary.csv")
        status = "fail"
        req_ids: list[str] = []
        policy_stats = {
            "total": 0,
            "tagged_preserve": 0,
            "tagged_architecture": 0,
            "generated_standard": 0,
            "unknown_policy": 0,
            "tagged_mismatch": 0,
        }
    else:
        req_ids = _read_ids(summary_csv)
        policy_stats = _read_policy_stats(summary_csv)
        if not req_ids:
            findings.append("No requirement IDs found in requirements_summary.csv")
            status = "fail"
        if policy_stats["unknown_policy"] > 0:
            findings.append(f"Unknown id_policy rows: {policy_stats['unknown_policy']}")
            status = "fail"
        if policy_stats["tagged_mismatch"] > 0:
            findings.append(f"tagged_preserve mismatches: {policy_stats['tagged_mismatch']}")
            status = "fail"

    if not rag_crosscheck.exists():
        findings.append("Missing requirements_rag_crosscheck.md")
        status = "fail"

    out_missing.parent.mkdir(parents=True, exist_ok=True)
    out_missing.write_text("source_hint,reason\n", encoding="utf-8")

    lines = [
        "# Requirements Coverage Crosscheck",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"Status: {status}",
        "",
        "## Summary",
        f"- Requirements in summary: {len(req_ids)}",
        f"- ID policy tagged_preserve rows: {policy_stats['tagged_preserve']}",
        f"- ID policy tagged_architecture rows: {policy_stats['tagged_architecture']}",
        f"- ID policy generated_standard rows: {policy_stats['generated_standard']}",
        f"- ID policy unknown rows: {policy_stats['unknown_policy']}",
        f"- tagged_preserve mismatches: {policy_stats['tagged_mismatch']}",
        "- Missing candidates generated: 0",
        "",
        "## Findings",
    ]
    if findings:
        lines.extend([f"- {f}" for f in findings])
    else:
        lines.append("- None")

    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if status != "pass":
        print(f"Requirements coverage crosscheck: FAIL ({out_report})")
        _append_log(repo_root, script_name, "FAIL")
        return 1

    print(f"Requirements coverage crosscheck: PASS ({out_report})")
    _append_log(repo_root, script_name, f"PASS requirements={len(req_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
