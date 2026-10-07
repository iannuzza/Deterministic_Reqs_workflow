---
name: workflow-stage-gate
description: "Run and control a project-independent staged requirements/specification workflow with strict gate criteria, required artifacts, crosscheck routing, source-table classification, architecture evidence rules, and strict forward-only execution. Use when orchestrating stage flow, deciding gate pass/fail, handling Stage 1 extraction, Stage 2 architecture evidence, SRS/ARS/DRS generation, or enforcing fail-stop execution."
---

# Workflow Stage-Gate Execution Skill

Use this skill as the canonical execution contract for stage orchestration.

## Objective

- Execute the strengthened workflow from S0 through Stage 7 deterministically.
- Treat `data/canonical/canonical_store.sqlite` as authoritative for requirements,
  revisions, provenance, mappings, workflow state, profiles, snapshots, audit, and rollback.
- Treat canonical SQLite as the only authoritative workflow store. Keep retrieval/index SQLite
  databases separate, rebuildable, and derived only. Treat CSV, JSON, Markdown, XLSX, and SysML
  as derived exports, review artifacts, or compatibility outputs only.
- SQLite/FTS5 is the current default local retrieval backend, not permanent workflow truth.
  Authoritative workflow code must not depend directly on retrieval table schemas, FTS5 syntax,
  query helpers, or index-specific internals; use a bounded retrieval interface and preserve
  source evidence/provenance independently.
- Use the centralized approved vocabulary as the lexical authority. Domain vocabulary, aliases,
  stopwords, and expansions must resolve from and remain aligned with approved vocabulary/profile
  context; local duplicated lexical resources are not authoritative.
- The authoritative workflow is deterministic and local-only. It must not require LLM calls,
  network access, cloud services, remote model downloads, or generative retrieval/mapping.
- Downstream generation, reports, SysML, and authoritative GUI actions must consume one approved
  immutable snapshot through the approved resolver. GUI display and chat remain non-authoritative.
- The local process username may be used only for non-authoritative audit/log actor fields and generated-document metadata. Generated specifications must render `Author <runtime-user>` immediately after `Snapshot ID` on the first page. It must not select or modify snapshot, allocation, ownership, partition, traceability, approval, or explicit reviewer authority.
- Every generated specification must render the immutable snapshot ID actually resolved for that run. If that snapshot differs from the existing generated document, increment the Version history value deterministically (`major.minor` -> `major.(minor+1)`); keep the existing version when the snapshot is unchanged. This metadata rule must not change requirement, allocation, ownership, traceability, or approval authority.

## Downstream Traceability And SysML Phase Contract

- `templates/MPT_IPOS_template.docx` is an IPOS presentation/layout and document-structure reference only. It may supply geometry, section setup, title/heading presentation, headers/footers, table rendering, theme, and general DOCX presentation. Generated Markdown remains the sole IPOS content source. Template body/sample content and the `STReq`, `STMacroReq`, and `NoSpacing` requirement-style chain are non-authoritative and must not leak into generated IPOS output.
- The IPOS generator and shared DOCX formatter own authored requirement formatting and content, including exact requirement text, `Covers:`, `[End]`, spacing, navigation order, page numbering, and final layout normalization. This is a shared rule, not a project-specific styling exception.

- All SRS, ARS, DRS, and IPOS DOCX conversion paths must reuse the shared
  `apply_docx_common_spec_formatting` helper. The helper owns deterministic
  rendered layout only: title and metadata on page 1, TOC first on page 2,
  Document Navigation after the TOC, and a right-aligned PAGE field
  in the default footer. Layout validation must not become a second authority
  for synthesis, topic coherence, repeated requirements, traceability,
  allocation, ownership, or snapshot behavior.

- Stages 3 through 7 each run their normal generator and crosschecks, producing the stage-specific
  document, traceability matrix, reports, and deterministic coverage/statistics artifacts. Do not
  collapse these outputs into one later report or remove them from GUI/work-area visibility.
- GUI status and traceability rendering refresh from the matrices and reports emitted by the stage
  that just completed. A later aggregate view is supplemental and cannot replace a missing stage
  output.
- The System Traceability window and SysML Architecture hierarchy window are separate relationship views.
  System Traceability renders only approved generated-document upstream `Covers` dependencies, including
  inter-document paths such as SRS -> DRS -> IPOS; it must not render SysML topology, source-spec adjacency,
  unapproved source-only shortcuts, or `covers ...` arrow labels. IPOS block nodes in that view show only name, coverage,
  and upstream blocks. The SysML Architecture hierarchy window renders only approved SysML structural/design
  relationships and must not receive generated-document dependency arrows. The central downstream validator
  owns this separation; no project-specific or parallel policy is permitted.
- The expanded System Traceability tree and graph consume the same central RM edge-statistics payload. Approved
  primary and supplementary source nodes appear only when their approved dependency edges exist; zero-scope
  SRS-to-DRS/ARS edges are omitted, edge percentages are rendered, and legacy source/allocation-denominator values
  are not shown.
- Approved generated traceability may define a direct supplementary-specification -> DRS/IPOS dependency.
  Render it only when the snapshot-bound allocation and generated `Covers` relationship explicitly support
  that source and target. Do not route it through a generated-document parent or infer it from source presence,
  file adjacency, or generic source/spec grouping.
- Every System Traceability dependency edge defines `coverage %` as unique upstream requirement IDs covered by
  the derived document divided by total unique requirement IDs in the upstream document. Deduplicate upstream IDs;
  never use downstream row counts, raw link counts, or downstream percentages.
- IPOS block nodes remain basic-info-only; when multiple approved upstream dependencies exist, show each upstream
  document or supplementary specification as `covered unique upstream requirement IDs / total requirement IDs`
  and its percentage, without rendering requirement details.
- `scripts/validate_downstream_coherence.py` owns the single RM edge-statistics payload used by both reports and GUI
  rendering. Each record includes the upstream node, derived node, edge/dependency type, covered unique upstream
  requirement IDs, total unique upstream requirement IDs, and percentage. Report generators and GUI code must consume
  those records and must not locally recompute the same edge from source intersections, generated-document `Covers`
  rows, or supplementary-source denominators.
- IPOS node coverage is explicitly `Source-ledger coverage`: unique source requirement IDs represented by the concrete
  node divided by unique IDs in the approved allocation ledger. A textual per-block table may show the distinct
  `Mapped requirement coverage` metric based on the approved Stage 2 mapping denominator, but must label it as such.
  `Upstream edge coverage` remains the central edge-payload metric. Never render these distinct percentages under one
  unlabeled `Coverage` heading.
- The RM graph renders concrete IPOS blocks with direct approved upstream edges. It must not materialize generic
  `Digital IPOS` or `Analog IPOS` group nodes. Central summary statistics may describe the aggregate IPOS destination
  without adding a generic graph node.
- Source-specification coverage is a separate, explicitly labeled metric. It must not be substituted for RM
  dependency-edge coverage, and two different denominators must not be shown for the same displayed edge.
- The Stage 3 SysML review is structural-only: model set, block/endpoint consistency, names,
  source I/O representation, and source interaction/XBAR structure. It does not validate complete
  requirement coverage, allocation, ownership, partition, or end-to-end coherence.
- The dedicated final SysML phase runs after the downstream document stages. It generates the full
  SysML set through the approved snapshot-bound generator and validates final requirement coverage
  and coherence through `scripts/validate_downstream_coherence.py`, the existing central
  validator-orchestrator. No parallel validator or local coverage implementation is permitted.
- Approved architecture mapping workbook/CSV and approved snapshot/SQLite materialization are the
  sole architectural authority. Stage 2 SysML is derived structural output for review and
  visualization only; its review is non-authoritative and must not block snapshot-authorized
  downstream generation or replace mapping approval. Final SysML is a separate snapshot- and
  contract-bound downstream phase.
- Stage 3 SysML structural review must resolve its expected block/model set from the selected
  approved snapshot and approved architecture mapping/allocation metadata. Only concrete blocks
  with approved Digital IPOS or Analog IPOS requirement scope are in scope. Raw inventories, OCR
  tables, source I/O catalogs, and legacy block lists must not make an otherwise out-of-scope
  block, port, or table required.
