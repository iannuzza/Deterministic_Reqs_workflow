# Focused restart handoff

## Start here

1. Read this file, the checkpoint README and publication/GUI receipts.
2. Verify the current runtime hashes against the archived member manifest.
3. Keep the existing dirty worktree. Do not reset, check out an old tag or extract
   an archive over the official project.

## Completed and accepted

The archived reusable fixes were integrated into the centralized, deterministic,
local-only, project-agnostic SRS/DRS/digital/analog IPOS workflow. There is no new
synthesis engine or project-name branch. The current source archive is the
integrated implementation, unlike the unintegrated 2026-10-27 archive.

The user approved the final SRS and DRS as official on 2026-10-29. Publication
copied the verified documents and matching companions; it did not regenerate
official Word files or change approved canonical authority.

Official files:

- `artifacts/stage3_srs/system_requirements_specification.docx`
- `artifacts/stage5_drs/digital_requirements_specification.docx`

Snapshot: `snap-8b3673edc9cf590589b8ab39`.
Architecture fingerprint:
`0b9f2b67360f480031d7482de1776326f602608327b2b5c17d1c84c074a0656d`.
Its 357 allocations comprise 55 DRS and 302 digital IPOS entries; SRS and
analog-local normative partitions are valid-empty.

## SRS details

- Existing SRS-authorized context meanings can be placed in 3.1/3.5 by the
  explicitly approved `semantic_system_overview_v1` policy; do not duplicate 3.4.
- The two reviewed introductions are project data in
  `config/srs_system_overview_summary.json` and
  `config/srs_digital_subsystem_summary.json`, not project prose in reusable code.
  Their snapshot, architecture, source hashes and paragraph hashes are checked.
- 3.6 now has a short domain-type/control explanation before the original table.
  Raw domain identifiers remain in the table; prose does not infer retention,
  switch-off conditions, reset behavior, sequencing or timing.

## DRS details

- Preserve the current structure, required concrete-block purposes, tables and
  indexes. Integration themes complement rather than replace block purposes.
- The historical ISPU fragment was reproduced against original PDF/OCR pages
  12-13. Current cross-page extraction already fixes continuity and is retained.
  Frozen records and snapshots were not rewritten.
- The complete authorized source
  `source-context-a7ad7724ccfbcfa39ae99669::requested-4b47ea65a38db1ca`
  supplies the capability, not the unusable matrix-like inventory Function.
  With the user-approved `supported_local_function_v1` placement amendment,
  the purpose in 3.1 is:
  `ISPU can execute signal processing and AI algorithms in the edge.`
- There are no applicable same-owner ISPU DRS requirements in this snapshot.
  Do not invent requirements or change ownership to fill the inventory defect.
- The new short section 3 paragraph combines approved function-mapping
  responsibilities at digital-domain level. It does not assert an invented
  execution chain. Existing overview/inventory remain; 3.1 is unchanged.
- Only the requested grammar changes `embedded process capabilities` to
  `embedded processing capabilities`, with strict meaning checks retained.
- No applicable common-bus/shared-resource arbitration policy was found in the
  original PDF or approved evidence. Section 4.2 visibly retains:
  `common bus and shared resources arbitration policy to be clarified`.
  This is a technical gap note, not a normative policy or new generation blocker.

## IPOS details

- The accepted Main Controller review has twelve matching summary/detail
  functions and 181 preserved normative requirements. Actual approved Word
  parity is protected by `tests/test_approved_ipos_document_parity.py`.
- Shared Word formatting gives numbered 1.4 subsections explicit Heading4
  outline level 3 without promoting requirement IDs into navigation.
- The accepted navigation-review Word is archived as review-only evidence.
  SRS/DRS approval did not automatically publish that Main Controller review.
- Analog valid-empty success does not certify prose for a real analog scope.

## Verification and residuals

- Official SRS/DRS crosschecks and Stage 3/5 gates passed after publication.
- 101 relevant regression tests passed; six unrelated failures were independently
  reproduced on the pre-change runtime and remain explicitly separate.
- Actual Markdown/Word checks preserve all normative content, tables, ownership,
  conditions, source I/O and traceability; new prose is checked independently
  from the producer and mutation-tested.
- GUI startup/command checks and the exact S3-to-S6 range results are recorded in
  the checkpoint GUI receipts/log. Do not substitute individual stage success
  for the actual GUI route result.
- Actual result: startup, retrieval preflight, S3/S4/S5 and S6 generation passed.
  The S6 regression suite exposed an obsolete synthetic DRS power-table fixture,
  not a document-generation failure. The fixture now includes the contract's
  4.2 note and actual Word headings. All 166 tests and the remaining S6 gate/
  materialization checks passed after targeted resume. S6 has 302 requirements
  across 8 blocks; final generation-input coherence reports zero findings.
  The original full-range exit 3 is retained in history, not relabeled exit 0.
  Do not repeat successful ten-minute generation solely to rerun this fixture.
- Regenerated SRS/DRS heading, paragraph and table events match the official
  approved documents after normalizing only workspace metadata path prefixes.
- DRS broader writing assessment: UNRESOLVED, 216 findings. Main Controller
  historical broader assessment: UNRESOLVED, 522 findings. Neither is readiness.
  The combined official writing sidecar also includes existing projection rows
  (451 total rows); do not confuse that combined count with distinct defects.
- Existing DRS-REQ-015 Word underscore loss is historical; each artifact was
  preserved against its own normative baseline. Do not claim universal
  normative Markdown/Word byte identity.
- The full downstream/SysML diagnostic previously encountered large-CSV and
  old-snapshot/absolute-path manifest issues in a copied workspace. GUI generation
  uses `validate_generation_inputs`, not that broader final SysML check.
  Do not weaken either check or claim global SysML readiness from document gates.

## Next actions

Wait for the user's next workflow improvement. Do not reopen broad writing cleanup,
restructure DRS, publish deferred IPOS, change snapshots, approve sources, create
the proposed tag, push or regenerate official documents without a new request.
For a GUI rerun select the explicit approved snapshot and use the normal
snapshot-input preparation path, not mutable-source reconstruction.
