# Deterministic_Reqs_workflow - Project Activity, Lessons, Errors, and Fixes

## 2026-10-06 16:35:30 - Local Restart Checkpoint Saved
- Updated local chat handoff, checkpoint, environment and synchronization
  manifest in the active Git clone. Older original-project history is retained
  below and does not override the newest checkpoint.
- No Git commit/branch/reset, rollback backup, approval change or pipeline run
  performed for this save. Existing worktree changes remain saved in place.

## 2026-10-06 - Final Snapshot-Only Version History Policy
- User's FINAL rule: one new history row per new approved snapshot version.
  Same-snapshot reruns leave the complete history table unchanged. Earlier
  requests to append on every run were superseded before production regeneration.
- Shared `document_version_history_markdown` in `scripts/workflow_routing.py`
  retains old rows and appends only when the document's snapshot changes.
  `document_version_for_snapshot` reads the last row; minor version increments
  only for changed snapshots. Snapshot authority still comes from the resolver.
- Integrated into SRS, ARS, DRS, Digital IPOS and Analog IPOS. Historical authors
  stay unchanged; current Markdown title and DOCX author remain consistent.
- DRS table preservation accepts append-only version history and rejects old-row
  loss, edits, reordering or duplicate history tables. Removed obsolete equality
  between the current approved snapshot and the historical preservation baseline.
  Other protected tables retain strict checks; baseline JSON was not rewritten.
- Source/test files changed: `scripts/workflow_routing.py`,
  `scripts/spec_document_contract.py`, `scripts/run_srs_gen_spec_agent.py`,
  `scripts/run_ars_gen_spec_agent.py`, `scripts/run_drs_gen_spec_agent.py`,
  `scripts/generate_ipos_specs.py`, `tests/test_generator_snapshot_binding.py`,
  `tests/test_drs_template_contract.py`, `tests/test_descriptive_summary.py`.
- Verification: 8 snapshot-binding, 8 DRS-contract and 74 descriptive tests PASS
  (90 total); central coherence PASS / 0 findings; independence guard exit 0.
  No specifications regenerated or new production snapshot approved in this edit.
- Remaining separate defect: undefined `text` in DRS
  `_is_non_normative_table_row`; not part of the history repair.

## 2026-10-06 - Stage 5 DRS Date And Failed-Output Recovery
- Failure: unchanged snapshot/version replaced the history date 2026-10-01 with
  2026-10-06. Markdown and DOCX protected-table checks failed; failed output also
  left stale contract hashes, producing three DRS-local central findings.
- First date-only repair was superseded by the final shared history helper above.
- Used existing `run_drs_gen_spec_agent.py --snapshot-id
  snap-b2e8101b00dc6909feaed885 --regenerate-downstream` to repair DRS-only outputs;
  crosscheck PASS, 55 requirements. Stage 5 gate PASS at 15:47:22; central PASS/0.
- Do not bypass unrelated snapshot/authority findings or silently rebaseline.
  Canonical DB may be touched by derived ledger/audit writes; do not claim
  byte-for-byte DB identity merely because approval authority is preserved.

## 2026-10-06 - Candidate-Only Fingerprint Drift Repair
- Nine approved row pairs differed only in `lineage_candidate_parent_req_ids`;
  no actual parent change justified stale SRS/SysML contract markers.
- Excluded that candidate field from the operational hash only, leaving review/
  audit evidence intact and real approved metadata hashed. Kept approval policy,
  mapping persistence and resolver behavior unchanged.
- Added candidate-drift stability and actual-contract-change negative regressions
  to `tests/test_srs_downstream_coherence.py`: 19 PASS.
- Refreshed SRS/final SysML once from the same snapshot; Stage 3 gate and central
  coherence PASS. Snapshot/mapping digest before and after remained
  `a218609a9ab755559e798a050b9400c964760bfe4cf81f1f144fbd09aa6db172`.
- Operational hash: `8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372`.

## 2026-10-06 - Workflow GUI Lifecycle, Reports And Zoom
- Active executable stage remains green; failed stage remains red after run
  completion/redraw. Lifecycle parsing matches actual CLI starts, including 2a;
  unbuffered subprocess output supports live status. Standalone Analog IPOS uses 7.
- Validation reports open in the built-in read-only viewer; diagnostics/reports
  allow selection, Ctrl+C and right-click Copy.
- Shared Canvas-bounds helper fits wrapped workflow labels in fixed-size boxes
  and starts compact fonts at zoom-scaled sizes. Full diagram also uses fitting.
  No layout/color/click changes; 15 zoom steps and three display scales checked.
- Files: `scripts/workflow_gui.py`, `tests/test_final_polish.py`; GUI suite 46 PASS.

## 2026-10-06 - Earlier Clone Portability And Stage 1 Recovery
- Active clone path normalization is centralized in `scripts/repo_paths.py`;
  legacy OCR address rebasing changes addresses, not requirement authority.
  VS Code tasks use the selected Python interpreter. Prior focused tests: 157 PASS.
- Stage 1 extraction preserves complete tagged bodies across pages/sections,
  avoiding truncation or accidental concatenation at the next ID/section.
  Recovered 271 rows / 191 IDs; 9 focused tests and Stage 1.4-1.7 PASS, RAG fail 0.
- Original `../STBIO_AI` remains a read-only reference for this work. Do not
  generalize successful focused tests into complete cross-project qualification.

## 2026-10-01 - SRS System Overview Audit-Backed Rollout
- Regenerated only SRS `3.1-3.7` from approved snapshot
  `snap-b2e8101b00dc6909feaed885`, using the same descriptive records that feed
  the SRS audits and reconsidering candidates previously rejected only for
  `topic output limit`.
- Added deterministic system-level projections for product identity, external
  sensing, ECG/BIA and acquisition capabilities, aggregated domains, operating
  modes, power-domain behavior, interface boundary narrative, and allocation
  scope. Raw normative text, DRS/ARS/IPOS authority, block lists, register/
  address/port/signal details and malformed OCR/table fragments remain out.
- Updated the SRS renderer, shared overview validator, Stage 3 gate wiring,
  central downstream validator wiring, SRS template and shared category
  convention contract. No requirements, `Covers`, mappings, allocation values
  or snapshot authority changed.
- Verification: 74 descriptive tests PASS; 7 document-contract tests PASS;
  compile/diagnostics PASS; SRS generation, LaTeX conversion, SRS crosscheck,
  LaTeX crosscheck, independent System Overview validator and Stage 3 gate PASS.
  Full Stage 0-7 validation had passed before the final SRS-only renderer edits;
  it was not rerun afterward.
- DOCX was regenerated at `17:44:08`; current hash capture was deferred because
  Word held the document open. Close Word before further DOCX regeneration or
  hash verification.

## 2026-10-01 - DRS Stage 1 Descriptions And Overview Readability
- Completed the DRS descriptive-evidence pass using Stage 1 OCR overview and explicitly block-attributed descriptions. Extraction filters page continuation/TOC noise, requires a unique block subject for block-local attribution, and records source locations in the descriptive audit. Normative requirements, `Covers`, snapshot authority, SRS, ARS, and IPOS remain unchanged.
- Reflowed generated DRS `3. Top Level Overview` into paragraphs of at most two sentences and regenerated Markdown/DOCX from the same approved snapshot. Latest DRS generation and crosscheck PASS; `tests/test_descriptive_summary.py`: 74 PASS. DRS remains at 55 requirements, 13 mapped, 42 unassigned. The preceding descriptive rollout's Stage 5 and central coherence PASS results were not rerun after this formatting-only update.
- Latest audit check: 5 overview descriptions retained, 6 Stage 1 block descriptions retained, 0 overview rejects. GUI/PPTX work in this rollout clarifies descriptive evidence, parallel specification generation, and IPOS lineage; GUI validation PASS (20 nodes, 24 edges, 10 selectable nodes), PPTX 19 slides with updated traceability on slide 14.
- Preserve the section 4.1 ISPU role text `need clarification`: its table and preservation baseline are locked, even though section 3.1 contains Stage 1 ISPU prose. Require explicit authorization before changing/rebaselining it.
- Snapshot: `snap-b2e8101b00dc6909feaed885`. SHA-256: DRS MD `e1a39bd4bb0bccd7ccae4e0148ec0125afe7852f72cd57804278f1e0f2f0dfde`; DOCX `89d4c15ab6161bae715d99cb79c1aa38bb009af2e98b3b883be66555b01c8681`; descriptive audit `585d9cbdc206aaafa752fa70c9b3671b4f644b3aa3a99635e1caa8a26dfd2452`; traceability `d8132195d71c7cbe8fac899dda5263181d7954589b8b844478cc7dd51d54b93c`; workflow PPTX `b3a952c6cbd6fb49d4c3561b40614e202b71b9c1c02da5e0d76e532e994ef635`.

## 2026-10-01 - DRS Conventions Moved To Section 2.1
- Preserved the user's template edit and changed the executable DRS contract to
  require `2.1 Conventions` under `2. Definitions and terminology`, with the
  four YAML definitions rendered in order and with the expected heading levels.
- Moved generation from document control to section 2; retained Table 6 as the
  separate ID convention table. TOC and internal index now use the numbered
  heading, and final Markdown/DOCX validation rejects the old placement after
  Table 2 and duplicate definitions.
- Focused contract tests: 7 PASS. DRS-only generation, crosscheck, Stage 5 gate
  and central downstream coherence: PASS. Word opened the final DOCX with
  `OpenAndRepair=False`; 42 tables were available and the hash was unchanged.
- Snapshot remains `snap-b2e8101b00dc6909feaed885`; no SRS, ARS or IPOS outputs
  were regenerated. Preserve the existing pre-pilot baseline.

## 2026-10-01 - DRS Word Open-Without-Repair Repair
- Word 16.0 rejected the final DRS DOCX with `OpenAndRepair=False`; raw Pandoc and the first two post-processors opened. The shared common formatter changed the core metadata `dcterms` prefix to `ns2` but left QName-valued `xsi:type` attributes referring to `dcterms`. Restored namespace registration and added a focused date-type regression.
- Re-exported only DRS DOCX; Word opened the actual final file without repair, read-only and without saving (42 tables, 7213 paragraphs). Hash evidence is in `logs/drs_word_open_verification_20261001.json`. Markdown, CSVs, canonical DB and snapshot unchanged; DRS crosscheck, Stage 5 gate and central coherence PASS.
- The global DOCX layout test currently expects exactly 11 documents but discovers 12 in the existing artifact tree; the namespace-focused test and other layout tests pass. This count assumption was not changed as part of the Word fix.

## 2026-10-01 - Executable DRS Template Contract Pilot
- Embedded version-1 YAML in the DRS template, merged document structure and prose rules, and reduced DRS-specific orchestrator rendering duplication. General Rules and approved snapshot authority remain above the document contract.
- Added strict loading, passive arrangement, final Markdown/DOCX checks, preservation baseline, metadata hashes and shared crosscheck/Stage 5/central enforcement. Missing or unsupported mandatory rules fail before generation. Only explicit DRS output repair is permitted during migration.
- Added negative tests for contract corruption, conventions placement/content/order, DOCX-only divergence, table/TOC loss, numeric index order and prose defects. 87 tests PASS; generation/crosscheck/Stage 5/central PASS.
- Corrected adjacent-table grouping and a zero-number navigation entry detected by gates. Rebuilt the parser inventory only from hash-verified pre-pilot backups. Preserve blank boundaries when moving tables; a heading alone does not prove its TOC entries survived.
- 291 protected files and 55 authored requirement bodies/Covers unchanged; traceability and descriptive/coverage audits identical. All 24 canonical DB tables compared, with only derived allocation created_at differences. No SRS/ARS/IPOS regeneration. Word opening without repair remains unverified.