- The central validator must reconcile every approved source-port catalog row, including its owner
  and direction, against every generated Digital and Analog IPOS Markdown and DOCX Source I/O
  table across all source pages. Missing or unapproved rendered ports block downstream approval.
- Final SysML inputs must be the same approved snapshot, `DownstreamContract`, allocation/ownership/
  partition data, source IDs, traceability matrices, port maps, and provenance fingerprints used by
  SRS, DRS, ARS, and IPOS generation.
- SysML block files must be generated exactly for the concrete blocks returned by
  `created_ipos_block_directories()` across Digital and Analog IPOS. The central validator rejects
  stale SysML block files and missing files for created IPOS blocks; valid-empty IPOS partitions
  produce no SysML block files or hierarchy nodes.
- Digital IPOS and Analog IPOS documents must emit deterministic unique anchors for every emitted
  section, subsection, and authored requirement entry. Same-document Markdown links and DOCX
  internal targets must resolve to anchors in that same document. The IPOS gate may enforce this
  rendered-output invariant, but it must not make allocation, ownership, snapshot, traceability,
  or downstream-contract decisions locally.
- Materialize an IPOS block document only when one or more approved block-local requirements are
  mapped to that concrete block in the selected snapshot. Do not emit a document, block directory,
  descriptive audit, or DOCX for zero-mapped inventory blocks. The central validator-orchestrator
  rejects stale or empty IPOS block directories; a zero-row IPOS partition is valid-empty and has
  no block documents.
- Use `created_ipos_block_directories()` for any downstream artifact inventory or GUI hierarchy.
  A created IPOS block must contain a generated Markdown or DOCX artifact. Do not display
  configured-only, stale, or valid-empty IPOS blocks as generated specifications.
- The shared DOCX formatter and existing IPOS gate enforce the document title and metadata on
  page 1, the Table of contents first on page 2, Document Navigation only after the TOC, and a
  bottom-right PAGE footer. Treat this as one shared rendered-layout invariant, not a new validation layer.
- All generated SRS, ARS, DRS, and IPOS documents use the shared contract in
  `scripts/spec_document_contract.py`: classify authority and discovery inputs, construct normalized
  records with ownership, provenance, retained/suppressed decisions and rationale, compose ordered
  semantic units once, render passively, materialize Markdown and DOCX, then write
  `materialization_audit.json` after DOCX post-processing. Local gates and the central downstream
  validator independently verify normalized-input parity, semantic-unit provenance and order,
  Markdown/DOCX fidelity, artifact hashes, and document-type boundaries. Re-running the composer
  alone is never sufficient validation. Keep shared policies, code, and tests free of project names,
  block catalogues, capability catalogues, and golden project prose.
- Each document type preserves its own contract. SRS owns system behavior; ARS owns analog and
  mixed-signal architecture; DRS owns top-digital and integration behavior; IPOS owns one approved
  concrete block. Support and discovery sources may identify candidates but cannot override these
  authority, abstraction, ownership, scope, section, promotion, or suppression boundaries.
- For the first instantiated path, materialized IPOS Block Overviews use one IPOS-only authority
  contract: the approved snapshot and approved `block_inventory.csv` `Function`, `Inputs`, and
  `Outputs` remain primary authority. Same-block approved IPOS requirement evidence may support
  evidence-gated, non-normative local refinements; it cannot change semantics, ownership,
  responsibility, or system-level behavior. Do not derive refinements from generated DRS prose,
  isolated keywords, acronyms alone, signal lists alone, I/O names alone, or tables alone, and reject
  cross-block evidence. Each retained refinement preserves its supported action and object and any
  meaningful local qualifier; deduplicate only equivalent behaviors, not distinct objects sharing a
  verb. If a safe object cannot be recovered, suppress the candidate rather than emit a generic
  action-family placeholder. Accepted candidates are retained through bounded, ordered semantic units in `1.2 Supported
  functions and scope`: closely related same-block refinements may share one rendered sub-function summary only when their
  distinct supported objects and meaningful qualifiers remain explicit. Each sub-function summary has a concise role-first
  opening, while each contributing refinement remains individually provenance-linked in the audit.
  A summary may include short source-backed
  behavior details and at most one interaction line when needed to preserve distinct qualifiers;
  avoid redundant self-interactions. Every suppressed candidate remains audit-only with a rationale. `Functionality`
  is a non-bulleted macro-purpose summary; `Supported functions and scope` is non-empty and bounded by
  the approved function and I/O. Valid-empty IPOS partitions remain unmaterialized.
  The shared deterministic full-evidence aggregation renderer preserves distinct accepted
  same-block responsibilities and explicit local interactions, deduplicates only equivalent phrases, and uses admitted
  evidence order. The same final-materialization quality rule applies to every materialized
  Digital and Analog IPOS block; do not use RRF,
  rank-based facet selection, or fixed facet-count truncation in IPOS rendering or its audit;
  RRF is reserved for Hybrid RAG retrieval/query fusion and retrieval benchmarks.
  Raw authoritative requirement statements, source IDs, `[TO: ...]`, `[DDS_...]`, `[IPOS_...]`, and
  `[Vpriority ...]` tags must not be copied into overview sections. The shared composer is the
  only IPOS descriptive-policy implementation: it owns evidence admissibility, topic coherence,
  scope, and omission rules. Use approved block-inventory function evidence for high-level IPOS
  synthesis; never promote requirement/interface parameters, register/address/value/timer/version
  fragments, connection-only text, or isolated keyword hits into an overview.
- IPOS topic coherence uses only the shared `assign_ipos_descriptive_topic` model. Topic
  vocabulary is evaluated against functional evidence only, never provenance, source IDs,
  artifact paths, ownership labels, or source metadata. Score all matching topics; retain one
  unique strongest topic and omit tied or unsupported evidence. `descriptive_summary_audit.csv`
  must retain the selected topic, matched functional evidence, and selection or rejection reason.
  The IPOS gate verifies this rendered-output invariant through the shared model and does not
  create a parallel downstream authority.
- IPOS overview paragraphs use the shared deterministic functional-summary composer only. It
  re-elaborates selected approved local evidence into concise engineering statements of block
  purpose, supported scope, local organization, internal functions, and local interfaces.
  Functionality states the block purpose; approved block-function evidence may be extended with
  approved local requirement/interface evidence only for distinct capability families or supported
  internal organization. The composer must not emit filler, raw evidence, requirement wording,
  IDs, markers, parameter/register/timer/value fragments, or port counts; unsupported sections are
  omitted and authoritative Block requirements remain exact.
- Shared IPOS refinement-audit input contract: for each materialized Digital or Analog IPOS block,
  generation and gate validation must classify the identical complete candidate-requirement set
  from that stage's approved snapshot-scoped traceability rows, using the same shared composer.
  Keep the inventory `Function`, `Inputs`, and `Outputs` and accepted refinement evidence local to
  the current block. Nonlocal rows may appear in the candidate audit only as suppressed
  cross-block-risk candidates; they must never support or enter rendered text. Compare the complete
  candidate key set and exact decision, derivation, candidate, and suppression fields. Do not narrow
  the validator's candidate inputs to local rows when generation uses the complete set; any change
  to the shared evidence universe requires parity tests for both IPOS domains.
- IPOS `1.2` shared final-materialization rule: keep the approved candidate universe and Stage 2a
  unchanged. Render a role-first opening for each supported local function; use consistent readable
  display names, retain distinct source-backed conditions and outcomes, and replace parser-like
  labels or leaked signal tokens with engineering prose without weakening provenance checks.
  Merge a dependent operation into its evidenced owning function when that function is present;
  suppress an orphaned atomic handoff rather than present it as an independent capability.
  Standalone summaries require an independently meaningful behavior and must not have raw-identifier
  headings, incomplete action fragments, or redundant self-interaction lines. Keep every accepted
  contributor and deliberate atomic suppression visible in the refinement and materialization
  audits; validate summary shape, quality, evidence parity, and Markdown/DOCX semantic-unit order.
  Full regeneration requires all materialized blocks to pass their descriptive-quality checks;
  report each failing block explicitly rather than treating a passing aggregate as a waiver.
