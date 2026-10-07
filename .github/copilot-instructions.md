- Do not process register tables as I/O, parameter, or interface tables when the caption or header contains `Register name`, `Register address`, `Register map`, `Register offset`, `Register access`, `Register reset`, `Register description`, `Register value`, `Register table`, or equivalent register-map terminology. Exclude the table from downstream copied-table rendering; do not infer rows or requirements from it.
# Copilot Workflow Instructions

## Purpose
These instructions define mandatory workflow rules for the strengthened S0 through Stage 7 execution model, strict requirement-ID compliance, artifact-driven Stage 2+ behavior, canonical SQLite authority, snapshot-driven generation, and fail-fast validation.

## Scope
- Applies to all work in this repository.
- Treat this file as the highest-priority local workflow policy.
- Rules are intentionally project-agnostic and reusable across repositories with the same staged pipeline.

## Project-Agnostic Policy
- Keep reusable scripts, templates, validators, and generated logic generic. Read project-specific values only from active runtime configuration or current artifacts.
- Human-readable owner, block, and display labels must use the deterministic normalizer and centrally approved canonical labels exposed by `scripts/validate_downstream_coherence.py`; never add local alias tables or fallback matching.
- Label normalization may only case-fold, normalize whitespace, equate hyphen/underscore/space, or apply an explicitly approved central alias. It must never use fuzzy, nearest-match, keyword guessing, or ambiguous resolution.
- Keep requirement IDs, canonical IDs, snapshot IDs, owning targets, allocation classes, and approved mapping keys exact. Do not normalize or infer authoritative fields.
- Never encode a project name, identifier, block, signal, path, source tag, paragraph, or special-case branch in reusable logic. Do not infer from prior-project memory; report missing or ambiguous evidence instead.

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
13. Stage 4: Generate ARS
14. Stage 5: Generate DRS
15. Stage 6: Generate Digital IPOS
16. Stage 7: Generate Analog IPOS

Execution sequence: `S0 -> S1 -> S2 -> S2A -> S2B -> S2C -> S2D -> S2E -> S2F -> S2G -> S2H -> 3 -> 4 -> 5 -> 6 -> 7`.
Legacy numeric stage commands remain compatibility aliases during migration.

## Canonical Storage And Snapshot Rules
- The authoritative store is `data/canonical/canonical_store.sqlite`, managed by explicit migrations in `schema_migrations`.
- Canonical SQLite owns requirements, revisions, provenance, mappings, workflow state, approved profiles, snapshots, audit, rollback, merge operations, impact analysis, and report metadata.
- Canonical SQLite is the authoritative workflow store. Retrieval/index SQLite databases are separate, rebuildable, derived-only stores. CSV, JSON, Markdown, XLSX, and SysML are derived or compatibility artifacts only.
- SQLite/FTS5 is the current default retrieval backend, not permanent core workflow truth. Authoritative workflow code must not depend directly on retrieval schemas, FTS5/query internals, or index-specific helpers; retrieval must remain behind a replaceable bounded interface.
- `scripts/approved_vocabulary.py` and the approved vocabulary/profile resolver are the lexical authority. Domain vocabulary, aliases, stopwords, and expansions must remain aligned with approved vocabulary/profile context; duplicated local lexical resources are non-authoritative.
- The authoritative workflow is deterministic and local-only. It must not require LLM calls, network access, cloud services, remote model downloads, or generative retrieval/mapping.
- Downstream generation, reports, SysML, and authoritative GUI actions must consume one approved immutable snapshot through the approved resolver. GUI display and chat are non-authoritative. Before Stage 3-7 or downstream SysML regeneration, run `scripts/validate_downstream_coherence.py --snapshot-id <approved-id>`; it is the single read-only precondition for snapshot, ledger, partition, traceability, and non-inference coherence.
- **Stage 2 mapping-review handoff:** `artifacts/stage1_specs/architecture_mapping_preview.xlsx` is the reviewer-editable mapping surface; `architecture_mapping_preview.csv` becomes the authoritative machine-readable handoff only after verified synchronization from the saved, closed workbook. Before Stage 2A approval, Stage 2A execution, or Stage 2B snapshot freezing, run the shared `scripts/mapping_review_sync.py` boundary. It must reject unsaved/locked workbooks and duplicate, missing, unknown, or CSV/workbook-mismatched requirement IDs; never consume a stale mapping CSV or silently substitute it for the workbook.
- The workflow boundary is `staging -> reviewed merge -> canonical revision -> impact analysis -> approved mapping -> immutable snapshot -> snapshot-only generation`.
- At workflow start, select exactly one snapshot input: explicit `--snapshot-id` or `--use-latest-approved`. Resolve latest immediately to one explicit immutable ID, then pass only that `--snapshot-id <resolved_id>` to Stage 3-7, validators, generated artifacts, and optional downstream steps; never reselect latest downstream.
- Impacted snapshots remain forensic-only until re-approved or superseded.
- The local process username may be derived once from the GUI/generator runtime and used only for non-authoritative logging/audit actor fields and generated-document metadata. Every generated specification shall add `Author <runtime-user>` immediately after its `Snapshot ID` metadata on the first page. The runtime username must never select or alter snapshot, allocation, ownership, partition, traceability, approval, or explicit reviewer authority; reviewer fields remain explicit user-approved values.
- Every generated specification shall write the resolved immutable `Snapshot ID` used for that run. When regeneration uses a different snapshot than the existing generated document, increment the document version in its Version history table deterministically (`major.minor` -> `major.(minor+1)`); retain the current version when the snapshot is unchanged. Snapshot identity and document version are derived metadata only and must not alter requirement semantics, allocation, ownership, traceability, or approval authority.

## Project-Agnostic Allocation And Lineage Rules
- Use the centralized policy in `scripts/requirement_allocation_policy.py` for requirement allocation. Ownership and placement must come from approved allocation metadata, never from `approved_block`, source type, filename, ID, keywords, text, or project-specific names.
- Allowed allocation classes are exactly `system_level`, `top_digital_architecture`, `top_analog_architecture`, `block_local_digital`, `block_local_analog`, and `descriptive_only`.
- The owning target is policy-controlled: `system_level` -> `SRS`; `top_digital_architecture` -> `DRS`; `top_analog_architecture` -> `ARS`; `block_local_digital` -> `Digital IPOS`; `block_local_analog` -> `Analog IPOS`; `descriptive_only` -> `none`.
- Digital source-to-destination connection contracts belong to `top_digital_architecture` -> `DRS` unless the evidence proves a truly abstract end-to-end system capability.
- Do not invent artificial parents or duplicate one normative requirement across levels.
- Allowed lineage modes are `normal_hierarchical`, `direct_source_to_ipos`, `direct_supplementary_to_ipos`, and `split_lineage`. Use `normal_hierarchical` unless artifact evidence explicitly supports a direct or split path.
- Every approved mapping must carry a non-empty allocation class, policy-matching owning target, allocation rationale, lineage mode, source-origin IDs, and owning domain before approval or snapshot freeze. `hierarchy_parent_req_ids` is required only for the explicit parent-requiring `split_lineage` mode; it is optional for top-level SRS/DRS/ARS placement and direct-to-IPOS lineage. Source-derived provenance or `normal_hierarchical` placement alone is not parent evidence. Never infer parent IDs, use `approved_block` as hierarchy evidence, or force a top-level requirement under an artificial parent.
- Before S2B freeze, a mandatory historical-warning safety cleanup must classify every historical or superseded ingestion/provenance warning by severity and root cause. Once the active batch is uniquely established, non-current batches are non-authoritative for future coherence and fingerprint checks; they may be marked historical in the remediation report, while source artifacts remain preserved for audit. Cleanup must not modify approved requirements, mappings, or snapshots.
- A pre-freeze remediation step may auto-populate `hierarchy_parent_req_ids` only from one unique parent ID already present in approved canonical lineage/source authority. It must not derive parents from approved blocks, source type/spec names, keywords, similarity, naming patterns, or guessed roots; ambiguous or absent authority remains a human-review item after remediation is exhausted.
- Before unresolved hierarchy-parent cases are escalated, crosscheck synchronized `architecture_mapping_preview.csv` authority across identity, allocation, lineage, provenance, review, supplementary metadata, statement, and notes fields. Classify self-origin-only provenance, single or multiple explicit Covers candidates, missing parent evidence, lineage/allocation inconsistency, misflagged top-level cases, and irreducible human-review cases; only the last category is escalated after deterministic remediation is exhausted.
- At the mapping/lineage review approval boundary, preserve explicit supplementary-to-primary `[Covers: ...]` requirement references in a separate candidate-parent field. For an already approved lower-level row, select `hierarchy_parent_req_ids` only when exactly one referenced ID is itself an approved requirement; preserve multiple candidates without selection. Candidate provenance is not approval and must never be treated as a parent until the unique-authority rule passes.
- The allocation fields are authoritative review metadata after workbook-to-CSV synchronization and canonical persistence; downstream stages must consume them from the approved immutable snapshot and must not reconstruct them heuristically.
- The existing central downstream validator-orchestrator (`scripts/validate_downstream_coherence.py`) is the single downstream source of truth and shared contract provider for snapshot binding, approved allocation lookup, partition enforcement, required metadata, `valid_empty` handling, concrete block ownership, and crosscheck expectations. Derived downstream artifacts must follow this central contract.
- Approved architecture mapping workbook/CSV and approved canonical snapshot/SQLite materialization are the sole architectural authority. Stage 2 SysML is derived structural output for review and visualization only; it is not allocation, ownership, placement, or architectural-foundation authority, and a rejected Stage 2 SysML review does not invalidate approved authority.
- Stage 3 SysML structural review scope is resolved from the selected approved snapshot and its approved architecture mapping/allocation metadata. Only concrete blocks with approved Digital IPOS or Analog IPOS requirement scope are required in the Stage 3 model set; blocks, ports, or tables appearing only in inventories, OCR output, source I/O catalogs, or legacy block lists must never expand that scope.
- The same validator-orchestrator owns deterministic human-label normalization for logical owner, block, and display comparisons. SysML and downstream scripts must call that shared API; they must not use raw exact label equality or recreate aliases locally.
- The central validator-orchestrator also owns SysML derived-artifact coherence. It must verify, against the selected snapshot and current traceability artifacts, that the system SysML mirrors approved SRS rows, `DigitalSubsystem.sysml` mirrors approved DRS rows, each represented block mirrors its approved IPOS rows, and each block's approved `sourceName` port map is present. Every mirrored row must preserve its exact authored/source ID and complete requirement description; valid-empty partitions remain valid-empty.
- The central validator-orchestrator must also reconcile every approved `source_port_catalog.csv` row, owner-scoped and direction-scoped, against every generated Digital and Analog IPOS block Markdown and DOCX Source I/O table. Missing or unapproved rendered ports are blocking findings; this check covers all source pages and all materialized blocks, not only recently repaired continuation pages.
- SysML block-file materialization is bound to `created_ipos_block_directories()`: the final SysML block set must equal the concrete blocks with generated Digital or Analog IPOS Markdown/DOCX artifacts. The central validator must reject stale SysML block files and missing SysML files for created IPOS blocks; a valid-empty IPOS partition has no SysML block files.
- An IPOS block document exists only for a concrete block with one or more approved block-local IPOS rows in the selected snapshot. Do not generate a Digital or Analog IPOS document, block directory, descriptive audit, or DOCX for an inventory block with no mapped IPOS requirements. The central validator-orchestrator must reject stale or empty IPOS block directories; an entirely empty IPOS partition remains valid-empty with no block documents.
- The central helper `created_ipos_block_directories()` is the sole artifact-discovery rule for downstream views: a block is created only when its IPOS directory contains a generated Markdown or DOCX document. The System Traceability hierarchy may list only those created blocks and must omit valid-empty IPOS partitions and configured-but-unmaterialized inventory blocks.
- SRS, ARS, DRS, IPOS generators, and downstream crosschecks must call the central downstream validator-orchestrator for shared rules. Stage-specific scripts are limited to stage-local generation and formatting; they must not reimplement shared ownership, partition, placement, metadata, or snapshot decisions.
- No local fallback inference is permitted for ownership, partition, or requirement placement. An approved-empty partition is valid when its output is empty and snapshot-coherent, while required metadata headers remain present.