## 2026-10-01 - DRS Behavior-First Section Cleanup
- Reproduced the count-shaped prose defect with a focused failing test. Shared deterministic relationship, clock and role composers now replace counts and matched-keyword inventories; final Markdown/DOCX prose is independently checked through the existing DRS and central validators. General Rules and orchestrator/stage-gate guidance were updated without pilot-name cases.
- Preserved section mapping, approved evidence, directed associations, concrete-block boundaries and exact supporting tables. Improved scope/context, power/clock/domain control, interconnect, shared resources, processing, configuration/interfaces/data paths, timing and boundary-interface prose. Detailed before/after and out-of-contract residuals are recorded in `docs/drs-descriptive-baseline.md`.
- Fixed coordinated-verb projection after rendered review exposed a grammatical defect; tests now preserve shared action objects and pronoun antecedents. Lesson: composer parity is not sufficient proof of technical prose quality, and a keyword match is not itself a functional summary.
- Only DRS regenerated at `snap-b2e8101b00dc6909feaed885`. DRS crosscheck/Stage 5/central coherence PASS (zero findings); 73 descriptive tests PASS. Supporting tables, section 9 onward, provenance and traceability CSVs are unchanged. Protected SRS/ARS/IPOS, configuration and mapping artifacts remain byte-identical.
- The existing generator's allocation-ledger refresh changes canonical DB bytes. Read-only comparison across 24 tables around the final run found only `requirement_allocations.created_at` changes, with allocation values and authoritative tables unchanged. Record this distinction instead of claiming DB byte identity. Legacy authority-scan findings in untouched scripts remain outside scope.

## 2026-09-30 - DRS Section-Level Synthesis Pilot
- Replaced repeated block-function and raw exchange/path narrative in DRS sections 3, 3.1, 4.2-4.7 and PMU/domain-control prose with deterministic theme grouping from approved Stage 2 and pinned-snapshot records. Kept one named 3.1 paragraph per selected concrete digital block, full provenance-bearing tables, owner-scoped I/O, and unsupported-topic clarification.
- Removed redundant singleton PMU status tables in 3.1/4.6 while preserving the approved status edge in prose/audit and all eight PMU-source clock routes, nine reset outputs, and 11 total clock routes. Updated the existing DRS descriptive validator and General Rules; added section synthesis and missing-clock-summary tests.
- DRS-only regeneration/crosscheck PASS (55 requirements), focused tests 71 PASS, Stage 5 gate PASS, central downstream coherence PASS (0 findings). Current hashes, before/after by section and residual weak evidence are in `docs/drs-descriptive-baseline.md`. Prior restore entries/hashes below are historical.

## 2026-09-30 - DRS Shared Sections, Reset Route, And Clock-Gating Controls
- Consolidated DRS 3.1 arbitration/control and shared resources into one topic; populated 4.2 and 4.6 from approved in-scope architectural evidence and added explicit clarification for unsupported facets. No generic arbitration, ordering, backpressure, performance, or synchronization policy was invented; non-block endpoints were not promoted to blocks.
- Crosschecked `DDS_STBIO1_2054` against OCR and approved PMU/Main Controller ports. The OCR table splits `i_rstn_sync_32`; the DB row has merged path text. DRS describes the corroborated PMU reset output to Main Controller reset input and leaves release/synchronization behavior open.
- Found the clock-gating clarification was a renderer defect: the approved snapshot contains gating expressions, but `_drs_clock_path_rows` captured only `with`/`without`. Updated DRS projection to carry expressions into both 4.6 and 4.7; escaped `|` in Markdown, confirmed DOCX cells preserve expression, and flagged OCR-split names instead of silently repairing them. `DDS_STBIO1_2024` endpoints remain independently unclear.
- Strengthened the existing central DRS validator to compare route/gating rows with the pinned snapshot in Markdown and DOCX. Added synthetic parser/facet coverage and a mutation regression for altered gate expressions. Existing General Rules already require preserving clock-gating table values.
- Regenerated only DRS Markdown/DOCX from `snap-b2e8101b00dc6909feaed885`; requirements remain 55. No canonical DB, Stage 1/2 authority, SRS/ARS/IPOS outputs, allocation, or approval metadata changed.
- Verification: focused descriptive tests 70 PASS; DRS generation/crosscheck PASS; Stage 5 DRS gate PASS; downstream coherence PASS with zero findings. Current DRS hashes and before/after details are in `docs/drs-descriptive-baseline.md`; latest restore instructions are in `local_memory/chat_handoff.md` and `local_memory/checkpoint.md`.
- Open evidence boundaries: OCR spelling and gating interpretation, `DDS_STBIO1_2024` endpoints, reset release/synchronization and CDC/RDC, measured latency/bandwidth/IRQ response, arbitration priority/concurrent access order, and flow control where not specified by approved evidence.

## 2026-09-29 - DRS Introductory Architecture Content
- Replaced generic DRS introductory descriptive placeholders and raw integration bullets with natural, deterministic summaries and topic/boundary tables from existing approved top-digital interaction authority. Added descriptive audit rows for section 3, section 4 topic rows, and section 7, checked against the matrix and final Markdown/DOCX. Kept selected concrete-block descriptions, owner I/O tables, approved snapshot, authored requirements, and SRS/ARS unchanged.
- Focused tests 63 PASS; DRS regeneration and crosscheck PASS (55 requirements); Stage 5 gate PASS; central downstream coherence PASS with zero findings. See `docs/drs-descriptive-baseline.md` for before/after examples and current Markdown/DOCX/audit fingerprints. Earlier DRS block-only hashes remain historical.

## 2026-09-29 - DRS Pilot Frozen As Current Descriptive Baseline
- The same shared document-neutral natural-prose rule is now validated for IPOS and DRS at `snap-b2e8101b00dc6909feaed885`. DRS selects approved concrete digital blocks from the existing inventory, preserves exact `Function` provenance and complete owner-scoped I/O tables, and shares Stage 5, crosscheck, and downstream quality checks. SRS/ARS rendering is unchanged pending separate pilot decisions.
- DRS regeneration and crosscheck PASS (55 requirements, 10/10 inputs); focused suite 62 PASS; Stage 5 DRS gate PASS; full read-only downstream coherence PASS (0 findings). This is a local output baseline, not a new approval snapshot or a complete S0-Stage 7 rerun.
- `docs/drs-descriptive-baseline.md` records hashes of DRS Markdown, DOCX, descriptive audit, traceability matrix, generation/crosscheck reports, and exact reproduction commands. The open DOCX was byte-fingerprinted via Python when PowerShell `Get-FileHash` could not read it; no regeneration was needed.

## 2026-09-29 - Completed Global IPOS Natural-Prose Rollout
- User explicitly approved replacing the frozen Main Controller pilot with one shared, project-agnostic final prose contract for every materialized Digital/Analog IPOS block. Regenerated only the three remaining outliers (Main Controller, Pad Mux, Regmap) from `snap-b2e8101b00dc6909feaed885` after the earlier scoped repair of ADSP, I2C_SPI_AHB, PMU, Sensor-Hub, and Smart FIFO. No new approved inputs, Stage 2a changes, source-spec reads downstream, block-specific rules, or authored requirement edits.
- `scripts/workflow_routing.py` now generates natural inventory-bounded 1.1/1.2 openings, derives supported subfunction details from accepted local statements, rejects final overview governance wording independently of composer parity, and preserves `register-map controls` rather than truncating it to `-map controls`. `tests/test_descriptive_summary.py` adds negative wording and compound-input regressions.
- Updated `.github/copilot-instructions.md` (General Rules), `.github/agents/workflow-orchestrator.agent.md`, `.github/skills/workflow-stage-gate/SKILL.md`, and `docs/ipos-descriptive-rendering.md` with the common future-project contract, explicit rollout decision, before/after findings, and historical/new Main Controller hashes. The earlier pilot-only and BLOCK_DOWNSTREAM records below are retained as history, not present blockers.
- Verification: descriptive tests 60 PASS; source-port coverage tests 2 PASS; full Digital gate PASS (259 requirements/8 blocks); Analog gate PASS valid-empty (0/0); full read-only downstream validator PASS (0 findings). Main Controller current hashes: Markdown `37E0C4030514B3A982638A4AB758107193078DBB93B5178C5B7FF6CE2ABD2FE3`; descriptive audit `46231A50CF86466142438A29165448E78FADD2C75FDC8EE24BCC9D7B358101C5`.
- Lesson: successful structural/traceability gates do not imply acceptable descriptive prose. Require an independent final-text quality check for governance scaffolding and full unscoped gates before declaring rollout complete; preserve the earlier FAIL evidence without treating it as current.

## 2026-09-29 - Full Shared IPOS Descriptive Rollout And Quality Findings
- User approved extending the common final 1.2 rendering/validation contract beyond the frozen Main Controller pilot. Promoted the shared workflow-stage-gate policy without adding block-specific rules or new approved inputs.
- Reused the exact approved snapshot candidate projection in `scripts/workflow_routing.py` for generation, IPOS gates, and downstream coherence; repaired all-block candidate/audit/normalized-input parity in the central validator. Added validator detection for truncated or generic subfunction summaries and a regression for the quality finding.
- Fully regenerated all eight Digital IPOS documents and valid-empty Analog IPOS at `snap-b2e8101b00dc6909feaed885`. Focused tests PASS (57), Analog gate PASS (0/0). Digital gate FAIL at ADSP. Full downstream coherence decision `BLOCK_DOWNSTREAM`: six quality findings across ADSP, I2C_SPI_AHB, PMU, Sensor-Hub, and Smart FIFO; exact headings in `docs/ipos-descriptive-rendering.md`. Other three Digital blocks have no descriptive findings.
- No Stage 2a, allocation, snapshot, or source-spec authority was changed. Do not waive descriptive failures merely because structural gates previously passed; retain Main Controller pilot hashes as a historical baseline.

## 2026-09-29 - Main Controller 1.2 Materialization And Pilot Freeze
- Retained approved snapshot `snap-b2e8101b00dc6909feaed885` and same-block requirement-candidate universe; changed final 1.2 grouping, presentation, and audit/validation only. No Stage 2a, source-ingestion, ownership, or normative-requirement edit.
- Merged ramp timing, GSR processing, ADC enable, FSM transition and PPG ALC handoff into supported functional units; suppressed standalone soft-reset and chopper-clock helpers and aligned the normalized materialization ledger. Accepted local candidates: 52 merged, 4 standalone, 2 suppressed atomic.
- Improved role-first FSM openings, heading capitalization, signal/timing and GSR/CDS phrasing, redundant self-interactions, and standalone-quality validation in `scripts/workflow_routing.py`; added focused tests in `tests/test_descriptive_summary.py` (57 passing). Regenerated only Main Controller Markdown/DOCX/audits; Main Controller-scoped Digital IPOS gate PASS (259 requirements, 8 blocks).
- Confirmed that `The second FSM called Elab_FSM, is in charge of` exists in supplementary source OCR outside the approved candidate set. It is not a new input for this pilot; Stage 2+ remains artifact-only.
- Froze Main Controller Markdown and descriptive audit SHA-256 fingerprints, snapshot, counts, and scoped commands in `docs/ipos-descriptive-rendering.md`. Centralized the block-agnostic rendering/validation rule in `.github/skills/workflow-stage-gate/SKILL.md`; 57 tests and Main Controller-only gate passed again after the governance edit. No other block was regenerated. Governance constrains rollout, but shared code is not runtime-gated by block.
- For subsequent work, consult `local_memory/chat_handoff.md` and `local_memory/checkpoint.md`. Any wider rollout requires a separate approval, per-block review, and a scoped gate; do not use blockless regeneration for this pilot.