- IPOS `1.1` and `1.2` are final technical documentation, not descriptions of the approval
  workflow. The shared deterministic composer must use approved inventory function/I/O and
  admitted same-block evidence to write natural prose for every materialized Digital or Analog
  IPOS block. The shared validator must inspect rendered sections independently of composer
  parity and reject `approved macro-purpose`, `approved ... function`, `local scope covers`,
  evidence/audit/process language, and equivalent template scaffolding in Markdown and DOCX.
  A scoped repair does not waive this rule for unchanged blocks: declare a full rollout only
  after regenerating any remaining outliers from the same approved snapshot and passing the
  full Digital/Analog gates and central downstream validation. Preserve exact normative text,
  candidate decisions, contributor provenance, and the authority boundary; never introduce
  project- or block-specific language rules to satisfy the gate.
- IPOS authored requirement blocks are governed only by `scripts/validate_downstream_coherence.py`.
  Every Digital IPOS and Analog IPOS block must render exactly as
  `IPOS-<concrete-approved-block-name>-xxx`, the exact approved requirement text,
  `Covers: <exact-approved-upstream-req_id>`, and `[End]`, in that order with no additional
  authored-block lines. Build the block token from the concrete approved block name with
  deterministic uppercase hyphen separation; keep `xxx` as the stable three-digit sequence
  within the IPOS document. This rule applies only to IPOS and never to DRS; traceability
  matrices retain approved provenance.
- **Stage 2 mapping-review handoff:** `artifacts/stage1_specs/architecture_mapping_preview.xlsx` is
  the reviewer-editable mapping surface. Its paired CSV becomes the authoritative machine-readable
  handoff only after the saved, closed workbook passes `scripts/mapping_review_sync.py`. Require
  that synchronization before Stage 2A approval, Stage 2A execution, or Stage 2B snapshot freezing.
  Stop on an unsaved/locked workbook or duplicate, missing, unknown, or CSV/workbook-mismatched
  requirement ID; never consume a stale CSV or silently substitute it for the reviewed workbook.
- Preserve staging, provenance, revision history, approval state, and immutable snapshot lineage.
- Enforce evidence-first gate decisions.
- Apply the centralized project-agnostic allocation policy in `scripts/requirement_allocation_policy.py`. Valid allocation classes are exactly `system_level`, `top_digital_architecture`, `top_analog_architecture`, `block_local_digital`, `block_local_analog`, and `descriptive_only`.
- Require the policy-defined owning target for each class: `SRS`, `DRS`, `ARS`, `Digital IPOS`, `Analog IPOS`, or `none`. Never derive the target from source type, approved block, block mention, or source naming.
- Route digital source-to-destination connection contracts to `top_digital_architecture` -> `DRS` unless evidence establishes an abstract end-to-end system capability. Do not invent artificial parents or duplicate normative requirements across levels.
- Require one of `normal_hierarchical`, `direct_source_to_ipos`, `direct_supplementary_to_ipos`, or `split_lineage` as `lineage_mode`; use the normal hierarchical mode unless approved evidence supports another mode.
- Before Stage 2A approval and Stage 2B freeze, require allocation class, matching target, rationale, lineage mode, source-origin lineage, and applicable hierarchy/domain metadata. Persist these fields in canonical SQLite and consume them from the approved snapshot downstream.
- Execute strict forward-only runs: one stage or an ascending contiguous range may begin at any stage; each selected stage runs once.
- For each selected stage, execute its runner once, require the runner's crosschecks, then execute its gate validator once. Stop immediately on any non-zero result; retries and loops are prohibited.
- Before every `workflow_cli.py run` execution, run the focused regression/retrieval test suite once. A failure stops the workflow before its first runner; record the result in `artifacts/orchestrator/workflow_cli_runs.jsonl`. Run the project retrieval benchmark in addition when Stage 0 is selected. Do not run workflow preflight tests for validation-only commands or the Stage 2A-to-DRS shortcut.
- Keep retrieval and benchmark logic project-agnostic. Generated benchmark reports identify the active project from `config/project_context.json` `project_name`; reusable code must not hardcode project names.
- Trigger one optional semantic recovery when legacy retrieval is empty or configured evidence-gap signals indicate uncertainty: no common lexical/normalized top candidate, a low top-1/top-2 margin within either channel, no exact normalized-term hit, too many unmatched query tokens, or a natural-language/paraphrase query profile. Treat the two candidate-overlap checks as one condition and never compare raw scores across channels.
- Record the trigger and recovery result; keep recovery one-shot and evidence-only. Exact IDs, protocol names, and reviewed evidence remain protected, and unresolved or failed selection falls back to legacy `hybrid`.

## Scope

- In scope: Stage 0 to 5 implemented profile and mandatory Stage 2 micro-architecture gate.
- Out of scope: optional later stages (vectors/rtl/synthesis/optimization) unless explicitly requested.

## Strengthened Canonical Stage Order

1. S0: Primary Source Baseline
2. S1: Source Spec Ingestion / OCR / Parsing / Req-ID Extraction
3. S2: Deterministic Classification into Staging Objects
4. S2A: Staging Review
5. S2B: Merge Impact Analysis
6. S2C: Merge Approval
7. S2D: Non-Destructive Merge into Integrated Canonical Corpus
8. S2E: Ontology / Vocabulary / Retrieval Index Refresh
9. S2F: Architecture Map Review
10. S2G: Architecture Mapping Approval
11. S2H: Immutable Approved Mapping Snapshot
12. Stage 3: Generate SRS from Approved Snapshot
13. Stage 4: Generate DRS
14. Stage 5: Generate ARS
15. Stage 6: Generate Digital IPOS
16. Stage 7: Generate Analog IPOS

Execution sequence: `S0 -> S1 -> S2 -> S2A -> S2B -> S2C -> S2D -> S2E -> S2F -> S2G -> S2H -> 3 -> 4 -> 5 -> 6 -> 7`.
Legacy numeric stage commands remain compatibility aliases during migration.

## Strengthened Workflow Invariants

## Downstream Validation And Recommendation

- Run `python scripts/workflow_cli.py validate-downstream` only after the main authoritative pipeline and approved snapshot-derived outputs are available. This is a post-pipeline validation step, not a replacement for stage gates and not a Stage 0 retrieval preflight.
- Use an explicit project benchmark configuration containing project name, benchmark case file, retrieval database/context, mapping artifact paths and column mappings, rendering targets, and output artifact paths. The evaluator framework must remain project-independent.
- Cases are deterministic review fixtures. They may reference expected source evidence IDs, required source attributes, evidence class (`structured`, `semi-structured`, or `free-prose`), expected scope/classification, noise markers, and optional downstream rendered attributes.
- Measure lexical, normalized, hybrid lexical-plus-normalized RRF, and optional local semantic widening. Semantic evaluation requires explicit command opt-in and configuration opt-in; it never enables or changes production retrieval.
- Produce Markdown, JSON, and per-case CSV results plus an approval-request artifact. Reports must separate retrieval, preservation/assembly, filtering, mapping, hierarchy, scope, ownership, rendering, and latency findings.
- Recommendation categories include retain baseline, fix evidence preservation, fix filtering, fix mapping, fix hierarchy, fix rendering/compaction, gated semantic evaluation, reject semantic widening, and manual review required.
- No recommendation may be applied by the validator. Semantic/transformer enablement, retrieval defaults, mapping policies, filtering rules, rendering policies, and benchmark thresholds all require explicit user approval before a separate implementation change.
- Reproducibility requires fixed local inputs, stable ordering, explicit configuration, protected exact identifiers, no network/cloud/LLM calls, no self-modification, and identical results for identical approved inputs and configuration. Environment-sensitive latency is reported but does not alter the recommendation.

