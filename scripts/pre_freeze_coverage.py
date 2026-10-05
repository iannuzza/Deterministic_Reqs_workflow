"""Deterministic canonical-coverage gate before immutable snapshot freezing."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from canonical_store import connect


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _source_key(row: dict[str, str], primary_source: str) -> str:
    supplementary = (row.get("supplementary_source_spec") or "").strip()
    return supplementary or primary_source


def validate_pre_freeze_coverage(repo_root: Path, *, project_id: str) -> dict[str, object]:
    """Validate approved review scope against canonical source and merge authority."""
    context_path = repo_root / "config/project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    primary_source = Path(str(context.get("source_spec_path") or "primary-source")).name
    review_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    if not review_path.exists():
        raise RuntimeError("Pre-freeze coverage requires architecture_mapping_preview.csv.")
    exclusions = {str(value).strip() for value in context.get("pre_freeze_approved_exclusions", []) if str(value).strip()}
    reviewed = [
        row for row in _read_rows(review_path)
        if (row.get("review_decision") or "").strip().casefold() in {"approved", "reassigned"}
    ]
    review_ids = {row.get("requirement_id", "").strip() for row in reviewed if row.get("requirement_id", "").strip()}
    expected_by_source: dict[str, set[str]] = {}
    for row in reviewed:
        requirement_id = row.get("requirement_id", "").strip()
        if requirement_id and requirement_id not in exclusions:
            expected_by_source.setdefault(_source_key(row, primary_source), set()).add(requirement_id)

    connection = connect(repo_root)
    try:
        registered = {
            str(row["source_name"]): str(row["source_spec_id"])
            for row in connection.execute(
                "SELECT source_spec_id, source_name FROM source_specs WHERE project_id = ?",
                (project_id,),
            ).fetchall()
        }
        canonical_by_source: dict[str, set[str]] = {}
        for row in connection.execute(
            """SELECT ss.source_name, rp.source_req_id
                 FROM requirement_provenance rp
                 JOIN source_revisions sr ON sr.source_revision_id = rp.source_revision_id
                 JOIN source_specs ss ON ss.source_spec_id = sr.source_spec_id
                WHERE ss.project_id = ?""",
            (project_id,),
        ).fetchall():
            if row["source_req_id"]:
                canonical_by_source.setdefault(str(row["source_name"]), set()).add(str(row["source_req_id"]))
        merged_source_ids = {
            str(row["source_spec_id"])
            for row in connection.execute(
                """SELECT DISTINCT sir.source_spec_id
                     FROM merge_operations mo
                     JOIN staging_batches sb ON sb.staging_batch_id = mo.staging_batch_id
                     JOIN source_integration_records sir ON sir.staging_batch_id = sb.staging_batch_id
                    WHERE mo.project_id = ? AND mo.decision = 'approved' AND mo.completed_at IS NOT NULL""",
                (project_id,),
            ).fetchall()
        }
    finally:
        connection.close()

    expected_sources = sorted(expected_by_source)
    missing_registrations = sorted(source for source in expected_sources if source not in registered)
    missing_merge_history = sorted(source for source in expected_sources if source in registered and registered[source] not in merged_source_ids)
    missing_ids = sorted(
        requirement_id
        for source, requirement_ids in expected_by_source.items()
        for requirement_id in requirement_ids - canonical_by_source.get(source, set())
    )
    source_counts = {
        source: {
            "review": len(expected_by_source.get(source, set())),
            "canonical": len(canonical_by_source.get(source, set()) & expected_by_source.get(source, set())),
        }
        for source in expected_sources
    }
    rejection_reasons = []
    if missing_registrations:
        rejection_reasons.append("missing canonical source registration: " + ", ".join(missing_registrations))
    if missing_merge_history:
        rejection_reasons.append("missing completed canonical merge: " + ", ".join(missing_merge_history))
    if missing_ids:
        rejection_reasons.append("approved review requirements missing from canonical authority: " + ", ".join(missing_ids[:20]))
    manifest = {
        "project_id": project_id,
        "expected_in_scope_source_specs": expected_sources,
        "registered_canonical_source_specs": sorted(registered),
        "missing_source_registrations": missing_registrations,
        "review_counts_by_source": {source: counts["review"] for source, counts in source_counts.items()},
        "canonical_counts_by_source": {source: counts["canonical"] for source, counts in source_counts.items()},
        "missing_approved_req_ids": missing_ids,
        "merge_history_present_by_source": {source: source in registered and registered[source] in merged_source_ids for source in expected_sources},
        "explicit_approved_exclusions": sorted(exclusions),
        "review_row_count": len(review_ids),
        "status": "pass" if not rejection_reasons else "fail",
        "rejection_reasons": rejection_reasons,
    }
    output = repo_root / "artifacts/traceability_reports/pre_freeze_canonical_coverage.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if rejection_reasons:
        raise RuntimeError("Pre-freeze canonical coverage failed: " + "; ".join(rejection_reasons))
    return manifest
