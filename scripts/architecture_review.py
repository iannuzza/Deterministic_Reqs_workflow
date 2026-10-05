"""Architecture Map Review boundary over canonical mappings."""

from __future__ import annotations

import json
from pathlib import Path

from canonical_store import connect, fingerprint, record_audit, utc_now
from workflow_states import transition


def review_mapping(
    repo_root: Path,
    *,
    project_id: str,
    mapping_id: str,
    approved_block: str | None,
    reviewer: str,
    decision: str,
    review_comment: str = "",
    identity_or_classification_issue: bool = False,
) -> dict[str, object]:
    """Review only mapping allocation; identity issues create tracked loopback."""
    if decision not in {"approved", "rework", "rejected"}:
        raise ValueError(f"Unknown mapping review decision: {decision}")
    connection = connect(repo_root)
    try:
        mapping = connection.execute("SELECT * FROM architecture_mappings WHERE mapping_id = ? AND project_id = ?", (mapping_id, project_id)).fetchone()
        if mapping is None:
            raise LookupError(f"Unknown architecture mapping: {mapping_id}")
        if identity_or_classification_issue:
            connection.execute("UPDATE architecture_mappings SET lifecycle_state = 'impacted' WHERE mapping_id = ?", (mapping_id,))
            record_audit(connection, project_id=project_id, event_type="architecture_review_loopback", entity_type="mapping", entity_id=mapping_id, actor=reviewer, payload={"reason": review_comment, "target": "S2A_STAGING_REVIEW"})
            connection.commit()
            transition(repo_root, entity_type="mapping", entity_id=mapping_id, target="needs_rework", actor=reviewer, reason=review_comment or "identity/classification issue detected", project_id=project_id)
            return {"mapping_id": mapping_id, "decision": "loopback", "target": "S2A_STAGING_REVIEW"}
        approval_state = "approved" if decision == "approved" else "rejected" if decision == "rejected" else "approval_required"
        connection.execute("UPDATE architecture_mappings SET approved_block = ?, lifecycle_state = ? WHERE mapping_id = ?", (approved_block, "approved" if decision == "approved" else "under_review", mapping_id))
        approval_id = "approval-" + fingerprint({"mapping_id": mapping_id, "reviewer": reviewer, "decision": decision, "approved_block": approved_block})[:24]
        connection.execute("INSERT OR REPLACE INTO mapping_approvals(approval_id, mapping_id, approval_state, decision, reviewer, review_comment, decided_at) VALUES (?, ?, ?, ?, ?, ?, ?)", (approval_id, mapping_id, approval_state, decision, reviewer, review_comment, utc_now()))
        record_audit(connection, project_id=project_id, event_type="architecture_mapping_reviewed", entity_type="mapping", entity_id=mapping_id, actor=reviewer, payload={"decision": decision, "approved_block": approved_block, "review_comment": review_comment})
        connection.commit()
        target_state = "mapping_approved" if decision == "approved" else "mapping_under_review"
        current = connection.execute("SELECT to_state FROM workflow_transitions WHERE entity_type = 'mapping' AND entity_id = ? ORDER BY transition_id DESC LIMIT 1", (mapping_id,)).fetchone()
        if not current:
            transition(repo_root, entity_type="mapping", entity_id=mapping_id, target="mapping_under_review", actor=reviewer, reason="architecture map review started", project_id=project_id)
        if target_state != "mapping_under_review":
            transition(repo_root, entity_type="mapping", entity_id=mapping_id, target=target_state, actor=reviewer, reason="architecture map review decision", project_id=project_id, approval_required=True)
        return {"mapping_id": mapping_id, "approval_id": approval_id, "decision": decision, "approved_block": approved_block}
    finally:
        connection.close()