## IPOS Internal-Link Integrity
- `templates/MPT_IPOS_template.docx` is the deterministic IPOS DOCX presentation baseline only. It may provide page geometry, section setup, title/subtitle and heading presentation, headers/footers, table rendering, theme, and general document structure. Generated Markdown remains the sole content source; the template body, placeholders, sample sections, sample requirement blocks, sample `Covers:` text, and sample `[End]` blocks are never authoritative and must not leak into output.
- The template styles `STReq`, `STMacroReq`, and their `NoSpacing` inheritance chain must not define authored IPOS requirement formatting. The IPOS generator and shared DOCX formatter remain authoritative for exact requirement text, `Covers:`, `[End]`, requirement spacing, and requirement presentation. The shared post-processing boundary remains authoritative for final navigation order, page numbering, and layout normalization.
- All generated SRS, ARS, DRS, and IPOS DOCX files must use the shared
	`apply_docx_common_spec_formatting` layout boundary. It shall produce a
	title-and-metadata first page, place the table of contents first on page 2,
	place Document Navigation after the TOC, and
	render a right-aligned PAGE field in the default footer. This is a rendered
	layout rule only and must not alter Markdown synthesis, requirement IDs,
	traceability, allocation, ownership, snapshot binding, or source content.
- Every generated Digital IPOS and Analog IPOS document must emit deterministic unique anchors for every section, subsection, and authored requirement entry.
- Every generated same-document Markdown link and requirement-navigation link must target an anchor emitted in that same document. Link integrity is a stage-local output property; it must not alter requirement IDs, `Covers` fields, snapshot IDs, allocation, ownership, traceability, or the central downstream contract.
- IPOS gates must validate Markdown targets and generated DOCX internal targets through the existing stage gate path. This check validates rendered outputs only and must not become a parallel authority or downstream contract validator.
- The shared IPOS DOCX formatter and existing IPOS gate jointly enforce the rendered layout: page 1 contains the document title and metadata; the Table of contents is first on page 2; `Document Navigation` follows the TOC; and the default footer has a bottom-right PAGE field. This is a shared layout check, not a new policy or validator.

## IPOS Descriptive Synthesis
- The shared Block Overview contract applies to SRS, DRS, ARS, Digital IPOS, and Analog IPOS: `Functionality` is a non-bulleted macro-purpose paragraph of up to three sentences; `Supported functions and scope` contains distinct capability families, protocols, limits, boundaries, and exclusions attested by approved block-local evidence; `Internal blocks or functions` is emitted only for evidence-supported logical organization. Each retained section must add information rather than repeat an earlier section; examples define content shape only and never authorize hardcoded project facts.
- IPOS authoritative requirement blocks are governed only by the existing central downstream validator-orchestrator. For Digital IPOS and Analog IPOS, every block must render exactly as `IPOS-<concrete-approved-block-name>-xxx`, the exact approved requirement text, `Covers: <exact-approved-upstream-req_id>`, and `[End]`, in that order with no additional authored-block lines. The block token derives from the concrete approved block name using deterministic uppercase hyphen separation; `xxx` is the stable three-digit sequence within that IPOS document. This rule applies only to IPOS, never DRS; the traceability matrix remains the approved provenance record.
- IPOS descriptive overview sections are governed centrally by the existing downstream validator-orchestrator contract and its shared deterministic descriptive assembly boundary. The shared composer is the only policy implementation for IPOS descriptive evidence admissibility, topic assignment, scope, omission, and gate expectations; renderers may not add local heuristics. For high-level overview synthesis, approved block-inventory function evidence is the sole default source. Isolated requirement, interface, parameter, register, address, timer, version, connection, and value fragments must not establish overview topics. Approved same-block requirements may nevertheless support complete functional relationships, including configurable acquisition intervals, sequencing, timing dependencies, and data/math behavior, within the inventory-bounded scope; do not discard those relationships merely because their source mentions a parameter or time.
- IPOS descriptive overview sections are block-local only. For materialized IPOS, the common functional authority is the approved snapshot plus approved `block_inventory.csv` `Function`, `Inputs`, and `Outputs`; same-block approved IPOS requirement rows and separately approved block-local descriptions are local refinement evidence only. Composition is top-down and may add detail but never alter semantics, ownership, or responsibility. Never use generated DRS prose or isolated keywords, tables, or signal lists as capability authority. `1.1 Functionality` and `1.2 Supported functions and scope` are always present and non-empty; valid-empty partitions produce no IPOS document. SRS/DRS are not changed in this phase.
- For every materialized Digital or Analog IPOS block in any project, `1.1 Functionality` and `1.2 Supported functions and scope` must read as natural technical documentation, not as a template, requirement, or explanation of the generation process. Final Markdown and DOCX must not contain `approved macro-purpose`, `approved ... function`, `local scope covers`, source-evidence/audit language, or equivalent governance scaffolding in these sections. The shared composer must derive prose deterministically from the same approved block-local function, I/O, and admitted refinements; the shared output validator must reject process wording independently of composer parity. Do not add block/project-specific rewrites, widen authority inputs, or weaken contributor provenance to pass this gate. A full rollout passes only when every materialized IPOS block meets the same rendered-text contract.
- The shared deterministic functional-summary composer re-elaborates approved block-function evidence into macro-purpose and uses approved local requirement/interface evidence only for distinct capability families or supported internal organization. Scope summaries preserve each supported behavior's action and object, retain meaningful context when supported, and group closely related same-block refinements into a bounded sub-function summary only when each distinct supported object or qualifier remains explicit and audit-linked. Each sub-function summary has a concise title/purpose line plus at most one inventory-bounded local-relationship line; they must not collapse distinct objects into generic verb-family labels or render one entry per accepted refinement. It must never emit filler, raw evidence, requirement wording, IDs, markers, parameter/register/timer/value fragments, or port counts; unsupported sections are omitted and authoritative Block requirements remain exact.
- IPOS descriptive rendering must use one shared deterministic aggregation path for every materialized block. It must aggregate the complete accepted same-block evidence set, preserve distinct supported responsibilities and explicit local interactions, deduplicate only equivalent responsibility phrases, and order contributors deterministically by admitted evidence order. RRF, rank-based facet selection, and fixed facet-count truncation are prohibited in IPOS descriptive rendering and its audits. RRF is reserved for Hybrid RAG retrieval/query fusion and retrieval benchmarks only.
- IPOS topic assignment must use the shared `assign_ipos_descriptive_topic` decision model. It evaluates deterministic topic vocabulary only against admissible functional evidence, never source IDs, provenance, artifact paths, ownership labels, source-metadata keywords, or isolated shared tokens such as `reset`, `signal`, `memory`, or an acronym substring. Power/clock/reset summaries require a supported functional combination; register/configuration/status semantics take precedence over incidental reset mentions; DSP requires explicit standalone signal-processing evidence. It scores all eligible topics, selects only one unique strongest match, and omits no-match or tied evidence. The descriptive audit must record the selected topic, matched functional evidence, and selection or rejection reason.
- Raw source IDs, `[TO: ...]` tags, and exact authoritative requirement statements must not appear in IPOS descriptive overview text. When supported synthesis cannot be produced, omit the descriptive entry.
- Every retained IPOS descriptive summary must retain approved provenance in `descriptive_summary_audit.csv`. The IPOS gate may enforce shared-topic and rendered-output invariants only, while snapshot, allocation, ownership, traceability, and downstream-contract decisions remain owned by the existing central validator-orchestrator.

### Approved Normative Evidence And Descriptive Projection
- Every applicable piece of text explicitly approved for the selected snapshot and block, whether extracted from requirements or subsequently approved as a description, must enter the IPOS evidence inventory with its approval and provenance. Preserve exact normative requirements in the requirement section; use supported functional meaning in the appropriate descriptive section without copying normative prose. Account for each distinct supported action, object, condition, calculation, and interaction in the rendered output and audit. Do not treat mere citation of an ID, shared keyword, or generic title as semantic coverage; unsupported, conflicting, or unreadable fragments require a specific auditable gap instead of silent omission or invented completion. An approved description does not by itself alter allocation, ownership, or the snapshot authority boundary.
- `shall define` in the same sentence is not a contradiction: `shall` expresses the normative modality and `define` expresses the predicate. A tagged, approved, same-block requirement remains eligible as supporting descriptive evidence when it establishes a functional relationship. A tag alone is not approval; retain the existing snapshot, ownership, scope, conflict, and provenance checks.
- Separate source eligibility from output wording. Preserve the exact approved requirement in normative artifacts. In descriptive prose, express its supported meaning without normative modality or raw requirement copying. Never classify an otherwise supported relationship as `suppressed_due_to_normative_reuse` solely because it contains `shall define`, because `define` is absent from an action vocabulary, or because the sentence contains timing/configuration terms.
- Preserve the complete subject/action/object relationship and meaningful qualifiers. Do not truncate at isolated words such as `time`, `number`, `parameter`, or `value`; distinguish raw implementation fields from the functional behavior they control. An output such as `Defines how many.` is an incomplete projection, not a valid summary. Group useful evidence into the relevant function or algorithm entry rather than emitting fragmentary micro-steps.
- Conditional or passive signal statements can express functional behavior, not just interface detail. An initial `When` introduces a condition; it must not erase the action object when projecting a passive predicate. Where approved same-block evidence explicitly connects a condition, signal action, functional effect, and state transition, preserve that relationship in descriptive form; do not reject it solely for using `shall be set` or signal identifiers. Supported internal behaviors and data/math algorithms do not require a literal FSM label to be described. Group related evidence into a useful function entry without inferring a new architectural block or completing missing source clauses.
- Descriptive coverage must preserve supported behavior, not merely mention its name or timing in another summary. A related FSM entry or an audit-linked contributor ID alone does not prove that initiation, evolution, completion, or interactions are represented. Check each of those aspects only where attested by approved evidence and record any projection gap; do not invent absent aspects or treat an upstream approval as automatic descriptive coverage.
- An unsupported parser construction is a projection gap, not evidence of missing source information or missing approval. Record the gap without changing approved source text or authority. Assess existing approved evidence before requiring a new upstream approval cycle. Formula layout that is ambiguous in extracted text must not be reconstructed by inference; a clearly supported qualitative relationship may still be described.
- These rules are project-agnostic. The following cases are user-requested traceable examples only, not a capability catalogue, rendering template, identifier-based exception, or source of new approval. This documentation update does not activate the experimental renderer, regenerate IPOS, or roll out behavior beyond the pilot.

#### Traceable Approved Example (Not Executable Policy)
- Requirement: `IPOS_STBIO1_MAIN_CONTROLLER_088`; reviewed owner: `Main Controller`; review decision: `approved`; allocation: `block_local_digital`; target: `Digital IPOS`.
- Evidence: `artifacts/stage1_specs/architecture_mapping_preview.csv` and the verified requirement text for snapshot `snap-b2e8101b00dc6909feaed885`. These identifiers locate the example only; runtime authority must still be resolved through the approved snapshot boundary.
- Exact approved extracted text:

> The i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] shall define how many time slots pass between two GSR acquisitions following this formula: GSRdata = time_slot 2 ∗ m_gsr

- Supported qualitative meaning: the configuration parameter determines how many time slots separate two GSR acquisitions. Integrate this meaning into the relevant acquisition-function description with provenance. Preserve the extracted formula as source text; do not infer missing mathematical operators or layout from this example.

