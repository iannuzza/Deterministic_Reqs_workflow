"""Derived conflict review summaries; never resolves conflicts automatically."""

from __future__ import annotations

import json
from pathlib import Path

from audit_log import record_event
from canonical_store import connect


def build_conflict_report(repo_root: Path, *, project_id: str, staging_batch_id: str, actor: str = "system") -> Path:
    connection = connect(repo_root)
    try:
        rows = connection.execute(
            """SELECT sr.source_req_id, sr.staged_id, sr.requirement_text, sr.review_decision,
                      rv.revision_number, rv.revision_date, rv.source_revision_id,
                      ss.source_spec_id, ss.source_name
                 FROM staged_requirements sr
                 JOIN source_revisions rv ON rv.source_revision_id = sr.source_revision_id
                 JOIN source_specs ss ON ss.source_spec_id = rv.source_spec_id
                WHERE sr.staging_batch_id = ? AND sr.proposed_classification = 'conflict'
                ORDER BY sr.source_req_id, rv.revision_date DESC, rv.revision_number DESC, sr.staged_id""",
            (staging_batch_id,),
        ).fetchall()
        groups = {}
        for row in rows:
            groups.setdefault(row["source_req_id"], []).append(dict(row))
        report = []
        for req_id, versions in sorted(groups.items()):
            proposed = versions[0] if versions else None
            report.append({"req_id": req_id, "competing_versions": versions, "default_proposed_winner": proposed["staged_id"] if proposed else None, "approval_status": "approval_required", "provenance_preserved": True})
        output = repo_root / "artifacts" / "canonical_workflow" / "conflicts" / f"{staging_batch_id}.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"project_id": project_id, "staging_batch_id": staging_batch_id, "conflicts": report}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    finally:
        connection.close()
    record_event(repo_root, event_type="conflict_review_generated", entity_type="staging_batch", entity_id=staging_batch_id, actor=actor, message="Conflict review report generated", project_id=project_id, payload={"report": str(output), "count": len(report)})
    return output
