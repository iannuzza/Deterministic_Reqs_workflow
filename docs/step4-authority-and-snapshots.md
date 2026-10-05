# Step 4 Authority And Snapshots

Step 4 makes auditability and approved snapshot authority enforceable at runtime.

## Audit

`audit_log.py` writes event records to canonical SQLite `audit_events` and optionally
exports append-only JSONL at `artifacts/audit/events.jsonl`. Event types cover source
processing, review, merge, mappings, profiles, retrieval, semantic fallback, snapshots,
rollback, SysML, reports, and conflict review.

## Snapshots

`snapshot_manager.py` creates deterministic approved snapshot IDs from canonical
revision IDs, approved mapping IDs, approved profile hashes, retrieval metadata, and
semantic flags. It rejects incomplete or impacted snapshots. The snapshot stores
profile versions/hashes and retrieval configuration metadata in canonical SQLite.

`approved_snapshot_resolver.py` is the authoritative consumer boundary. It requires
an explicit snapshot ID or an explicit latest-approved selector, validates project
identity, and requires approved vocabulary, taxonomy, and architecture profiles.

## Rollback

`rollback_service.py` restores a prior requirement revision or supersedes a snapshot
without deleting any record. Each operation writes `rollback_records` and an audit
event and marks that a new approved snapshot is required.

## Downstream outputs

SRS, DRS, ARS, Digital IPOS, Analog IPOS, and SysML CLI entry points require an
explicit snapshot selector. CSV, JSON, Markdown, XLSX, and SysML outputs are derived
artifacts and include snapshot provenance where applicable.

The legacy file resolver remains available to existing Python compatibility callers,
but it is not used by authoritative CLI generation paths.

## Conflicts and reports

`conflict_review_service.py` produces derived JSON summaries for same-ID/different-text
conflicts. It preserves competing source revisions, dates, texts, and provenance and
selects the latest revision/date only as a proposed winner. Approval remains required.

`report_generation_service.py` provides a snapshot-only report metadata boundary. Report
records reference the approved snapshot in canonical `report_metadata`; output files are
never authoritative.

## Cleanup scanner

`scripts/authority_consistency_scan.py` reports likely authority bypasses, direct
mutable-artifact reads, hardcoded project identifiers, and embedded lexical resources
in reusable-looking modules. It is intentionally diagnostic: source-derived adapters
and explicit legacy-only compatibility code may remain, but each finding should be
reviewed and either moved behind configuration/resolver context or documented as an
adapter boundary.

The scanner output is a derived validation artifact and does not change workflow state.