## 2026-09-28 - Shared Deterministic IPOS Aggregation
- Replaced IPOS rendering-time RRF/ranked facet selection with one shared deterministic aggregation renderer for every materialized block. It aggregates the full accepted same-block evidence set, preserves distinct responsibilities and explicit local interactions, deduplicates only equivalent phrasing, and retains admitted evidence order.
- Removed the Main Controller-only pilot module/configuration and migrated audit fields from RRF rank/score to `structural_selection_mode` and `structural_aggregation_order`.
- Retained RRF only for Hybrid RAG retrieval/query fusion and retrieval benchmark paths. No extraction, acceptance/suppression, ownership, snapshot, allocation, or traceability logic changed.
- Updated General Rules, workflow gate guidance, and IPOS rendering documentation. Added regressions for complete accepted-action retention and suppressed single-token materialization false positives.
- Regenerated all Digital IPOS blocks for snapshot `snap-b2e8101b00dc6909feaed885`.
- Validation: focused contract and descriptive tests PASS (47 tests); full Digital IPOS gate PASS (259 requirements, 8 blocks); downstream coherence PASS with 0 findings.

## 2026-09-23 - Central IPOS Descriptive Quality, Materialization, And Layout
- Recorded 2026-09-21 through 2026-09-23: no additional project code fix is recorded locally for 2026-09-21/22; the local-memory manifest was refreshed on 2026-09-22. This entry records the completed 2026-09-23 IPOS pass.
- Centralized IPOS descriptive quality in `scripts/workflow_routing.py`: only approved block-inventory functional evidence drives high-level overview synthesis; requirement text remains authoritative detail only.
- Strengthened topic admissibility: rejects article-prefixed parameter/value/address forms and low-level fragments; requires topic-specific functional combinations; handles ADSP before generic DSP; gives register/configuration/status precedence over incidental reset; rejects isolated reset/signal/memory/acronym matches.
- Added deterministic local purpose synthesis for supported inventory evidence, including Sensor-Hub I2C target control, data collection, and FIFO coordination. Regmap remains register configuration/status; Smart FIFO remains FIFO storage/local memory access.
- Changed IPOS materialization to emit documents only for blocks with mapped approved IPOS requirements. Digital now has 8 documents for 259 rows; Analog remains valid-empty with no documents. Zero-mapped blocks such as OTP and ISPU are intentionally omitted.
- Extended the existing IPOS gate with shared DOCX layout verification. The shared formatter now recognizes IPOS `1. Block overview` when moving the title/TOC/navigation section: title and metadata on page 1, TOC first on page 2, Document Navigation after TOC, PAGE field bottom-right.
- Updated General Rules and workflow-stage-gate skill to make central orchestrator-validator governance, evidence/scope/omission behavior, zero-mapped document omission, and shared layout explicit.
- Validation: py_compile PASS; Digital IPOS regeneration complete; Digital IPOS gate PASS (259 requirements, 8 blocks); Analog IPOS gate PASS (0 requirements, 0 blocks); `validate_downstream_coherence.py` PASS with 0 findings for snapshot `snap-b2e8101b00dc6909feaed885`.

## 2026-09-17 - Explicit Stage 2 Workbook Review And CSV Authority
- Fixed `scripts/mapping_review_sync.py` so non-empty workbook review values are authoritative during XLSX-to-CSV synchronization. Empty cells may preserve existing CSV values; an empty decision normalizes to `pending_review`.
- Removed formula-driven and inferred approval from `scripts/generate_stage2_specs.py`. `review_decision` is now an editable literal cell with dropdown values `pending_review`, `approved`, `reassigned`, `rejected`, and `needs_clarification`.
- Preserved prior reviewed values across Stage 2 regeneration by `requirement_id`; conservative allocation prefill only fills clearly supported empty fields.
- Unified workbook formatting: all review fields remain red while incomplete/invalid and become green only for an explicitly `approved` or `reassigned` row whose required fields and allocation class/target pair are valid.
- Updated Architecture Map Review GUI help to require an explicit review decision. Gate order remains save/close workbook -> synchronize XLSX to CSV -> validate synchronized CSV -> record CSV hash.
- Added/updated focused sync and workbook-generation tests for workbook-authoritative decisions, no auto-approval, literal decision cells, dropdown contents, unlocked decision editing, and row-validity conditional formatting.
- Validation: 5 focused tests passed; modified scripts compiled; diagnostics were clean. No Stage 2A or downstream stage was run.

## 2026-09-14 - Ownership-Safe DFT Context And SysML Find
- Changed Stage 1 ownership inference to derive concrete ownership from the parent section rather than block-like terms in paragraph titles. This prevents `ADC TEST LOW NOISE` from becoming an inferred ADC owner.
- Added dedicated DFT/test source-context precedence in Stage 2 preview generation. `DDS_STBIO1_0701` and `DDS_STBIO1_0702` preserve their original paragraphs, show candidate evidence only for review, and remain blank/pending for approved concrete ownership by default.
- Kept authoritative non-specific Stage 2 routing at `Unassigned`; no fake SysML/block-IPOS owner is created. Reviewer-selected hierarchy promotion remains the only path to a concrete owner.
- Preserved user control of Stage 2 approval hashes and snapshots. Refreshed preview inputs require explicit Architecture Map Review before Stage 2A and downstream regeneration.
- Added reusable SysML `Ctrl+F` search behavior to the main source viewer and hierarchy-window details/source viewer. Search is case-insensitive, highlights all matches and the current match, supports Enter/Shift+Enter and Prev/Next navigation, reports match counts, closes on Escape, and cleans up with the hierarchy window.
- Work Area text and CSV `Ctrl+F` behavior remains intact.
- Validation: `python.exe -m unittest discover -s STBIO_AI\\tests -p test_final_polish.py` passed 22 tests; `python.exe -m py_compile STBIO_AI\\scripts\\workflow_gui.py` passed; diagnostics were clean.
- Next action: review the refreshed architecture map, explicitly approve it, rerun Stage 2A, freeze the snapshot, and regenerate Stage 3/downstream artifacts.

## 2026-09-11 - SRS Power Sequence And Reusable Specification Rules
- Updated `scripts/run_srs_gen_spec_agent.py` so `Entry, exit, wake-up, and restore` is populated from approved power-domain evidence rather than `needed clarification from user` when source facts are available.
- Added source-bounded sequence wording for always-on entry, OTP supply availability, switchable-domain power-down, and software-controlled wake-up. Missing retention/restore timing remains explicitly unspecified.
- Removed power-domain evidence from the general SRS system-function topic and Operating Modes classification to avoid repeating the same detailed domain descriptions.
- Saved reusable ownership and formatting rules in `.github/copilot-instructions.md`, `.github/skills/workflow-stage-gate/SKILL.md`, and SRS/ARS/DRS generator-agent instructions.
- Rules require SRS interface summaries only, DRS complete digital block I/O tables, single-block IPOS detailed I/O, no complete I/O duplication, and numerical TOC nesting preserved in DOCX.
- Validation: edited Python files compiled successfully; `python -m unittest STBIO_AI.tests.test_descriptive_summary -q` passed all 13 tests; SRS Markdown/LaTeX regeneration passed.
- Remaining work: remove legacy SRS section 3.4 complete I/O table emission and validate DOCX TOC list levels after successful DOCX conversion. Empty approved snapshot remains a known traceability blocker.

## 2026-09-10 - Architecture Map Review, Top-Level Routing, And Stage 2A Validation
- Added `approved_block` Excel validation in `scripts/generate_stage2_specs.py`, sourced only from `approved_block_list.xlsx`, plus top-level choices `System`, `Digital`, and `Analog`. ADC and interface/context labels are excluded from the allowed block list.
- Added `approved_classification` Excel validation for `System`, `Digital`, and `Analog`.
- Added a hidden baseline sheet and formula-driven `review_decision` cells so a user edit to classification, block, or notes immediately displays `reassigned`. GUI workbook import independently detects those changes and writes `reassigned` into the authoritative mapping CSV, ignoring manually edited decision text.
- Workbook protection was removed because it prevented user editing in the active Excel environment. `review_decision` authority is instead enforced by its formula and GUI import logic.
- Fixed dropdown disappearance after workbook import: `_sync_mapping_workbook_to_csv()` now reads the XLSX and writes only the mapping CSV. It no longer uses openpyxl to resave the XLSX, which had stripped Excel validation extensions.
- Defined top-level routing semantics: `System` maps to SRS only, `Digital` to DRS only, `Analog` to ARS only; none are treated as real architectural/SysML/IPOS block names. Concrete approved real-block mappings continue to feed block-specific IPOS.
- Updated DRS and ARS selection to honor explicit categories, avoiding heuristic leakage from System/Analog to DRS or System/Digital to ARS.
- Fixed `scripts/validate_stage2_mapping.py` so exact reviewer-approved `reassigned` ownership is recognized as semantic evidence. This resolved false lexical-overlap failures for Regmap, Main Controller, and BIST Controller assignments.
- Verified: `python scripts/validate_stage2_mapping.py` PASS; `python scripts/workflow_cli.py run --stage 2a` PASS with 314 requirements, zero uncovered, Stage 2A profile crosscheck PASS, post-mapping semantic crosscheck PASS, and Stage 2A gate PASS.
- Updated GUI layout persistence to save only on explicit `Save Window Layout` or GUI close. Added local Live Chat persistence at `logs/workflow_gui_chat.log`, reloading the latest 200 entries on startup.

## 2026-09-08 - Strengthened Workflow And GUI/Stage 1 Specs Fixes
- Fixed `scripts/generate_stage2_specs.py` missing `_write_mapping_preview(..., approved_classifications)` argument. The generator now resolves approved canonical classifications once and passes them to both supplementary review loading and mapping preview generation.
- Stage 1 specs Gate 2 full wrapper passed: generation, specs crosscheck, and `validate_stage2_gate.py`.
- Updated `README.md` with S0 through Stage 7 canonical order, canonical SQLite/derived artifact boundaries, snapshot/profile authority, and GUI selector mapping.
- Updated `scripts/workflow_gui.py` stage selectors: both single-stage and range menus expose S0-S2H and Stage 3-7; Optional Architecture Comparison is last. Approval-only ranges are rejected with guidance rather than sent to unsupported workflow CLI stages.
- Added compact diagram vertical scroll/mouse-wheel support; preserved horizontal Shift-wheel and Ctrl-wheel zoom.
- Added hover descriptions for new diagram nodes and shortened supplementary source descriptions.
- Hardened tooltip dismissal and supplementary-dialog popup cleanup.
- Added/extended focused tests in `tests/test_final_polish.py` and `tests/test_end_to_end_authority.py` for menu completeness, diagram descriptions, report metadata, SysML completeness, snapshot/profile authority, bootstrap metadata, and multi-source provenance.
- Validation: Stage 1 specs Gate 2 PASS; GUI/generator compilation PASS; latest focused GUI suite PASS with 8 tests; prior full suite PASS with 57 tests; diagnostics clean for latest touched files.

Next action: load the 2026-09-08 restore checkpoint before any further workflow or GUI edits. Keep approval metadata user-controlled and avoid broad refactors of diagnostic scanner findings.

