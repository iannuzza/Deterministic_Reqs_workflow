"""Authoritative, revisioned SQLite workflow model for Step 2.

CSV, JSON, and Markdown files are compatibility or review artifacts. This module
owns the canonical workflow state and keeps retrieval indexes out of band.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Mapping, Sequence

DEFAULT_CANONICAL_DB = Path("data/canonical/canonical_store.sqlite")
SCHEMA_VERSION = 5

LIFECYCLE_STATES = frozenset({"staged", "under_review", "approved", "impacted", "superseded", "rejected", "rolled_back"})
APPROVAL_STATES = frozenset({"pending", "approved", "rejected", "approval_required", "revoked"})
CLASSIFICATION_STATES = frozenset({"unknown", "functional", "non_functional", "constraint", "interface", "digital", "analog", "mixed", "digital_or_system", "analog_or_system"})
WORKFLOW_STATES = frozenset({
    "S0_PRIMARY_SOURCE_BASELINE", "S1_SOURCE_INGESTION", "S2_DETERMINISTIC_CLASSIFICATION",
    "S2A_STAGING_REVIEW", "S2B_MERGE_IMPACT_ANALYSIS", "S2C_MERGE_APPROVAL",
    "S2D_NON_DESTRUCTIVE_MERGE", "S2E_INDEX_REFRESH", "S2F_ARCHITECTURE_MAP_REVIEW",
    "S2G_ARCHITECTURE_MAPPING_APPROVAL", "S2H_APPROVED_MAPPING_SNAPSHOT",
    "STAGE3_SRS", "STAGE4_DRS", "STAGE5_ARS", "STAGE6_DIGITAL_IPOS", "STAGE7_ANALOG_IPOS",
})

_TRANSITIONS = {
    "staged": {"under_review", "rejected"},
    "under_review": {"approved", "rejected", "approval_required"},
    "approval_required": {"approved", "rejected"},
    "approved": {"impacted", "superseded", "revoked"},
    "impacted": {"approved", "superseded", "revoked"},
    "superseded": set(),
    "rejected": {"under_review"},
    "rolled_back": {"under_review"},
}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY, name TEXT NOT NULL, checksum TEXT NOT NULL,
    applied_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY, project_name TEXT NOT NULL, created_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS source_specs (
    source_spec_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    source_name TEXT NOT NULL, source_kind TEXT NOT NULL, source_scope TEXT NOT NULL DEFAULT '',
    target_scope TEXT NOT NULL DEFAULT '', applies_to_blocks_json TEXT NOT NULL DEFAULT '[]',
    applies_to_architecture_layer TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS source_revisions (
    source_revision_id TEXT PRIMARY KEY, source_spec_id TEXT NOT NULL REFERENCES source_specs(source_spec_id),
    revision_number TEXT NOT NULL, revision_date TEXT, content_fingerprint TEXT NOT NULL,
    ingestion_timestamp TEXT NOT NULL, lifecycle_state TEXT NOT NULL DEFAULT 'staged',
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS ingestion_batches (
    ingestion_batch_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    batch_kind TEXT NOT NULL, started_at TEXT NOT NULL, completed_at TEXT, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS staging_batches (
    staging_batch_id TEXT PRIMARY KEY, ingestion_batch_id TEXT NOT NULL REFERENCES ingestion_batches(ingestion_batch_id),
    workflow_state TEXT NOT NULL, created_at TEXT NOT NULL, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS source_integration_records (
    integration_record_id TEXT PRIMARY KEY, source_spec_id TEXT NOT NULL REFERENCES source_specs(source_spec_id),
    source_revision_id TEXT NOT NULL REFERENCES source_revisions(source_revision_id),
    ingestion_batch_id TEXT NOT NULL REFERENCES ingestion_batches(ingestion_batch_id),
    staging_batch_id TEXT REFERENCES staging_batches(staging_batch_id),
    review_decision_record_ref TEXT, merge_operation_record_ref TEXT, impact_analysis_record_ref TEXT,
    integration_scope TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS staged_requirements (
    staged_id TEXT PRIMARY KEY, staging_batch_id TEXT NOT NULL REFERENCES staging_batches(staging_batch_id),
    source_revision_id TEXT NOT NULL REFERENCES source_revisions(source_revision_id),
    source_req_id TEXT, requirement_text TEXT NOT NULL, source_page TEXT, source_section TEXT,
    source_chunk_id TEXT, proposed_classification TEXT NOT NULL DEFAULT 'unknown',
    approved_classification TEXT, classification_reason TEXT NOT NULL DEFAULT '',
    classification_method TEXT NOT NULL DEFAULT '', classification_confidence REAL,
    review_comment TEXT NOT NULL DEFAULT '', lifecycle_state TEXT NOT NULL DEFAULT 'staged',
    review_decision TEXT NOT NULL DEFAULT 'pending', content_fingerprint TEXT NOT NULL,
    auxiliary_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS canonical_requirements (
    canonical_requirement_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    source_req_id TEXT, current_revision_id TEXT, lifecycle_state TEXT NOT NULL DEFAULT 'approved',
    workflow_state TEXT NOT NULL DEFAULT 'S2D_NON_DESTRUCTIVE_MERGE',
    created_at TEXT NOT NULL, updated_at TEXT NOT NULL, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS canonical_requirement_revisions (
    revision_id TEXT PRIMARY KEY, canonical_requirement_id TEXT NOT NULL REFERENCES canonical_requirements(canonical_requirement_id),
    revision_number INTEGER NOT NULL, requirement_text TEXT NOT NULL, content_fingerprint TEXT NOT NULL,
    proposed_classification TEXT NOT NULL DEFAULT 'unknown', approved_classification TEXT,
    classification_reason TEXT NOT NULL DEFAULT '', classification_method TEXT NOT NULL DEFAULT '',
    classification_confidence REAL, review_comment TEXT NOT NULL DEFAULT '', lifecycle_state TEXT NOT NULL DEFAULT 'approved',
    created_at TEXT NOT NULL, supersedes_revision_id TEXT, UNIQUE(canonical_requirement_id, revision_number)
);
CREATE TABLE IF NOT EXISTS requirement_provenance (
    provenance_id INTEGER PRIMARY KEY AUTOINCREMENT, revision_id TEXT NOT NULL REFERENCES canonical_requirement_revisions(revision_id),
    source_spec_id TEXT NOT NULL REFERENCES source_specs(source_spec_id), source_revision_id TEXT NOT NULL REFERENCES source_revisions(source_revision_id),
    staged_id TEXT REFERENCES staged_requirements(staged_id), source_req_id TEXT, source_page TEXT, source_section TEXT,
    source_chunk_id TEXT, provenance_role TEXT NOT NULL DEFAULT 'source', metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(revision_id, source_revision_id, source_req_id, source_page, source_chunk_id)
);
CREATE TABLE IF NOT EXISTS profile_revisions (
    profile_revision_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    profile_kind TEXT NOT NULL, profile_name TEXT NOT NULL, revision_number TEXT NOT NULL,
    profile_payload_json TEXT NOT NULL, content_fingerprint TEXT NOT NULL, lifecycle_state TEXT NOT NULL DEFAULT 'staged',
    approval_state TEXT NOT NULL DEFAULT 'pending', approved_by TEXT, approved_at TEXT, created_at TEXT NOT NULL,
    UNIQUE(project_id, profile_kind, profile_name, revision_number)
);
CREATE TABLE IF NOT EXISTS architecture_mappings (
    mapping_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    canonical_requirement_id TEXT NOT NULL REFERENCES canonical_requirements(canonical_requirement_id),
    architecture_layer TEXT NOT NULL, candidate_block TEXT, approved_block TEXT,
    mapping_reason TEXT NOT NULL DEFAULT '', lifecycle_state TEXT NOT NULL DEFAULT 'staged',
    content_fingerprint TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS mapping_approvals (
    approval_id TEXT PRIMARY KEY, mapping_id TEXT NOT NULL REFERENCES architecture_mappings(mapping_id),
    approval_state TEXT NOT NULL DEFAULT 'pending', decision TEXT NOT NULL DEFAULT 'pending',
    reviewer TEXT, review_comment TEXT NOT NULL DEFAULT '', decided_at TEXT
);
CREATE TABLE IF NOT EXISTS merge_operations (
    merge_operation_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    staging_batch_id TEXT NOT NULL REFERENCES staging_batches(staging_batch_id), impact_analysis_id TEXT,
    decision TEXT NOT NULL DEFAULT 'pending', approved_by TEXT, started_at TEXT NOT NULL, completed_at TEXT,
    result_fingerprint TEXT, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS impact_analyses (
    impact_analysis_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    staging_batch_id TEXT NOT NULL REFERENCES staging_batches(staging_batch_id), affected_requirement_ids_json TEXT NOT NULL DEFAULT '[]',
    affected_mapping_ids_json TEXT NOT NULL DEFAULT '[]', regeneration_scope TEXT NOT NULL DEFAULT 'none',
    approval_state TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL, analysis_fingerprint TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    snapshot_kind TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'candidate', canonical_revision_set_json TEXT NOT NULL,
    mapping_revision_set_json TEXT NOT NULL DEFAULT '[]', vocabulary_profile_version TEXT, vocabulary_profile_hash TEXT,
    taxonomy_profile_version TEXT, taxonomy_profile_hash TEXT, retrieval_config_version TEXT, retrieval_config_hash TEXT,
    semantic_enabled INTEGER NOT NULL DEFAULT 0, content_fingerprint TEXT NOT NULL, approved_by TEXT, approved_at TEXT,
    impacted_at TEXT, created_at TEXT NOT NULL, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS rollback_records (
    rollback_id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(project_id),
    target_type TEXT NOT NULL, target_id TEXT NOT NULL, from_state TEXT NOT NULL, to_state TEXT NOT NULL,
    reason TEXT NOT NULL, actor TEXT NOT NULL, created_at TEXT NOT NULL, metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS audit_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT, event_type TEXT NOT NULL, entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL, actor TEXT NOT NULL, event_at TEXT NOT NULL, payload_json TEXT NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS report_metadata (
    report_id TEXT PRIMARY KEY, snapshot_id TEXT NOT NULL REFERENCES snapshots(snapshot_id),
    report_kind TEXT NOT NULL, output_format TEXT NOT NULL DEFAULT 'xlsx', output_path TEXT,
    source_fingerprint TEXT NOT NULL, generated_at TEXT, status TEXT NOT NULL DEFAULT 'planned', metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_source_revisions_spec ON source_revisions(source_spec_id);
CREATE INDEX IF NOT EXISTS idx_staged_requirements_source ON staged_requirements(source_revision_id);
CREATE INDEX IF NOT EXISTS idx_canonical_req_source_id ON canonical_requirements(source_req_id);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_events(entity_type, entity_id);
"""

