#!/usr/bin/env python3
"""Apply only deterministic, authorized pre-freeze warning remediation."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from canonical_store import connect, record_audit
from requirement_allocation_policy import is_approved_top_level_without_parent, requires_hierarchy_parent


CSV_CROSSCHECK_CATEGORIES = (
    "TOP_LEVEL_PARENT_WARNING_SUPPRESSED",
    "SOURCE_DERIVED_PROVENANCE_EXEMPT",
    "SELF_ORIGIN_ONLY_NOT_PARENT_EVIDENCE",
    "SINGLE_SOURCE_ORIGIN_CANDIDATE",
    "SINGLE_COVERS_CANDIDATE",
    "MULTI_COVERS_AMBIGUOUS",
    "LOWER_LEVEL_BUT_NO_PARENT_EVIDENCE",
    "POSSIBLE_LINEAGE_OR_ALLOCATION_INCONSISTENCY",
    "TOP_LEVEL_OR_NON_PARENT_CASE_MISFLAGGED",
    "HUMAN_REVIEW_REQUIRED",
)


def historical_warning_cleanup(repo_root: Path, phase1_report_path: Path) -> dict[str, object]:
    """Classify non-current ingestion warnings without deleting or rewriting history."""
    if not phase1_report_path.exists():
        return {"complete": False, "groups": [], "cleared_count": 0}
    report = json.loads(phase1_report_path.read_text(encoding="utf-8"))
    active_path = str(report.get("active_batch", {}).get("batch_path") or "")
    groups: dict[tuple[str, str], dict[str, object]] = {}
    for finding in report.get("findings", []):
        if finding.get("category") != "stale_state":
            continue
        path = Path(str(finding.get("path") or ""))
        metadata_path = path / "source_metadata.json"
        metadata = _read_json(metadata_path) if metadata_path.exists() else {}
        key = (
            str(metadata.get("source_spec") or "unknown"),
            str(metadata.get("source_kind") or "unknown"),
        )
        group = groups.setdefault(key, {
            "source_spec": key[0],
            "source_kind": key[1],
            "count": 0,
            "paths": [],
            "severity": "LOW",
            "root_cause": "historical/superseded ingestion batch coexists with the active batch",
            "current_authority_effect": "none; active batch is selected separately",
            "future_validation_effect": "can add stale-state noise or affect selection if timestamps become ambiguous",
            "action": "mark_historical_non_authoritative",
            "active_authority_uniquely_established": bool(active_path),
            "workflow_triage": "INFO_ONLY; preserved for audit and excluded from current authority",
            "status": "historical_non_authoritative",
        })
        group["count"] = int(group["count"]) + 1
        group["paths"].append(str(path))
        if str(path) == active_path:
            group["severity"] = "HIGH"
            group["current_authority_effect"] = "active-batch selection risk"
    resolved = sum(int(group["count"]) for group in groups.values() if group["severity"] == "LOW")
    return {
        "complete": True,
        "active_batch_path": active_path,
        "groups": sorted(groups.values(), key=lambda item: (str(item["source_spec"]), str(item["source_kind"]))),
        "cleared_count": resolved,
        "preserved_for_audit": True,
        "authority_content_changed": False,
    }


def _read_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _ids(value: str) -> list[str]:
    return sorted({item.strip() for item in re.split(r"[,;\s]+", value or "") if item.strip()})


def _covers_ids(statement: str) -> list[str]:
    return sorted({item.strip() for group in re.findall(
        r"\[\s*Covers\s*:\s*([^\]]+)\]", statement or "", flags=re.IGNORECASE
    ) for item in _ids(group)})


def crosscheck_mapping_authority(repo_root: Path) -> dict[str, object]:
    """Classify unresolved hierarchy rows using synchronized CSV authority only."""
    path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    if not path.exists():
        return {"counts": {}, "rows": {}, "unresolved_count": 0}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    approved_ids = {
        (row.get("requirement_id") or "").strip()
        for row in rows
        if (row.get("review_decision") or "").strip().casefold() in {"approved", "reassigned"}
    }
    results: dict[str, str] = {}
    details: dict[str, dict[str, object]] = {}
    for row in rows:
        requirement_id = (row.get("requirement_id") or "").strip()
        allocation_class = (row.get("allocation_class") or "").strip()
        lineage_mode = (row.get("lineage_mode") or "").strip()
        if not requirement_id:
            continue
        if (row.get("hierarchy_parent_req_ids") or "").strip():
            continue
        if is_approved_top_level_without_parent(row):
            results[requirement_id] = "TOP_LEVEL_PARENT_WARNING_SUPPRESSED"
            details[requirement_id] = {
                "category": "TOP_LEVEL_PARENT_WARNING_SUPPRESSED",
                "allocation_class": allocation_class,
                "owning_target": (row.get("owning_target") or "").strip(),
                "lineage_mode": lineage_mode,
            }
            continue
        origin_ids = _ids(row.get("source_origin_req_ids") or "")
        covers_ids = _covers_ids(row.get("requirement_statement") or "")
        if not requires_hierarchy_parent(allocation_class, lineage_mode):
            if origin_ids or not covers_ids:
                results[requirement_id] = "SOURCE_DERIVED_PROVENANCE_EXEMPT"
                details[requirement_id] = {
                    "category": "SOURCE_DERIVED_PROVENANCE_EXEMPT",
                    "source_origin_req_ids": origin_ids,
                    "covers_req_ids": covers_ids,
                    "allocation_class": allocation_class,
                    "lineage_mode": lineage_mode,
                }
            continue
        valid_covers = [item for item in covers_ids if item in approved_ids and item != requirement_id]
        own_ids = {requirement_id, (row.get("source_req_id") or "").strip()} - {""}
        if not set(origin_ids) - own_ids and not covers_ids:
            category = "SELF_ORIGIN_ONLY_NOT_PARENT_EVIDENCE"
        elif len(valid_covers) == 1 and len(covers_ids) == 1:
            category = "SINGLE_COVERS_CANDIDATE"
        elif len(covers_ids) > 1:
            category = "MULTI_COVERS_AMBIGUOUS"
        elif len(origin_ids) == 1 and origin_ids[0] not in own_ids and origin_ids[0] in approved_ids:
            category = "SINGLE_SOURCE_ORIGIN_CANDIDATE"
        elif covers_ids and not valid_covers:
            category = "HUMAN_REVIEW_REQUIRED"
        elif origin_ids and not (set(origin_ids) - own_ids):
            category = "LOWER_LEVEL_BUT_NO_PARENT_EVIDENCE"
        elif not origin_ids and not covers_ids:
            category = "POSSIBLE_LINEAGE_OR_ALLOCATION_INCONSISTENCY"
        else:
            category = "HUMAN_REVIEW_REQUIRED"
        results[requirement_id] = category
        details[requirement_id] = {
            "category": category,
            "source_origin_req_ids": origin_ids,
            "covers_req_ids": covers_ids,
            "approved_covers_req_ids": valid_covers,
            "allocation_class": allocation_class,
            "lineage_mode": lineage_mode,
            "approved_block": (row.get("approved_block") or "").strip(),
        }
    counts = {category: sum(value == category for value in results.values()) for category in CSV_CROSSCHECK_CATEGORIES}
    return {"counts": counts, "rows": details, "unresolved_count": len(results)}


def _approved_parent_candidates(connection, requirement_id: str) -> set[str]:
    """Read only explicit approved parent relations from canonical lineage authority."""
    candidates: set[str] = set()
    for query, parameter in (
        (
            "SELECT hierarchy_parent_req_ids, lineage_candidate_parent_req_ids FROM architecture_mappings "
            "WHERE canonical_requirement_id = ? AND lifecycle_state = 'approved'",
            requirement_id,
        ),
        (
            "SELECT immediate_parent_req_ids FROM requirement_allocations "
            "WHERE req_id = ? AND approval_state = 'true'",
            requirement_id,
        ),
    ):
        try:
            rows = connection.execute(query, (parameter,)).fetchall()
        except Exception:
            rows = []
        for row in rows:
            for value in row:
                candidates.update(item.strip() for item in str(value or "").split(";") if item.strip())
    candidates.discard(requirement_id)
    return candidates


def derive_authoritative_parent_candidates(repo_root: Path) -> dict[str, list[str]]:
    """Find unique parent candidates without inferring from block, source, or text."""
    mapping_path = repo_root / "artifacts/stage1_specs/architecture_mapping_preview.csv"
    if not mapping_path.exists():
        return {}
    with mapping_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    connection = connect(repo_root)
    try:
        candidates: dict[str, list[str]] = {}
        for row in rows:
            requirement_id = (row.get("requirement_id") or "").strip()
            if not requirement_id or (row.get("review_decision") or "").strip().casefold() not in {"approved", "reassigned"}:
                continue
            allocation_class = (row.get("allocation_class") or "").strip()
            lineage_mode = (row.get("lineage_mode") or "").strip()
            if not requires_hierarchy_parent(allocation_class, lineage_mode) or (row.get("hierarchy_parent_req_ids") or "").strip():
                continue
            parents = sorted(_approved_parent_candidates(connection, requirement_id))
            if len(parents) == 1:
                candidates[requirement_id] = parents
        return candidates
    finally:
        connection.close()


def quarantine_stale_approved_snapshots(repo_root: Path) -> list[str]:
    """Mark approved snapshots with stale canonical revision sets as impacted."""
    connection = connect(repo_root)
    project_rows = connection.execute("SELECT project_id FROM projects ORDER BY project_id").fetchall()
    if len(project_rows) != 1:
        connection.close()
        raise RuntimeError("Automatic snapshot quarantine requires one unambiguous project.")
    project_id = str(project_rows[0][0])
    current = {
        str(row[0])
        for row in connection.execute(
            "SELECT current_revision_id FROM canonical_requirements WHERE project_id = ? AND current_revision_id IS NOT NULL",
            (project_id,),
        ).fetchall()
    }
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    quarantined: list[str] = []
    rows = connection.execute(
        "SELECT snapshot_id, canonical_revision_set_json, metadata_json FROM snapshots WHERE project_id = ? AND status = 'approved' ORDER BY snapshot_id",
        (project_id,),
    ).fetchall()
    try:
        for row in rows:
            try:
                revisions = set(json.loads(row[1] or "[]"))
            except json.JSONDecodeError:
                revisions = set()
            if revisions == current:
                continue
            metadata = json.loads(row[2] or "{}") if row[2] else {}
            metadata["pre_freeze_quarantine"] = {
                "reason": "canonical revision set is stale or invalid",
                "quarantined_at": now,
                "actor": "pre-freeze-warning-remediation",
            }
            connection.execute(
                "UPDATE snapshots SET status = 'impacted', impacted_at = ?, metadata_json = ? WHERE snapshot_id = ? AND status = 'approved'",
                (now, json.dumps(metadata, sort_keys=True), row[0]),
            )
            record_audit(
                connection,
                project_id=project_id,
                event_type="snapshot_quarantined",
                entity_type="snapshot",
                entity_id=str(row[0]),
                actor="pre-freeze-warning-remediation",
                payload={"reason": "canonical revision set is stale or invalid"},
            )
            quarantined.append(str(row[0]))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return quarantined


def main() -> int:
    parser = argparse.ArgumentParser(description="Quarantine only stale approved snapshots before pre-freeze validation")
    parser.add_argument("--report", default="artifacts/validation/pre_freeze_warning_remediation.json")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    quarantined = quarantine_stale_approved_snapshots(repo_root)
    phase1_report_path = repo_root / "artifacts/validation/source_to_stage2b_coherence.json"
    historical_cleanup = historical_warning_cleanup(repo_root, phase1_report_path)
    derivable = derive_authoritative_parent_candidates(repo_root)
    csv_crosscheck = crosscheck_mapping_authority(repo_root)
    report = {
        "remediation": "pre_freeze_warning_remediation",
        "mode": "deterministic_local_authorized_only",
        "quarantined_snapshots": quarantined,
        "placement_changes": [],
        "authoritative_parent_candidates": derivable,
        "candidate_source": "approved canonical lineage candidate fields only",
        "auto_resolved_count": 0,
        "remediation_exhausted": True,
        "csv_authority_crosscheck": csv_crosscheck,
        "historical_warning_cleanup": historical_cleanup,
        "approval_boundary_items": [
            "Rows without one unique approved canonical parent relation were not modified or inferred; candidate provenance remains separate from approved parent lineage."
        ],
    }
    report_path = repo_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