## 2026-09-07 - Single-Workbook Supplementary Approval And Stage 2A Corpus Repair
- Simplified supplementary review persistence in `scripts/workflow_gui.py` to one `comparison_results.xlsx` per staged package. The GUI no longer creates alternate approved workbook files.
- Enforced manual-save ownership: user saves/closes Excel; GUI checks that the exact workbook is saved and closed before reading it. CSV synchronization is performed only by explicit Merge.
- Removed automatic review-workbook color saves from Refresh Review Colors and Merge. GUI layout autosave remains unrelated and only writes GUI state.
- Accept All is an explicit write action after the user-save/close gate; it updates the same workbook, reopens it, and defers CSV reading/synchronization until Merge.
- Added duplicate-name workbook detection and default-on verbose GUI execution tracing with an ON/OFF push button.
- Added Stage 2A approval enforcement: Run Stage 2A reopens the architecture map and asks for review/save/close/gate enablement if approval is not active.
- Fixed Stage 2A mixed-corpus validation: `run_stage2_micro_arch_and_crosscheck.py` now passes its resolver-selected authoritative corpus to `validate_stage2_mapping.py`.
- Fixed supplementary merge idempotency: `ingest_source_spec.py` now deduplicates existing and new rows by `source_req_id`/canonical identity rather than only `id`.
- Repaired the current integrated corpus from 1052 duplicated rows to 314 unique rows; 123 supplementary IPOS IDs remain represented.
- Validation: changed-file compilation passed; `python -m unittest discover -s tests -q` passed all 18 tests.
- Stage 2A’s remaining stop is intentional stale approval evidence after corpus repair. User must review the refreshed architecture mapping and re-enable approval; do not edit approval hashes automatically.

## 2026-09-04 - GUI Layout Persistence, SysML Workspace, And Rendered PDF Reader Checkpoint
- Completed the GUI usability pass in `scripts/workflow_gui.py`: compacted the workflow CLI/Work Area top region, kept Live Chat commands visible, removed Execution Log zoom controls, and placed `Save Window Layout` in the application header.
- Layout persistence now covers the main window geometry and all GUI paned splits: main vertical, CLI/Work Area, workflow diagram/Live Chat, chat input, artifact navigation/viewer, SysML graph/source workspace, SysML source tree/viewer, and System Traceability. Saved values are restored after Tk layout settles, with bounds-aware recovery for collapsed/off-screen sashes.
- SysML Architecture now presents the block graph beside the source-file selection and selected-source viewer. Source tree and source viewer remain separately resizable and are included in saved layout state.
- SysML block clicks highlight the selected block in blue, switch to the SysML tab, expand its source-tree ancestors, and open the matching `.sysml` file. Selected source text supports plus/minus and Ctrl+mouse-wheel zoom.
- Work Area PDF selection now opens a rendered PDF Reader Toplevel using PyMuPDF and Pillow. The reader supports page navigation, scrollbars, plus/minus zoom, Ctrl+mouse-wheel zoom, and clean PDF-document shutdown.
- `requirements.txt` already includes `PyMuPDF`; PyMuPDF was installed into `C:\python\python39` and Pillow was confirmed available. A repository PDF render smoke test passed on `specs/DDS_STBIO1.pdf` at 596x842 pixels.
- Validation passed: GUI compilation, VS Code diagnostics, PDF dependency import, and PDF page rendering. Preserve user-controlled `config/gui_state.json` settings and use the Save Window Layout button for explicit persistence.

## 2026-09-04 - Optional Semantic Recovery And Ownership-Safe Retrieval Checkpoint
- Added project-agnostic retrieval governance to `.github/copilot-instructions.md`: legacy lexical/normalized/hybrid modes remain compatible; semantic and hybrid-semantic retrieval are optional, local-only, deterministic evidence channels.
- Added one-shot semantic recovery after an empty legacy query, controlled by `config/retrieval_config.json` and disableable with `--no-semantic-fallback`. Missing semantic resources leave the legacy result unchanged.
- Restricted evidence semantic retrieval to `chunk` entities so blocks, functions, interfaces, and requirements cannot outrank source evidence in chunk-scoped queries.
- Added advisory requirement-ID mapping checks against the Stage 1 catalog, including expected owner and evidence presence. The check is diagnostic and cannot change deterministic ownership.
- Preserved exact-ID protection, conservative semantic RRF weighting, provenance, per-channel scores/ranks, and the ownership chain through Architecture Map Review and independent validators.
- Verified `DDS_STBIO1_0104` is PMU-owned in Stage 1, Stage 2, SRS/DRS, and `pmu.sysml`; the earlier apparent discrepancy was semantic entity/evidence confusion, not an architecture ownership change.
- Validation: 12 retrieval tests passed; query compilation passed; PMU audit passed; explicit no-fallback and unavailable-resource fallback behavior passed.


## 2026-09-04 - Canonical Block Identity And Coverage Report Checkpoint
- Expanded the shared architecture generator alias table for FIFO/Smart FIFO, Sensor Hub spelling variants, ISPU debug/integration variants, and I2C/SPI/AHB interface/controller variants.
- Updated `scripts/traceability_hierarchy_coverage.py` to use canonical block normalization, prefer reviewed mapping ownership, and filter coverage rows to concrete generated blocks.
- Preserved the authority boundary: hybrid RAG can retrieve candidate evidence, but reviewed deterministic mappings control final ownership and generated SysML.
- Verified architecture state: review approved, 191/191 source requirements represented, 154 mapped assignments verified, 648/648 ports represented, and 21/21 source XBAR edges matched.
- Final rerun PASS: architecture generation produced 191 requirements, 16 blocks, 648 ports, and 33 connections; coverage reports SRS 175/191 (91.6%), DRS 154/191 (80.6%), and end-to-end 154/191 (80.6%).
- Report inspection confirms canonical concrete block rows only. Legacy/context fragments `fifo`, `bistmode`, `ispuintegration`, and `xbarconnectionmatrix` are absent; `smartfifo` is the canonical FIFO row.
- Focused compilation passed for `scripts/generate_architecture_sysml.py` and `scripts/traceability_hierarchy_coverage.py`. Do not refresh Stage 2 approval hashes automatically.
- Decision confirmed: non-block-specific requirements can stay at system level. Preserve them as `Unassigned`/system-context entries with source provenance instead of assigning them to concrete SysML blocks.

## 2026-09-02 - Table 23 OCR Row Reconstruction Checkpoint
- Root cause: standalone Table 23 source-ID lines were recovered by a lookbehind limited to four lines, and lookahead detection finalized the preceding row too early. Wrapped cells were therefore truncated or rows were merged.
- Fixed `scripts/generate_stage1_requirements.py` to collect standalone-ID table context back to the previous table/requirement boundary and defer lookahead-only IDs only within recognizable parameter-table columns.
- Stage 1 regenerated PASS with 191 requirements. `DDS_STBIO1_8100` and `DDS_STBIO1_8101` now contain their complete Table 23 row text; unrelated `DDS_STBIO1_00000199` remains preserved.
- Canonical `architecture_mapping_preview.csv` regenerated PASS; both affected rows map to `I2C_SPI_AHB` with repaired source statements.
- RAG check confirmed page 99 was already intact in the indexed chunk, so the defect was Stage 1 extraction, not RAG chunk building.
- Stage 2 correctly stops for reapproval because refreshed source/draft/preview hashes no longer match the user-approved profile. Approval metadata must remain user-controlled.

## 2026-09-02 - Project-Agnostic Hybrid RAG Retrieval Checkpoint
- Updated `scripts/build_rag_index.py` with 150-character overlap, atomic table chunks, figure chunks containing caption/OCR/nearby text, and page/section/source-type metadata.
- Added deterministic normalized-term indexing with configurable `config/domain_vocabulary.json`: protected terms, acronym expansions, synonym groups, phrase mappings, exceptions, units, stopwords, and simple lemmatization.
- Added `chunk_terms_fts` alongside original-text `chunk_fts`; preserved original chunk text as the evidence source.
- Updated `scripts/query_rag_index.py` with lexical, normalized, and hybrid modes. Hybrid mode fuses rankings with RRF and reports lexical/normalized ranks.
- Rebuilt and checked the active index: 163 pages, 376 chunks, 248 text / 71 table / 57 figure chunks, and normalized terms present for 376/376 chunks.
- Validation passed: Python compilation, JSON validation, build, lexical/normalized/hybrid query trials, SQLite schema/count checks, and edited-file diagnostics. Temporary trial outputs were removed.
- Reusable boundary: retrieval remains deterministic lexical plus controlled-vocabulary normalization; no embeddings, vector database, spaCy model, or LLM retrieval authority is present.

## 2026-09-02 - Source-Baselined Hierarchy Coverage And System Traceability
- Added `scripts/traceability_hierarchy_coverage.py`, a project-agnostic Stage 5 reporting module. It joins downstream SRS/ARS/DRS matrices to the complete Stage 1 source-requirement catalog through `source_req_id` and emits source coverage, direct hierarchy-link coverage, end-to-end coverage, and explicit gaps.
- The report takes source-document identity from `artifacts/stage1_requirements/ocr_extracts/index.csv`, avoiding project context or source-file hardcoding.
- Scoped lower-level documents are `Not applicable` when their matrix contains no requirement in the declared scope. Context-only rows are counted separately and excluded from coverage percentages.
- Stage 5 DRS crosscheck regenerates `artifacts/stage5_drs/requirements_hierarchy_coverage_report.md`; the Stage 5 gate requires it.
- Added the `System Traceability` GUI tab. It renders Source Spec, SRS, ARS, and DRS with source document identity, source-spec coverage in nodes, direct-link percentages on arrows, `N/A` for non-applicable links, scrollbars, report open/refresh controls, and shared Work Area refresh behavior.
- Added the portable contract to README, orchestration spec, Copilot instructions, and workflow-stage-gate skill.
- Validation: DRS crosscheck PASS; Stage 5 gate PASS; `workflow_gui.py` and `traceability_hierarchy_coverage.py` compile.

## 2026-09-01 - Source-Fidelity Recovery And Architecture Map Review Checkpoint
- Recovered previously omitted tagged source requirements through deterministic Stage 1 source-backed records with table-line provenance; Gate 1 accepts these records because their provenance is explicit and reviewable.
- Removed legacy downstream source-ID exclusion and project-specific inferred behavior. SRS preserves the Stage 1 source statement rather than inventing functionality from a source identifier or domain-specific assumption.
- Stage 2 preview regeneration preserves existing validated mapping-review decisions rather than resetting approved/reassigned rows to `pending_review` after a Stage 1 refresh.
- The GUI workflow diagram has an interactive `Architecture Map Review` node between Stage 2 and Stage 2A. Its label and popup terminology match the dedicated review workspace exactly.
- Verified: Stage 1 has 191 requirements; Stage 2A PASS with 191 analyzed and zero uncovered; Stage 3 PASS with 155 SRS requirements, including the recovered source coverage. `workflow_gui.py` compiles. Pandoc remains unavailable, so DOCX generation is skipped.
- Follow-up: run Stages 4 and 5 when refreshed ARS/DRS artifacts are needed. Before editing the approved architecture profile, reread its current user-controlled approval metadata.