_MIGRATION_2 = """
CREATE TABLE IF NOT EXISTS workflow_transitions (
    transition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT NOT NULL,
    transition_kind TEXT NOT NULL,
    actor TEXT NOT NULL,
    reason TEXT NOT NULL DEFAULT '',
    approval_required INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);
CREATE INDEX IF NOT EXISTS idx_workflow_transition_entity
    ON workflow_transitions(entity_type, entity_id, transition_id);
"""

_MIGRATION_3 = """
CREATE TABLE IF NOT EXISTS stage2_descriptive_evidence (
    evidence_id TEXT PRIMARY KEY,
    evidence_profile TEXT NOT NULL,
    statement TEXT NOT NULL,
    source TEXT NOT NULL,
    scope TEXT NOT NULL,
    domain TEXT NOT NULL,
    evidence_kind TEXT NOT NULL,
    content_fingerprint TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL DEFAULT 'approved',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stage2_descriptive_profile
    ON stage2_descriptive_evidence(evidence_profile, evidence_kind, lifecycle_state);
"""

_MIGRATION_4 = """
CREATE TABLE IF NOT EXISTS requirement_allocations (
    allocation_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(project_id),
    req_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_origin_req_ids TEXT NOT NULL DEFAULT '',
    spec_level TEXT NOT NULL,
    owning_target TEXT NOT NULL DEFAULT '',
    owning_block TEXT NOT NULL DEFAULT '',
    owning_domain TEXT NOT NULL DEFAULT '',
    requirement_class TEXT NOT NULL,
    topic_family TEXT NOT NULL DEFAULT '',
    abstraction_level TEXT NOT NULL DEFAULT '',
    immediate_parent_req_ids TEXT NOT NULL DEFAULT '',
    split_parent_req_id TEXT NOT NULL DEFAULT '',
    valid_downstream_targets TEXT NOT NULL DEFAULT '',
    required_downstream_targets TEXT NOT NULL DEFAULT '',
    actual_downstream_targets TEXT NOT NULL DEFAULT '',
    rendered_in_specs TEXT NOT NULL DEFAULT '',
    lineage_mode TEXT NOT NULL,
    coverage_status TEXT NOT NULL,
    direct_source_to_ipos INTEGER NOT NULL DEFAULT 0,
    policy_rationale TEXT NOT NULL DEFAULT '',
    snapshot_id TEXT NOT NULL DEFAULT '',
    approval_state TEXT NOT NULL DEFAULT 'approved',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    UNIQUE(project_id, snapshot_id, req_id, spec_level)
);
CREATE INDEX IF NOT EXISTS idx_requirement_allocations_lineage
    ON requirement_allocations(project_id, snapshot_id, source_origin_req_ids);
CREATE INDEX IF NOT EXISTS idx_requirement_allocations_status
    ON requirement_allocations(project_id, snapshot_id, coverage_status);
"""