## Shared Descriptive-Summary Contract
- Apply the frozen preferred SRS introductory rule `srs-introductory-authority-bounded-v1` from `.github/copilot-instructions.md` and `SRS_INTRODUCTORY_WRITING_RULE` in `scripts/workflow_routing.py` only within the SRS document-content profile. Introduction and terminology use concise professional prose bounded by approved content; they do not promise coverage, create allocation, assert performance/implementation detail, or make glossary definitions independent authority. Preserve the shared literal category conventions. Validate rule identity/fingerprint, provenance and final Markdown/DOCX through existing SRS gates. This presentation preference contains no project-specific wording and does not change DRS/ARS/IPOS profiles, activate generators, or create approval/snapshot authority.
- Apply the general cross-document descriptive policy from `.github/copilot-instructions.md` through one deterministic shared assembly boundary. This skill defines how the policy is gated: evidence must be artifact-only after Stage 1, scope and authority filters must be explicit, provenance must be audited, Markdown and final DOCX must be checked independently, and descriptive output must never create requirements or `Covers` dependencies.
- For the SRS-first normalized descriptive flow, apply the common evidence/fact/profile/preservation rules in that policy. Validate profile fingerprint, normalized-record/fact/semantic-unit linkage and selected sentences through the existing SRS/central checker, not a parallel authority gate. DRS/ARS/IPOS profile hooks are runtime-disabled; policy tests do not activate them. SRS exclusions must not become generic defaults. Unsupported adapter constructions remain audited projection gaps; later migration requires separate authorization and profile-specific validation.
- Natural technical prose and readable block/function summaries are a document-type-independent
  quality rule for appropriate descriptive sections, not an IPOS section-number template.
  Rendered prose must be bounded by approved document-specific authority, deterministic,
  auditable, and independently checked against approval/process scaffolding and normative form.
  Existing legacy checks cover DRS and scoped SRS descriptive sections. Adoption of the new
  normalized evidence/fact/profile flow is SRS-only; DRS/ARS/IPOS hooks remain inactive until
  separately authorized and validated.
- The validated DRS path uses existing approved inventory `Function` and explicit `Entity kind =
  concrete_block` plus the established digital-block selection policy. Every selected block
  receives one natural-purpose sentence with exact inventory provenance in the existing
  descriptive audit; non-block entities get no block paragraph. Preserve complete approved
  owner-scoped source I/O as Markdown/DOCX tables, never port-name bullet lists. Stage 5,
  crosscheck, and central downstream validation share one DRS descriptive-artifact check.
- DRS introductory context and topic sections project existing approved top-digital
  integration relationships into concise non-normative prose and source/destination/exchange
  tables. Require deterministic ordering, exact provenance in the descriptive audit, and
  independent final-artifact validation; no raw requirement dumps, speculative behavior,
  unapproved block promotion, or expansion beyond the approved document scope.
- The shared Stage 1 descriptive-evidence adapter may read only Stage 1 OCR/index artifacts,
  emits complete statements with page/line provenance, and assigns `system` or one uniquely
  matched runtime block scope. Ambiguous matches remain system-scoped; it never guesses an owner.
  DRS may map system evidence to its top-digital descriptive context and uniquely matched block
  evidence to the existing approved DRS block scope. The SRS normalized adapter accepts only
  explicit system/architecture context admitted by its profile, not block-local evidence.
  Neither path changes authored requirements, allocations, snapshots,
  hierarchy, source-origin lineage, or `Covers`.
- SRS, DRS, ARS, Digital IPOS, Analog IPOS, and any future approved block- or layer-level generated specification may render configured descriptive overview sections such as System Main Functions, Digital Main Functions, Analog Main Functions, Operating Modes, Power States, and other configured topics.
- These summaries are derived, non-authoritative outputs only. They must not create or modify requirement authority, canonical approval state, mapping authority, block/layer ownership authority, provenance, or source-of-truth artifacts.
- Approved normative requirements may remain eligible evidence for descriptive grouping and provenance-preserving rendering. The renderer must not create new requirement IDs, obligations, `shall` statements, acceptance criteria, design decisions, ownership decisions, or unstated architecture.
- Descriptive assembly must use one independently testable shared helper boundary, be deterministic and local-only, and reproduce the same result from the same approved snapshot and configuration. No LLM, network, cloud dependency, or remote model is permitted.
- Permitted evidence includes approved snapshot rows, approved mappings, approved structural/interface/context evidence, approved descriptive artifacts, and governed vocabulary/taxonomy/profile signals. Domain, scope, block, and layer ownership filters must be explicit.
- Source-backed architecture descriptions may be reused across SRS, ARS, DRS, and approved layer-level specifications when scope is explicit and wording remains descriptive. Generic SoC/mixed-signal vocabulary may cover system or subsystem role, analog front end integration, sensor/external interfaces, data paths and buffering, host protocols, embedded processing, register/configuration access, power domains, clock/reset, interrupts/status, boot, test, and low-power states. Vocabulary guides classification only; it never creates evidence or requirements.
- Traceability follows content type: authored normative ARS/DRS requirements derived from SRS retain `Covers: SRS-REQ-xxx`; descriptive source-backed sentences and capabilities retain source/provenance audit links but do not create normative `Covers` dependencies.
- SRS/DRS/ARS and downstream IPOS/block generators share the same assembly behavior. Differences are limited to configured scope/domain filtering, block/layer ownership, topic visibility, and explicitly allowed evidence selection. Hidden generator-specific heuristics are prohibited.
- Deterministic lexical/normalized selection plus approved category/type, structural/context, ownership, vocabulary, taxonomy/profile, and provenance signals is the primary basis. Optional local hybrid/semantic retrieval may widen candidate discovery only when deterministic coverage is weak; semantic similarity alone is insufficient and widened candidates must pass deterministic eligibility and scope checks.
- Operating Modes and Power States must use the shared assembly path and must not depend primarily on fixed headings or project-specific hardcoded labels. Project refinements require explicit reviewable configuration or adapters.
- Empty topics are omitted by default. Insufficient-evidence wording is emitted only when required by the document contract or review-visibility configuration; filler text is forbidden.
- Configured output limits must be stable and auditable. The descriptive audit must expose selected evidence, rejected evidence and reasons, topic assignment, deduplication, ordering, limit truncation, scope/ownership filtering, and omitted-versus-insufficient outcomes.
- Power and low-power architecture is governed as one project-agnostic descriptive topic family across SRS, DRS, and ARS. Use the isolated shared low-power assembly boundary, reviewed configuration seeds, approved vocabulary/taxonomy signals, and explicit document scope profiles.
- Candidate discovery defaults to lexical plus normalized plus RRF retrieval. Optional local semantic widening is a gated candidate-discovery aid only; similarity alone cannot select evidence, and the authoritative default remains unchanged when semantic support is disabled.
- SRS is system-scoped, DRS is digital/top-digital/integration-scoped, and ARS is analog/mixed-signal/power-scoped. Block-local low-power evidence is not sufficient for DRS top-level coverage.
- Each generator writes `descriptive_low_power_audit.csv` beside its generated Markdown. The audit records query seed, source/provenance, selected and rejected candidates, exclusions, scope/domain decisions, deduplication, and grouped output order.
- Low-power descriptions are derived and non-authoritative. They preserve provenance and source wording, are deterministic and local-only, and must not introduce requirements, `shall` statements, ownership decisions, or filler.

- Apply explicit versioned SQLite migrations recorded in `schema_migrations`.
- Preserve source name, revision number/date, source kind/scope, target scope, applicable
  blocks/layer, ingestion batch, staging batch, review reference, merge reference, and impact reference.
- Keep proposed and approved classification, reason, method, confidence, and review comment separate.
- Keep lifecycle state separate from semantic approval/category transitions and validate both centrally.
- Preserve conflicting same-ID source versions and provenance; a latest revision/date is only a proposed winner.
- Candidate taxonomy, vocabulary, and architecture profiles are never approved implicitly.
- Authoritative generation requires exactly one explicit `--snapshot-id` or approved selector such as
  `--use-latest-approved`; impacted snapshots are forensic-only until re-approved or superseded.
- Snapshot identity includes canonical revisions, mappings, profile hashes, retrieval configuration,
  and semantic-enabled metadata. Semantic retrieval remains optional and local-only.
- GUI chat is visibly non-authoritative and cannot modify workflow-authoritative state.

## Step 3 Workflow Enforcement

- Persist workflow entity states as `ingested`, `parsed`, `classified`, `under_review`,
  `impact_analyzed`, `approved_for_merge`, `merged`, `mapping_under_review`,
  `mapping_approved`, `snapshotted`, `rejected`, or `needs_rework`.
- Validate transitions centrally through the workflow transition service. Record every
  transition with actor, reason, approval requirement, timestamp, and metadata. Loopbacks
  create new history entries and never erase prior state.