## 2026-09-01 - Project-Agnostic Local Requirements for Source Function Context
- Root cause: SRS allocated local IDs for retained source-context entries, while ARS and DRS emitted raw ledger prose directly from `unmapped_requirement_routing.csv`, bypassing their `ars_id_map`/`drs_id_map` and SRS upstream mappings.
- Updated ARS and DRS generation so each `retained_as_non_block_function_context` entry is rendered exactly once under `Source Function Context` as a complete local requirement: bold `**[<PREFIX>-REQ-xxx] Requirement:**`, complete preserved source body, one `Covers: SRS-REQ-xxx`, `[End]`, and `Source paragraph:`.
- Retained context IDs are excluded from residual, dedicated-source, and user-specific catalogs to prevent duplicate authored requirements. The implementation uses only runtime artifacts and generic `<PREFIX>` contracts.
- `scripts/validate_common_formatting.py` now enforces the cross-specification invariant: every `Source paragraph:` in a `Source Function Context` section must have a preceding local SRS/ARS/DRS header, `Covers:`, and `[End]`.
- Canonical authored headers in all generated SRS/ARS/DRS Markdown are now bold: `**[<PREFIX>-REQ-xxx] Requirement:**`. Shared DOCX post-processing applies bold Word runs after Pandoc conversion.
- Stage 4 skip behavior was revised: ARS can skip only when both Analog-category source requirements and retained Source Function Context rows are absent. For the current project, ARS generated 46 retained-context local requirements despite zero Analog-category inputs.
- Validation: Stage 3 SRS full flow PASS; Stage 4 ARS full flow PASS; Stage 5 DRS full flow PASS; direct Stage 3/4/5 gates PASS; changed Python scripts compile. Pandoc unavailable, so no DOCX was produced or visually inspected.

## 2026-09-01 - Shared Authored-Requirement Formatting And Requirements-Only Rendering
- Centralized project-agnostic authored SRS/ARS/DRS Markdown formatting in `scripts/workflow_routing.py`. The required portable boundary is `[End]`, a blank line, `<p>&nbsp;</p>`, a blank line, then `[<PREFIX>-REQ-xxx] Requirement:`.
- Integrated `normalize_authored_requirement_blocks(...)` as the final rendering operation in the SRS, ARS, and DRS generators so list/table post-processing cannot remove or relocate the boundary.
- Centralized DOCX header post-processing in `apply_docx_authored_requirement_formatting(...)`: authored requirement headers receive XML bold runs and 160 twips (8 pt) space before. This establishes document structure only; visual rendering in Word/PDF is still unverified.
- Corrected `validate_common_formatting.py` to recognize the blank / spacer / blank / header form rather than requiring the HTML spacer on the line immediately before each header.
- Replaced the DRS-specific register-only source exclusion with `_exclude_non_requirement_snippet(...)`, which prevents tagged raw `Definition`, `Assumption`, and `Comment` entries from being emitted as generated-spec excerpts. Confirmed that the prior `DDS_STBIO1_300` Definition was removed from regenerated DRS Markdown.
- Updated `docs/orchestration-spec.md` with the universal authored-boundary rule and requirements-only source-excerpt policy. Literal `<blank line>` text is not a Markdown/Word spacing mechanism and must not be restored.
- Validation status: an earlier Stage 3 run failed solely on the old spacer validator behavior. The validator patch was made afterward, but the focused Stage 3 gate result was not captured; rerun `validate_stage3_srs_gate.py` before declaring success. Rerun Stage 5 only after Stage 3 passes. Do not claim visible DOCX layout until rendered output has been inspected.

## 2026-08-31 - Project-Agnostic Domain, ARS, and Source-Context Rules
- Explicit Stage 1 classification is authoritative downstream. Digital requirements are excluded from ARS before analog/power/clock keyword heuristics are evaluated.
- A source set may legitimately omit a domain. Category coverage records this as a warning and must not synthesize requirements to satisfy a fixed category count.
- Stage 4 explicitly skips ARS generation only when the current Stage 1 summary has zero Analog-category rows with source requirement IDs. The Stage 4 validator independently rechecks the condition before passing the recorded skip.
- SRS and DRS now contain source-backed clock/reset and power-sequencing summaries generated from current PMU structural rows and normative requirements. The summaries preserve connection, timing, gating, reset, and power evidence.
- Dedicated-source rendering requires a real parent-section reference. OCR numbered-list labels are retained only as neutral unheaded source context, preventing false DRS navigation paragraphs.
- GUI now provides persistent Architecture Map Review access before, during, and after Stage 2. The dialog opens mapping-preview CSV/Markdown artifacts, supports Excel launch, shows live `review_decision` counts, and shows the recorded Stage 2A approval decision/reviewer.
- GUI review readability and visibility: fonts are enlarged across controls/viewers/tables/chat/logs/diagram; Architecture Map Review and `S5 after S2a (Req-only)` are on a second visible action row; every stage box opens a hover popup with its purpose or the captured failure reason.
- Validation: Stage 1 RAG crosscheck PASS (189 requirements; 0 RAG/rule failures); Stage 3 SRS flow PASS; Stage 4 skip and gate PASS; Stage 5 DRS flow and gate PASS. Pandoc remains unavailable, so DOCX conversion is skipped.

## 2026-08-28 - Ontology-Driven Mapping And Independent Post-Mapping Check
- Added project-agnostic `config/ontology_role_taxonomy.json` containing reusable mixed-signal role categories; it is a discovery vocabulary, not asserted source truth.
- Updated `.github/agents/ontological-spec-analyzer.agent.md` to require the ordered sequence: ontology analysis, generic role assignment, then requirement mapping through relationships and function/property evidence.
- Updated `scripts/generate_stage0_ontology_outputs.py` to generate `artifacts/stage0_ontology/ontology_requirement_links.csv` with source requirement ID, role, relation type, related roles, function/property evidence, source locator, and confidence.
- Updated `scripts/run_stage2_micro_arch_and_crosscheck.py` to require ontology links and use semantic compatibility between link evidence and configured block Function/Inputs/Outputs before lexical fallback.
- Added independent `scripts/validate_stage2_mapping.py`; it checks final Stage 2A requirement-to-block mappings against Stage 1 requirements, ontology links, block inventory, and interaction evidence. Matrix IDs use exact interaction evidence; explicit source ownership and configured role aliases are accepted generic evidence.
- Wired the post-mapping checker into Stage 2A generation and `scripts/validate_stage2_micro_arc_gate.py`; added `stage2_mapping_crosscheck_report.md` to required outputs and updated README/runbooks/orchestration docs.
- Replaced workflow CLI retry-capable stage helper with a structural one-run/one-validator path in `scripts/workflow_cli.py`; updated forward-only governance documentation.
- Initial post-mapping threshold was too strict for requirements with explicit source ownership but sparse lexical overlap; corrected it by accepting validated source ownership and ontology role/alias evidence while retaining semantic checks for unsupported mappings.
- Validation: Stage 0 PASS, Stage 2A profile crosscheck PASS, post-mapping semantic crosscheck PASS, Stage 2A gate PASS. Full downstream validator sequence had passed before the latest Stage 2A-only integration; regenerate Stages 3-5 after future Stage 2A mapping changes. Pandoc unavailable, so DOCX conversion remains skipped.

## 2026-08-28 Follow-up - Stage 2A Matrix And Downstream Context Fixes
- Added project-agnostic `scripts/validate_stage2_profile.py`, wired before Stage 2A matrix generation and into the Stage 2A gate. It compares the runtime profile with `artifacts/stage1_requirements/source_matrix_edges.csv`, checks source-ID coverage/uniqueness, and rejects endpoint mismatches. Negative test confirmed `DDS_STBIO1_0211: SENSOR HUB -> ISPU` is rejected.
- Corrected the source-backed profile mapping for `DDS_STBIO1_0211` to `SENSOR HUB -> FIFO`; regenerated Stage 2A and downstream artifacts.
- Restored tagged structural table-ID extraction for the source XBAR connection matrix while excluding standalone tagged `[ID] Requirement:` anchors from table recovery. This restored matrix IDs such as `DDS_STBIO1_0201`, `DDS_STBIO1_0202`, and `DDS_STBIO1_0219` without reintroducing duplicate-ID false positives.
- Normalized removable inline source-ID markers and empty brackets in shared source-content comparison; SRS continues to keep upstream IDs in `Covers:`.
- Removed legacy reset/clock exclusions from SRS retained-context rendering so Stage 2A `Unassigned` rows remain under their source-parent context.
- Validation: Stage 1 PASS with 189 tagged requirements and zero duplicate-report rows; Stage 2 and Stage 2A PASS with zero uncovered requirements; Stage 3 SRS PASS; Stage 4 ARS PASS; Stage 5 DRS PASS. Pandoc unavailable, so DOCX conversion was skipped.

## 2026-08-28 Checkpoint - Strict Forward Pipeline And Ownership Authority
- Added strict forward-only workflow execution in `scripts/workflow_cli.py`: runs may execute one stage or an ascending contiguous range from any stage within `0 -> 1 -> 2 -> 2A -> 3 -> 4 -> 5`, execute each selected stage once, validate after each stage, and stop on the first failure. Removed retry controls; the Stage 2A-to-DRS requirements-only shortcut remains as an approved forward path.
- Updated SRS generation so Stage 2A mappings are consumed without downstream ownership remapping.
- Updated SRS crosschecking so every SRS source ID must match the Stage 2A owner set exactly; `Unassigned` cannot become a concrete SRS block and no lexical/source-section exceptions are allowed.
- Stage 1 duplicate-ID logic now ignores OCR continuation and embedded-marker artifacts while stopping on substantive duplicate definitions. Corrected source validation produced an empty duplicate report, Stage 1 generation PASS, and Gate 1 PASS with 151 tagged requirements.
- Updated project instructions, workflow skill, README, CLI quick card, orchestration specification, and workflow diagram to remove retry/loop/backward guidance and document terminal STOP behavior.
- Validation: workflow dry-run confirmed canonical order and one attempt per stage; nonzero starts and `retry` are rejected; forward DRS shortcut passes; edited Python scripts compile.
- Current blocker: Stage 2A regeneration fails on pre-existing interaction-matrix rows with `source='unknown'` for `DDS_STBIO1_0201`, `DDS_STBIO1_0202`, `DDS_STBIO1_0219`, and related IDs. Downstream regeneration must wait until Stage 2A evidence is corrected.

## 2026-08-27 Checkpoint - Editable DRS Tables
- OTP I/O and PAD MUX TOP source evidence now render as native Markdown pipe tables, which Pandoc converts to editable Word `w:tbl` tables.
- DRS conversion retains visible table borders and validates the generated DOCX table structure when Pandoc is available.
- Full Stage 0-5 validation: PASS; local DOCX conversion remains skipped because Pandoc is unavailable.

## 2026-08-27 Checkpoint - DOCX-Ready DRS Source Tables
- Updated DRS source table rendering for compact OCR `Pin Name Function` rows and `Port name Direction Type Description` headers.
- OTP I/O List and PAD MUX TOP I/O List now emit native Markdown pipe tables suitable for editable DOCX conversion.
- Generic register-map exclusion remains active; no project-specific exceptions were added.
- Full Stage 0-5 validation: PASS. Pandoc unavailable, so DOCX output remains ungenerated locally.

## 2026-08-27 Checkpoint - Register Table Exclusion
- Added a generic OCR-tolerant DRS source-evidence filter for tagged register-map definitions and tables.
- The filter recognizes `regbank`, `register map`, or register-table column evidence and excludes the full definition/table block from generated DRS content.
- Confirmed no `DDS_STBIO1_0013`, `regbank`, `Register Title`, or `OTP_PDN` in generated SRS, ARS, or DRS specifications.
- Full Stage 0-5 workflow validation: PASS.

## 2026-08-27 Checkpoint - Cross-Page Tagged Requirement Continuation
- Fixed Stage 1 tagged extraction to continue across OCR pages and stop at the next tagged requirement or next numbered structural heading.
- `DDS_STBIO1_0147` now preserves all continuation-page content: `CURR_SEL_TX_FRAME{n}` and `TX1_OUTAB_SEL_FRAME_{n}` through `TX4_OUTAB_SEL_FRAME_{n}`.
- Fixed generic Markdown formatting for Stage 1 output and wrapped list blocks; no project-specific exception was added.
- Regenerated Stage 2 through Stage 5 artifacts. Final full validation `python scripts/workflow_cli.py validate --all`: PASS.