#### Traceable Digital Ramp Example (Not Executable Policy)
- Requirement: `IPOS_STBIO1_MAIN_CONTROLLER_104`; reviewed owner: `Main Controller`; review decision: `approved` in `artifacts/stage1_specs/architecture_mapping_preview.csv`.
- Exact approved extracted text:

> When in FIRST_ALC_SAMPLES state, when i_end_average is set to 1, the o_start_digital_ramp signal shall be set high to start the rising of the digital ramp and go into the RISING_RAMP state.

- Supported meaning: in the specified initial sampling state, assertion of the averaging-completion input triggers the rising digital ramp and the transition to the rising-ramp state. This is functional sequencing evidence, not an isolated signal fragment. It supports the initiation relationship, not an entire ramp algorithm by itself; further behavior requires its own approved evidence.
- Observed projection gap: the persisted Main Controller `descriptive_summary_audit.csv` classifies this candidate as `suppressed_due_to_normative_reuse` with no candidate refinement. The existing `1.2` PPG FSM summary mentions rising/falling-ramp timing but does not preserve this initiation relationship or provide a distinct ramp-function description. Neither the timing mention nor retention in normative requirements resolves that descriptive gap. This example documents the gap only; it does not change the parser or regenerate the document.

## Downstream Traceability And Final SysML Rules
- Stages 3, 4, 5, 6, and 7 must each generate their own stage-specific document, traceability matrix, crosscheck outputs, and deterministic statistics from the same approved snapshot and central downstream contract.
- Stage-specific matrices, reports, and statistics remain visible as independent artifacts. GUI refresh, stage status, and traceability views must consume those generated outputs; they must not substitute a later aggregate report for a missing stage artifact.
- Stage 3 SysML review is limited to local structural checks: model-set completeness, block/endpoint consistency, naming, approved source I/O representation, and source interaction/XBAR edge structure. It must not decide full requirement coverage, allocation, ownership, partition validity, or end-to-end SysML coherence.
- Any Stage 2 SysML review gate is a derived-artifact workflow deliverable only. It must not block snapshot-authorized downstream generation by implying that architectural authority is missing; final SysML remains a separate snapshot- and contract-bound downstream phase.
- Full SysML generation and requirement coverage/coherence validation occur only in the dedicated final SysML phase after the required downstream documents are available. That phase must generate the complete SysML set with the same approved snapshot-bound data and `DownstreamContract` used by SRS, DRS, ARS, and IPOS generation, then invoke `scripts/validate_downstream_coherence.py` as the single end-to-end authority.
- The final SysML phase must use the same approved allocation class, owning target, partition, owner normalization, created-IPOS block set, source IDs, traceability matrices, port maps, and snapshot/contract fingerprint data as the generated specifications. It must not introduce a parallel validator, local coverage algorithm, authority source, or snapshot selection.

## Shared Descriptive-Summary Contract
- **Preferred SRS introductory writing rule:** `srs-introductory-authority-bounded-v1`, centralized in `SRS_INTRODUCTORY_WRITING_RULE` in `scripts/workflow_routing.py`, is the frozen preference for SRS introduction and terminology. Use concise, natural, professional prose bounded by the selected approved content. Present requirements and supporting context without promising complete coverage, establishing allocation, or asserting unsupported behavior, performance or implementation detail. Scope describes only allocated requirements and supported context, including valid-empty partitions; document headings and glossary entries do not establish technical coverage.
- For SRS terminology, describe terms as reading aids. Applicable meanings, operating conditions, limits and acceptance criteria remain bounded by approved content; definitions cannot introduce independent authority, obligations, supported features or architectural ownership. Reference listings do not establish applicability or approval. Preserve the existing literal category conventions rather than rewriting their policy meaning.
- Keep this preference in the explicit SRS document-content profile, not shared defaults. Centralized rules contain no project, block, signal, threshold or example-specific prose. DRS, ARS and IPOS retain their own profiles and wording; this rule does not activate or migrate them. Persist the writing-rule identity/fingerprint as derived presentation metadata and validate it through existing SRS boundaries. Deliberate future changes to the frozen preference require explicit authorization and an updated rule version; neither the rule nor its fingerprint creates canonical approval or snapshot authority.
- The single deterministic flow is admissible evidence -> structured facts -> compatible aggregation -> paragraph composition -> audit linkage -> independent validation. Reuse existing `NormalizedSourceRecord` and `SemanticUnit` contracts; admission verifies caller-supplied workflow eligibility and never creates approval, ownership, allocation, snapshot or source authority.
- Every runtime caller must supply a versioned explicit document profile. Profile controls declare allowed scopes, evidence kinds, authority tiers, owner policy, domains/layers, projection adapters, topic roles, detail exclusions and activation. Empty domain/layer/detail controls mean explicitly unrestricted, not inherited SRS rules. Shared invariants retain all projected facts and contributors in input order, audit unsupported projections and exclusions, and prohibit silent output caps or normative rendered prose.
- SRS is the only active adopter of the normalized fact flow. DRS digital-integration, ARS analog/mixed-signal-integration and later IPOS same-owner block-local profiles are declared extension hooks only, with runtime activation disabled. Policy tests may inspect these boundaries without enabling generators. Their existing descriptive paths remain unchanged until separately authorized and validated.
- SRS profile-specific implementation-detail/block-local exclusions are not shared defaults. DRS and ARS profiles constrain their approved integration domain/layer; IPOS permits approved same-owner normative refinement evidence and legitimate local detail, preserving normative source text separately. Neither profile discovery nor adapter registration promotes evidence authority.
- Persist profile version/fingerprint, adapter identity, normalized source-record linkage, fact contributors and semantic-unit linkage in derived audits. Validate these links and final artifact text independently; audit IDs and presentation profiles are not canonical approval/snapshot metadata. Reject unknown profiles/adapters and altered or inactive built-in runtime profiles rather than falling back to SRS.
- SRS System Overview is a deterministic projection of already admitted system/architecture evidence, not an authority-discovery stage. Reconsider all scoped candidates before declaring an overview section unsupported; a separate topic/output cap or prior audit rejection alone is not evidence of authority absence. Do not add sources, widen snapshot scope, or import parallel-document authority.
- Keep the seven SRS overview roles distinct: identify the product; summarize top-level capabilities; aggregate functional domains; explain external/system boundaries; describe operating-mode roles; summarize only supported top-level power/clock/reset structure; and state engineering scope, assumptions, and allocation boundaries. Do not fill a section from block inventories, port/signal presence, connection lists, or generator/audit metadata.
- For SRS System Overview, render natural technical prose from complete, scoped evidence. Exclude OCR fragments, stitched tables, paths, block-local purpose prose, implementation detail, normative wording, and audit language. These SRS exclusions do not prohibit approved block-local functional refinement in IPOS. Preserve descriptive provenance in audit artifacts and normative traceability only through approved mechanisms. When a role is not described, state that narrow technical gap without inventing behavior or leaving spacer-only content.
- Within SRS overview, deduplicate concepts across sections and remove repeated block-purpose prose from subsystem lists and data-path summaries. Repeated structured items use a distinct bold item name and indented attributes; tables support a system-level explanation and never replace it with a raw dump. Other profiles define their own topic roles and detail boundaries.
- The SRS overview composer and independent output validator are centralized and project-agnostic. Generic vocabulary may classify scoped evidence but cannot create a capability, domain, interface role, operating mode, or power behavior. Do not hardcode project, block, signal, or review-example names.
- SRS, DRS, ARS, Digital IPOS, Analog IPOS, and any future approved block- or layer-level generated specification may render configured descriptive overview sections, including System Main Functions, Digital Main Functions, Analog Main Functions, Operating Modes, Power States, and other explicitly configured topics.
- Descriptive summaries are derived, non-authoritative outputs. They are not requirement sources and must never create or modify requirement authority, canonical approval state, mapping authority, block/layer ownership authority, provenance, or any source-of-truth artifact.
- A descriptive renderer must not create a new requirement ID, obligation, `shall` statement, acceptance criterion, design decision, ownership decision, or unstated architectural meaning. Approved normative evidence may contribute as source evidence when rendered as descriptive, provenance-preserving context; it must not be rewritten into new normative prose.
- Descriptive assembly must be deterministic, local-only, offline, rule-based, reviewable, and reproducible from the same approved immutable snapshot plus the same configuration, vocabulary, taxonomy, profile, and adapter inputs. It must not require an LLM, network, cloud service, or remote model.
- The reusable writing core projects admitted evidence into explicit descriptive facts (subject, action, objects, polarity, modality, conditions, mode, qualifiers, results and exact provenance), then aggregates only compatible facts and renders deterministic paragraphs. Preserve distinct actions and every contributor; do not merge alternatives, different conditions, modes, polarity or modal strength. Vocabulary classifies evidence but cannot supply a missing relationship. Fact IDs are derived audit identifiers, never requirement IDs or new authority.
- Unsupported constructions are projection gaps in the audit, not proof that source evidence or approval is absent. Do not silently truncate meaningful qualifiers or promote conditional/optional behavior to unconditional behavior. Document-specific adapters define supported constructions; this is not a general semantic parser or a proof of complete source meaning.
- Independently check contributor coverage and retained factual terms, qualifiers, polarity and modality; validate persisted contributor IDs and selected sentences against final Markdown and DOCX without comparing only with recomposed expected prose. Keep these descriptive checks within existing stage/central validation boundaries.
- The structured fact-to-prose rollout is activated first for SRS overview capabilities, modes, functional responsibilities and supported power relationships. Other descriptive paths retain their existing behavior until separately migrated and validated. Future DRS/ARS/IPOS adapters reuse the core with explicit document profiles, not inherited SRS exclusions; IPOS may use approved same-block normative rows as refinement evidence while preserving exact normative output and removing normative modality only in the derived description.
- Allowed evidence is limited to approved snapshot rows, approved mappings, approved structural/interface/context evidence, approved descriptive artifacts, and approved vocabulary/taxonomy/profile signals governed by the workflow. Scope, domain, block, and layer filters must be explicit.
- Source-backed architecture descriptions may be reused across SRS, ARS, DRS, and approved layer-level specifications when their scope is explicit and their wording remains descriptive. Project-agnostic capability vocabulary may cover system-on-chip or subsystem role, analog front end or mixed-signal integration, sensor and external interfaces, data paths and buffering, host protocols, embedded processing, register/configuration access, power domains, clock/reset coordination, interrupts/status, boot, test, and low-power states. These terms guide classification only; they never create evidence or requirements.
- Traceability follows content type: authored normative ARS/DRS requirements derived from SRS retain `Covers: SRS-REQ-xxx`; descriptive source-backed sentences and capabilities retain source/provenance audit links but do not create normative `Covers` dependencies.
- Migrated generated specs must use the shared descriptive flow in `scripts/workflow_routing.py` or its approved successor. Document differences are explicit profiles/adapters, not generator-local selection/composition algorithms. Legacy DRS/ARS/IPOS paths remain unchanged during SRS-first adoption; this rule does not activate or silently migrate them.
- Primary evidence selection uses deterministic lexical/normalized signals together with approved category/type, structural/context, ownership, vocabulary, taxonomy/profile, and provenance signals. Optional local hybrid/semantic retrieval may widen candidate discovery only when deterministic coverage is weak; similarity alone is never sufficient, and every widened candidate must pass the same deterministic eligibility and scope checks.
- Operating Modes and Power States must not depend primarily on fixed headings, project-specific labels, or hardcoded mode names. They use the shared assembly path and reusable configured category signals. Project-specific refinements must be explicit, reviewable, and adapter/configuration based.
- Power and low-power architecture is a project-agnostic descriptive topic family. Use the shared low-power retrieval/assembly contract and explicit scope profiles for SRS, DRS, and ARS; do not add generator-specific keyword truth.
- Low-power topic seeds are configuration-, vocabulary-, and taxonomy-driven retrieval aids. Candidate discovery uses lexical, normalized, and RRF retrieval by default. Optional local semantic widening is gated, one-shot, non-authoritative, and never sufficient by similarity alone.
- SRS renders system-level power/domain architecture and coordination; DRS renders only approved digital/top-digital/shared-domain integration behavior; ARS renders analog or mixed-signal supply, bias, domain, sequencing, retention, isolation, and wake-up behavior. DRS block-local evidence cannot establish top-level coverage.
- Low-power descriptive audits are emitted beside each generated specification as `descriptive_low_power_audit.csv` and must expose query seed, candidate provenance, selected/rejected evidence, scope/domain decisions, deduplication, exclusion reasons, and final topic order.
- Descriptive low-power output remains derived, non-authoritative, provenance-preserving, reproducible, local-only, and free of new requirements, new `shall` statements, or invented filler.
- Empty topics are omitted by default. Explicit insufficient-evidence text is allowed only when required by a document contract or review-visibility configuration; generators must not add filler content.
- Output limits, when configured, must be stable, topic-configured, deterministic, and auditable. They must record selected evidence, rejected evidence and reason, topic assignment, duplicate handling, ordering, truncation, scope/ownership filtering, and omitted-versus-insufficient outcomes.

