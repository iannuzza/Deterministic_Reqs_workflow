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

### GUI Downstream Runs

The **workflow_cli Runs** single-stage and range actions request a snapshot before
launching any Stage 3-7 work. The picker lists stored snapshot history, not only
the ten newest records. Current-workflow and latest-approved choices resolve to
one explicit immutable ID before launch; cancellation launches nothing. Historical
or impacted entries remain visible, but only the shared resolver can authorize
their use. Selecting Stage 3 does not automatically refresh mutable Stage 0-2
source or review artifacts or replace the selected snapshot with the latest one.

The CLI retains that same `--snapshot-id` through the selected downstream range.
Its central generation precondition still requires the derived allocation ledger
to match the chosen snapshot. GUI runs entirely within Stage 3-7 pass
`--prepare-snapshot-inputs`: the CLI rebuilds that ledger through the shared
snapshot-only materializer, then runs the unchanged generation precondition.
It never reruns source ingestion or changes approvals. The same explicit snapshot
is retained in hierarchy coverage reports, rather than reselecting latest.
Prepared IPOS runs also request the existing downstream regeneration mode.
These runs replace derived outputs in the current workspace; canonical snapshot
history remains unchanged. Cancelling the picker makes no changes. CLI callers
can opt into the same preparation flag; without it, a stale ledger remains a
blocking workspace-binding failure. With `--dry-run`, preparation is only printed,
no ledger is written, and coherence of the planned replacement is not certified.

To launch a historical run yourself, choose Stage 3 as the range start and Stage 7
as the end in **workflow_cli Runs**, click **Run Stage Range**, select the desired
approved snapshot, and confirm **Use Snapshot**. The GUI streams the normal CLI
stage/gate results and stops at the first failure; no approval bypass is added.

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
