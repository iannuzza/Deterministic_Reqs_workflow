"""Canonical supplementary-source staging and non-destructive merge services."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from canonical_store import connect, fingerprint, record_audit, utc_now
from category_transition_rules import can_merge, validate_category
from impact_analysis import analyze_merge
from workflow_states import transition


_APPROVED = {"approved"}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: (value or "").strip() for key, value in row.items()} for row in csv.DictReader(handle)]


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "source"


def _project_id(repo_root: Path, metadata: Mapping[str, object]) -> str:
    context_path = repo_root / "config" / "project_context.json"
    context = json.loads(context_path.read_text(encoding="utf-8")) if context_path.exists() else {}
    return str(metadata.get("project_id") or context.get("project_name") or repo_root.name)


def _ensure_project(connection, project_id: str) -> None:
    connection.execute(
        "INSERT OR IGNORE INTO projects(project_id, project_name, created_at) VALUES (?, ?, ?)",
        (project_id, project_id, utc_now()),
    )


def register_staged_ingestion(repo_root: Path, ingestion_dir: Path) -> str:
    """Register a reviewed source corpus as canonical staging objects."""
    metadata_path = ingestion_dir / "source_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    normalized_path = ingestion_dir / "normalized_requirements.csv"
    review_path = ingestion_dir / "comparison_results.csv"
    staged_rows = _read_csv(normalized_path) if normalized_path.exists() else []
    review_rows = {row.get("staged_id", ""): row for row in _read_csv(review_path)} if review_path.exists() else {}
    source_name = str(metadata.get("source_spec") or ingestion_dir.name)
    source_revision = str(metadata.get("source_revision") or "")
    source_revision_date = str(metadata.get("source_revision_date") or "") or None
    source_kind = str(metadata.get("source_kind") or "supplementary")
    project_id = _project_id(repo_root, metadata)
    ingestion_id = str(metadata.get("ingestion_id") or ingestion_dir.name)
    source_spec_id = "spec-" + fingerprint({"project_id": project_id, "source_name": source_name})[:24]
    source_revision_id = "source-rev-" + fingerprint({"source_spec_id": source_spec_id, "revision": source_revision, "date": source_revision_date, "rows": staged_rows})[:24]
    ingestion_batch_id = "ingest-" + _slug(ingestion_id)
    staging_batch_id = "stage-" + _slug(ingestion_id)
    connection = connect(repo_root)
    try:
        existing_batch = connection.execute("SELECT staging_batch_id FROM staging_batches WHERE staging_batch_id = ?", (staging_batch_id,)).fetchone()
        if existing_batch:
            for staged_id, review in review_rows.items():
                category = str(review.get("req_class") or review.get("classification") or "new").lower()
                staged = connection.execute(
                    "SELECT source_req_id, requirement_text FROM staged_requirements WHERE staged_id = ? AND staging_batch_id = ?",
                    (staged_id, staging_batch_id),
                ).fetchone()
                if staged and staged[0]:
                    canonical = connection.execute(
                        """SELECT crr.requirement_text
                             FROM canonical_requirements cr
                             JOIN canonical_requirement_revisions crr ON crr.revision_id = cr.current_revision_id
                            WHERE cr.project_id = ? AND cr.source_req_id = ?""",
                        (project_id, staged[0]),
                    ).fetchone()
                    if canonical and canonical[0].strip() != (staged[1] or "").strip():
                        category = "conflict"
                validate_category(category)
                proposed = str(review.get("classification") or "unknown")
                connection.execute(
                    """UPDATE staged_requirements
                          SET proposed_classification = ?, review_decision = ?, review_comment = ?,
                              auxiliary_json = ?
                        WHERE staged_id = ? AND staging_batch_id = ?""",
                    (
                        proposed,
                        review.get("review_decision") or "pending",
                        review.get("reviewer_notes") or "",
                        json.dumps({"category": category, "source_spec": source_name, "source_revision": source_revision}, sort_keys=True),
                        staged_id,
                        staging_batch_id,
                    ),
                )
            connection.commit()
            return staging_batch_id
        _ensure_project(connection, project_id)
        connection.execute(
            """INSERT OR IGNORE INTO source_specs(
                source_spec_id, project_id, source_name, source_kind, source_scope,
                target_scope, created_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (source_spec_id, project_id, source_name, source_kind, str(metadata.get("source_scope") or ""), str(metadata.get("target_scope") or ""), utc_now(), json.dumps(metadata, sort_keys=True)),
        )
        connection.execute(
            """INSERT OR IGNORE INTO source_revisions(
                source_revision_id, source_spec_id, revision_number, revision_date,
                content_fingerprint, ingestion_timestamp, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (source_revision_id, source_spec_id, source_revision, source_revision_date, fingerprint(staged_rows), utc_now(), json.dumps(metadata, sort_keys=True)),
        )
        connection.execute(
            "INSERT OR IGNORE INTO ingestion_batches(ingestion_batch_id, project_id, batch_kind, started_at, completed_at, metadata_json) VALUES (?, ?, ?, ?, ?, ?)",
            (ingestion_batch_id, project_id, source_kind, utc_now(), utc_now(), json.dumps(metadata, sort_keys=True)),
        )
        connection.execute(
            "INSERT OR IGNORE INTO staging_batches(staging_batch_id, ingestion_batch_id, workflow_state, created_at, metadata_json) VALUES (?, ?, 'S2_DETERMINISTIC_CLASSIFICATION', ?, ?)",
            (staging_batch_id, ingestion_batch_id, utc_now(), json.dumps({"source_spec_id": source_spec_id, "source_revision_id": source_revision_id, "source_scope": metadata.get("source_scope", ""), "target_scope": metadata.get("target_scope", "")}, sort_keys=True)),
        )
        connection.execute(
            """INSERT OR REPLACE INTO source_integration_records(
                integration_record_id, source_spec_id, source_revision_id, ingestion_batch_id,
                staging_batch_id, integration_scope, created_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ("integration-" + fingerprint({"source_revision_id": source_revision_id, "staging_batch_id": staging_batch_id})[:24], source_spec_id, source_revision_id, ingestion_batch_id, staging_batch_id, str(metadata.get("source_scope") or metadata.get("target_scope") or "unknown"), utc_now(), json.dumps(metadata, sort_keys=True)),
        )
        for row in staged_rows:
            staged_id = row.get("staged_id") or (staging_batch_id + ":" + (row.get("source_req_id") or fingerprint(row)[:12]))
            review = review_rows.get(staged_id, {})
            category = str(review.get("req_class") or review.get("classification") or row.get("req_class") or "new").lower()
            existing_requirement = connection.execute(
                """SELECT crr.requirement_text FROM canonical_requirements cr
                   JOIN canonical_requirement_revisions crr ON crr.revision_id = cr.current_revision_id
                  WHERE cr.project_id = ? AND cr.source_req_id = ?""",
                (project_id, row.get("source_req_id")),
            ).fetchone() if row.get("source_req_id") else None
            requirement_text = row.get("requirement_statement") or row.get("requirement_text") or ""
            if existing_requirement and existing_requirement[0].strip() != requirement_text.strip():
                category = "conflict"
            validate_category(category)
            proposed = str(review.get("classification") or row.get("proposed_classification") or row.get("classification") or "unknown")
            connection.execute(
                """INSERT OR REPLACE INTO staged_requirements(
                    staged_id, staging_batch_id, source_revision_id, source_req_id, requirement_text,
                    source_page, source_chunk_id, proposed_classification, classification_reason,
                    classification_method, classification_confidence, review_comment, lifecycle_state,
                    review_decision, content_fingerprint, auxiliary_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'staged', ?, ?, ?)""",
                (staged_id, staging_batch_id, source_revision_id, row.get("source_req_id") or None, requirement_text, row.get("source_page") or row.get("source_page_no") or None, row.get("source_chunk_id") or None, proposed, review.get("match_reason") or "", "legacy_deterministic_review", float(row.get("classification_confidence") or 0) or None, review.get("reviewer_notes") or "", "approval_required" if category == "conflict" else review.get("review_decision") or "pending", fingerprint({"source_req_id": row.get("source_req_id"), "text": requirement_text}), json.dumps({"category": category, "source_spec": source_name, "source_revision": source_revision}, sort_keys=True)),
            )
            connection.commit()
            for target in ("ingested", "parsed", "classified", "under_review"):
                transition(repo_root, entity_type="staged_requirement", entity_id=staged_id, target=target, actor="legacy-ingestion", reason="registered from deterministic supplementary ingestion", project_id=project_id)
        connection.execute("UPDATE source_revisions SET lifecycle_state = 'staged' WHERE source_revision_id = ?", (source_revision_id,))
        record_audit(connection, project_id=project_id, event_type=f"{source_kind}_staged", entity_type="staging_batch", entity_id=staging_batch_id, actor="canonical-ingestion", payload={"source_spec_id": source_spec_id, "source_revision_id": source_revision_id, "ingestion_batch_id": ingestion_batch_id})
        connection.commit()
        return staging_batch_id
    finally:
        connection.close()


def merge_staging_batch(repo_root: Path, *, project_id: str, staging_batch_id: str, approved_by: str, conflict_winner_ids: Sequence[str] = ()) -> dict[str, object]:
    """Apply an approved batch as new canonical revisions without destructive updates."""
    impact = analyze_merge(repo_root, project_id=project_id, staging_batch_id=staging_batch_id, actor=approved_by)
    connection = connect(repo_root)
    try:
        if impact.risk == "blocked" and not conflict_winner_ids:
            raise PermissionError("Merge is blocked by conflict or identity ambiguity.")
        staged = connection.execute("SELECT * FROM staged_requirements WHERE staging_batch_id = ? ORDER BY staged_id", (staging_batch_id,)).fetchall()
        if not staged:
            raise ValueError(f"No staged rows for {staging_batch_id}.")
        completed = connection.execute(
            "SELECT merge_operation_id, impact_analysis_id FROM merge_operations WHERE project_id = ? AND staging_batch_id = ? AND decision = 'approved' AND completed_at IS NOT NULL ORDER BY completed_at DESC LIMIT 1",
            (project_id, staging_batch_id),
        ).fetchone()
        if completed:
            canonical_ids = [
                row[0] for row in connection.execute(
                    """SELECT DISTINCT cr.canonical_requirement_id
                         FROM canonical_requirements cr
                         JOIN requirement_provenance rp ON rp.revision_id = cr.current_revision_id
                         JOIN staged_requirements sr ON sr.staged_id = rp.staged_id
                        WHERE sr.staging_batch_id = ? ORDER BY cr.canonical_requirement_id""",
                    (staging_batch_id,),
                ).fetchall()
            ]
            return {"merge_operation_id": completed["merge_operation_id"], "impact_analysis_id": completed["impact_analysis_id"], "canonical_requirement_ids": tuple(canonical_ids), "regeneration_scope": impact.regeneration_scope}
        merge_id = "merge-" + fingerprint({"project_id": project_id, "staging_batch_id": staging_batch_id})[:24]
        connection.execute("INSERT OR REPLACE INTO merge_operations(merge_operation_id, project_id, staging_batch_id, impact_analysis_id, decision, approved_by, started_at) VALUES (?, ?, ?, ?, 'approved', ?, ?)", (merge_id, project_id, staging_batch_id, impact.impact_analysis_id, approved_by, utc_now()))
        merged_ids: list[str] = []
        for row in staged:
            review_decision = str(row["review_decision"] or "pending")
            category = json.loads(row["auxiliary_json"] or "{}").get("category") or row["proposed_classification"] or "new"
            existing = connection.execute("SELECT * FROM canonical_requirements WHERE project_id = ? AND source_req_id = ?", (project_id, row["source_req_id"])).fetchall() if row["source_req_id"] else []
            replaces_mapping = bool(existing and connection.execute("SELECT 1 FROM architecture_mappings WHERE canonical_requirement_id = ? AND lifecycle_state = 'approved' LIMIT 1", (existing[0]["canonical_requirement_id"],)).fetchone())
            decision = can_merge(category, review_decision=review_decision, replaces_approved_mapping=replaces_mapping)
            if category == "conflict" and row["staged_id"] not in set(conflict_winner_ids):
                raise PermissionError(f"Conflict requires explicit winner approval: {row['staged_id']}")
            if not decision.merge_allowed and row["staged_id"] not in set(conflict_winner_ids):
                raise PermissionError(f"Staged row is not approved for merge: {row['staged_id']} ({decision.reason})")
            if existing:
                canonical_id = existing[0]["canonical_requirement_id"]
                current = connection.execute("SELECT * FROM canonical_requirement_revisions WHERE revision_id = ?", (existing[0]["current_revision_id"],)).fetchone()
                if current and current["content_fingerprint"] == row["content_fingerprint"]:
                    revision_id = current["revision_id"]
                else:
                    next_number = connection.execute("SELECT COALESCE(MAX(revision_number), 0) + 1 FROM canonical_requirement_revisions WHERE canonical_requirement_id = ?", (canonical_id,)).fetchone()[0]
                    revision_id = f"{canonical_id}:r{next_number}"
                    connection.execute("INSERT INTO canonical_requirement_revisions(revision_id, canonical_requirement_id, revision_number, requirement_text, content_fingerprint, proposed_classification, approved_classification, classification_reason, classification_method, classification_confidence, review_comment, lifecycle_state, created_at, supersedes_revision_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'approved', ?, ?)", (revision_id, canonical_id, next_number, row["requirement_text"], row["content_fingerprint"], row["proposed_classification"], row["approved_classification"] or row["proposed_classification"], row["classification_reason"], row["classification_method"], row["classification_confidence"], row["review_comment"], utc_now(), existing[0]["current_revision_id"]))
                    connection.execute("UPDATE canonical_requirements SET current_revision_id = ?, updated_at = ?, workflow_state = 'S2D_NON_DESTRUCTIVE_MERGE' WHERE canonical_requirement_id = ?", (revision_id, utc_now(), canonical_id))
                    connection.execute("UPDATE architecture_mappings SET lifecycle_state = 'impacted' WHERE canonical_requirement_id = ? AND lifecycle_state = 'approved'", (canonical_id,))
                    connection.execute("UPDATE snapshots SET status = 'impacted', impacted_at = ? WHERE project_id = ? AND status = 'approved'", (utc_now(), project_id))
            else:
                canonical_id = "can-" + fingerprint({"project_id": project_id, "source_req_id": row["source_req_id"], "text": row["requirement_text"]})[:24]
                revision_id = canonical_id + ":r1"
                connection.execute("INSERT INTO canonical_requirements(canonical_requirement_id, project_id, source_req_id, current_revision_id, lifecycle_state, workflow_state, created_at, updated_at) VALUES (?, ?, ?, ?, 'approved', 'S2D_NON_DESTRUCTIVE_MERGE', ?, ?)", (canonical_id, project_id, row["source_req_id"], revision_id, utc_now(), utc_now()))
                connection.execute("INSERT INTO canonical_requirement_revisions(revision_id, canonical_requirement_id, revision_number, requirement_text, content_fingerprint, proposed_classification, approved_classification, classification_reason, classification_method, classification_confidence, review_comment, created_at) VALUES (?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (revision_id, canonical_id, row["requirement_text"], row["content_fingerprint"], row["proposed_classification"], row["approved_classification"] or row["proposed_classification"], row["classification_reason"], row["classification_method"], row["classification_confidence"], row["review_comment"], utc_now()))
            source_revision = connection.execute("SELECT source_spec_id, source_revision_id FROM staged_requirements JOIN source_revisions USING(source_revision_id) WHERE staged_id = ?", (row["staged_id"],)).fetchone()
            connection.execute("INSERT OR IGNORE INTO requirement_provenance(revision_id, source_spec_id, source_revision_id, staged_id, source_req_id, source_page, source_chunk_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (revision_id, source_revision[0], source_revision[1], row["staged_id"], row["source_req_id"], row["source_page"], row["source_chunk_id"]))
            merged_ids.append(canonical_id)
        connection.execute("UPDATE merge_operations SET completed_at = ?, result_fingerprint = ? WHERE merge_operation_id = ?", (utc_now(), fingerprint(merged_ids), merge_id))
        record_audit(connection, project_id=project_id, event_type="canonical_merge_completed", entity_type="merge_operation", entity_id=merge_id, actor=approved_by, payload={"staging_batch_id": staging_batch_id, "canonical_requirement_ids": merged_ids, "impact_analysis_id": impact.impact_analysis_id})
        connection.commit()
        for row in staged:
            transition(repo_root, entity_type="staged_requirement", entity_id=row["staged_id"], target="impact_analyzed", actor=approved_by, reason="impact analysis approved for merge", project_id=project_id)
            transition(repo_root, entity_type="staged_requirement", entity_id=row["staged_id"], target="approved_for_merge", actor=approved_by, reason="explicit merge approval", project_id=project_id, approval_required=True)
            transition(repo_root, entity_type="staged_requirement", entity_id=row["staged_id"], target="merged", actor=approved_by, reason="non-destructive canonical revision created", project_id=project_id)
        return {"merge_operation_id": merge_id, "impact_analysis_id": impact.impact_analysis_id, "canonical_requirement_ids": tuple(merged_ids), "regeneration_scope": impact.regeneration_scope}
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