## Revision, Provenance, And Approval Rules
- Preserve multiple supplementary specifications and revisions, including source/revision IDs, source name, revision number/date, kind/scope, target scope, applicable blocks/layer, ingestion/staging batches, review, merge, and impact references.
- Same `req_id` with different text must preserve both source versions and provenance. A latest revision/date may be recorded only as a proposed winner, with approval required.
- Keep proposed/approved classification, classification reason/method/confidence, and review comment as separate fields.
- Keep lifecycle state separate from semantic approval/category transitions and validate transitions centrally. Never silently revoke approvals.
- Taxonomy, vocabulary, and architecture profiles are revisioned; candidate revisions are not approved implicitly.
- Snapshot IDs are deterministic content/configuration-derived identities including canonical revisions, mappings, profile hashes, retrieval configuration, and semantic-enabled metadata.
- Semantic retrieval is optional, local-only, version-pinned, auditable, and never required for the deterministic core. GUI chat is visibly non-authoritative.

## Step 3 Workflow Enforcement Rules
- Persist and centrally validate workflow states: `ingested`, `parsed`, `classified`, `under_review`, `impact_analyzed`, `approved_for_merge`, `merged`, `mapping_under_review`, `mapping_approved`, `snapshotted`, `rejected`, and `needs_rework`.
- Record every transition with actor, reason, approval requirement, timestamp, and metadata. Loopbacks add history and never erase prior state.
- Before merge approval, run deterministic impact analysis for affected requirements, classifications, mappings, approved profiles, snapshots, downstream targets, identity ambiguities, scope, and full versus partial regeneration.
- Merge only through the canonical SQLite approval path. Staged objects create new canonical revisions and provenance; they never overwrite canonical text in place.
- Use explicit categories `new`, `duplication`, `refines`, `conflict`, and `removed`. Semantic/category changes require approval; conflicts never auto-merge; removals preserve rationale and lineage.
- Same-ID different-text conflicts preserve both source versions and remain approval-required. The latest source revision/date is only a proposed winner.
- Mark affected mappings, profiles, and snapshots as impacted or requiring re-review; never delete history or silently revoke approvals.
- Architecture Map Review may modify mapping allocation and coverage decisions only. It must not modify canonical text, provenance, approved classification, or merge category. Identity/classification defects must create a tracked loopback.
- Legacy supplementary ingestion may continue producing compatibility CSV/XLSX/JSON, but canonical SQLite staging, impact analysis, approval, and merge are authoritative.

## Step 4 Authority, Audit, And Rollback Rules
- Record event-level audit events for source import, parsing, ID validation, classification, review, impact analysis, merge, mapping, snapshot, rollback, vocabulary/taxonomy, retrieval, semantic fallback, SysML, report, and conflict-review actions.
- Rollback never deletes history. It creates a rollback record, tracked state/revision, audit event, and explicit `new_snapshot_required` indication.
- Create approved snapshots only through the canonical snapshot manager. Snapshot identity must include canonical revisions, approved mappings, approved profile hashes, retrieval configuration, semantic flags, and traceability context.
- Authoritative classification, review, snapshot, SysML, report, and downstream generation paths must resolve approved vocabulary/taxonomy/profile context through the approved resolver. Mutable compatibility files and unapproved profiles are not authoritative.
- SRS, DRS, ARS, Digital IPOS, Analog IPOS, SysML generation, validators, and optional/future downstream generation must consume the one immutable snapshot ID selected at workflow start. Only the workflow entry boundary may accept `--use-latest-approved`; downstream commands must receive `--snapshot-id <resolved_id>`.
- Impacted, incomplete, or project-mismatched snapshots must be rejected for authoritative generation.
- Architecture Map Review may affect future snapshots but must not directly mutate generated SysML or downstream reports.
- Conflict review output may show the latest source revision/date as the proposed winner, but it is derived evidence and cannot decide a merge automatically.

## S0 Primary Source Bootstrap Rules
- S0 may run a deterministic local assessment on the user-selected primary source before OCR.
- Once explicitly approved, the primary source and its approved immutable metadata are the deterministic bootstrap context for applicable OCR, local RAG preparation, vocabulary context, and taxonomy processing. Supplementary sources are additive and do not replace that bootstrap context.
- Report only `tagged`, `untagged`, or `ambiguous` status, a proposed base req-ID prefix, preserved evidence, and a reason.
- Inspect configured req-ID patterns in both narrative and table contexts. Normalize table headers so `Req-ID`, `Req_ID`, `Req Id`, `Requirement ID`, and equivalent forms are recognized.
- Status and prefix are proposals only. Never silently approve, change, or promote the active primary source baseline. Store candidate metadata as pending profile context until explicit user approval, edit, or rejection.
- Source-selection UI, approval/edit/reject controls, and primary-baseline promotion are deferred to Step 5.

Derived output and GUI boundaries:
- SRS/ARS/DRS XLSX and SysML outputs are snapshot-derived and must expose the approved snapshot/provenance context.
- SysML includes all approved requirements relevant to represented created-IPOS blocks by default; partial export requires an explicit opt-in and must be recorded.
- Generated SysML structure is contractual: the top-level system model reflects SRS, the digital subsystem reflects DRS, and each concrete block reflects the corresponding IPOS traceability matrix with complete descriptions and the approved port map. These checks are centralized in `validate_downstream_coherence.py` and must not be replaced by generator-local heuristics.
- `artifacts/validation/authority_consistency_scan.json` is diagnostic only. Residual SysML aliases, Stage 1 tagged-source rules, Stage 2 source-derived adapters, and legacy architecture evidence rules must remain explicitly documented or configuration/adaptor-backed rather than being mistaken for reusable core policy.
- The GUI is non-authoritative. Pure status/action helpers are testable without Tk; full display-session and Excel interaction remains an explicit runtime limitation.

## Compatibility Boundary Hardening
- Direct compatibility callables must fail closed unless they receive an explicit approved snapshot selector or explicit legacy/migration opt-in.
- `load_approved_input`, `freeze_legacy_export`, and direct IPOS callable compatibility are non-authoritative, must carry deprecation guidance, and must not be used by default GUI, CLI, stage runners, validators, or report generation.
- Compatibility exports may write derived artifacts only; they must not imply canonical approval, snapshot authority, or workflow state.
- Stage mapping/classification must prefer approved canonical classification context. Staged CSV category fields are review evidence, not authoritative decisions.
- Run `scripts/authority_consistency_scan.py` during cleanup validation. Review findings for legacy resolver calls, mutable artifact reads, hardcoded project identifiers, and embedded lexical resources; explicit source-derived adapters and legacy-only compatibility boundaries must remain documented.

Supplementary source review is additive after the primary source completes Stage 2. Accepted rows are added to the updated integrated source baseline. The follow-on loop is an incremental refresh/recompute, not a destructive restart: invalidate and regenerate the current canonical corpus, architecture review mapping, approved mapping snapshot, hierarchical specifications, and SysML traceability through Stage 0, Stage 1 OCR/tag extraction, Stage 2, Architecture Map Review, and Stage 2A. Preserve prior approvals, review workbooks, workflow manifests, and artifact history for audit; changed evidence requires fresh current approval hashes, while prior approvals remain historical.

## Stage Progression Invariants
- Execute the workflow as a strict forward-only pipeline: a run may execute one stage or an ascending contiguous range beginning at any stage in `0 -> 1 -> 2 -> 2A -> 3 -> 4 -> 5 -> 6 -> 7`.
- Every `workflow_cli.py run` workflow execution must run the focused regression/retrieval test suite once before any selected stage. A failure stops the workflow before execution; results are recorded in `artifacts/orchestrator/workflow_cli_runs.jsonl`. The project retrieval benchmark remains Stage 0-specific. Validation-only commands and the Stage 2A-to-DRS shortcut do not run workflow preflight tests.
- Do not retry, loop, skip within a selected range, or return to an earlier stage during ordinary execution. The sole explicit loopback is the post-Stage-2 supplementary refresh: after accepted rows are merged, the GUI reruns Stage 0, Stage 1 OCR/tag extraction, and Stage 2 before continuing to architecture review.
- The Stage 2A-to-DRS requirements-only shortcut is allowed because it is a forward transition; no Stage 3, 4, or 5 path may invoke an earlier stage.
- Architecture comparison is an optional command (`workflow_cli.py arch-compare --project-to-compare <project_name>`), separate from numbered workflow stages. Numbered Stage 6 is Digital IPOS and Stage 7 is Analog IPOS; both are snapshot-backed and use the immutable ID selected at workflow start. Optional and future downstream steps must accept and propagate that same ID.
- Never advance a stage without required artifacts and required crosscheck report.
- A gate cannot pass with unresolved critical findings.
- Stage 1 is blocked if Stage 0 has unresolved critical semantic issues.
- Stage 3, Stage 4, and Stage 5 are blocked if Stage 2A architectural crosscheck has unresolved critical issues.
- All Stage 0-7 fixes and generated outputs must follow the Project-Agnostic Policy above.

## Efficiency Protocol (Mandatory)
- Keep each chat scoped to one stage or one failure class. Do not mix Stage 1 and Stage 3+ fixes in the same thread.
- Trigger context compaction every 25 to 30 turns, or immediately after a stage boundary.
- After any FAIL result, summarize root cause, patch scope, and next command in 5 lines or less before continuing.
- Do not perform corrective loops inside one workflow execution; publish the blocker and rerun only after correction, using a single stage or ascending range.
- Prefer specialized stage agents for generation and crosscheck work; keep orchestrator decisions concise and artifact-grounded.

