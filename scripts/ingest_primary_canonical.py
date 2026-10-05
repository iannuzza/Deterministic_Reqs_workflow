#!/usr/bin/env python3
"""Promote the approved primary Stage 1 corpus through the canonical merge path."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from merge_engine import merge_staging_batch, register_staged_ingestion


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def prepare_primary_ingestion(repo_root: Path) -> Path:
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8"))
    source_name = Path(str(context["source_spec_path"])).name
    corpus_path = repo_root / "artifacts/stage1_requirements/requirements_summary.csv"
    source_rows = [row for row in _read_rows(corpus_path) if row.get("source_req_id")]
    if not source_rows:
        raise ValueError(f"Primary corpus has no source_req_id rows: {corpus_path}")
    digest = hashlib.sha256(json.dumps(source_rows, sort_keys=True).encode("utf-8")).hexdigest()[:24]
    ingestion_dir = repo_root / "artifacts/source_ingestion" / f"primary_{digest}"
    ingestion_dir.mkdir(parents=True, exist_ok=True)
    normalized = []
    review = []
    for row in source_rows:
        requirement_id = row["source_req_id"]
        common = {
            "staged_id": f"primary:{requirement_id}",
            "source_req_id": requirement_id,
            "requirement_statement": row.get("requirement_statement", ""),
            "source_spec": source_name,
            "source_revision": "stage1-approved",
            "source_page": row.get("source_section_owner", ""),
            "source_chunk_id": row.get("source_section_owner", ""),
            "classification": row.get("category", "unknown"),
            "req_class": "new",
        }
        normalized.append(common)
        review.append({
            **common,
            "matched_canonical_id": "",
            "match_reason": "approved primary Stage 1 source corpus",
            "recommended_action": "merge",
            "review_decision": "approved",
            "reviewer_notes": "",
        })
    _write_rows(ingestion_dir / "normalized_requirements.csv", list(normalized[0]), normalized)
    _write_rows(ingestion_dir / "comparison_results.csv", list(review[0]), review)
    metadata = {
        "project_id": context.get("project_name") or repo_root.name,
        "source_spec": source_name,
        "source_kind": "primary",
        "source_revision": "stage1-approved",
        "source_scope": "system",
        "target_scope": "system",
        "ingestion_id": f"primary_{digest}",
        "approved_by": "stage1-approved",
    }
    (ingestion_dir / "source_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ingestion_dir


def ingest_primary(repo_root: Path, reviewer: str) -> dict[str, object]:
    ingestion_dir = prepare_primary_ingestion(repo_root)
    staging_batch_id = register_staged_ingestion(repo_root, ingestion_dir)
    context = json.loads((repo_root / "config/project_context.json").read_text(encoding="utf-8"))
    project_id = str(context.get("project_name") or repo_root.name)
    result = merge_staging_batch(repo_root, project_id=project_id, staging_batch_id=staging_batch_id, approved_by=reviewer)
    return {"ingestion_dir": str(ingestion_dir), "staging_batch_id": staging_batch_id, **result}


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge the approved primary Stage 1 corpus into canonical SQLite.")
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    print(json.dumps(ingest_primary(Path(__file__).resolve().parents[1], args.reviewer), indent=2, default=list))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())