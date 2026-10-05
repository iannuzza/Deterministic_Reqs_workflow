"""Creation and completeness validation for immutable approved snapshots."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

from approved_profile_resolver import resolve_approved_profiles
from audit_log import record_event
from canonical_store import connect, create_snapshot_id, fingerprint, snapshot_material, utc_now
from requirement_allocation_policy import requires_hierarchy_parent


class SnapshotError(RuntimeError):
    pass


def validate_snapshot_row(row, *, require_approved: bool = True) -> None:
    if row is None:
        raise SnapshotError("Snapshot does not exist.")
    if require_approved and row["status"] != "approved":
        raise SnapshotError(f"Snapshot is not approved: {row['status']}")
    for field in ("canonical_revision_set_json", "mapping_revision_set_json", "content_fingerprint"):
        if not row[field]:
            raise SnapshotError(f"Snapshot is incomplete: {field}")
    if row["status"] == "impacted" and require_approved:
        raise SnapshotError("Impacted snapshots cannot support authoritative generation.")


def create_approved_snapshot(
    repo_root: Path,
    *,
    project_id: str,
    canonical_revision_ids: Sequence[str],
    mapping_ids: Sequence[str],
    approved_by: str,
    retrieval: Mapping[str, str | None],
    semantic_enabled: bool,
    semantic_fallback_enabled: bool = False,
    profile_kinds: Sequence[str] = ("vocabulary", "taxonomy", "architecture"),
) -> str:
    if len(canonical_revision_ids) != len(mapping_ids):
        raise SnapshotError(
            "Snapshot completeness failure: every canonical requirement must have exactly one approved mapping. "
            f"revisions={len(canonical_revision_ids)}, mappings={len(mapping_ids)}"
        )
    profiles = resolve_approved_profiles(repo_root, project_id=project_id, profile_kinds=profile_kinds)
    profile_hashes = {kind: str(row["content_fingerprint"]) for kind, row in profiles.items()}
    material = snapshot_material(canonical_revision_ids, mapping_ids, profile_hashes, retrieval, semantic_enabled)
    material["semantic_fallback_enabled"] = bool(semantic_fallback_enabled)
    snapshot_id = create_snapshot_id(material)
    connection = connect(repo_root)
    try:
        missing_revisions = [item for item in canonical_revision_ids if connection.execute("SELECT 1 FROM canonical_requirement_revisions WHERE revision_id = ?", (item,)).fetchone() is None]
        missing_mappings = [item for item in mapping_ids if connection.execute("SELECT 1 FROM architecture_mappings WHERE mapping_id = ? AND lifecycle_state = 'approved'", (item,)).fetchone() is None]
        incomplete_allocations = []
        for item in mapping_ids:
            row = connection.execute(
                """SELECT allocation_class, owning_target, lineage_mode,
                          source_origin_req_ids, hierarchy_parent_req_ids
                     FROM architecture_mappings
                    WHERE mapping_id = ? AND lifecycle_state = 'approved'""",
                (item,),
            ).fetchone()
            if row is None or any(not str(row[field] or "").strip() for field in (
                "allocation_class", "owning_target", "lineage_mode", "source_origin_req_ids"
            )) or (
                requires_hierarchy_parent(str(row["allocation_class"] or "").strip(), str(row["lineage_mode"] or "").strip())
                and not str(row["hierarchy_parent_req_ids"] or "").strip()
            ):
                incomplete_allocations.append(item)
        if missing_revisions or missing_mappings or incomplete_allocations:
            raise SnapshotError(
                "Snapshot completeness failure: "
                f"revisions={missing_revisions}, mappings={missing_mappings}, "
                f"incomplete_allocations={incomplete_allocations}"
            )
        connection.execute(
            """INSERT OR IGNORE INTO snapshots(
                snapshot_id, project_id, snapshot_kind, status, canonical_revision_set_json,
                mapping_revision_set_json, vocabulary_profile_version, vocabulary_profile_hash,
                taxonomy_profile_version, taxonomy_profile_hash, retrieval_config_version,
                retrieval_config_hash, semantic_enabled, content_fingerprint, approved_by,
                approved_at, created_at, metadata_json)
                VALUES (?, ?, 'mapping', 'approved', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (snapshot_id, project_id, json.dumps(sorted(canonical_revision_ids)), json.dumps(sorted(mapping_ids)), profiles.get("vocabulary", {}).get("revision_number"), profile_hashes.get("vocabulary"), profiles.get("taxonomy", {}).get("revision_number"), profile_hashes.get("taxonomy"), retrieval.get("version"), retrieval.get("hash"), int(semantic_enabled), fingerprint(material), approved_by, utc_now(), utc_now(), json.dumps({"semantic_fallback_enabled": bool(semantic_fallback_enabled), "profiles": profile_hashes, "retrieval": dict(retrieval)}, sort_keys=True)),
        )
        connection.commit()
    finally:
        connection.close()
    record_event(repo_root, event_type="snapshot_created", entity_type="snapshot", entity_id=snapshot_id, actor=approved_by, message="Approved immutable snapshot created", project_id=project_id, payload=material)
    return snapshot_id


def resolve_approved_snapshot(repo_root: Path, *, snapshot_id: str | None = None, use_latest_approved: bool = False):
    from canonical_store import resolve_snapshot
    connection = connect(repo_root)
    try:
        try:
            row = resolve_snapshot(connection, snapshot_id=snapshot_id, use_latest_approved=use_latest_approved)
        except (LookupError, PermissionError, ValueError) as exc:
            raise SnapshotError(str(exc)) from exc
        validate_snapshot_row(row)
        return dict(row)
    finally:
        connection.close()
