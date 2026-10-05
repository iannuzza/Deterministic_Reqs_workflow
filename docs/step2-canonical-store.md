# Step 2 Canonical Store

Step 2 introduces the authoritative workflow model at:

`data/canonical/canonical_store.sqlite`

The database is created lazily by `scripts/canonical_store.py`. The first migration
creates `schema_migrations` and records the checksum of the initial relational schema.
Retrieval/index SQLite databases remain separate and rebuildable.

## Workflow model

The model represents the strengthened sequence:

`S0 -> S1 -> S2 -> S2A -> S2B -> S2C -> S2D -> S2E -> S2F -> S2G -> S2H -> Stage 3..7`

Staged requirements are stored in `staged_requirements` and canonical requirements are
stored as stable identities plus append-only rows in
`canonical_requirement_revisions`. A staged row cannot replace a canonical row merely
by being ingested.

Lifecycle states and approval states are separate. Central validators in
`canonical_store.py` reject unknown states and invalid lifecycle transitions. An
impacted snapshot remains queryable for forensic use, but `resolve_snapshot` permits
only approved snapshots for authoritative generation.

## Supplementary sources

`source_specs` and `source_revisions` preserve multiple source specifications and
separate source revision number/date from ingestion timestamp. Batch tables make
repeated, multi-source ingestion traceable. `source_integration_records` connects a
source revision to its ingestion/staging batches and to review, merge, and impact
records.

Two staged rows may use the same `source_req_id` while retaining different source
revision IDs and content fingerprints. This represents a conflict without silently
choosing a winner. A later merge service may record the latest revision/date as a
proposed winner, but approval remains required.

## Profiles, mappings, and snapshots

`profile_revisions` stores taxonomy, vocabulary, and architecture profile candidates
and approvals as revisioned authoritative records. `architecture_mappings` and
`mapping_approvals` keep candidate mappings separate from approved mappings.

Snapshot IDs are derived from canonical revision IDs, mapping IDs, profile hashes,
retrieval configuration, and the semantic-enabled flag. Downstream code must select
one explicitly with `snapshot_id` or `use_latest_approved=True`; no implicit latest
selection is provided.

CSV, JSON, Markdown, and XLSX files remain derived exports or review artifacts. The
existing legacy CSV resolver remains available for migration and historical runs via
`allow_legacy=True`, while `load_sqlite_snapshot_input` is the SQLite boundary for
future snapshot-based generators.
