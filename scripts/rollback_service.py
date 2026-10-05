"""Tracked rollback and supersession operations."""

from __future__ import annotations

import json
from pathlib import Path

from audit_log import record_event
from canonical_store import connect, fingerprint, utc_now


def rollback_requirement_revision(repo_root: Path, *, project_id: str, canonical_requirement_id: str, target_revision_id: str, actor: str, reason: str) -> str:
    connection = connect(repo_root)
    try:
        current = connection.execute("SELECT current_revision_id FROM canonical_requirements WHERE canonical_requirement_id = ? AND project_id = ?", (canonical_requirement_id, project_id)).fetchone()
        target = connection.execute("SELECT 1 FROM canonical_requirement_revisions WHERE revision_id = ? AND canonical_requirement_id = ?", (target_revision_id, canonical_requirement_id)).fetchone()
        if current is None or target is None:
            raise LookupError("Requirement or target revision does not exist.")
        rollback_id = "rollback-" + fingerprint({"type": "requirement", "id": canonical_requirement_id, "target": target_revision_id, "reason": reason})[:24]
        connection.execute("UPDATE canonical_requirements SET current_revision_id = ?, updated_at = ? WHERE canonical_requirement_id = ?", (target_revision_id, utc_now(), canonical_requirement_id))
        connection.execute("INSERT OR REPLACE INTO rollback_records(rollback_id, project_id, target_type, target_id, from_state, to_state, reason, actor, created_at, metadata_json) VALUES (?, ?, 'requirement_revision', ?, ?, ?, ?, ?, ?, ?)", (rollback_id, project_id, canonical_requirement_id, current[0], target_revision_id, reason, actor, utc_now(), json.dumps({"new_snapshot_required": True, "target_revision_id": target_revision_id}, sort_keys=True)))
        connection.commit()
    finally:
        connection.close()
    record_event(repo_root, event_type="rollback_executed", entity_type="canonical_requirement", entity_id=canonical_requirement_id, actor=actor, message=reason, project_id=project_id, payload={"rollback_id": rollback_id, "target_revision_id": target_revision_id, "new_snapshot_required": True})
    return rollback_id


def supersede_snapshot(repo_root: Path, *, project_id: str, snapshot_id: str, actor: str, reason: str) -> str:
    connection = connect(repo_root)
    try:
        row = connection.execute("SELECT status FROM snapshots WHERE snapshot_id = ? AND project_id = ?", (snapshot_id, project_id)).fetchone()
        if row is None:
            raise LookupError("Snapshot does not exist.")
        rollback_id = "rollback-" + fingerprint({"type": "snapshot", "id": snapshot_id, "reason": reason})[:24]
        connection.execute("UPDATE snapshots SET status = 'superseded', impacted_at = ? WHERE snapshot_id = ?", (utc_now(), snapshot_id))
        connection.execute("INSERT OR REPLACE INTO rollback_records(rollback_id, project_id, target_type, target_id, from_state, to_state, reason, actor, created_at, metadata_json) VALUES (?, ?, 'snapshot', ?, ?, 'superseded', ?, ?, ?, ?)", (rollback_id, project_id, snapshot_id, row[0], reason, actor, utc_now(), json.dumps({"new_snapshot_required": True}, sort_keys=True)))
        connection.commit()
    finally:
        connection.close()
    record_event(repo_root, event_type="rollback_executed", entity_type="snapshot", entity_id=snapshot_id, actor=actor, message=reason, project_id=project_id, payload={"rollback_id": rollback_id, "new_snapshot_required": True})
    return rollback_id