## 2026-08-27 Checkpoint - Source Text Completeness
- Added generic normalization of the generated `:.` punctuation artifact in `scripts/traceability_content_checks.py`; `&nbsp;` normalization was already present.
- Regenerated DRS after SRS refresh. The DRS generator preserves technical register/signal names because only exact Stage 1 source IDs are sanitized.
- Final SRS, ARS, and DRS crosschecks: PASS.
- Verified `OTP_PRG10` in SRS/DRS and `PPG_ALC_CONFIG_PARAM_1` in SRS/DRS; `DDS_STBIO1_0147` content is complete.
- Pandoc remains unavailable, so DOCX generation was skipped.

## RESTORE CHECKPOINT - 2026-08-26 - Descriptive Table Exclusion
- Added the same generic `_is_non_normative_table_row` guard to `run_srs_gen_spec_agent.py`, `run_ars_gen_spec_agent.py`, and `run_drs_gen_spec_agent.py`.
- The guard excludes descriptive table evidence and malformed header-split table rows lacking an explicit `Requirement` marker before downstream authored IDs and traceability rows are created.
- It deliberately keeps normative rows and structural reset/clock-derived rows; it contains no project-specific names or IDs.
- Updated `.github/copilot-instructions.md` and `.github/skills/workflow-stage-gate/SKILL.md` with the project-agnostic policy.
- Focused check confirmed the selected non-normative row is excluded by all three generators.
- Stage 1, ARS, and DRS validations pass. SRS regeneration removes the unwanted row, but its crosscheck still reports existing duplicate connection-matrix SRS IDs unrelated to this change.
- Pandoc was unavailable; DOCX conversion remains unverified locally.

## RESTORE CHECKPOINT - 2026-08-26
- Restore from `local_memory/chat_handoff.md` and this activity log.
- Current validation: Stage 0, 1, 2, 2A, 3, 4, and 5 PASS using `C:\python\python39\python.exe scripts/workflow_cli.py validate --all`.
- Preserve Stage 1-only source reads and Stage 2+ artifact-only execution.
- Shared formatting validator: `scripts/validate_common_formatting.py`, called by every Stage 0-5 validator.
- Preserve source list order, numbered subsection boundaries, standard Markdown bullets, blank paragraph separation around authored headers and `Covers:`, native I/O/Parameter tables, and generic register-table exclusion.
- DRS DOCX conversion includes editable native Word table validation and visible borders; Pandoc remains unavailable locally, so actual DOCX output still requires a machine with Pandoc.
- First action in the next session: read the restore checkpoint, then run full validation before making further changes.

## Update Record (2026-08-26 - Shared Formatting, Source Tables, and DOCX)
- Added `scripts/validate_common_formatting.py` and wired it into the existing validators for Stage 0, 1, 2, 2A, 3, 4, and 5.
- Enforced generic Markdown formatting: final newline, authored-header separation, blank lines before generated lists, standard bullets, and visible spacing around authored headers and `Covers:`.
- Updated SRS/ARS/DRS renderers to preserve source list structure, numbered subsection markers, bullet order, and separate paragraphs. Fixed the SRS secondary source-body path that reintroduced Unicode bullets.
- DRS reconstructs reliable source I/O and parameter tables as native Markdown pipe tables; `Sensor Hub I/O List` and `ADSP Parameter Table` were verified after regeneration. Unreliable OCR uses fenced source evidence.
- Added generic register-table exclusion based on register caption/header terminology; register tables are not processed as I/O, parameter, or interface tables.
- DRS DOCX conversion adds visible borders to native Word tables and validates editable `w:tbl` elements. Pandoc was unavailable locally, so actual DOCX generation was skipped.
- Verified source-faithful DRS `DRS-REQ-178`: sections `5.1` through `5.4` and all bullet items remain in source order. Verified the visible spacer after `Covers: SRS-REQ-001` before `[DRS-REQ-103] Requirement:`.
- Final validation: `python scripts/workflow_cli.py validate --all` PASS for Stage 0, 1, 2, 2A, 3, 4, and 5; affected Python files compile successfully.

## Activities Completed
- Restored and validated stage-gated flow for Stage 0 through Stage 5.
- Executed deterministic taxonomy updates before Stage 1 full flows.
- Re-ran Stage 2 through Stage 5 full flow to refresh generated artifacts.
- Executed Stage 6 architecture comparisons against MEMS_3axis_gyro.

## Latest Verified Stage Status
- Stage 0: PASS (2026-08-10 21:52:56)
- Stage 1: PASS (2026-08-10 22:02:48)
- Stage 2: PASS (2026-08-10 22:05:49)
- Stage 2a: PASS (2026-08-10 22:05:50)
- Stage 3: PASS (2026-08-10 22:05:51)
- Stage 4: PASS (2026-08-10 22:05:52)
- Stage 5: PASS (2026-08-10 22:05:53)
- Stage 6: PASS across multiple runs on 2026-08-10 (project_to_compare=MEMS_3axis_gyro)

## Extraction and Traceability Metrics (Latest)
- Stage 1 extracted requirements: 303
- Domain split:
  - System: 65
  - Analog: 40
  - Digital: 198
- Stage 1 RAG text quality cross-check:
  - Corrected split/truncated: 3
  - Exact: 231
  - Warn: 63
  - Fail: 9
- Stage 2a micro-architecture:
  - Blocks: 12
  - Interfaces: 13
  - Requirement-to-block links: 303

## Stage 3/4/5 Snapshot
- Stage SRS report: pass, fully mapped to owning block=303.
- Stage ARS report: pass, generated ANA=39 and XDN=20, fully mapped=59.
- Stage DRS report: pass, generated DIG=254 and XDN=9, fully mapped=263.

## Workflow History Notes
- workflow_cli run history confirms consistent PASS runs across Stage 0..5 on 2026-07-24 and 2026-08-10.
- One transient Stage 3 runner failure occurred on 2026-08-10 20:16:38 and was resolved by the later successful full rerun sequence.

## Reusable Lessons
- Keep Stage 1 as the only direct source-spec read stage.
- Keep Stage 2+ artifact-driven and protected by guard_stage2_plus_spec_independence.py.
- Run taxonomy update before Stage 1 when source-derived context changes.
- Run full stage gate scripts (not standalone generators) when validating release-ready artifacts.

## Fast Resume Commands
1. python scripts/run_stage0_gate0.py
2. python scripts/run_stage1_requirements_gate1.py
3. python scripts/run_stage1_specs_gate2.py
4. python scripts/run_stage2_micro_arc_gate.py
5. python scripts/run_stage3_srs_gate.py
6. python scripts/run_stage4_ars_gate.py
7. python scripts/run_stage5_drs_gate.py
8. Optional Stage 6: python scripts/workflow_cli.py arch-compare --project-to-compare MEMS_3axis_gyro

## Restoration Record
- Restored on 2026-08-11 from STBIO_AI artifacts/orchestrator results and workflow_cli_runs.jsonl.

## Update Record (2026-08-11)
- Stage1 Req-ID extraction was hardened for tagged source mode with table-aware detection.
- Added robust Req-ID header variant handling for tables, including Req_id, REQ_ID, Req ID, ID, and fallback variants.
- Added custom family Req-ID detection for tokens like DDS_STBIO1_XXXXX across OCR lines, including non-bracketed cases.
- Added strict rule checks so tagged mode fails when generated_standard IDs appear or source_req_id is missing.
- Added table line trace metadata in notes via table_line_info=pageX:lines[...].
- Fixed cross-row contamination for table Req-ID rows:
  - Explicit Req-ID rows no longer borrow forward/next-row text.
  - Standalone Req-ID lines now resolve context from previous lines only, preserving same logical row.
  - Compact table-ID fallback path also enforces same-row behavior and avoids multi-line forward stitching.
- Current expected behavior for register-map rows:
  - Rows like DDS_STBIO1_3002 are extracted directly from their own line when content exists.
  - Standalone ID rows like DDS_STBIO1_3000/3001/3003+ use backward row context only, never next-row context.

## Update Record (2026-08-19)
- Gate and stage-flow integrity:
  - Hardened Stage 0/1/2/2a validators against stale or inconsistent evidence and false PASS conditions.
  - Restored Stage 2a pass by correcting requirement-to-block coverage behavior and aligning validator checks to emitted `Decision: go` evidence.
  - Kept Stage 1 as the sole direct source-spec read stage; Stage 2+ remains artifact-driven under `scripts/guard_stage2_plus_spec_independence.py`.
- Workflow presentation:
  - Updated workflow presentation generator/output with latest stage wording and a GUI description slide.
- GUI updates in `scripts/workflow_gui.py`:
  - Added Work Area navigator plus read-only open-file viewer.
  - Added strongly visible horizontal scrollbars in navigation, open-file viewer, CSV viewer, workflow_cli Runs controls, compact workflow diagram, chat/log areas, and related tool windows.
  - Added CSV table rendering similar to Excel, including row stripes and scrollbars.
  - Restored `requirements_summary.csv` right-click popup for ID counts.
  - Added extension-aware text highlighting and Markdown internal jumps for both generated slugs and explicit `{#anchor}` headings.
  - Added Ctrl+F find bar for open files with text-match highlighting, CSV row search, Next/Prev buttons, Enter/Shift+Enter navigation, and Escape/Close behavior.
  - Added S5 dual connection display in compact workflow diagram: `S4 -> S5` and req-only `S2a -> S5`.
  - Added graceful GUI Ctrl+C handling.
- SRS/ARS/DRS authored requirement format:
  - Canonical authored-entry header is now `[SRS-REQ-xxx] Requirement:`, `[ARS-REQ-xxx] Requirement:`, `[DRS-REQ-xxx] Requirement:`.
  - Removed old emitted format `Requirement ID: *RS-REQ-###` from generators and regenerated artifacts.
  - Updated SRS/ARS/DRS generators, crosscheck scripts, stage validators, gen-agent files, and templates to enforce/describe bracketed headers.
  - Crosschecks and gate validators now reject the deprecated `Requirement ID: SRS-REQ-###`, `Requirement ID: ARS-REQ-###`, and `Requirement ID: DRS-REQ-###` forms.
- Regenerated artifacts and validation:
  - Stage 3 SRS run: PASS; generated 203 requirements; traceability mapped 203; unassigned 0.
  - Stage 4 ARS run: PASS; generated 10 requirements; traceability mapped 10; unassigned 0.
  - Stage 5 DRS run: PASS; generated 200 requirements; traceability mapped 200; unassigned 0.
  - Final grep confirmed old `Requirement ID: *RS-REQ-###` artifact form is absent and bracketed headers are present.
  - Python compile passed for modified GUI, generator, crosscheck, and validator scripts.
  - VS Code diagnostics reported no errors for touched files.
  - Pandoc remains unavailable, so DOCX conversion is skipped during SRS/ARS/DRS runs.

## Active Resume Notes (2026-08-19)
- Primary GUI file: `scripts/workflow_gui.py`.
- Primary generation/check files for requirement header format:
  - `scripts/run_srs_gen_spec_agent.py`, `scripts/run_ars_gen_spec_agent.py`, `scripts/run_drs_gen_spec_agent.py`
  - `scripts/run_srs_crosscheck_agent.py`, `scripts/run_ars_crosscheck_agent.py`, `scripts/run_drs_crosscheck_agent.py`
  - `scripts/validate_stage3_srs_gate.py`, `scripts/validate_stage4_ars_gate.py`, `scripts/validate_stage5_drs_gate.py`
  - `.github/agents/*_gen_spec.agent.md`, `.github/agents/*-crosscheck.agent.md`, `templates/*RS_gen_AI_template_prompt.md`