## Non-Negotiable Correction Guardrails
- Never output generated standard IDs in tagged-source mode.
- Do not treat an image, figure, table label, legend, encoded-value enumeration, or other descriptive graphic content as a DDS-tagged requirement. A source ID may be preserved only when it belongs to an explicit normative statement or a structurally defined requirement row.
- Image-derived behavior must be captured only after the full function/signal names are available from the rendered source image. Create one source-faithful requirement per distinct depicted function, use explicit image/figure provenance, and leave `source_req_id` and `covered_source_req_id` empty unless the image itself explicitly associates that function with a source requirement ID. Never infer a DDS relationship from page proximity, OCR order, or adjacent text.
- SRS authored requirements must use unique `SRS-REQ-xxx` IDs; ARS authored requirements must use unique `ARS-REQ-xxx` IDs; DRS authored requirements must use unique `DRS-REQ-xxx` IDs, where `xxx` is exactly three decimal digits (`001`-`999`). Never reuse an authored ID within its artifact or substitute another artifact's ID namespace.
- Never claim PASS when any hard check is failing.
- Never modify unrelated stages while fixing a single stage gate issue.
- Never drop requirement sentence beginnings or truncate requirement text.
- Supplementary ingestion shall preserve each source-backed requirement body in source order from its tagged header through its explicit terminator, normally `[End]`; OCR line breaks and whitespace inside IDs must be normalized before extraction, and missing terminators or incomplete trailing bodies are hard validation failures.
- For one normalized source requirement ID, candidate selection is monotonic: a shorter or incomplete candidate may never replace a longer complete candidate. Validate this invariant at supplementary staging and the Stage 1 handoff before merge, mapping, or generation.
- Generated CSV artifacts shall define one explicit, stable column schema for every record-producing path; never infer field names from the first row or allow optional record fields to create path-dependent schemas.
- Never duplicate requirement-reference notation when a single canonical reference is already present. For one atomic source requirement, retain one canonical authored SRS coverage reference; do not create or require an additional authored SRS ID for the same source requirement unless current source evidence defines a separate atomic requirement or distinct connection-matrix cell. Apply the same rule generically to all projects and source-ID families.
- If a source requirement is explicitly classified by the active project configuration as a non-canonical duplicate, exclude it before authored SRS ID allocation; do not repair the duplicate by assigning it another authored ID. The exclusion list is runtime configuration, not project-specific generator logic.
- Never continue if source/read policy is violated; run independence guard and fix first.

## Pre-Response Validation Snapshot (Required)
- Before each final response on stage work, explicitly verify and report:
- active stage and mode (tagged-source or untagged-source)
- hard-check result summary (pass or fail with counts)
- exact files changed in this loop only
- exact rerun command(s) used for validation
- decision: done, blocked, or escalation

## Source Read Policy
- Stage 1 may read the source specification directly.
- Stage 2 and above must be artifact-driven only.
- Stage 2/2A architecture content must be derived from current Stage 2 and Stage 2A outputs (traceability, block inventory, interface catalog, interaction matrix, and reports), not from project-specific static wording.
- Supplementary requirements must map only to existing architecture blocks. When source metadata is incomplete, normalized source-ID matching may propose an existing block; never invent a block. Classify from explicit source/category metadata, optional configured block classification, or deterministic requirement/block evidence. Use `System` only when Analog/Digital evidence is insufficient, and require user approval before Stage 2A.
- Keep the Stage 2 profile schema, mapping algorithm, and validation rules reusable across domains. Its `block_defs`, mapping terms, interfaces, and interaction rows may contain project-specific values only when they are generated from the active source evidence; they must not be fixed by prior-project assumptions.
- Enforce guard script when applicable: scripts/guard_stage2_plus_spec_independence.py.

## Deterministic Semantic Retrieval Rules
- Lexical, normalized, and legacy hybrid retrieval are the backward-compatible baseline. Keep semantic and hybrid-semantic retrieval optional and never require a semantic index or model for legacy modes.
- Semantic retrieval must be deterministic, local-only, and source-backed. Do not use LLMs, external AI services, network model downloads, or generative output in retrieval or mapping.
- The semantic index may contain blocks, functions, requirements, interfaces, and evidence chunks, but evidence retrieval and evidence fusion must filter to the requested entity type. Do not allow architecture entities to outrank source evidence chunks in a chunk-scoped query.
- Trigger one optional semantic recovery when a legacy query returns no results or when configured evidence-gap signals are present: lexical and normalized results have no common top candidate; either channel's top-1/top-2 score margin is below its own configured threshold; no exact normalized-term hit exists; the query contains too many unmatched tokens; or the query matches the configured natural-language/paraphrase profile. Treat disjoint candidate sets and no common top candidate as one condition, and compare score margins only within the same channel.
- Record which trigger fired and whether semantic recovery produced results. Run recovery once only; do not loop, retry indefinitely, or replace a non-empty legacy result automatically unless the benchmark-approved `auto` policy selects the semantic method.
- Semantic recovery is an evidence candidate mechanism only. It must not assign requirement ownership, modify Architecture Map Review decisions, change approved blocks, refresh approval hashes, or override Stage 2A traceability.
- Preserve original source text and provenance alongside normalized terms, embeddings, similarity scores, channel ranks, and fused scores. Normalized or embedded representations are retrieval aids, never normative evidence replacements.
- Three-channel fusion must use explicit channel weights and retain per-channel rank/score explainability. Start semantic weighting conservatively and require benchmark evidence before increasing it or making semantic retrieval the default.
- Protect exact technical identifiers and reviewed source evidence from semantic demotion. Exact requirement IDs, protocol names, signal names, and other configured technical tokens remain lexical/normalized strengths.
- When a query contains a configured source requirement ID, emit an advisory mapping audit containing the Stage 1-known status, expected owner when available, returned evidence IDs, and pass/review status. This audit is diagnostic only and must not change deterministic ownership.
- Keep the ownership authority chain unchanged: current artifact evidence -> deterministic Stage 2/2A mapping -> human Architecture Map Review -> independent ownership validator -> generated SysML/SRS/ARS/DRS artifacts.
- Benchmark lexical, normalized, legacy hybrid, semantic, and hybrid-semantic modes across exact IDs, acronyms, synonyms/paraphrases, sparse descriptions, and mixed entity queries. Inspect top-k deltas and report wrong-entity bias, latency, Recall@k, and MRR before rollout.
- Keep benchmark and retrieval code project-agnostic. Generated benchmark reports must identify the active project from `config/project_context.json` `project_name`; never hardcode a project name in reusable logic.
- After the retrieval tests pass, run the active project's benchmark cases across all retrieval modes. Select a mode only when labels, latency thresholds, and exact-ID protection pass; otherwise persist legacy `hybrid` as the selected mode for `auto` queries.

## Downstream Validation And Recommendation Rules
- After the authoritative pipeline and approved snapshot flow completes, downstream validation may run through `python scripts/workflow_cli.py validate-downstream`.
- The downstream evaluator is project-agnostic. It must receive project-specific paths, column mappings, labels, benchmark cases, and output locations from an explicit benchmark configuration; reusable code must not contain product names, source IDs, block names, or fixed artifact paths.
- Benchmark cases are review fixtures, not new authority. Each case should declare a query, expected evidence IDs, evidence class, required attributes, expected scope/classification where applicable, noise markers, and optional rendered-artifact attributes.
- The evaluator must measure lexical, normalized, hybrid RRF, and optional local semantic widening only when semantic evaluation is explicitly enabled in both the command and project configuration. Semantic evaluation must never change production defaults.
- The evaluator must report retrieval quality, evidence preservation, structured-evidence hits, scope, latency, mapping, hierarchy, rendering usefulness, and causal failure categories including discovery/ranking, preservation/filtering, scope filtering, rendering loss, mapping, hierarchy, and ownership failures.
- Results must be local-only, deterministic, reproducible, and non-authoritative. Record input/configuration identity and keep latency as a diagnostic measurement rather than a cross-machine quality gate.
- Recommendations are advisory. The evaluator must emit an explicit approval request and must never apply semantic enablement, retrieval-default changes, filtering or mapping-policy changes, rendering-policy changes, or benchmark-threshold changes automatically. A user must approve each proposed change before implementation.

## Dedicated Source-Section Preservation Rule
- When the current source evidence contains a dedicated paragraph or section for BIST, SCAN, Debug, DFT, Test Mode, ADC test mode, PAD mux, Alternate functions, Power-up, Power-down, BOOT, Configuration,  or an equivalent explicitly named test, lifecycle, startup, shutdown, or configuration topic, preserve that source label and paragraph grouping in SRS, ARS, and DRS.
- Map each requirement from a dedicated source paragraph within its corresponding source context unless current Stage 2A block `Function` evidence supports a concrete owner. Equivalent local labels for one requirement family (for example, case or wording variants of a routine or operation) may be grouped under one normalized child paragraph beneath the nearest explicit source parent. Preserve the parent title and source wording; retain artifact-derived block ownership when supported, and keep only unsupported dedicated content in the dedicated context.
- Preserve the source requirement IDs through the normal SRS `Covers:` field and preserve the corresponding authored SRS IDs as the only ARS/DRS `Covers:` values.
- Detect dedicated paragraphs from current Stage 1 source/section metadata and artifacts; do not hardcode one project's section names, identifiers, or block names. If no such source paragraph exists, do not create an empty dedicated section.
- Preserve the complete dedicated source body, including every bullet/numeric item, in source order and equivalent formatting; do not summarize or omit items.
- If OCR concatenates list items, split on source markers and render one item per line, preserving marker, numbering, order, and text under the same authored requirement.
- Insert a blank line before each rendered list block so Markdown/Pandoc preserves item boundaries in DOCX; do not insert blank lines between list items.
- Render every authored requirement header (`[SRS-REQ-xxx]`, `[ARS-REQ-xxx]`, `[DRS-REQ-xxx]`) after at least one blank line; never place two authored requirement blocks directly adjacent.
- Render every authored requirement as separate Markdown paragraphs: blank line after the authored header, blank line before `Covers:`, and blank line after `Covers:` before the next paragraph or requirement.
- Use standard Markdown list markers (`-`, `*`, or `+`) for generated bullet lists so Pandoc converts them to native DOCX lists; preserve original bullet order and item text. Unicode bullet characters may remain only inside fenced source-evidence blocks.
- Render each independent paragraph after a blank line, including paragraphs following headings or metadata fields; keep list items and table rows contiguous within their own block.
- Add every emitted dedicated or non-block-specific source paragraph to the document table of contents before the section-navigation index, assign it a stable hierarchical paragraph number matching its document location, provide a stable internal cross-link, and keep its requirement mapping under that same linked paragraph.
- Render every SRS, ARS, and DRS table-of-contents entry with indentation derived from its numerical section depth: top-level sections at zero indentation, `x.y` sections one level deeper, and so on. The TOC hierarchy must match the internal navigation index and must be generated from section numbers, never from project-specific headings.
- Preserve the same numerical TOC indentation in DOCX as in Markdown. DOCX conversion and validation must retain nested list levels in navigation order; a flat Word TOC is a formatting defect even when the Markdown TOC is correct.

## Non-Block Requirement Routing Rule
- Keep the workflow project-agnostic: classify a requirement as non-block-specific only from current Stage 1 source metadata and Stage 2A artifacts, never from a project name, fixed identifier, or hardcoded paragraph.
- When an unassigned requirement starts with or contains `The user shall`, treat it as a general-function requirement and cascade the nearest explicit source parent through same-page child paragraphs. Keep it in that source-function paragraph unless a known Stage 2A block owner supports the behavior.
- Preserve the nearest meaningful source parent heading through child requirements and continuation pages. When no supported inventory `Function` owns the behavior, retain the requirement under that cascaded source-function context with `Identified Block Mapping=Unassigned` and `Routing Status=retained_as_non_block_function_context`.
- For tagged source requirements, preserve the exact requirement text in source order through the end of its phrase, stopping at the configured tag terminator or the next tagged requirement ID. Join OCR-wrapped physical lines with spaces; do not merge text from adjacent requirements.
- Downstream SRS, ARS, and DRS generators must consume Stage 2A routing as authoritative and must not remap retained context requirements using lexical keywords, source headings, signal/IP names, or broad traceability matches.
- SRS crosscheck must compare every SRS source ID with the current Stage 2A requirement-to-block traceability exactly. An `Unassigned` Stage 2A row must remain non-specific in SRS; no downstream exception or lexical fallback may override Stage 2A ownership.
- Preserve one authored requirement per source ID, place the source ID only in SRS `Covers:`, and carry the authored SRS ID into ARS/DRS `Covers:`. `Unassigned` is a routing state, never an authored architecture block.

