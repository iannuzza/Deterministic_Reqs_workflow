#!/usr/bin/env python3
"""Preflight: read reusable execution experience before running workflow steps."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def _append_log(repo_root: Path, script_name: str, message: str) -> None:
    logs_dir = repo_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "python_run_execution.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] [{script_name}] {message}\n")


def _extract_relevant_sections(text: str, keywords: list[str]) -> str:
    if not keywords:
        return text

    lines = text.splitlines()
    sections: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if line.startswith("### "):
            if current:
                sections.append(current)
            current = [line]
        else:
            if current:
                current.append(line)

    if current:
        sections.append(current)

    if not sections:
        return text

    lowered = [kw.lower() for kw in keywords]
    matched: list[str] = []
    for sec in sections:
        block = "\n".join(sec)
        block_l = block.lower()
        if any(kw in block_l for kw in lowered):
            matched.append(block)

    if not matched:
        return text

    header = [
        "# Preflight Experience Extract",
        "",
        f"- Keywords: {', '.join(keywords)}",
        "",
    ]
    return "\n".join(header + matched) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Read and print execution experience before workflow run")
    parser.add_argument(
        "--experience-file",
        default="docs/execution-experience-log.md",
        help="Path to local execution experience log",
    )
    parser.add_argument(
        "--keywords",
        default="",
        help="Comma-separated keywords to focus relevant sections (example: stage1,rag,pypdf)",
    )
    parser.add_argument(
        "--summary-out",
        default="artifacts/orchestrator/preflight_experience_summary.md",
        help="Where to save printed preflight summary",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    script_name = Path(__file__).name
    _append_log(repo_root, script_name, "START")

    exp_path = Path(args.experience_file)
    if not exp_path.is_absolute():
        exp_path = (repo_root / exp_path).resolve()

    if not exp_path.exists():
        print(f"Preflight experience: FAIL (file not found: {exp_path})")
        _append_log(repo_root, script_name, f"FAIL missing={exp_path.as_posix()}")
        return 1

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    text = exp_path.read_text(encoding="utf-8", errors="ignore")
    extracted = _extract_relevant_sections(text, keywords)

    summary_path = Path(args.summary_out)
    if not summary_path.is_absolute():
        summary_path = (repo_root / summary_path).resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(extracted, encoding="utf-8")

    print("Preflight experience: PASS")
    print(f"- Source: {exp_path}")
    if keywords:
        print(f"- Keywords: {', '.join(keywords)}")
    print(f"- Summary: {summary_path}")

    _append_log(
        repo_root,
        script_name,
        f"PASS source={exp_path.as_posix()} keywords={','.join(keywords)} summary={summary_path.as_posix()}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
