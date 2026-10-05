"""Event-level audit logging for the canonical workflow."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from canonical_store import connect, record_audit, utc_now

EVENT_TYPES = frozenset({
    "source_imported", "parsed", "req_id_validated", "classified", "classification_changed",
    "review_requested", "review_approved", "review_rejected", "impact_analysis_generated",
    "merge_approved", "merged", "mapping_changed", "mapping_reviewed", "mapping_approved",
    "snapshot_created", "rollback_executed", "vocabulary_candidates_extracted",
    "vocabulary_candidate_approved", "vocabulary_candidate_rejected", "taxonomy_updated",
    "rag_index_built", "rag_crosscheck_executed", "semantic_fallback_triggered",
    "sysml_generated", "report_generated", "conflict_review_generated",
})


def record_event(
    repo_root: Path,
    *,
    event_type: str,
    entity_type: str,
    entity_id: str,
    actor: str = "system",
    message: str = "",
    project_id: str | None = None,
    source: str | None = None,
    payload: Mapping[str, object] | None = None,
    export_jsonl: bool = True,
) -> int:
    if event_type not in EVENT_TYPES:
        raise ValueError(f"Unknown audit event type: {event_type}")
    event_payload = {"message": message, "source": source, **dict(payload or {})}
    connection = connect(repo_root)
    try:
        record_audit(connection, project_id=project_id, event_type=event_type, entity_type=entity_type, entity_id=entity_id, actor=actor, payload=event_payload)
        event_id = connection.execute("SELECT last_insert_rowid()").fetchone()[0]
        connection.commit()
    finally:
        connection.close()
    if export_jsonl:
        path = repo_root / "artifacts" / "audit" / "events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        line = {"event_id": event_id, "timestamp": utc_now(), "event_type": event_type, "entity_type": entity_type, "entity_id": entity_id, "actor": actor, "source": source, "message": message, **dict(payload or {})}
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(line, ensure_ascii=True, sort_keys=True) + "\n")
    return int(event_id)