## Architecture Rules
- ARS shall report only analog-relevant requirements and related analog, mixed-signal, or power architecture blocks supported by current artifacts; digital-only and system-control-only requirements belong in SRS/DRS and shall not be promoted into ARS by dedicated-section or cross-domain shortcuts.
- Prefer generic architecture terms and evidence-grounded mapping from current artifacts.
- Generated narrative sections (for example SRS/ARS/DRS section 3.1) must be grounded in the current project artifacts only; foreign project identifiers or legacy aliases are blocking defects.
- Template directive text (for example "Summarize ...") must not remain in final generated artifacts; if present, treat as generation failure and regenerate.

## Source-Baselined Hierarchy Coverage Rules
- Calculate document-hierarchy coverage from the complete Stage 1 source-requirement catalog, joining each downstream traceability matrix through `source_req_id`. Do not use local authored IDs, source text matching, or project-specific identifier patterns as the coverage key.
- Stage 5 shall generate `artifacts/stage5_drs/requirements_hierarchy_coverage_report.md` and report Source-to-SRS coverage, each applicable lower-level document's source coverage, end-to-end coverage, and explicit uncovered source IDs.
- A scoped downstream document is not applicable when its traceability matrix contains no authored requirement in its declared scope. Report that state as `Not applicable`; do not represent it as zero coverage or a failed coverage condition.
- Context-only traceability rows are supporting evidence, not in-scope requirement coverage. Report their count separately and exclude them from coverage numerators.
- The System Traceability GUI tab shall read the generated coverage report and display the source specification, SRS, ARS, and DRS as linked evidence nodes with the report's percentage or not-applicable value on each link. It must not embed project names, source IDs, counts, or coverage values.
- Selecting System Traceability shall open a dedicated vertical hierarchy view. That view must include approved supplementary/source nodes when their dependency edges exist, generated SRS/ARS/DRS, and only created Digital/Analog IPOS block documents. Its tree and graph shall consume the central RM edge-statistics payload, omit zero-scope SRS edges, and never invent coverage for missing or valid-empty outputs.
- The System Traceability window is exclusively the approved RM dependency view. Its arrows must come from the central payload for approved generated-document `Covers` dependencies and approved primary/supplementary source-specification dependencies, including real paths such as primary source -> DRS and DRS -> IPOS; it must not render unapproved source-spec adjacency, SysML architecture edges, or design topology. Do not print `covers ...` labels on those arrows. IPOS block nodes show only the IPOS name, coverage percentage, and upstream blocks.
- Approved generated traceability may also define a direct supplementary-specification -> DRS/IPOS dependency. Render that arrow only when the snapshot-bound allocation and generated traceability explicitly identify the approved supplementary source and upstream `Covers` relationship; never force it through a generated-document parent and never infer it from generic source presence or file adjacency.
- Every System Traceability dependency edge shall define `coverage %` as `unique upstream requirement IDs covered by the derived document / total unique requirement IDs in the upstream document`; deduplicate upstream IDs before counting. This applies equally to SRS -> DRS, DRS -> IPOS, and approved supplementary-specification -> IPOS edges.
- For each IPOS block node, retain basic-info-only rendering but include approved upstream-document coverage as `covered unique upstream requirement IDs / total requirement IDs in that upstream document`, broken down by each rendered upstream document or supplementary specification when more than one upstream dependency exists.
- The central downstream validator-orchestrator owns one RM edge-statistics payload for these dependencies. Each record must expose the upstream node, derived node, edge/dependency type, covered unique upstream requirement IDs, total unique upstream requirement IDs, and percentage. Textual reports and GUI renderers must consume this payload directly; they must not recompute source-set intersections, generated-document `Covers` counts, or supplementary denominators locally for the same displayed edge.
- IPOS node coverage is a separate validator-owned metric named `Source-ledger coverage`: unique source requirement IDs represented by that concrete IPOS node divided by unique IDs in the approved allocation ledger. Textual per-block tables may retain `Mapped requirement coverage`, whose denominator is the approved Stage 2 mapping for that block, but must label it explicitly. `Upstream edge coverage` always uses the central edge payload. These labels and meanings must be rendered wherever the values appear.
- The RM dependency graph must contain concrete generated-document nodes and direct edges only. Do not create generic `Digital IPOS` or `Analog IPOS` group nodes; connect each concrete IPOS block directly to its approved DRS, ARS, generated-document, or supplementary-specification upstream edge. High-level IPOS percentages may be emitted as central summary statistics without materializing a generic group node.
- Source-specification coverage and RM dependency-edge coverage are different metrics only when explicitly labeled as such. A source-allocation percentage must never be displayed as the percentage of an RM dependency edge.
- The SysML Architecture hierarchy window is exclusively the approved SysML architectural/design relationship view. Its edges must come from the generated SysML structural representation and must not be replaced by or supplemented with RM document dependency arrows. Keep the two relationship contracts separate and centrally defined by the downstream validator.

## Source Structural Table And Port Coverage Rules
- Treat top-source I/O tables, port lists, pin maps, and other approved structural interface tables as source-baselined evidence. They describe architecture and interface context; they are not an independent requirement authority and must not create normative requirements by themselves.
- Use the approved snapshot-derived structural catalogs as the centralized baseline when present: `artifacts/stage2_mirco_arc/source_io_table_coverage.csv` for table identity, ownership, provenance, and extracted-row counts, and `artifacts/stage2_mirco_arc/source_port_catalog.csv` for port identity, direction, details, owner, source page/file, and ownership status. Do not create parallel per-stage I/O catalogs.
- Preserve stable table identity from normalized source table title plus approved owner and source provenance. Preserve stable port identity from table identity plus port name, direction, owner, and source provenance. Do not identify a table or port from generated wording alone when approved source metadata is available.
- Distinguish `context` tables from `requirement_bound` tables deterministically. Context tables provide architectural, interface, descriptive, timing, mode, or configuration evidence. A requirement-bound table is recognized only from explicit source-derived table metadata associated with a requirement, such as `source_table_title`, `table_title`, `source_table_number`, or `table_number`; incidental prose mentioning `Table N` is not sufficient.
- Requirement-bound tables follow the applicable requirement routing into SRS, ARS, or DRS. Context tables follow deterministic stage applicability and ownership rules. If applicability cannot be established from approved artifacts, report the ambiguity instead of guessing.
- Every applicable generated SRS, DRS, ARS, and SysML output must preserve the required source table identity and applicable source ports. Markdown and DOCX must be checked as derived representations of the same generated content; SysML must be checked in the owning block file.
- Keep interface-evidence ownership by document level: SRS may summarize system interfaces but must not render complete digital block I/O, port, pin, clock, or reset lists; DRS owns complete digital block interface tables under the corresponding block paragraph; each Digital or Analog IPOS owns detailed I/O evidence for its single approved block. Do not duplicate complete block I/O lists across SRS, DRS, and IPOS.
- Reuse the shared deterministic coverage checker `scripts/source_io_coverage.py` from existing stage crosschecks and SysML review. It must report `covered`, `not_applicable`, `missing_table`, and `missing_port` statuses and write a stage-specific structural coverage report under `artifacts/orchestrator/`.
- A missing applicable table or port is a blocking finding for that output's existing validation gate. A genuinely out-of-scope table is `not_applicable`, not a failure. Skipped or empty scoped documents must report structural coverage as `not_applicable` rather than zero coverage.
- Keep source page/file/table/owner provenance in generated reference tables and reports. If reliable table reconstruction is impossible, preserve source-extracted text with provenance rather than inventing columns or values.
- DOCX conversion must occur from the validated generated Markdown, and the structural checker must inspect the resulting DOCX content. Do not claim DOCX coverage solely because Markdown coverage passed.
- Structural-table coverage is a derived-output validation concern. It must not alter canonical requirement text, requirement IDs, ownership authority, approved mappings, snapshot contents, or requirement traceability denominators.

## Workflow GUI Usability Rules
- Treat `.sysml` as a supported artifact text format everywhere the GUI supports readable source files. The SysML Architecture tab must show both a parsed hierarchy graph and the selected SysML source text; after refresh, select and display the generated top-level SysML file by default while retaining tree selection for every subsystem, shared-definition, and block file.
- SysML graph rendering must parse current generated `part` declarations without project-specific block names and must display an explicit empty-state message when required generated files are absent or no hierarchy nodes can be parsed.
- After every GUI fix, verify the complete window layout before declaring the fix done: main-window geometry, visible panels and controls, tab/pane arrangement, splitter sash positions, scrolling/resizing behavior, and restoration from `config/gui_state.json` must remain usable. Do not treat a passing backend or unit test alone as sufficient GUI validation.
- GUI fixes must end with an executable layout check when the environment permits it: launch or exercise the GUI, confirm the relevant controls are visible and reachable, resize or restore the window, and record any display-session limitation explicitly.
- Button, control, and stage-hover popups shall be positioned from runtime widget geometry and the work area of the monitor containing the hovered control, so the entire popup remains visible in multi-monitor sessions. If the preferred below-control placement would exceed that monitor, place the popup above or clamp it within that monitor's work area.
- Tooltip and popup placement logic must use runtime widget geometry and screen bounds; do not use fixed coordinates or project-specific values.
- When Stage 1 reports ambiguous table rows, the GUI shall open the generated table-review CSV in Excel and ask the user for explicit acceptance in a popup. Acceptance shall be recorded in the GUI log, and Stage 1 must be rerun and pass before architecture-map generation continues.
- `table_row_review.csv` is the single review table for all explicit configured table requirement IDs, including reconstructed parameter/interface rows and structural clock/reset/interrupt rows. Do not create separate review CSVs by table type.

## Architecture Naming Rule
- Identify architecture blocks only from the active project's source evidence and current Stage 2/2A artifacts.
- Do not invent generic replacement names when source evidence provides an exact block, IP, module, or matrix label.
- Preserve exact evidence-derived terminology in inventories, matrices, and generated specifications.
- Generic terms may describe reusable rules or classifications, but must not become emitted project block names.
- A product, device, subsystem, signal-chain, or capability description is not a block name unless the active evidence explicitly defines it as a block, IP, module, or matrix row/column label.
- If a project-specific name is unsupported or ambiguous, report missing evidence instead of guessing.
- Stage 2+ must consume resolved names from current artifacts and must not import names from another project or prior session.

