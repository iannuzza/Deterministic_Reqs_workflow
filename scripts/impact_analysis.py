"""Deterministic, scope-aware merge impact analysis."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping

from canonical_store import connect, fingerprint, record_audit, utc_now

SCOPE_TARGETS = frozenset({"block", "digital", "analog", "system", "general", "cross_layer", "unknown"})


@dataclass(frozen=True)
class ImpactResult:
    impact_analysis_id: str
    staging_batch_id: str
    affected_canonical_requirement_ids: tuple[str, ...]
    affected_mapping_ids: tuple[str, ...]
    affected_profile_revision_ids: tuple[str, ...]
    affected_snapshot_ids: tuple[str, ...]
    affected_downstream_targets: tuple[str, ...]
    identity_ambiguities: tuple[str, ...]
    scopes: tuple[str, ...]
    regeneration_scope: str
    risk: str
    approval_required: bool
    reason: str


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _scope(row: Mapping[str, object]) -> str:
    value = str(row.get("source_scope") or row.get("target_scope") or "unknown").strip().lower()
    if value in {"digital architecture", "digital"}:
        return "digital"
    if value in {"analog architecture", "analog"}:
        return "analog"
    if value in {"system architecture", "system", "general architecture", "general"}:
        return "system"
    if value in {"block", "block-only"}:
        return "block"
    return "cross_layer" if "," in value or "cross" in value else "unknown"


def analyze_merge(repo_root: Path, *, project_id: str, staging_batch_id: str, actor: str = "system") -> ImpactResult:
    connection = connect(repo_root)
    try:
        staged = connection.execute(
            """SELECT sr.*, ss.source_scope, ss.target_scope, ss.applies_to_architecture_layer
               FROM staged_requirements sr
               JOIN source_revisions rv ON rv.source_revision_id = sr.source_revision_id
               JOIN source_specs ss ON ss.source_spec_id = rv.source_spec_id
              WHERE sr.staging_batch_id = ? ORDER BY sr.staged_id""",
            (staging_batch_id,),
        ).fetchall()
        if not staged:
            raise ValueError(f"No staged requirements found for {staging_batch_id}.")
        affected_requirements: set[str] = set()
        affected_mappings: set[str] = set()
        affected_profiles: set[str] = set()
        affected_snapshots: set[str] = set()
        ambiguities: list[str] = []
        scopes = {_scope(dict(row)) for row in staged}
        for row in staged:
            source_req_id = (row["source_req_id"] or "").strip()
            candidates = connection.execute(
                "SELECT canonical_requirement_id, current_revision_id FROM canonical_requirements WHERE project_id = ? AND source_req_id = ?",
                (project_id, source_req_id),
            ).fetchall() if source_req_id else []
            if len(candidates) > 1:
                ambiguities.append(source_req_id or row["staged_id"])
            for candidate in candidates:
                canonical_id = candidate[0]
                affected_requirements.add(canonical_id)
                for mapping in connection.execute("SELECT mapping_id FROM architecture_mappings WHERE canonical_requirement_id = ?", (canonical_id,)).fetchall():
                    affected_mappings.add(mapping[0])
                    for snapshot in connection.execute("SELECT snapshot_id FROM snapshots WHERE instr(mapping_revision_set_json, ?) > 0", (mapping[0],)).fetchall():
                        affected_snapshots.add(snapshot[0])
        profile_kinds = {"taxonomy", "vocabulary", "architecture"}
        if scopes & {"digital", "analog", "system", "cross_layer"}:
            profile_rows = connection.execute(
                "SELECT profile_revision_id FROM profile_revisions WHERE project_id = ? AND profile_kind IN (?, ?, ?)",
                (project_id, *sorted(profile_kinds)),
            ).fetchall()
            affected_profiles.update(row[0] for row in profile_rows)
        downstream = {"SRS", "DRS", "ARS"}
        if "digital" in scopes:
            downstream.add("Digital IPOS")
        if "analog" in scopes:
            downstream.add("Analog IPOS")
        if "system" in scopes or "cross_layer" in scopes:
            downstream.update({"SRS", "DRS", "ARS", "Digital IPOS", "Analog IPOS"})
        category_changes = {row["staged_id"] for row in staged if row["proposed_classification"] != row["approved_classification"] and row["approved_classification"]}
        conflicts = {row["staged_id"] for row in staged if (row["review_decision"] or "").lower() == "conflict" or row["proposed_classification"] == "conflict"}
        full = bool(scopes & {"system", "cross_layer"}) or bool(ambiguities)
        regeneration_scope = "full" if full else "partial" if affected_requirements or downstream else "none"
        risk = "blocked" if ambiguities or conflicts else "risky" if category_changes or affected_snapshots else "safe"
        reason = "conflict or identity ambiguity requires review" if ambiguities or conflicts else "scope and dependency analysis complete"
        material = {
            "staging_batch_id": staging_batch_id,
            "requirements": sorted(affected_requirements),
            "mappings": sorted(affected_mappings),
            "profiles": sorted(affected_profiles),
            "snapshots": sorted(affected_snapshots),
            "scopes": sorted(scopes),
            "risk": risk,
            "regeneration_scope": regeneration_scope,
        }
        impact_id = "impact-" + fingerprint(material)[:24]
        connection.execute(
            """INSERT OR REPLACE INTO impact_analyses(
                impact_analysis_id, project_id, staging_batch_id, affected_requirement_ids_json,
                affected_mapping_ids_json, regeneration_scope, approval_state, created_at,
                analysis_fingerprint, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (impact_id, project_id, staging_batch_id, _json(sorted(affected_requirements)), _json(sorted(affected_mappings)), regeneration_scope, "approval_required" if risk != "safe" else "pending", utc_now(), fingerprint(material), _json({"profiles": sorted(affected_profiles), "snapshots": sorted(affected_snapshots), "downstream": sorted(downstream), "identity_ambiguities": sorted(ambiguities), "scopes": sorted(scopes), "risk": risk, "reason": reason})),
        )
        connection.execute("UPDATE merge_operations SET impact_analysis_id = ? WHERE staging_batch_id = ? AND project_id = ?", (impact_id, staging_batch_id, project_id))
        record_audit(connection, project_id=project_id, event_type="impact_analysis_created", entity_type="staging_batch", entity_id=staging_batch_id, actor=actor, payload=material | {"impact_analysis_id": impact_id, "risk": risk})
        connection.commit()
        artifact_dir = repo_root / "artifacts" / "canonical_workflow" / "impact_analysis"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / f"{impact_id}.json").write_text(json.dumps({**asdict(ImpactResult(impact_id, staging_batch_id, tuple(sorted(affected_requirements)), tuple(sorted(affected_mappings)), tuple(sorted(affected_profiles)), tuple(sorted(affected_snapshots)), tuple(sorted(downstream)), tuple(sorted(ambiguities)), tuple(sorted(scopes)), regeneration_scope, risk, risk != "safe", reason))}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return ImpactResult(impact_id, staging_batch_id, tuple(sorted(affected_requirements)), tuple(sorted(affected_mappings)), tuple(sorted(affected_profiles)), tuple(sorted(affected_snapshots)), tuple(sorted(downstream)), tuple(sorted(ambiguities)), tuple(sorted(scopes)), regeneration_scope, risk, risk != "safe", reason)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