- Run deterministic impact analysis before merge approval. It must identify affected
  requirements, classifications, mappings, profiles, snapshots, downstream targets,
  identity ambiguities, source scopes, and full versus partial regeneration.
- Merge only through the approval-gated canonical merge service. Staged rows create new
  canonical revisions and provenance rows; they never overwrite canonical text in place.
- Category decisions are explicit: `new`, `duplication`, `refines`, `conflict`, or `removed`.
  Semantic changes require approval, conflicts never auto-merge, and removals preserve
  rationale and lineage.
- Same-ID different-text conflicts preserve both source versions and remain approval-required.
  The latest source revision/date may be recorded as a proposed winner only.
- Approved mappings, profiles, and snapshots affected by a merge are marked impacted or
  require re-review. Do not delete history or silently revoke approvals.
- Architecture Map Review may change mapping allocation and coverage decisions only. It
  must not edit canonical requirement text, provenance, approved classification, or merge
  category. Identity/classification defects trigger a tracked loopback.
- Legacy supplementary ingestion may emit CSV/XLSX/JSON compatibility artifacts, but
  canonical SQLite registration, impact analysis, approval, and merge are authoritative.

## Step 4 Authority, Audit, And Rollback

- Record event-level audit entries for imports, parsing, ID validation, classification,
  reviews, impact analysis, merge, mapping, snapshots, rollback, vocabulary/taxonomy,
  retrieval, semantic fallback, SysML, reports, and conflict review.
- Rollback never deletes history. It creates a rollback record, a new tracked state or
  revision, an audit event, and indicates whether a new approved snapshot is required.
- Freeze snapshots through the canonical snapshot manager only. Snapshot identity must
  include canonical revisions, approved mappings, approved profile hashes, retrieval
  metadata, semantic flags, and traceability basis.
- Authoritative classification, review, snapshot, SysML, report, and downstream
  generation consumers must resolve approved profile context through the approved
  profile/snapshot resolver. Mutable files and unapproved profiles are not authority.
- SRS, DRS, ARS, Digital IPOS, Analog IPOS, and SysML generation must require exactly
  one explicit snapshot selector. Compatibility file resolvers are migration-only.
- Impacted or incomplete snapshots are forbidden for authoritative generation.
- Architecture mapping review may affect future snapshots only; it must not directly
  mutate generated SysML or downstream reports.
- Conflict reports may propose the latest source revision/date as winner, but remain
  derived review artifacts and never decide a merge automatically.

## S0 Primary Source Bootstrap

- S0 may assess a user-selected primary source locally before OCR workflow execution.
- The assessment must deterministically classify the source as `tagged`, `untagged`,
  or `ambiguous`, inspect configured IDs in narrative and table contexts, and propose
  a base ID prefix with preserved evidence and reason.
- Table ID detection must recognize normalized header variants including `Req-ID`,
  `Req_ID`, `Req Id`, `Requirement ID`, and equivalent configured forms.
- Detected status and prefix are proposals only. S0 must not silently approve or
  change the active source baseline. Candidate metadata is stored as pending profile
  context and requires explicit user approval, edit, or rejection.
- Source-selection UI, approval controls, and baseline promotion remain Step 5 work.

## Compatibility Boundary Hardening

- Direct compatibility callables must fail closed unless given an explicit approved
  snapshot selector or an explicit legacy/migration opt-in.
- `load_approved_input`, `freeze_legacy_export`, and direct IPOS callable compatibility
  remain non-authoritative, must emit deprecation guidance, and must not be used by
  default GUI, CLI, stage runners, validators, or report generation.
- Compatibility exports may write derived artifacts only; they must not imply or create
  canonical approval, snapshot authority, or workflow state.
- Stage mapping/classification output must prefer approved canonical classification
  context. Staged CSV category fields are review evidence, not authoritative decisions.
- Run `scripts/authority_consistency_scan.py` during cleanup validation to detect legacy
  resolver calls, direct mutable-artifact reads, hardcoded project identifiers, and
  embedded lexical resources. Findings require review; explicit source-derived adapters
  and legacy-only compatibility boundaries may remain documented.

## Agent Delegation Order (Current Profile)

1. Ontological Specification Analyzer Agent
2. Ontology Crosscheck Agent
3. Requirements Extraction Agent (Stage 1 Controller)
4. Requirements Coverage Cross-Check Agent
5. Specs Agent
6. Specs Crosscheck Agent
7. Micro-Architectural Analysis Agent
8. Architectural Crosscheck Agent
9. SRS Gen Spec Agent
10. SRS Crosscheck Agent
11. SRS Markdown To LaTeX Agent
12. SRS LaTeX Crosscheck Agent
13. ARS Gen Spec Agent
14. ARS Crosscheck Agent
15. DRS Gen Spec Agent
16. DRS Crosscheck Agent

## Script-First Execution Map

- Stage 0 runner: `python scripts/run_stage0_gate0.py`
- Stage 1 runner: `python scripts/run_stage1_requirements_gate1.py`
- Stage 2 specs runner: `python scripts/run_stage1_specs_gate2.py`
- Stage 2A micro-architecture runner: `python scripts/run_stage2_micro_arc_gate.py`
- Stage 3 runner: `python scripts/run_stage3_srs_gate.py`
- Stage 4 runner: `python scripts/run_stage4_ars_gate.py`
- Stage 5 runner: `python scripts/run_stage5_drs_gate.py`

Execution rule:
- Prefer one full runner invocation per stage.
- On failure, stop the pipeline. Do not retry or loop; rerun the affected stage or an ascending range only after correction, never in reverse.

## Hard Invariants

- Do not advance a stage without required artifacts and its crosscheck report.
- All Stage 0-5 fixes and generated outputs must remain project-agnostic; project-specific values may enter only through active runtime configuration and generated artifacts.
- SRS authored requirements must use unique `SRS-REQ-xxx` IDs; ARS authored requirements must use unique `ARS-REQ-xxx` IDs; DRS authored requirements must use unique `DRS-REQ-xxx` IDs, where `xxx` is exactly three decimal digits (`001`-`999`). Do not reuse an authored ID within an artifact or substitute another artifact's ID namespace. One atomic source requirement shall have one canonical authored SRS coverage reference; do not create or require a second authored SRS ID for duplicate coverage unless current source evidence defines a separate atomic requirement or distinct connection-matrix cell. This rule is project-agnostic.
- When the active project configuration explicitly classifies a source requirement as a non-canonical duplicate, exclude it before authored SRS ID allocation; do not assign it a replacement authored ID. The exclusion list is runtime configuration, not project-specific generator logic.
- Before Stage 2A, Stage 1 must write `artifacts/stage1_requirements/duplicate_source_req_ids.csv` containing only repeated IDs with multiple substantive normative statements, including counts, source locations, statements, and status.
- If that duplicate list is non-empty, stop the flow and ask the user to resolve source-ID uniqueness. Ignore marker-only, continuation, and inline-reference fragments when deciding whether an ID is duplicated.
- A gate can pass only when unresolved `critical` findings are zero.
- Stage 1 is blocked if Stage 0 has unresolved `critical` semantic issues.
- Stage 3/4/5 are blocked if Stage 2A architectural crosscheck has unresolved `critical` issues.
- Source-read policy:
  - Stage 1 may read the source spec directly.
  - Stage 2+ must be artifact-driven.
  - Guard enforcement: `scripts/guard_stage2_plus_spec_independence.py`.

## Required Gate Evidence

- Gate 0:
  - `artifacts/stage0_ontology/ontology.md`
  - `artifacts/stage0_ontology/glossary.csv`
  - `artifacts/stage0_ontology/semantic_issues.md`
  - `artifacts/orchestrator/stage_00_report.md`