## Block Description Contract
- DRS document structure, Conventions, navigation/table preservation and descriptive-writing policy are consolidated in `templates/DRS_gen_AI_template_prompt.md` with a versioned embedded YAML contract. That document contract is subordinate to these General Rules and cannot replace the approved snapshot as technical authority. The DRS generator must load it before generation; the existing DRS crosscheck and central downstream validator must enforce it on final Markdown and DOCX. Record template version/hash independently from snapshot identity. Unknown mandatory rules fail closed.
- DRS system digital-context, power/clock/domain-control, buses/interconnect, arbitration/control/shared-resource, digital-processing, configuration/interface/data-path, and timing/performance sections must explain known behavior, roles, and directed relationships before supporting tables or brief targeted `need clarification` statements. Never describe a section by counting evidence, paths, endpoints, or grouped items, or emit approval/audit-shaped prose such as `approved integration evidence groups`, `approved block functions identify`, or `approved clock routes reach`. Use the shared deterministic composers in `workflow_routing.py` and independent final Markdown/DOCX prose checks through the existing central orchestrator-validator. Preserve section mapping, evidence eligibility, authority scope, provenance, I/O tables, and approved concrete-block boundaries; an interface, signal, or interaction label is not a new block. Review names are examples only: reusable code, governance, and orchestrator policy must not add project-specific names, alias lists, capability catalogues, or hardcoded cases. Keep numerical engineering values and exact source-linked table details; counts are not technical synthesis. This rule applies to the current DRS and system-scope SRS rollout.
- The project-agnostic descriptive-quality contract applies to appropriate SRS, DRS, and ARS narrative sections without prescribing IPOS section numbers: use natural technical prose, readable inventory-bounded block/function summaries, and independent final-text checks rejecting approval, template, audit, or requirement-form language. The first rollout consumes artifact-only Stage 1 descriptive evidence in DRS and bounded system-scope SRS sections; IPOS and ARS remain unchanged until separately authorized.
- In DRS, render one concise block-purpose paragraph only for inventory rows explicitly marked `concrete_block` and selected by existing digital-block policy. Preserve the complete matching approved inventory `Function` meaning and record its exact source value, rendered sentence, block, and order in the existing descriptive audit. Do not create paragraphs for non-block entities or logic labels unless explicitly approved as concrete digital blocks. Keep every approved block's I/O in owner-scoped Markdown and DOCX tables, not port-name bullets; Stage 5 and the central downstream validator both check prose, audit, and table coverage.
- Populate DRS introductory architectural descriptions from existing approved top-digital context, integration evidence, and artifact-only Stage 1 system-scope descriptions. Summarize actual relationships in natural, non-normative language; render source/destination/exchange relationships in deterministic tables, with per-row provenance in the descriptive audit and independent Stage 5/central validation. Do not copy raw requirements, introduce generic `shall define` placeholders, promote an interaction endpoint to a concrete block, or alter Stage 2/snapshot authority. SRS may consume the same evidence only in system-scope descriptive sections; ARS and IPOS stay unchanged in this rollout.
- Synthesize DRS section narratives deterministically from approved in-scope evidence grouped by section theme, not by repeating block-purpose paragraphs or concatenating raw path lists. Retain one named 3.1 sub-paragraph per approved concrete digital block only. Use tables when they clarify exchanges, clock routes, frequencies, gate expressions, domains, or reset outputs, and validate section prose and underlying evidence in both Markdown and DOCX through the existing central orchestrator-validator. For power/clock sections, represent all documented destinations and state when broader destination-block coverage is not approved; do not infer block identity, timing, or synchronization from signal labels. Emit a minimal informative statement and `need clarification` for unsupported expected topics. This rule applies to the current rollout without introducing a project-specific pilot catalog.
- In DRS, treat arbitration/control and shared resources as one coherent descriptive section. Use approved in-scope block functions and interaction records for resource ownership, register/memory access, flow control, synchronization, reset/boot coordination, latency/bandwidth, and power/clock interaction; mark each unsupported expected facet `need clarification` rather than inventing an arbitration or SoC policy. When approved clock/reset evidence gives the power/clock owner multiple destinations, list every supported route, frequency and gating status, plus approved reset-output descriptions; never reduce that coverage to one status edge or infer a destination from a port name alone. Keep malformed or incomplete routes explicitly unresolved. The shared DRS validator invoked by the central downstream orchestrator must check these sections in Markdown and DOCX against the same approved snapshot and owner-scoped Stage 2 evidence.
- SRS/ARS retain their existing literal `General functional description: <Function>` requirement for now. Do not derive any document's block purpose from linked requirements, interfaces, source OCR, or general block vocabulary.
- A block with an empty inventory `Function` is a blocking Stage 3/4/5 input defect; correct and regenerate Stage 2 before generating downstream specifications.

## Block Ownership Contract
- For SRS, ARS, and DRS project-specific block requirements, resolve the owning block only from the matching current `artifacts/stage2_mirco_arc/block_inventory.csv` `Function` fields. Do not use source-section headings, source-specific tags, signal/IP names, broad Stage 2 traceability mappings, or `Linked requirements` lists as ownership shortcuts.
- A requirement may be placed under a block only when its behavior is within that block's declared inventory function. Leave a requirement unassigned and report an inventory/mapping defect when no function supports ownership.
- Stage 1/2 may use original-spec functional-role wording, including `is in charge of`, `main activities are`, `main functionalities are`, `main purpose is/are`, and equivalent phrases, only to discover or correct the evidence-backed block `Function` fields in the Stage 2 inventory.
- After Stage 2, downstream generators must consume the inventory functions as the sole ownership authority; they must not reread or reinterpret original-spec role wording.

## Downstream Function-Only Validation Contract
- SRS and ARS crosscheckers must retain their exact inventory `Function` checks; DRS must check the deterministic natural sentence against the complete approved `Function` and audit instead. All three reject empty `Function` and emitted owners absent from the inventory.
- For non-matrix requirements, crosscheckers must verify that the requirement behavior is supported by the owning block's `Function`; broad traceability, interfaces, inputs, outputs, linked requirements, source headings, signal names, and source tags are not ownership evidence.
- Matrix-derived requirements are the sole exception: validate them against the exact interaction-matrix source-row block and authored matrix traceability, not lexical function matching.
- Crosscheckers must report unsupported or ambiguous ownership as an unassigned inventory/mapping defect and return a failing gate status.

## Connection Matrix Requirement Rule (Mandatory)
- When a current source artifact contains a connection matrix with `Source` rows and `Destination` columns, inspect every populated cross-cell.
- Recover the complete `Destination` header set before mapping cells; OCR text may omit a header or merge it with an adjacent row. If extracted text is incomplete or ambiguous, use source-page coordinates or a rendered-page inspection to resolve the header positions.
- Map each requirement ID by the geometric intersection of its source row and destination column. Never assign an ID to a neighboring column based only on OCR line order or proximity.
- For each populated cross-cell, use the exact source-row label and destination-column label printed in that table; do not normalize, alias, translate, or invent either name from a block inventory or prior project.
- Rewrite the cross-cell as one textual requirement: `The <exact Source label> block shall be connected to the <exact Destination label> block.`
- Preserve every requirement ID code found in that cross-cell in the SRS requirement's `Covers:` traceability field. Do not place those IDs in the authored sentence.
- Keep one populated cross-cell as one requirement unless the source table explicitly defines separate requirements within that cell.
- In SRS, assign one unique authored `SRS-REQ-xxx` ID to each populated cross-cell. This authored SRS ID is the upstream requirement for downstream ARS/DRS entries derived from that cell.
- In ARS and DRS, assign a unique artifact-local `ARS-REQ-xxx` or `DRS-REQ-xxx` ID to every authored entry. `Covers:` must reference only the corresponding `SRS-REQ-xxx` upstream ID.
- Stage 1 source IDs (for example `DDS_*`, `SYS-RQ-*`, `ANA-RQ-*`, `DIG-RQ-*`, `XDN-RQ-*`) shall appear in `Covers:` only in SRS authored entries.
- In ARS/DRS, a matrix-derived entry belongs to the exact source-row block only. Do not copy a matrix requirement into every block named by broad Stage 1 ownership mapping.
- In ARS/DRS, render matrix-derived behavior from the interaction-matrix edge as `The <Source label> block shall implement: connection to the <Destination label> block.` Do not reuse truncated, merged, or otherwise non-atomic Stage 1 OCR prose for that entry.
- In ARS/DRS, use the corresponding authored `SRS-REQ-xxx` as the single `Covers:` upstream ID for the matrix-derived entry. Raw source cell IDs remain documented by the SRS `Covers:` field and source artifacts.
- If matrix labels differ from Stage 2 inventory labels, retain the matrix labels in the connection requirement and report the mismatch as an evidence/reconciliation item.

## DRS Source Interface Table Preservation
- DRS generation must preserve source I/O, port, pin, clock, reset, and interface tables as reference tables in the proper project-specific block paragraph whenever the table can be evidence-matched to a current block inventory entry or exact matrix/source label.
- Place copied source interface tables after the block `Inputs:`/`Outputs:` summary and before authored DRS requirements for that block.
- Keep copied source tables clearly labeled with their original source table title and page/section provenance. If OCR quality prevents reliable markdown table reconstruction, preserve the extracted table text in a fenced text block rather than inventing columns.
- Copied source table snippets must stop before any source requirement header, source peculiar-requirements paragraph, or raw source requirement body. Raw source requirement IDs must not appear as `[SOURCE_ID] Requirement` headings in DRS.
- Do not use copied source interface tables as normative requirement rows by themselves. They support interface context and traceability only; normative requirements still require explicit requirement wording or connection-matrix rules.
- If a source interface table appears relevant to multiple blocks, attach it only to the exact block named by the table title/section or report it as shared evidence; do not duplicate it across unrelated blocks based on broad lexical overlap.

## Ownership and Connection-Matrix Traceability Rules
- When multiple architecture candidates match a requirement, prefer the candidate supported by explicit named IP/block evidence and remove candidates supported only by generic vocabulary.
- Generic terms such as analog, digital, signal, sample, or block must not establish ownership by themselves.
- If two candidates remain, apply the active project's evidence-based precedence rules and report the ambiguity; do not encode a fixed project-specific precedence in this common file.
- The generated `interaction_matrix.csv` must include a `Requirement IDs` column for connection-matrix-derived rows. Every recovered populated-cell ID must remain attached to its exact source/destination row.
- Emit a connection row only when the corresponding source connection-matrix cell contains a requirement ID; a blank cell is not a connection.

## Global Stage 2A Contract (Mandatory)
- Treat the Stage 2A profile structure and mapping logic as reusable, while allowing its generated project-value sections to store the active project's source-derived block names, interfaces, and interactions. Never copy those values from another project.
- Profile text must not include project names, project IDs, product code names, or one-project internal hierarchy paths.
- Architecture outputs must be regenerated each run from current stage artifacts and requirement evidence.
- If Stage 2A output appears stale, verify in this order: active repo root, Stage 1 requirement timestamp, Stage 2 report timestamp, and Stage 2A result timestamp; after correction, restart the pipeline from Stage 0.
- A Stage 2A pass must report both coverage and provenance (profile path and source document from OCR index).

## Global Vocabulary Guard (Mandatory)
- Keep mapping rules generic: protocol terms, register terms, clock/reset/power terms, buffer/interrupt terms, interface/control terms.
- Avoid domain-locked synonyms unless they are present in the current requirement artifacts and needed for coverage.
- When adding terms to improve coverage, prefer reusable lexical families over project identifiers.

## Stage 1 ID Policy (Hard Rule)
- Before Stage 2A, Stage 1 must write `artifacts/stage1_requirements/duplicate_source_req_ids.csv` containing only repeated IDs with multiple substantive normative statements, including counts, source locations, statements, and status.
- If that duplicate list is non-empty, stop the flow and ask the user to resolve source-ID uniqueness. Ignore marker-only, continuation, and inline-reference fragments when deciding whether an ID is duplicated.
- If source is tagged, output must use only strict original tagged requirement IDs.
- In tagged-source mode, generated standard IDs are forbidden in final Stage 1 outputs.
- No mixed-ID output is allowed in tagged-source mode.
- If source is untagged, standard generated ID rules are allowed.

## Stage 1 OCR Requirement-ID Recognition (Mandatory)
- For table and figure rows, recognize source IDs only from the configured table-ID family in `config/project_context.json` (for example `PROJECT_REQ_<digits>`).
- During OCR extraction, analyze every table row that contains a configured source requirement ID. Retain the table title, column headers, and page-to-page continuation context needed to reconstruct that row; do not reduce a recognized table row to isolated OCR text.
- Table IDs may be accepted from an ID column or an OCR row with verified table/figure context, including continued rows on the next OCR page when a numbered table marker establishes the context; do not infer IDs from arbitrary narrative text.
- For non-table text, recognize a source ID only when the tag is followed by the configured `Requirement` keyword, for example `[PROJECT_REQ_0001] Requirement: ...`.
- Reject bare IDs, IDs followed by other labels such as `Definition`, and compact alternatives such as `A3` as source requirement IDs unless an explicit project rule authorizes them.
- Keep table context, tag-label requirements, compact-ID handling, and metadata-label rejection configurable through `requirement_id_rules`; do not hardcode a source-ID family in reusable scripts.
- Keep `source_req_id` recognition separate from requirement classification and taxonomy assignment; an ID alone is not evidence that a row is a requirement.
- Preserve the recognized source ID in `source_req_id` and apply the configured tagged-source `id_policy` downstream.