- Use `python scripts/workflow_cli.py run --stage 3`, `--stage 4`, and `--stage 5` after any future format-policy changes.

## Update Record (2026-08-19 - Latest)
- Requirement fidelity:
  - Removed the legacy authored `Statement:` line from SRS/ARS/DRS requirement blocks.
  - Kept upstream requirement IDs exclusively in `Covers:` and removed them from authored prose.
  - Preserved multiline source bullet lists as a single requirement through Stage 1, SRS, ARS, and DRS.
- Validation policy:
  - Updated SRS/ARS/DRS crosschecks and Stage 3/4/5 gates to parse direct multiline authored statements, require `Covers:`, reject authored `Statement:`, and detect upstream-ID leakage.
- Architecture naming:
  - Replaced generic Stage 2 profile names with project-specific names derived from the architecture evidence and inventory.
  - Updated generators, agent instructions, templates, and `.github/copilot-instructions.md` to resolve names from the runtime Stage 2 inventory; illustrative examples are not fixed names.
- Diagram parity:
  - Updated `artifacts/stage2_mirco_arc/micro_architecture_block_diagram.mmd` and `micro_architecture_block_diagram.md` to match the current project-specific inventory and interaction matrix.
  - Removed stale generic nodes and labels.
- Regeneration result:
  - Re-ran the dependent Stage 2, Stage 3, Stage 4, and Stage 5 workflows; micro-architecture and SRS/ARS/DRS crosschecks and gates passed with complete mapping.
  - Python compilation and VS Code diagnostics passed for touched scripts/files.
  - Pandoc is unavailable; DOCX outputs remain intentionally skipped.

## Active Resume Notes (latest)
- Architecture source of truth: `artifacts/stage2_mirco_arc/block_inventory.csv` plus the Stage 2 profile and interaction matrix.
- Diagram files: `artifacts/stage2_mirco_arc/micro_architecture_block_diagram.mmd` and `.md`.
- Before changing spec format or architecture naming, update the owning generator/profile and then rerun the relevant crosscheck and gate scripts.

## Update Record (2026-08-19 - Generic Name Crosscheck)
- Cross-checked Stage 2 architecture results, Stage 3/4/5 outputs, orchestrator reports, and docs for generic block names.
- Removed unsupported `Analog Front End` from the Stage 2 profile and regenerated architecture artifacts. Its occurrence in the source overview is a product/device description, not a block definition.
- Synchronized both micro-architecture diagram files to the current interaction matrix and removed stale `DCTRL`, `PWR`, and `CAL` nodes/edges.
- Confirmed no forbidden generic names (`BufferingBlock`, `SensorInputBlock`, `ControlProcessingBlock`, `SamplingInterfaceBlock`) remain in generated architecture/spec results or next-step documentation.
- Validation: Stage 2 and Stage 3 full flows PASS; SRS traceability 205/205 mapped; DOCX remains skipped because Pandoc is unavailable.

## Update Record (2026-08-19 - Connection-Matrix IDs and Ownership Fix)
- Fixed Stage 2 ownership precedence to avoid ADC misassignment:
  - ADC mapping now requires explicit ADC evidence.
  - ADSP remains owner for DSP-oriented rows unless ADC evidence is explicit.
- Updated Stage 2 interaction-matrix generation to persist `Requirement IDs` in `artifacts/stage2_mirco_arc/interaction_matrix.csv`.
- Backfilled missing connection-matrix requirement ID `DDS_STBIO1_0222` for `ISPU -> FIFO` in matrix/profile-driven outputs.
- Extended SRS generation to produce explicit connection-matrix-derived requirements from interaction rows carrying IDs.
- Updated common governance to generic terminology:
  - Replaced `XBAR`-specific wording with `connection matrix` wording in `.github/copilot-instructions.md` and `.github/skills/workflow-stage-gate/SKILL.md`.
  - Verified no remaining `XBAR|xbar` tokens in those shared rule files.
- Validation summary:
  - Stage 2 gate PASS after ownership and matrix-ID updates.
  - Stage 3/4/5 passes confirm traceability propagation into SRS/ARS/DRS.

## Update Record (2026-08-19 - Connection Matrix Contract and Block Functions)
- Connection-matrix downstream contract:
  - SRS creates authored `SRS-REQ` entries for populated matrix cells.
  - ARS/DRS matrix-derived requirements use the owning source-row block and cover the corresponding authored SRS matrix ID, not a raw Stage 1 ID.
  - DRS renders each matrix requirement as an explicit connection to the destination block; generic or unrelated source text is not acceptable.
  - Governance in `.github/copilot-instructions.md`, stage-gate skill, generator agents, and ARS/DRS crosscheck agents now records this policy.
- Block-inventory audit and regeneration:
  - `config/stage2_mirco_arc_profile.json` is the curated source of `block_inventory.csv` Function, Inputs, and Outputs values.
  - Reviewed all real blocks against Stage 1 evidence. Material corrections include Sensor-Hub as an external-target I2C master, Smart FIFO as a Unique/Multiple-mode AHB/memory FIFO, BIST Controller as BIST plus ADC/OTP test control, and I2C_SPI_AHB as the serial-to-AHB bridge.
  - PMU function is source-grounded: POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clock sequencing, clock-ready signaling, and digital-reset release for boot and power modes.
  - PMU interfaces: inputs are supplies, POR, clock references/start requests, and power-mode configuration; outputs are LDO/power controls, clock enable/ready signals, reset release, and power-state status.
- Renderer root cause and fix:
  - SRS, ARS, and DRS read `Function` from Stage 2 inventory but previously generated their general descriptions from noisy linked-requirement text instead.
  - All three generators now treat the curated inventory Function as authoritative and use requirement synthesis only as a legacy fallback.
- Validation after regeneration:
  - Stage 2 micro-architecture crosscheck: 205 requirements analyzed, 0 uncovered, recommendation `go`.
  - Stage 3 SRS, Stage 4 ARS, and Stage 5 DRS gates: PASS.
  - Diagnostics reported no errors in the modified profile and SRS/ARS/DRS generator scripts.

## Update Record (2026-08-20 - Function-Only Ownership and Project-Agnostic Rules)
- Removed the DRS-specific `[TO: IPOS_PMU]` regex and PMU/source-heading owner heuristics. Source tags and source sections are no longer ownership shortcuts.
- Hardened DRS owner resolution so Stage 2 traceability supplies candidates only; each retained owner must be supported by the matching `block_inventory.csv` `Function`. Unsupported mappings become `Unassigned`.
- Added equivalent Function-only checks to `run_srs_crosscheck_agent.py`, `run_ars_crosscheck_agent.py`, and `run_drs_crosscheck_agent.py`:
  - inventory Functions must be non-empty;
  - generated block descriptions must exactly match inventory Functions;
  - traceability owners must exist in the inventory;
  - non-matrix requirement behavior must be supported by the owner's Function;
  - matrix-derived requirements remain governed by the interaction-matrix source-row rule.
- ARS/DRS crosschecker classification now uses Function text only, excluding inputs, outputs, interfaces, and linked requirements.
- Removed project-specific identifiers/examples from reusable SRS/ARS/DRS generators and agent instructions. DOCX templates are explicit optional runtime inputs.
- Updated common governance and workflow-stage rules to make Function-only ownership and project-agnostic reusable content mandatory.
- Validation: all six modified Python files compile and report no VS Code diagnostics; project-specific literal scans are clean. Current SRS/ARS/DRS crosschecks fail on stale generated artifacts with unsupported/unassigned mappings, as intended; downstream regeneration is the next action.

## Update Record (2026-08-20 - Stage 3 Function Filtering)
- Root cause of the Stage 3 gate failure: SRS generation copied broad Stage 2 `Block(s)` mappings directly into traceability, while the new crosschecker correctly required non-matrix ownership support from inventory `Function` fields.
- Fixed `scripts/run_srs_gen_spec_agent.py` to filter non-matrix owners through current `block_inventory.csv` Functions before writing SRS traceability and block sections. Matrix-derived requirements retain their interaction-matrix source-row path.
- Validation: `python scripts/run_stage3_srs_gate.py` PASS end to end. SRS generated 205 requirements, mapped 181, left 24 unsupported requirements explicitly unassigned, and passed SRS, LaTeX, and Stage 3 gate checks. Pandoc remains unavailable, so DOCX export was skipped.

## Update Record (2026-08-20 - ARS/DRS Function-Only Gate Fix)
- ARS reproduced the same broad-owner problem and contained project-specific fallback ownership names. Removed the fallback and filtered non-matrix ARS owners through inventory Functions; explicit `Unassigned` results are retained for unsupported mappings.
- DRS still classified `Main Controller` as analog because its generator used inputs, outputs, interfaces, and linked requirements in block classification. SRS, ARS, and DRS generator classification is now Function-only, matching the crosscheckers.
- ARS/DRS crosschecks now skip explicit `Unassigned` rows when checking named block validity, while still reporting unassigned counts in stage reports. Unsupported named owners remain blocking findings.
- Validation: Stage 3 SRS PASS, Stage 4 ARS PASS, Stage 5 DRS PASS. DRS generated 203 requirements with 173 mapped and 30 unassigned; ARS generated 3 requirements with all 3 mapped. All six generators/crosscheckers compile and report no diagnostics. No project-specific fallback identifiers remain in the reusable scripts.

## Update Record (2026-08-20 - Consolidated New-Chat Restore Point)
- Saved all fixes from today into `local_memory/chat_handoff.md` and this activity log.
- Architecture authority: current Stage 2 profile and `block_inventory.csv` Function fields.
- Downstream ownership: non-matrix requirements require Function support; broad Stage 2 mappings are candidates only; unsupported requirements remain `Unassigned`.
- Removed project-specific ownership logic: `[TO: IPOS_PMU]`, PMU/source-heading heuristics, ARS fallback owner names, fixed project identifiers/examples, and fixed DOCX template default.
- SRS/ARS/DRS descriptions and block classification are Function-only. Crosscheckers validate exact descriptions, non-empty Functions, known owners, Function support, and matrix source-row exceptions.
- Today’s final gate results: Stage 3 SRS PASS (205 generated, 181 mapped, 24 unassigned), Stage 4 ARS PASS (3 generated, 3 mapped), Stage 5 DRS PASS (203 generated, 173 mapped, 30 unassigned). LaTeX crosscheck PASS. Compilation and diagnostics PASS. Pandoc unavailable, DOCX skipped.
- New chat should load both local memory files and use the bootstrap prompt at the end of `chat_handoff.md`.

## Restored Checkpoint (2026-08-20)
- Recovered local-memory context from `chat_handoff.md`, the Stage 3/4/5 result artifacts, and the current stage reports.
- Digital taxonomy precedence is active: protocol/bus and processor terms are authoritative digital indicators; mixed-signal context does not override them.
- Latest result files verify Stage 3 PASS at 16:12:36, Stage 4 PASS at 12:17:59, and Stage 5 PASS at 12:18:03.
- Current report metrics: SRS 189 generated (170 mapped, 19 unassigned); ARS 3 generated (3 mapped, 0 unassigned); DRS 187 generated (168 mapped, 19 unassigned). All reports show a Stage 2 crosscheck decision of `go` and no blocking issues.
- Pandoc remains unavailable; DOCX conversion is intentionally skipped.

