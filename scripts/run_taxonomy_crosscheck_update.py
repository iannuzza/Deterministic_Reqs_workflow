#!/usr/bin/env python3
"""Run taxonomy cross-check/update from Stage 1 OCR outputs.

Deterministic script (no LLM calls):
- reads OCR index CSV
- resolves source spec path
- updates Stage 2 mapping_rules from detected domain signals
- writes taxonomy crosscheck report
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from repo_paths import resolve_repo_path
from typing import List

from extract_requirements_ocr import _update_taxonomy_rules_from_spec


def _read_index_rows(index_path: Path) -> List[list[str]]:
    rows: List[list[str]] = []
    with index_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required_cols = {"source_file", "page", "text_file", "status"}
        if set(reader.fieldnames or []) != required_cols:
            missing = sorted(required_cols - set(reader.fieldnames or []))
            raise ValueError(f"Invalid OCR index format: missing columns {missing}")

        for row in reader:
            rows.append(
                [
                    (row.get("source_file") or "").strip(),
                    (row.get("page") or "").strip(),
                    (row.get("text_file") or "").strip(),
                    (row.get("status") or "").strip(),
                ]
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Stage 1 taxonomy cross-check/update from OCR index")
    parser.add_argument(
        "--index-csv",
        default="artifacts/stage1_requirements/ocr_extracts/index.csv",
        help="Path to OCR index CSV",
    )
    parser.add_argument(
        "--initial-spec",
        default=None,
        help="Optional explicit source spec path (.pdf/.html/.docx). If omitted, inferred from index.csv",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    index_path = Path(args.index_csv)
    if not index_path.is_absolute():
        index_path = repo_root / index_path

    if not index_path.exists():
        print(f"Taxonomy crosscheck/update: FAIL - missing OCR index: {index_path}")
        return 1

    try:
        rows = _read_index_rows(index_path)
    except Exception as exc:
        print(f"Taxonomy crosscheck/update: FAIL - cannot read index: {exc}")
        return 1

    if not rows:
        print("Taxonomy crosscheck/update: FAIL - OCR index is empty")
        return 1

    if args.initial_spec:
        initial_spec = Path(args.initial_spec)
        if not initial_spec.is_absolute():
            initial_spec = repo_root / initial_spec
    else:
        source_file = rows[0][0]
        if not source_file:
            print("Taxonomy crosscheck/update: FAIL - source_file is empty in OCR index")
            return 1
        initial_spec = resolve_repo_path(repo_root, source_file)

    try:
        _update_taxonomy_rules_from_spec(repo_root, initial_spec.resolve(), rows)
    except Exception as exc:
        print(f"Taxonomy crosscheck/update: FAIL - {exc}")
        return 1

    print("Taxonomy crosscheck/update: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
