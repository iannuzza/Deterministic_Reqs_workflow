"""Persistent deterministic workflow state transitions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Mapping

from canonical_store import (
    APPROVAL_STATES,
    connect,
    record_audit,
    utc_now,
)

WORKFLOW_ENTITY_STATES = frozenset({
    "ingested", "parsed", "classified", "under_review", "impact_analyzed",
    "approved_for_merge", "merged", "mapping_under_review", "mapping_approved",
    "snapshotted", "rejected", "needs_rework",
})

TRANSITIONS = {
    "ingested": {"parsed", "rejected", "needs_rework"},
    "parsed": {"classified", "rejected", "needs_rework"},
    "classified": {"under_review", "rejected", "needs_rework"},
    "under_review": {"impact_analyzed", "rejected", "needs_rework"},
    "impact_analyzed": {"approved_for_merge", "under_review", "rejected", "needs_rework"},
    "approved_for_merge": {"merged", "under_review", "rejected", "needs_rework"},
    "merged": {"mapping_under_review", "needs_rework"},
    "mapping_under_review": {"mapping_approved", "needs_rework", "rejected"},
    "mapping_approved": {"snapshotted", "mapping_under_review", "needs_rework"},
    "snapshotted": {"needs_rework"},
    "rejected": {"under_review", "needs_rework"},
    "needs_rework": {"under_review", "parsed", "classified"},
}


@dataclass(frozen=True)
class Transition:
    entity_type: str
    entity_id: str
    from_state: str | None
    to_state: str
    actor: str
    reason: str
    approval_required: bool


def validate_state(state: str) -> None:
    if state not in WORKFLOW_ENTITY_STATES:
        raise ValueError(f"Unknown workflow entity state: {state}")


def validate_transition(current: str | None, target: str) -> None:
    validate_state(target)
    if current is None:
        if target != "ingested":
            raise ValueError("A new workflow entity must start in ingested state.")
        return
    validate_state(current)
    if target not in TRANSITIONS[current]:
        raise ValueError(f"Invalid workflow transition: {current} -> {target}")


def transition(
    repo_root,
    *,
    entity_type: str,
    entity_id: str,
    target: str,
    actor: str,
    reason: str = "",
    project_id: str | None = None,
    approval_required: bool = False,
    metadata: Mapping[str, object] | None = None,
) -> Transition:
    connection = connect(repo_root)
    try:
        row = connection.execute(
            "SELECT to_state FROM workflow_transitions WHERE entity_type = ? AND entity_id = ? ORDER BY transition_id DESC LIMIT 1",
            (entity_type, entity_id),
        ).fetchone()
        current = row[0] if row else None
        validate_transition(current, target)
        payload = dict(metadata or {})
        connection.execute(
            """INSERT INTO workflow_transitions(
                project_id, entity_type, entity_id, from_state, to_state, transition_kind,
                actor, reason, approval_required, created_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, 'workflow', ?, ?, ?, ?, ?)""",
            (project_id, entity_type, entity_id, current, target, actor, reason, int(approval_required), utc_now(), json.dumps(payload, sort_keys=True)),
        )
        record_audit(
            connection,
            project_id=project_id,
            event_type="workflow_transition",
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            payload={"from_state": current, "to_state": target, "reason": reason, "approval_required": approval_required, **payload},
        )
        connection.commit()
        return Transition(entity_type, entity_id, current, target, actor, reason, approval_required)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def history(repo_root, *, entity_type: str, entity_id: str) -> tuple[dict, ...]:
    connection = connect(repo_root)
    try:
        rows = connection.execute(
            "SELECT * FROM workflow_transitions WHERE entity_type = ? AND entity_id = ? ORDER BY transition_id",
            (entity_type, entity_id),
        ).fetchall()
        return tuple(dict(row) for row in rows)
    finally:
        connection.close()