_MIGRATION_5 = """
ALTER TABLE architecture_mappings ADD COLUMN allocation_class TEXT NOT NULL DEFAULT '';
ALTER TABLE architecture_mappings ADD COLUMN owning_target TEXT NOT NULL DEFAULT '';
ALTER TABLE architecture_mappings ADD COLUMN allocation_rationale TEXT NOT NULL DEFAULT '';
ALTER TABLE architecture_mappings ADD COLUMN lineage_mode TEXT NOT NULL DEFAULT '';
ALTER TABLE architecture_mappings ADD COLUMN source_origin_req_ids TEXT NOT NULL DEFAULT '';
ALTER TABLE architecture_mappings ADD COLUMN hierarchy_parent_req_ids TEXT NOT NULL DEFAULT '';
ALTER TABLE architecture_mappings ADD COLUMN owning_domain TEXT NOT NULL DEFAULT '';
"""

_MIGRATION_6 = """
ALTER TABLE architecture_mappings ADD COLUMN lineage_candidate_parent_req_ids TEXT NOT NULL DEFAULT '';
ALTER TABLE requirement_allocations ADD COLUMN lineage_candidate_parent_req_ids TEXT NOT NULL DEFAULT '';
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fingerprint(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_db_path(repo_root: Path) -> Path:
    return repo_root / DEFAULT_CANONICAL_DB


def connect(repo_root: Path, db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or canonical_db_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    migrate(connection)
    return connection


def migrate(connection: sqlite3.Connection) -> None:
    schema_checksum = hashlib.sha256(_SCHEMA.encode("utf-8")).hexdigest()
    connection.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, name TEXT NOT NULL, checksum TEXT NOT NULL, applied_at TEXT NOT NULL)")
    migration_1 = connection.execute("SELECT checksum FROM schema_migrations WHERE version = 1").fetchone()
    if not migration_1:
        with connection:
            connection.executescript(_SCHEMA)
            connection.execute("INSERT INTO schema_migrations(version, name, checksum, applied_at) VALUES (?, ?, ?, ?)", (1, "initial_workflow_model", schema_checksum, utc_now()))
    elif migration_1[0] != schema_checksum:
        raise RuntimeError("Canonical schema migration checksum changed after application.")
    migration_2_checksum = hashlib.sha256(_MIGRATION_2.encode("utf-8")).hexdigest()
    migration_2 = connection.execute("SELECT checksum FROM schema_migrations WHERE version = 2").fetchone()
    if not migration_2:
        with connection:
            connection.executescript(_MIGRATION_2)
            connection.execute("INSERT INTO schema_migrations(version, name, checksum, applied_at) VALUES (?, ?, ?, ?)", (2, "workflow_transition_history", migration_2_checksum, utc_now()))
    elif migration_2[0] != migration_2_checksum:
        raise RuntimeError("Workflow transition migration checksum changed after application.")
    migration_3_checksum = hashlib.sha256(_MIGRATION_3.encode("utf-8")).hexdigest()
    migration_3 = connection.execute("SELECT checksum FROM schema_migrations WHERE version = 3").fetchone()
    if not migration_3:
        with connection:
            connection.executescript(_MIGRATION_3)
            connection.execute("INSERT INTO schema_migrations(version, name, checksum, applied_at) VALUES (?, ?, ?, ?)", (3, "stage2_descriptive_evidence", migration_3_checksum, utc_now()))
    elif migration_3[0] != migration_3_checksum:
        raise RuntimeError("Stage 2 descriptive evidence migration checksum changed after application.")
    migration_4_checksum = hashlib.sha256(_MIGRATION_4.encode("utf-8")).hexdigest()
    migration_4 = connection.execute("SELECT checksum FROM schema_migrations WHERE version = 4").fetchone()
    if not migration_4:
        with connection:
            connection.executescript(_MIGRATION_4)
            connection.execute("INSERT INTO schema_migrations(version, name, checksum, applied_at) VALUES (?, ?, ?, ?)", (4, "requirement_allocation_lineage", migration_4_checksum, utc_now()))
    elif migration_4[0] != migration_4_checksum:
        raise RuntimeError("Requirement allocation migration checksum changed after application.")
    migration_5_checksum = hashlib.sha256(_MIGRATION_5.encode("utf-8")).hexdigest()
    migration_5 = connection.execute("SELECT checksum FROM schema_migrations WHERE version = 5").fetchone()
    if not migration_5:
        with connection:
            connection.executescript(_MIGRATION_5)
            connection.execute("INSERT INTO schema_migrations(version, name, checksum, applied_at) VALUES (?, ?, ?, ?)", (5, "approved_allocation_metadata", migration_5_checksum, utc_now()))
    elif migration_5[0] != migration_5_checksum:
        raise RuntimeError("Approved allocation metadata migration checksum changed after application.")
    migration_6_checksum = hashlib.sha256(_MIGRATION_6.encode("utf-8")).hexdigest()
    migration_6 = connection.execute("SELECT checksum FROM schema_migrations WHERE version = 6").fetchone()
    if not migration_6:
        with connection:
            connection.executescript(_MIGRATION_6)
            connection.execute("INSERT INTO schema_migrations(version, name, checksum, applied_at) VALUES (?, ?, ?, ?)", (6, "lineage_candidate_provenance", migration_6_checksum, utc_now()))
    elif migration_6[0] != migration_6_checksum:
        raise RuntimeError("Lineage candidate provenance migration checksum changed after application.")


def replace_stage2_descriptive_evidence(repo_root: Path, records: Sequence[Mapping[str, object]]) -> None:
    with transaction(repo_root) as connection:
        connection.execute("DELETE FROM stage2_descriptive_evidence WHERE evidence_profile = ?", ("low_power",))
        for record in records:
            statement = str(record.get("statement") or "").strip()
            source = str(record.get("source") or "").strip()
            if not statement or not source:
                continue
            material = {
                "profile": "low_power",
                "statement": statement,
                "source": source,
                "scope": str(record.get("scope") or "").strip(),
                "domain": str(record.get("domain") or "").strip(),
                "evidence_kind": str(record.get("evidence_kind") or "").strip(),
            }
            evidence_id = "stage2-low-power-" + fingerprint(material)[:24]
            connection.execute(
                "INSERT INTO stage2_descriptive_evidence VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (evidence_id, "low_power", statement, source, material["scope"], material["domain"], material["evidence_kind"], fingerprint(material), "approved", utc_now()),
            )


def read_stage2_descriptive_evidence(repo_root: Path, *, profile: str = "low_power") -> list[dict[str, str]]:
    with connect(repo_root) as connection:
        rows = connection.execute(
            "SELECT statement, source, scope, domain, evidence_kind FROM stage2_descriptive_evidence WHERE evidence_profile = ? AND lifecycle_state = 'approved' ORDER BY rowid",
            (profile,),
        ).fetchall()
    return [dict(row) for row in rows]


@contextmanager
def transaction(repo_root: Path, db_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    connection = connect(repo_root, db_path)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def validate_lifecycle_transition(current: str, target: str) -> None:
    if current not in LIFECYCLE_STATES or target not in LIFECYCLE_STATES:
        raise ValueError(f"Unknown lifecycle state: {current} -> {target}")
    if target not in _TRANSITIONS[current]:
        raise ValueError(f"Invalid lifecycle transition: {current} -> {target}")


def validate_approval_state(state: str) -> None:
    if state not in APPROVAL_STATES:
        raise ValueError(f"Unknown approval state: {state}")


def validate_classification(value: str) -> None:
    if value not in CLASSIFICATION_STATES:
        raise ValueError(f"Unknown classification: {value}")


def validate_workflow_state(value: str) -> None:
    if value not in WORKFLOW_STATES:
        raise ValueError(f"Unknown workflow state: {value}")


def create_snapshot_id(material: Mapping[str, object]) -> str:
    return "snap-" + fingerprint(material)[:24]


def snapshot_material(
    canonical_revision_ids: Sequence[str], mapping_ids: Sequence[str], profiles: Mapping[str, str | None],
    retrieval: Mapping[str, str | None], semantic_enabled: bool,
) -> dict[str, object]:
    return {
        "canonical_revision_ids": sorted(canonical_revision_ids),
        "mapping_ids": sorted(mapping_ids),
        "profiles": dict(sorted(profiles.items())),
        "retrieval": dict(sorted(retrieval.items())),
        "semantic_enabled": bool(semantic_enabled),
    }


def resolve_snapshot(connection: sqlite3.Connection, *, snapshot_id: str | None = None, use_latest_approved: bool = False) -> sqlite3.Row:
    if bool(snapshot_id) == bool(use_latest_approved):
        raise ValueError("Provide exactly one of snapshot_id or use_latest_approved.")
    if snapshot_id:
        row = connection.execute("SELECT * FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)).fetchone()
    else:
        row = connection.execute("SELECT * FROM snapshots WHERE status = 'approved' ORDER BY approved_at DESC, snapshot_id DESC LIMIT 1").fetchone()
    if row is None:
        raise LookupError("No matching approved snapshot exists.")
    if row["status"] != "approved":
        raise PermissionError("Only approved snapshots may be used for authoritative generation.")
    return row


def record_audit(connection: sqlite3.Connection, *, project_id: str | None, event_type: str, entity_type: str, entity_id: str, actor: str, payload: Mapping[str, object] | None = None) -> None:
    connection.execute(
        "INSERT INTO audit_events(project_id, event_type, entity_type, entity_id, actor, event_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (project_id, event_type, entity_type, entity_id, actor, utc_now(), json.dumps(payload or {}, ensure_ascii=True, sort_keys=True)),
    )
