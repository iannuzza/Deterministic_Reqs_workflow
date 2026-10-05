# Step 3 Workflow Enforcement

Step 3 adds the execution boundary around the Step 2 canonical SQLite model.

## State history

`workflow_states.py` validates and persists transitions for ingestion, parsing,
classification, review, impact analysis, merge approval, merge completion, mapping
review, mapping approval, snapshotting, rejection, and rework. Every transition is
append-only in `workflow_transitions` and is mirrored in `audit_events`. Loopbacks
create new entries and preserve the earlier history.

## Impact analysis

`impact_analysis.py` analyzes a staging batch deterministically before merge. It
records affected canonical requirements, mappings, profiles, snapshots, downstream
outputs, identity ambiguities, source scopes, risk, and regeneration scope. The
result is stored in `impact_analyses` and exported as a JSON review artifact under
`artifacts/canonical_workflow/impact_analysis/`.

Supported scope labels include block, digital, analog, system/general architecture,
and cross-layer impact. System and cross-layer changes require full regeneration;
block and branch-specific changes can request partial regeneration when no identity
ambiguity or conflict blocks the merge.

## Merge policy

`merge_engine.py` registers legacy supplementary staging artifacts in canonical
SQLite and performs approval-gated, non-destructive merges. Canonical requirement
revisions are append-only and preserve `supersedes_revision_id` plus source
provenance. Existing mappings and approved snapshots are marked impacted when a
canonical requirement changes.

Same source requirement IDs with different text are stored as separate staged rows
with separate source revisions and are classified as `conflict`. They cannot merge
without an explicit winner approval. The latest source revision/date can be selected
as a proposal, but is not silently authoritative.

CSV, XLSX, JSON, and retrieval index rebuilds remain compatibility outputs after the
canonical merge succeeds. They do not authorize a merge.

## Architecture review boundary

`architecture_review.py` can approve or reject mapping allocation and record review
comments. It cannot edit canonical requirement text, provenance, approved
classification, or merge category. Identity or classification defects mark the
mapping impacted and create a tracked loopback to staging review.

## Vocabulary and retrieval

Step 3 does not introduce a vocabulary implementation. Classification and mapping
services consume approved profile references from the canonical model. Existing
lexical, normalized, hybrid, semantic, and hybrid-semantic retrieval implementations
remain unchanged; retrieval results are evidence only and cannot mutate canonical
workflow state.