- Gate 1:
  - `artifacts/stage1_requirements/requirements_summary.csv`
  - `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
  - `artifacts/stage1_requirements/coverage_crosscheck.md`
  - `artifacts/stage1_requirements/missing_requirements_candidates.csv`
  - `artifacts/orchestrator/stage_01_report.md`
- Gate 2:
  - `artifacts/stage1_specs/specs.md`
  - `artifacts/stage1_specs/traceability_seed.csv`
  - `artifacts/orchestrator/stage_02_report.md`
- Gate 2A:
  - `artifacts/stage2_mirco_arc/architecture_crosscheck_report.md`
- Gate 3:
  - `artifacts/stage3_srs/system_requirements_specification.md`
  - `artifacts/orchestrator/stage_srs_crosscheck_report.md`
- Gate 4:
  - `artifacts/stage4_ars/analog_requirements_specification.md`
  - `artifacts/orchestrator/stage_ars_crosscheck_report.md`
- Gate 5:
  - `artifacts/stage5_drs/digital_requirements_specification.md`
  - `artifacts/orchestrator/stage_drs_crosscheck_report.md`

## Strict Forward Pipeline Policy

- Step 1: Select one stage or an ascending contiguous range within `0 -> 1 -> 2 -> 2A -> 3 -> 4 -> 5`.
- Step 2: Validate each stage before advancing.
- Step 3: On runner or gate failure, stop immediately and record the blocker.
- Step 4: Correct the owning stage, then rerun that stage or an ascending range from it; never execute backward.
- Step 5: The Stage 2A-to-DRS requirements-only path is permitted because it moves forward; no later stage may invoke an earlier stage.

## Stage-Specific Compliance Checks

- Stage 0: enforce phased execution (Phase 0 through Phase 7), ontology-study sections, and no placeholders.
- Stage 1: enforce sentence completeness, no truncation, RAG alignment, and explicit `go`/`no-go` gate decision.
- Stage 3/4/5: enforce authored ID patterns, one-to-one `Covers`, navigation sections, sequential table numbering, and forbidden wording checks.
- Optional Stage 6: treat cross-project architecture comparison as a standalone post-Stage 5 activity. It may run through `workflow_cli.py run --stage 6 --project-to-compare <project_name>` or `workflow_cli.py arch-compare --project-to-compare <project_name>`, but it must not enter stage ranges or block/unblock Stage 0-5 gates. It must compare only current generated artifacts from the base project and the user-selected comparison project.

## Source-Baselined Hierarchy Coverage

- Use the full Stage 1 source-requirement ID catalog as the coverage denominator. Join SRS, ARS, and DRS traceability records using `source_req_id`; never infer coverage from local authored IDs, matching statement text, or a source-specific ID pattern.
- Stage 5 must write `artifacts/stage5_drs/requirements_hierarchy_coverage_report.md`. The report must include Source-to-SRS coverage, source coverage for each applicable lower-level document, end-to-end coverage, and the explicit source-ID gap sets.
- Treat a scoped lower-level specification with no authored requirements in its declared scope as `Not applicable`. Do not treat it as a coverage failure or count context-only traceability rows as in-scope coverage.
- The System Traceability GUI view is a read-only visualization of this generated report. It must display the source specification, SRS, ARS, and DRS as linked nodes and use the report's calculated percentage or not-applicable value on each link.
- Selecting System Traceability opens a dedicated vertical hierarchy window. It must include primary
  and provenance-backed supplementary sources, generated SRS/ARS/DRS, and only created IPOS blocks,
  with dependency labels and source-baselined covered/total counts and percentages.
- All workflow GUI button, control, and stage-hover popups must remain fully visible inside the work area of the monitor containing the hovered control, including multi-monitor sessions. Compute placement from runtime widget geometry and monitor work-area bounds; flip above or clamp within a monitor margin when the preferred position would overflow. Do not use project-specific names, source IDs, coverage values, monitor sizes, or fixed coordinates to place popups.

## Source Structural Table And Port Coverage

- Treat source I/O tables, port lists, pin maps, and other approved structural interface tables as derived architectural evidence, never as an independent requirement authority.
- Reuse the centralized snapshot-derived catalogs when present: `artifacts/stage2_mirco_arc/source_io_table_coverage.csv` for table-level identity, ownership, provenance, and row counts, and `artifacts/stage2_mirco_arc/source_port_catalog.csv` for port-level identity, direction, details, ownership, and source provenance. Do not create separate SRS, ARS, DRS, or SysML catalogs.
- Preserve deterministic identity from normalized source table title, owner, and provenance; identify ports from table identity, port name, direction, owner, and provenance. Generated text is not the authority for identity when catalog metadata exists.
- Classify tables as `context` or `requirement_bound` only from approved source-derived metadata. Context tables provide architecture/interface/descriptive evidence. Requirement-bound tables have explicit associated metadata such as `source_table_title`, `table_title`, `source_table_number`, or `table_number`; an incidental `Table N` phrase in requirement prose is not enough.
- Requirement-bound tables follow the applicable requirement route into SRS, ARS, or DRS. Context tables use deterministic owner/domain applicability. Unknown applicability is a reported evidence problem, not a reason to guess.
- Use `scripts/source_io_coverage.py` as the single coverage implementation. Reuse it from the existing SRS, ARS, DRS, and SysML validators; do not add a parallel workflow. It must scan generated Markdown, generated DOCX content, and owning SysML block files.
- The checker reports `covered`, `not_applicable`, `missing_table`, and `missing_port`. Missing applicable structural coverage fails the owning existing gate. A skipped or out-of-scope document is explicitly `not_applicable`.
- Preserve source table title, owner, page/file, port, and requirement linkage provenance in generated reference tables and coverage reports. If OCR prevents reliable table reconstruction, retain source-extracted text rather than inventing structure.
- Validate DOCX after conversion from generated Markdown; Markdown success alone is insufficient. Structural coverage must not modify canonical requirements, requirement IDs, mapping authority, snapshot contents, or requirement coverage denominators.

## Architecture Naming and Connection-Matrix Checks

- Every fix must remain project-agnostic: modify reusable logic or shared policy, validate it against the generic workflow contract, and read project-specific values only from runtime configuration or generated artifacts. Never encode a one-project correction as a hardcoded branch, identifier, name, source path, or special-case exception.
- ARS shall emit only analog-relevant requirements and related analog, mixed-signal, or power blocks supported by current runtime artifacts; digital-only and system-control-only requirements shall remain in SRS/DRS and must not enter ARS through dedicated-section or cross-domain shortcuts.
- Every emitted block name must be traceable to current source/Stage 2A evidence; never invent fallback names.
- Supplementary source requirements must be checked against the existing Stage 2 block inventory. If source metadata is incomplete, normalized source-ID matching may propose an existing block, but no new block may be invented. Derive `Analog`, `Digital`, or `System` from explicit source metadata, optional block classification, or deterministic requirement/block evidence; insufficient evidence remains a user-review item before Stage 2A approval.
- Never hardcode project names, blocks, signals, paths, IDs, aliases, tags, or special cases in SRS/ARS/DRS scripts; load them from runtime artifacts.
- Do not promote a product, device, subsystem, signal-chain, or capability description to a block name unless the source explicitly defines it as a block, IP, module, or matrix row/column label. A phrase such as `Analog Front End Device` is source description text, not automatically a block.
- In SRS and ARS, each project-specific block's literal `General functional description` continues to equal its current inventory `Function` until their separate rollout. In DRS, the shared natural-purpose renderer must retain the entire approved `Function` meaning, with the exact inventory value audited and independently validated. Reject invented or requirement-derived descriptions and empty `Function` values in all three.
- In SRS, ARS, and DRS, assign a non-matrix requirement to a project-specific block only when the requirement behavior is supported by that block's current inventory `Function`. Reject ownership derived from source headings, source-specific tags, signal/IP names, broad traceability mappings, or `Linked requirements` lists. When no inventory function supports ownership, retain the requirement under its cascaded source-function context with `Unassigned` routing and status `retained_as_non_block_function_context`; do not invent a block owner.
- When an unassigned requirement starts with or contains `The user shall`, treat it as a general-function requirement and cascade the nearest explicit source parent through same-page child paragraphs. Keep it in that source-function paragraph unless a known Stage 2A block owner supports the behavior.
- For tagged source requirements, preserve exact source text in source order until the configured tag terminator or the next tagged requirement ID. Join OCR-wrapped physical lines with spaces and never carry text across a requirement boundary.
- During Stage 1/2 inventory construction only, original-spec functional-role statements such as `is in charge of`, `main activities are`, `main functionalities are`, and equivalent wording may supply evidence for a block `Function`. Stage 3+ must use the resulting inventory `Function` only and must not reinterpret original-spec wording.
- SRS/ARS crosscheckers retain the exact `General functional description` check; DRS validates its natural sentence, approved concrete digital-block selection, audited inventory provenance, and table-form source I/O instead. All crosscheckers still validate non-empty `Function`, known owners, and function support for non-matrix owners.
- Matrix-derived ownership is checked against the exact interaction-matrix source row and authored matrix traceability; it is not inferred from broad mappings or generic lexical matching.
- Crosscheckers and downstream generators must contain no product names, project IDs, source-specific tags, source-section shortcuts, fixed block names, or project-specific template wording. Project values enter only through current runtime artifacts.
- The SRS crosschecker must compare every SRS source ID with the current Stage 2A requirement-to-block traceability exactly. It shall fail on any ownership difference, including an `Unassigned` Stage 2A row receiving a concrete SRS owner.

## Dedicated Source-Section Preservation
- Do not treat an image, figure, table label, legend, encoded-value enumeration, or other descriptive graphic content as a project-tagged requirement. Preserve a source ID only for an explicit normative statement or structurally defined requirement row.
- Derive image requirements only after full function/signal names are available from the rendered source image. Emit one source-faithful requirement per distinct image function with explicit image/figure provenance; leave `source_req_id` and `covered_source_req_id` empty unless the image explicitly associates the function with a source requirement ID. Do not infer a DDS relationship from page proximity, OCR order, or adjacent text.
- When current source evidence contains a dedicated paragraph or section for BIST, SCAN, Debug, DFT, Test Mode, ADC test mode, PAD mux, Alternate functions, Power-up, Power-down, BOOT, Configuration, or an equivalent explicitly named test, lifecycle, startup, shutdown, or configuration topic, preserve the exact source label and paragraph grouping in SRS, ARS, and DRS.
- Requirements from such a dedicated paragraph must remain in its corresponding source context downstream unless current Stage 2A block `Function` evidence supports a concrete owner. Equivalent local labels for one requirement family, including case or wording variants of a routine or operation, may be grouped under one normalized child paragraph beneath the nearest explicit source parent. Preserve the parent title and source wording, and retain artifact-derived ownership rather than lexical guesses; unsupported dedicated content stays in the dedicated context.
- Keep raw source IDs in SRS `Covers:` and use only the corresponding authored SRS IDs in ARS/DRS `Covers:`. Do not create a dedicated section when the current source evidence does not contain one.
- Detection must use current Stage 1 source/section metadata and remain generic; section names and project values must not be hardcoded for one source project.
- Preserve the complete dedicated source body, including every bullet/numeric item, in source order and equivalent formatting; do not summarize or omit items.
- If OCR concatenates list items, split on source markers and render one item per line, preserving marker, numbering, order, and text under the same authored requirement.
- Insert a blank line before each rendered list block so Markdown/Pandoc preserves item boundaries in DOCX; do not insert blank lines between list items.
- Render every authored requirement header (`[SRS-REQ-xxx]`, `[ARS-REQ-xxx]`, `[DRS-REQ-xxx]`) after at least one blank line; never place two authored requirement blocks directly adjacent.
- Render every authored requirement as separate Markdown paragraphs: blank line after the authored header, blank line before `Covers:`, and blank line after `Covers:` before the next paragraph or requirement.
- Use standard Markdown list markers (`-`, `*`, or `+`) for generated bullet lists so Pandoc converts them to native DOCX lists; preserve original bullet order and item text. Unicode bullet characters may remain only inside fenced source-evidence blocks.
- Render each independent paragraph after a blank line, including paragraphs following headings or metadata fields; keep list items and table rows contiguous within their own block.
- Add every emitted dedicated or non-block-specific source paragraph to the table of contents before the section-navigation index, assign it a stable hierarchical paragraph number matching its document location, provide a stable internal cross-link, and keep its requirement mapping under that linked paragraph.
- Render SRS, ARS, and DRS table-of-contents entries with indentation derived from their numerical section depth so the TOC hierarchy matches the navigation index; never flatten nested numbered sections.
- Preserve the same numerical TOC indentation through DOCX conversion and validate Word list nesting, not only Markdown whitespace.
- Unsupported or ambiguous ownership must be reported as `Unassigned` routing and retained in the source-function context. It is a blocking defect only when an explicit block requirement is left unresolved or when required source content/traceability is missing.
- For a source connection matrix with `Source` rows and `Destination` columns, use the exact labels from each populated cell. Rewrite each cell as `The <Source label> block shall be connected to the <Destination label> block.` and preserve the cell requirement IDs in SRS `Covers:` only.
- Assign one unique authored `SRS-REQ-xxx` to each populated SRS matrix cell. Treat that SRS ID as the sole upstream ID for corresponding ARS/DRS matrix-derived entries.
- Assign one unique artifact-local `ARS-REQ-xxx` or `DRS-REQ-xxx` ID to every authored ARS/DRS entry. `Covers:` in ARS/DRS shall reference only `SRS-REQ-xxx` upstream IDs.
- Stage 1 source IDs (for example `DDS_*`, `SYS-RQ-*`, `ANA-RQ-*`, `DIG-RQ-*`, `XDN-RQ-*`) shall appear in `Covers:` only in SRS authored entries.
- Assign matrix-derived ARS/DRS entries to the source-row block only; broad Stage 1 block mappings must not duplicate an edge into unrelated blocks.
- Build ARS/DRS matrix-derived descriptions from the exact interaction-matrix edge (`connection to <Destination label>`), never from truncated or merged OCR prose.
- Recover the complete destination-header set before mapping cells; when OCR omits or merges a header, resolve it from source-page coordinates or rendered-page inspection.
- Assign each cell ID by the geometric intersection of its source row and destination column, never by OCR line order or neighboring-text proximity.
- If matrix labels and Stage 2 inventory labels differ, retain the matrix labels for matrix-derived connection requirements and report the mismatch as an evidence/reconciliation item.
- Before sign-off, cross-check Stage 2/2A results, generated SRS/ARS/DRS artifacts, orchestrator reports, and next-step guidance for unsupported or generic block names.

## Stage 2 Ownership and Connection-Matrix Checks

- Explicit named IP/block/module evidence maps to the exact current source-derived block label; generic protocol, analog/digital, signal, sample, or block vocabulary must not establish ownership by itself.
- If multiple candidate owners remain, keep only candidates supported by the current block inventory `Function` text or exact connection-matrix source-row evidence. Report remaining ambiguity as an inventory/mapping defect instead of encoding project-specific precedence.
- Require `interaction_matrix.csv` to contain `Requirement IDs` for connection-matrix rows and verify every recovered cell ID is attached to the exact source/destination row.
- Emit a connection row only when the corresponding source connection-matrix cell contains a requirement ID; a blank cell is not a connection.

## Source Table Classification Checks

- For complex source tables without a recoverable normative requirement statement, emit only the table number and caption in SRS/ARS/DRS requirement statements. Do not copy table rows, headers, or cell contents into normative prose; retain the source linkage in `Covers:`.
- Do not generate requirements from memory-map, address-map, register-map summary, connectivity-check, static-connectivity-check, revision-history, abbreviation, repository, or metadata tables. These tables may remain reference evidence, but they are not normative requirement sources unless a row explicitly carries the configured `Requirement` marker and passes normal requirement-quality checks.
- Do not emit descriptive table captions or non-normative table rows, including operating-mode, state, configuration-summary, timing-summary, or equivalent tables, as SRS, ARS, or DRS requirements. Keep them as reference evidence.
- Do not emit descriptive table captions or non-normative table rows, including operating-mode, state, configuration-summary, timing-summary, or equivalent tables, as SRS, ARS, or DRS requirements. Keep them as reference evidence; emit a table row normatively only when it contains the configured `Requirement` marker and passes normal requirement-quality checks.
- Do not process register tables as I/O, parameter, or interface tables when the caption or header contains `Register name`, `Register address`, `Register map`, `Register offset`, `Register access`, `Register reset`, `Register description`, `Register value`, `Register table`, or equivalent register-map terminology. Exclude the table from downstream copied-table rendering; do not infer rows or requirements from it.
- During OCR extraction, analyze each table row containing a configured requirement ID and retain its table title, column headers, and page-to-page continuation context. Do not treat a recognized table-row ID as isolated OCR prose.
- Stage 1 table extraction follows: PDF/OCR text -> table block detection -> line grouping -> row candidate buffering -> continuation detection -> row validation -> row reconstruction -> architecture-map generation. Do not finalize a row when only the ID is present, a cell ends with a dangling token, a line is a continuation, or an expected final value is missing. Finalize only when mandatory fields are present, the next line clearly starts a new row, or a strong table boundary is detected.
- Generate one unified `artifacts/stage1_requirements/table_row_review.csv` for every table row carrying an explicit configured requirement ID, including ordinary reconstructed rows and structural clock/reset/interrupt rows. Classify rows with `table_kind`; mark incomplete or conflicting rows `manual_review` with a reason and do not silently promote them. Ambiguous table blocks must be routed to manual review; do not create separate review tables per table type.
- When `manual_review` rows exist, generate `artifacts/stage1_requirements/table_row_review_request.md`, stop Stage 1 before architecture-map generation, and explicitly ask the user to review and correct/confirm the rows. Resume only after the reviewed table evidence is regenerated and validated.
- Treat connection-matrix tables as interaction evidence only: generate exact source/destination edges and matrix-derived SRS/ARS/DRS connection requirements, but do not use merged OCR prose as broad ownership evidence.
- Treat I/O list, port list, pin list, clock list, reset list, and interface list tables as source interface evidence. Preserve them in downstream specs where relevant; do not turn each row into a requirement unless the row explicitly states a requirement.
- Enforce document-level interface ownership: SRS may summarize system interfaces but must not render complete digital block I/O/port/pin/clock/reset lists; DRS owns complete digital block interface tables under the matching block paragraph; each Digital or Analog IPOS owns detailed I/O evidence for its single approved block. Do not duplicate complete block I/O lists across SRS, DRS, and IPOS.
- Reset/clock connectivity table rows with a requirement ID plus source and destination/target fields are structural derived requirements. Assign them to the current project's power/clock/reset owner from Stage 2 inventory/profile: PMU when PMU is the clock/reset sequencer, otherwise the project-specific clock/reset-management block. Do not assign them to arbitrary source/destination hierarchy blocks based only on signal paths.
- Carry reset/clock table headers to continuation OCR pages containing requirement IDs, so source, destination/target, frequency, and clock-gating cells remain available for structural derivation.
- Carry source requirement bodies across the next OCR page when a requirement starts near a page boundary. Stop at the next source requirement marker or section heading, and rewrite table-like fragments into clear authored SRS prose rather than emitting raw OCR cell tokens.
- For Reset or clock connectivity tables, rewrite each table line as `The <Source label> signal shall be connected to the <Destination label> signal`, if <Destination label>, or `<Target label> signal ` if <Target label> present, `with <Clock gating>.` if <Clock gating> is present with content different by `<No label>`, `without Clock gating.` if <Clock gating> is absent or present with content specified by `<No label>`; preserve the cell requirement IDs in SRS `Covers:` only.
- Keep the table classifier generic. Match table and section titles by reusable terms, not by product names, block names, project IDs, or one-project source tags.
- For Interrupt tables, use names contained in that table's columns such as `Interrupt`, `bit`, `Description` to write a derived requirement statement, and preserve the original table requirement ID in SRS `Covers:`. Do not invent a block name or alias from the interrupt table; use only the current Stage 2 inventory block that matches the source evidence.
- For Interrupt tables, rewrite each table line as `The <Interrupt label> interrupt shall be connected to the <Destination label> block.`, if <Destination label> is present in the table or `shall be connected to <Description label> to bit <bit label>` if <Description label> and <bit label> are present, and preserve the cell requirement IDs in SRS `Covers:` only. Do not invent a block name or alias from the interrupt table; use only the current Stage 2 inventory block that matches the source evidence.

## Block Domain Taxonomy Checks

- Distinguish `real block`, `interface/port`, and `source context` in every mapping artifact. Only a current Stage 2 inventory implementation unit with a non-empty `Function` may be an IPOS owner.
- For example, labels such as `I2C interface` and `SPI interface` may be interface endpoints owned by a real implementation block such as `I2C_SPI_AHB`. Determine this relationship from the current `interface_catalog.csv` owner/purpose and `block_inventory.csv` function evidence; do not hardcode these names or assume the same relationship in another project. Never create an IPOS document for an interface endpoint.
- Channel-only, mode-only, phase, and debug labels are source context, not blocks, and must not enter `approved_block`, `owning_block`, block headings, or filenames.
- Treat ADC as analog/mixed when its inventory function implements analog-to-digital conversion or sampling. ADC must not enter Digital IPOS solely because it emits digital samples.
- Digital IPOS gates must fail on non-digital, interface, or context owners instead of generating empty or misleading block documents.
- Classify protocol, bus, processor, controller, register, and digital state/data-path blocks as digital when that behavior is supported by the block function, interface catalog, or textual architecture evidence.
- Treat `I2C`, `SPI`, `AHB`, `AXI`, `APB`, `UART`, `JTAG`, `serial`, `protocol`, `bus`, `processor`, `CPU`, `microprocessor`, `core`, and `digital` as authoritative digital-domain terms in block taxonomy.
- Protocol or processor evidence overrides generic analog terms from connected requirements or mixed-signal context. Do not classify a digital bridge or processor as analog/mixed because it interfaces with analog blocks.
- Reserve analog/mixed and power/supply categories for blocks whose own function or interfaces implement those domains. Keep the vocabulary project-independent and do not encode project block names.

## DRS Interface Table Preservation Checks

- DRS block paragraphs must include source I/O, port, pin, clock, reset, and interface tables when the table can be matched to the current block inventory or exact matrix/source label.
- Place copied source interface tables after the block `Inputs:`/`Outputs:` summary and before authored DRS requirements.
- Preserve original source title and provenance. If OCR quality is too poor for reliable markdown table reconstruction, copy the extracted source text in a fenced text block instead of inventing columns.
- Copied source table snippets must stop before source requirement headers, source peculiar-requirements paragraphs, and raw source requirement bodies. DRS must not contain `[SOURCE_ID] Requirement` headings outside authored `DRS-REQ-xxx` entries.
- Copied source interface tables are contextual/reference evidence only. They must not create normative requirements without explicit requirement wording or a valid connection-matrix rule.
- Shared or ambiguous source interface tables must be reported as shared/ambiguous evidence; do not duplicate them into unrelated blocks based on broad lexical overlap.

## Orchestrator Output Contract

## Shared GUI Artifact Visualization
- Treat `.sysml` as a readable artifact text format wherever the GUI exposes source files.
- The SysML Architecture view must show the parsed hierarchy graph and selected SysML source text together. Refresh shall select the generated top-level SysML file by default, while retaining selectable subsystem, shared-definition, and block files.
- Parse current generated `part` declarations generically and show an explicit empty-state message when required SysML files or hierarchy declarations are unavailable.

1. Current stage and gate status
2. Delegations executed and outcomes
3. Open risks and blockers
4. Next delegated action with owner
5. End-to-end readiness summary

## Primary References

- `README.md`
- `docs/workflow-diagram.md`
- `docs/orchestration-spec.md`

## Local Deterministic CLI (No LLM Calls)

Use the local Python CLI when the workflow is stable and you want script-only execution.

- Status check:
  - `python scripts/workflow_cli.py status`
- Run deterministic taxonomy update from Stage 1 OCR index:
  - `python scripts/workflow_cli.py taxonomy-update`
  - `python scripts/run_taxonomy_crosscheck_update.py --index-csv artifacts/stage1_requirements/ocr_extracts/index.csv`
- Run the top-down pipeline (example Stage 0 through Stage 3):
  - `python scripts/workflow_cli.py run --from-stage 0 --to-stage 3`
- Run the approved forward requirements-only shortcut:
  - `python scripts/workflow_cli.py drs-after-stage2a`
- Validate all gates:
  - `python scripts/workflow_cli.py validate --all`

Execution policy:
- Every run executes one stage or an ascending contiguous range, with each selected stage executed once.
- Any failure stops the run; correction may rerun the affected stage or an ascending range, but never a backward range.
