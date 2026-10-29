# SysML GUI readability checkpoint - 2026-10-29

## Scope and status

This checkpoint saves the current local SysML readability fixes, focused tests,
memory and evidence. It is not approval of SysML implementation readiness.
The approved snapshot remains `snap-8b3673edc9cf590589b8ab39`.

- Both GUI source panes wrap long lines.
- The lower-right Model Views source pane has shared text zoom controls and
  Ctrl+mouse wheel support, independent of graph and port zoom.
- Existing governed descriptions receive display-only spacing at numbered
  subsections, sentences and enumeration items. The actual Main Controller
  check preserved all wording, all 12 subsection starts, exact non-descriptive
  code and file bytes; blank paragraph breaks increased from 5 to 170.
- Future generated descriptions preserve headings, short paragraphs and complete
  ordered documentation fragments. Central checks reject missing, duplicate,
  reordered, malformed or changed fragments.
- Earlier post-tag fixes are preserved: clickable Final SysML diagram nodes,
  exact approved inventory-owner binding and complete large-field CSV reading
  with restoration of the previous field limit.

The archive contains current Python scripts/tests, related documentation and
memory, the existing generated SysML files and their manifest, and bounded test
and failed-precheck evidence. Its manifest records every member's SHA-256.
Existing generated models are forensic evidence, not newly regenerated output.

## Verification and blocking boundary

See `validation_tests.log` and `validation_tests.json` for the focused checkpoint
test run and exact selectors. No generation or broad coherence run is repeated
to create this archive.

The previously authorized coherence precheck returned `BLOCK_DOWNSTREAM` with
33 hard findings: 32 Digital IPOS materialization-audit normalized-input
fingerprint/record mismatches across eight blocks, and one
`SYSML_READINESS_ASSESSMENT_STALE`. The full receipt is saved as
`coherence_precheck_20261029.json`.

Generation and structural review did not start after that failure. No whole-phase
PASS, publication approval or implementation readiness is claimed. Approved
documents, normative content, sources, ownership, reviews, approvals, canonical
data and snapshots are not modified by this checkpoint.

## Git and recovery

Follow [GIT_PUBLICATION.md](GIT_PUBLICATION.md). The user authorized a local
checkpoint commit, the same-named annotated tag and push to configured `origin`.
Local and remote Git refs are the exact publication receipt.

This follows the existing repository memory/archive convention. Only the new
checkpoint directory and the four current memory/index files are committed.
Live dirty source, runtime/database/artifact changes and unrelated checkpoints
remain unstaged. The current implementation is preserved inside
`runtime_sources_and_evidence.zip`; a checkout of the tag alone does not replace
the dirty live runtime.

The preceding official checkpoint is commit
`543f461c3e46c44754aff025568c025dbe113af1`, tag
`srs-drs-official-approved-2026-10-29`. Its committed archive supplies the earlier
full project/document baseline; the new archive records current implementation
and focused evidence, not a new complete canonical/source-document backup.

Inspect or extract archives only into a new isolated directory. Never restore
them over the dirty working tree or use them to rewrite canonical data, source
scope, review workbooks, approvals or snapshot authority.