## Source Table Classification Rules
- For complex source tables without a recoverable normative requirement statement, emit only the table number and caption in the SRS/ARS/DRS requirement statement. Do not copy table rows, headers, or cell contents into normative prose; retain the source linkage in `Covers:`.
- Do not generate normative requirements from memory-map, address-map, register-map summary, connectivity-check, static-connectivity-check, revision-history, abbreviation, repository, or metadata tables. These tables may be copied or cited as reference evidence, but they are not requirement-generation sources unless a row explicitly uses the configured `Requirement` marker and passes the normal requirement-quality checks.
- Do not emit descriptive table captions or non-normative table rows, including operating-mode, state, configuration-summary, timing-summary, or equivalent tables, as SRS, ARS, or DRS requirements. Keep them as reference evidence; emit a row normatively only when it contains the configured `Requirement` marker and passes normal requirement-quality checks.
- Connection-matrix tables are a separate artifact class: use them only to generate interaction-matrix edges and matrix-derived SRS/ARS/DRS connection requirements. Do not treat row/column labels or merged OCR context as broad block ownership evidence.
- I/O list, port list, pin list, clock list, reset list, interface list, and similar block-interface tables are reference-interface evidence. Preserve them for downstream specification context, but do not convert table rows into normative requirements unless the row itself contains an explicit requirement statement.
- Reset or clock connectivity tables are an explicit exception to the reference-interface rule: when a row contains a requirement ID plus source and destination/target fields, derive a normative connection requirement from that row. For clock rows, also include the exact `F max`/`Frequency` value when present. For clock rows, add the `clock gating` column info, if present. Use these table information to write a consistent textual derived requirement statement. 
- OCR table analysis must carry reset/clock table headers to continuation pages containing requirement IDs, so source, destination/target, frequency, and clock-gating cells are reconstructed as one row.
- OCR requirement analysis must carry a requirement body across the next page when the source requirement begins near a page boundary. Stop at the next source requirement marker or section heading; do not truncate to a partial table fragment when a continuation page completes the source context.
- Reset/clock table-derived requirements belong to the current project's power/clock/reset owner block. Resolve that owner from the current Stage 2 inventory/profile: use the PMU block when the project defines PMU ownership for clock/reset sequencing, or use the project-specific clock/reset-management block when that is the named inventory authority. Do not assign these derived requirements to arbitrary source/destination hierarchy blocks based only on signal paths.
- For derived reset/clock statements, preserve the exact source and destination/target hierarchy paths and exact frequency text as printed or reliably reconstructed from the table. Do not normalize, simplify, alias, translate, shorten, or invent path names or frequency text. Include the clock gating column text in the derived requirement statement when present.
- The original table requirement ID is the upstream requirement being covered in SRS. SRS shall assign a distinct authored requirement ID to the generated connection/frequency statement and link it with `Covers: <original table req_id>`. ARS and DRS authored entries shall reference the corresponding `SRS-REQ-xxx` in `Covers:` only.
- When filtering source tables, classify by table title and nearby section title using generic terms such as `memory map`, `address map`, `connectivity check`, `I/O list`, `port list`, `clock`, `reset`, `interface`, and `connection matrix`; do not hardcode project names, product names, block names, or source-specific requirement IDs.
- For Interrupt tables, preserve them as reference evidence in the block paragraph only when they can be matched to a current Stage 2 inventory block. Put interrupt derived requirements in the `processor`, or `CPU` o `microcontroller` or similar names paragraph. Do not generate requirements from an interrupt table unless the row explicitly contains a requirement statement. Use names contained in that tables columns such as `Interrupt`, `bit`, `Description` to write a derived requierement statement, and preserve the original table requirement ID in SRS `Covers:`. Do not invent a block name or alias from the interrupt table; use only the current Stage 2 inventory block that matches the source evidence.

## Block Domain Taxonomy Rules
- Keep three architecture entity types distinct: a `real block` is a current Stage 2 inventory implementation unit with a non-empty `Function`; an `interface/port` is a connection endpoint from `interface_catalog.csv`; a `source context` is a paragraph, mode, use case, or section label.
- Labels such as `I2C interface` and `SPI interface` are examples of interface endpoints that may belong to a real implementation block such as `I2C_SPI_AHB`. Resolve the relationship from current interface-catalog owner/purpose and block-inventory function evidence; never hardcode these names or reuse this relationship across projects. Interface names must not become IPOS documents or approved block names.
- Source-context labels such as `ECG Only`, `PPG Only`, `Configuration Phase`, and `Debug mode` must never become `approved_block`, `owning_block`, block headings, or filenames.
- ADC is analog/mixed when its own function implements analog-to-digital conversion or sampling. Digital output signals do not make ADC a Digital IPOS block.
- Digital IPOS shall contain only approved real digital/system blocks; a non-digital, interface, or source-context owner is a blocking mapping error.
- Classify a block as digital when its architectural function implements a digital protocol, bus, processor, controller, register path, or digital state/data path.
- The terms `I2C`, `SPI`, `AHB`, `AXI`, `APB`, `UART`, `JTAG`, `serial`, `protocol`, `bus`, `processor`, `CPU`, `microprocessor`, `core`, and `digital` are authoritative digital-domain indicators when they describe the block function, interfaces, or source architecture evidence.
- Protocol and processor evidence takes precedence over generic analog-word matches in surrounding requirement text. Do not classify a protocol bridge or processor as analog/mixed merely because it has analog-connected requirements or appears in a mixed-signal system.
- Use `analog_or_mixed` only when the block's own function or interfaces implement analog sensing, conversion, conditioning, power, or other analog behavior; use `power_or_supply` for power-management ownership.
- Keep these terms as reusable taxonomy vocabulary. Do not hardcode project-specific block names or infer a block domain from a figure alone.

## Stage 1 Extraction and Validation Order (Mandatory)
1. OCR extraction and index generation
2. Taxonomy crosscheck update
3. Requirements extraction output generation
4. Requirements RAG/text quality crosscheck
5. Requirements coverage crosscheck
6. Gate validation and sign-off decision

## Fail-Fast Validation Policy
- Crosscheck and gate scripts must return nonzero exit codes on hard-rule violations.
- In tagged-source mode, any generated_standard presence must fail Stage 1 crosscheck/gate.
- Do not report PASS when any hard rule is violated.

## Crosscheck Severity Matrix (Hard vs Heuristic)
- Hard checks are blocking and must fail the stage:
- tagged-ID strictness
- source_req_id presence in tagged mode
- summary contract/schema violations
- explicit script/gate nonzero exit conditions
- Heuristic checks are non-blocking and must be WARN unless explicitly promoted by project decision:
- ontology/image/table coverage density
- overlap quality hints and soft completeness signals
- Never escalate heuristic-only findings to stage FAIL unless a hard-check dependency is violated.

## Required Stage 1 Output Contract
At minimum, ensure these outputs are updated consistently:
- artifacts/stage1_requirements/requirements_raw.md
- artifacts/stage1_requirements/requirements_summary.csv
- artifacts/stage1_requirements/requirements_summary.md
- artifacts/stage1_requirements/requirements_rag_crosscheck.md
- artifacts/stage1_requirements/coverage_crosscheck.md
- artifacts/stage1_requirements/missing_requirements_candidates.csv
- artifacts/orchestrator/stage_01_report.md

## Patch Scope Discipline
- Keep fixes minimal and scoped to failing checks.
- Preserve compatibility for downstream scripts consuming source_req_id and id_policy.
- Avoid unrelated refactors while fixing a gate/blocker issue.
- Do not introduce project-specific one-off script behavior for Stage 2/2A architecture generation. Project-specific names and interactions must come through the standard source-evidence-to-profile/artifact path.

## Autonomous Context Refresh (Mandatory Before Editing)
- Before each stage patch, re-read current project context and active stage artifacts.
- Do not reuse assumptions from sibling projects or previous sessions without verification in current artifacts.
- If context differs from previous assumptions, publish a short delta summary before patching.

## Stage Acceptance Checklist (Mandatory Before Done)
- Before declaring completion for Stage 1 work, verify all of the following in current artifacts:
- requirements_summary.csv id_policy distribution matches active mode policy
- requirements_raw.md and requirements_summary.md use aligned IDs
- requirements_rag_crosscheck.md hard checks pass
- validate_stage1_gate.py reports pass
- If any item fails, do not mark done.

## Truncation and Completeness Guard
- Truncated statements, broken sentence starts, or malformed requirement text are blocking quality defects for stage completion.
- Perform one targeted normalization pass for sentence completeness before final write.
- If truncation remains after one pass, report affected IDs and block stage sign-off.

## Preferred Execution Mode
- Run one stage or an ascending contiguous range with validation after every selected stage.
- If any runner or validator fails, stop immediately, publish blocker evidence, correct the owning stage, and rerun forward from that stage.

## Blocker Escalation Bundle (Required)
- After a failed pipeline run, stop execution and publish a blocker bundle with:
- failing rule names and counts
- affected artifacts and key IDs
- smallest next patch set and responsible owner/stage
- Do not retry or continue execution from the failed stage.

## Completion Proof Block (Required in responses)
For each substantial stage fix, include:
- Changed files
- Validation commands executed
- Crosscheck/gate pass or fail summary
- Open risks/blockers and next action

## Agent Routing Guidance

## Repeatable Pre-Freeze Coherence Gate
- Warnings must be deterministically grouped, root-caused, and reduced before user escalation; raw warning lists are not an approval request.
- Historical/superseded ingestion coexistence remains visible in audit findings, but must be emitted as INFO rather than a user-facing WARNING when the active batch is unique and workflow metadata proves the older batch is non-authoritative with no current authority effect and INFO_ONLY/non-blocking triage. Keep WARNING when that proof is absent or authority ambiguity remains real.
- Historical warning metadata must carry the active batch path, historical batch identity, authority effect, cleanup action, status, and final workflow triage so severity can be aligned at detection time without hiding audit evidence.
- S2A approval is a shared evidence contract for all project types: `approval.status=approved`, non-empty reviewer identity, current mapping CSV hash, and current draft-profile review hash must be validated by both the S2A gate and the S2B freeze. Internal reports must publish the contract result; a PASS from artifact checks alone is insufficient.
- Approved top-level routing to SRS, DRS, or ARS may have no concrete `approved_block`; validators must accept the routing decision without inventing a block or parent.
- S2A, internal reports, and S2B must consume the same current mapping/profile evidence. Any hash, approval, or authority mismatch blocks progression and requires re-review; no automatic repair is allowed.
- `lineage_candidate_parent_req_ids` is optional candidate metadata, never approved parent evidence.
- Remediation may apply only explicitly authorized, auditable cleanup; it must not infer or rewrite approved placement. Escalate irreducible approval-boundary conflicts.
- Derived artifacts must not outrun canonical, mapping, profile, or snapshot authority.
- Stage 2B freeze and approved snapshot creation are allowed only from current coherent approved pre-freeze authority.
- The read-only Phase 1 coherence check and post-Phase-1 warning-triage gate are mandatory and repeatable after every authority-changing event and before freeze or downstream execution.
- Any new supplementary import, review decision, merge manifest change, canonical merge-impacting change, Architecture Map change, architecture-profile change, approval/hash change, active batch/revision change, or lineage/ID change invalidates prior pre-freeze readiness.
- Preserve approved allocation metadata end-to-end; the central downstream coherence validator enforces snapshot ID, allocation class, owning target, lineage, provenance, parent evidence when required, domain, strict partitions, and generator non-inference.
- Use specialized Stage 1 workflow/requirements agents for extraction and crosscheck tasks.
- Use orchestrator role for gate decisions, blocker routing, and handoff readiness only.