## Update Record (2026-08-20 - Reset/Clock Provenance and SRS/DRS ID Namespaces)
- Added structural Stage 1 extraction for reset/clock table rows, including exact source-table hierarchy paths, source/destination signals, operations, optional frequency/F max values, `derivation_kind`, and `table_line_info` provenance.
- Added the reset/clock structural-derivation exception to RAG crosschecking so table-derived statements are not incorrectly rejected for low lexical overlap.
- Preserved original table requirement IDs as upstream coverage IDs. Downstream authored IDs are now artifact-specific: SRS traceability uses `SRS-REQ-###`; DRS traceability uses `DRS-REQ-###`.
- Updated `scripts/run_srs_gen_spec_agent.py` and `scripts/run_drs_gen_spec_agent.py` to generate those namespaces in their traceability matrices. Updated DRS numbering-convention text accordingly.
- Verified reset requirement `DDS_STBIO1_1053`: SRS row `SRS-REQ-048`; DRS row `DRS-REQ-047`; both preserve the exact `resetn_fifo` to `HRESETn` hierarchy path and cover the original ID.
- Validation: Python compilation passed; Stage 3 SRS full flow and gate PASS (185 generated, 181 mapped, 4 unassigned); Stage 5 DRS full flow and gate PASS (183 generated, 165 mapped, 18 unassigned); no `DIG-RQ-` entries remain in SRS/DRS traceability matrices. Pandoc unavailable, DOCX skipped.
- Remaining quality note: broad Stage 2 ownership can still cause a reset-derived Markdown statement to appear under multiple blocks; this does not alter source coverage or authored ID namespaces and should be resolved with deterministic single-owner selection in a later pass.

## Restore Record (2026-08-21 - Local Memory and Chat Handoff)
- Restored `local_memory/chat_handoff.md` and this activity log from the current local-memory files plus DDS_STBIO1 artifacts.
- Confirmed active environment file still points at `specs/DDS_STBIO1.pdf`, `artifacts/rag_DDS_STBIO1/rag_index.sqlite`, and the Stage 1-only source-read / Stage 2+ artifact-only contract.
- Confirmed current Stage 1 artifacts: 185 requirements, coverage crosscheck pass, tagged-preserve rows 185, generated-standard rows 0, RAG exact 178, RAG warn 7, RAG fail 0, rule-check fail 0.
- Confirmed current Stage 2a artifacts: 185 requirements analyzed, 14 blocks with assigned requirements, 0 potentially unassigned, architecture crosscheck decision `go`, blocking findings none.
- Confirmed latest orchestrator pass records on 2026-08-20: Stage 0/1/2/2a PASS at 17:52-17:53, Stage 3 PASS at 17:53:14, Stage 4 PASS at 17:58:56, Stage 5 PASS at 17:59:01.
- Preserved the Function-only downstream ownership rule, matrix source-row exception, structural reset/clock provenance rule, authored bracketed requirement headers, and artifact-specific SRS/ARS/DRS ID namespaces.
- Refreshed the new-chat bootstrap prompt in `chat_handoff.md` so future sessions resume from this restore checkpoint.

## Update Record (2026-08-21 - Reset/Clock Owner Cascade)
- Added reset/clock table-derived ownership exception to common Copilot instructions, workflow-stage-gate guidance, and SRS/ARS/DRS generation-agent instructions.
- Updated SRS/ARS/DRS generators to carry Stage 1 derivation metadata and assign reset/clock structural table rows to the current Stage 2 power/clock/reset owner, PMU for STBIO_AI.

## Update Record (2026-08-21 - Clock/Interrupt Table Rendering and Generic Generators)
- Stage 1 OCR/table extraction now carries reset/clock header context onto continuation pages that contain requirement-ID rows and generically recognizes dotted hierarchy paths without embedding a project path in code.
- Clock/reset structural statements preserve exact source/target paths, frequency, and gating. For `DDS_STBIO1_1024`, the regenerated statement contains the source/target paths, `16 MHz`, and the extracted non-`No` clock-gating condition.
- Interrupt structural rendering was corrected from `... <Description> label to <bit>` to the mandatory `... <Description> to bit <bit>` form. SRS now propagates the corrected statements for the interrupt table rows.
- Removed fixed controller aliases and exact PMU-name owner shortcuts from reusable SRS/ARS/DRS generator scripts. Removed stale alias-initializer calls from SRS and DRS entrypoints; all project values are read from runtime artifacts.
- Validation: Stage 1 generation PASS; Stage 3 SRS full flow/gate PASS; Python compilation and VS Code diagnostics PASS for touched generators. DRS regenerated with the corrected clock statement, but its Gate 5 crosscheck reports unrelated unmapped IDs `DDS_STBIO1_0201`, `DDS_STBIO1_0202`, `DDS_STBIO1_0211`, and `DDS_STBIO1_0219`.
- Updated SRS/ARS/DRS crosscheckers to validate the same exception without weakening Function-only checks for ordinary non-matrix requirements.
- Updated SRS/DRS block grouping so reset table rows render under PMU and do not appear in residual unmapped sections.
- Validation: Python compilation passed; Stage 3 SRS, Stage 4 ARS, and Stage 5 DRS gates all PASS. SRS and DRS traceability map `DDS_STBIO1_1050`, `DDS_STBIO1_1051`, `DDS_STBIO1_1052`, `DDS_STBIO1_2053`, and `DDS_STBIO1_1053` to PMU.

## Update Record (2026-08-21 - Reset/Clock Statement Wording Propagation)
- Reloaded user-updated Copilot instructions and workflow-stage-gate reset/clock rules.
- Updated Stage 1 reset/clock table derivation to emit `The <source> signal shall be connected to the <destination> signal`, with optional frequency/F max and clock-gating text carried when present.
- Updated SRS/DRS generation agents and script rendering so reset/clock structural rows use the new signal wording in generated specs.

## Update Record (2026-08-21 - Centralized SRS/ARS/DRS Authored-ID Policy)
- Clarified the shared authored-ID policy in `.github/copilot-instructions.md` and `.github/skills/workflow-stage-gate/SKILL.md`: SRS, ARS, and DRS authored IDs use exactly three decimal digits (`001`-`999`) in artifact-local namespaces.
- Removed duplicated ID-format rules from `.github/agents/srs_gen_spec.agent.md`, `ars_gen_spec.agent.md`, `drs_gen_spec.agent.md`, and the corresponding crosscheck agent files. Local agents now refer to the shared policy.
- Tightened SRS/ARS/DRS generators, crosscheckers, and Stage 3/4/5 validators from variable-width digit matching to `REQ-\d{3}` matching.
- Regenerated artifacts and verified full flow: Stage 3 SRS PASS, Stage 4 ARS PASS, Stage 5 DRS PASS. No permissive variable-width ID regex remains in the scripts; modified-script diagnostics are clean.
- Pandoc remains unavailable, so DOCX outputs are skipped; Markdown, CSV, crosschecks, and gates are passing.
- Regenerated Stage 1, Stage 3 SRS, and Stage 5 DRS; Stage 3 and Stage 5 gates PASS. The Stage 2 gate command did not refresh its result artifact in the current terminal, so SRS/DRS validation used refreshed Stage 1 plus current Stage 2 inventory.
- Verified the five STBIO_AI reset-derived rows map to PMU in SRS/DRS traceability and render under PMU with the updated signal wording.

## Update Record (2026-08-21 - Compact Reset/Clock and Interrupt Rule Patch)
- Removed the invented `without clock gating` fallback from Stage 1, SRS, and DRS reset/clock rendering. Clock-gating text is emitted only when present in source table evidence.
- Added Stage 1 interrupt table derivation using only `Interrupt`, `bit`, and `Description` row content and preserving the original table requirement ID in traceability.
- Added structural interrupt-table handling to Stage 1 RAG crosscheck and SRS/DRS ownership checks; STBIO_AI interrupt-derived rows route to `IRQ logic`.
- Fixed interrupt row collection so `[END]` and following description tags are not absorbed into the derived `irq_timer` row.
- Validation: `py_compile` passed; direct Stage 1 generation PASS; Stage 1 RAG/coverage/gate PASS; Stage 3 SRS gate PASS; Stage 5 DRS gate PASS. Exact checks found no generated `without clock gating` or `clock_gating=not_present` strings.

## Restore Record (2026-08-21 - Local Memory + Chat Handoff)
- Executed restore request from the active STBIO_AI workspace.
- Verified local memory files present: `local_memory/chat_handoff.md`, `local_memory/project_activity_log.md`, `local_memory/environment.md`, `local_memory/sync_manifest.json`.
- Re-synced local memory manifest via `python scripts/sync_repo_memory_local.py`; result: `Memory sync: PASS (local files=3)`.
- No policy changes were introduced during restore; the restore state remains aligned with the latest local-memory checkpoint flow.

## Update Record (2026-08-27 - DCC Enumeration Exclusion and Traceability Repair)
- Fixed the root Stage 1 issue in `scripts/generate_stage1_requirements.py`: non-normative encoded-value/table enumerations are filtered before tagged DDS records are emitted. `DDS_STBIO1_395` no longer enters the Stage 1 catalog or downstream SRS/ARS/DRS traceability.
- Do not create DCC image-derived requirements from partial OCR, page proximity, or unreadable diagrams. Wait for a readable rendered image with complete function names and relationships; record image provenance and do not invent DDS links unless the image explicitly provides them.
- Refreshed dependent artifacts after the Stage 1 correction. Final status: Stage 1 PASS (185 tagged, 0 generated), Stage 2 PASS, Stage 2A PASS (185 analyzed, 0 uncovered, `go`), Stage 3 PASS (142 generated), Stage 4 PASS, Stage 5 PASS. Source-keyed DRS-to-SRS coverage passes.
- Confirmed the corrected mapping: `SRS-REQ-042` and the corresponding DRS row cover `DDS_STBIO1_0014`; the old shifted association must not be restored.
- Continue enforcing Stage 1-only source reads, Stage 2+ artifact-only execution, Function-only non-matrix ownership, matrix source-row ownership, and explicit `Unassigned` for unsupported mappings.
- Pandoc and a usable PDF renderer remain unavailable. DOCX regeneration/visual verification and DCC image inspection are pending external tooling or a readable rendered source image.

## Next Chat Bootstrap Prompt
"Load `STBIO_AI/local_memory/chat_handoff.md` and `STBIO_AI/local_memory/project_activity_log.md`. Restore the 2026-08-27 DCC enumeration exclusion checkpoint. Keep `DDS_STBIO1_395` excluded, do not infer DCC behavior or DDS relationships from partial OCR/unreadable images, and require complete readable image labels plus explicit provenance for any future image-derived requirements. Preserve Stage 1-only source reads, Stage 2+ artifact-only execution, Function-only ownership, matrix source-row ownership, artifact-local SRS/ARS/DRS IDs, and source-keyed DRS-to-SRS validation. Run the full Stage 0-5 validation before further changes; DOCX/PDF rendering remains unavailable locally."

## Update Record (2026-08-27 - Project-Agnostic Spec Generation)
- Confirmed SRS, ARS, and DRS generators already load `project_name` from the common `config/project_context.json` and pass it into document rendering.
- Removed the remaining hard-coded `STBIO` example from `templates/SRS_gen_AI_template_prompt.md`; reusable SRS/ARS/DRS generation surfaces now contain no `STBIO` or `DDS_STBIO` literals.
- New projects should initialize `project_name` in their own common project-context file. Keep project names out of reusable generators, agent instructions, and templates.
- Added common config fields `ars_document_author` and `drs_document_author`, initialized to `ARS Gen Spec Agent` and `DRS Gen Spec Agent`; the ARS and DRS generators now read these dedicated fields.
