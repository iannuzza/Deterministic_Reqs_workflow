# Orchestration Specification

## Objective
Define a reproducible stage-gated workflow for this repository, with enforced crosschecks and validator gates for Stages 0 through 7 plus a dedicated final SysML phase.

## Implemented Stage Sequence (0 to 7, Plus Final SysML)
0. Stage 0: Ontology baseline and Gate 0
1. Stage 1: Requirements extraction plus RAG and coverage crosschecks, Gate 1
2. Stage 2: Requirement formalization (specs) plus specs crosscheck, Gate 2
3. Stage 3: SRS generation plus markdown and LaTeX crosschecks, Stage 3 gate
4. Stage 4: ARS generation plus ARS crosscheck, Stage 4 gate
5. Stage 5: DRS generation plus DRS crosscheck, Stage 5 gate
6. Stage 6: Digital IPOS generation and validation
7. Stage 7: Analog IPOS generation and validation
8. Final SysML phase: complete snapshot-bound SysML generation and central coherence validation

Notes:
- The main workflow is strict and forward-only: a run may execute one stage or an ascending contiguous range beginning at any stage in `0 -> 1 -> 2 -> 2A -> 3 -> 4 -> 5 -> 6 -> 7`. Each selected stage runs once, validates before advancement, and stops on the first failure. Retries and implicit loops are prohibited. The explicit supplementary-refresh transition after Stage 2 is the only permitted loopback: after approved supplementary rows are merged, the GUI runs Stage 0, Stage 1 OCR/tag extraction, and Stage 2 as a fresh refresh sequence. Stage 4 is the sole conditional skip: it is allowed only when both its runner and validator confirm zero Analog-category source requirement IDs.
- Execution rule: the dispatcher invokes exactly one stage runner, then its stage crosschecks/gate validator exactly once. A non-zero runner or validator result stops the selected range immediately; no retry parameter or implicit loop is permitted.
- The `drs-after-stage2a` requirements-only command is the sole approved shortcut because it is forward-only from Stage 2A to Stage 5. No Stage 3, 4, or 5 path may invoke an earlier stage.
- Cross-project architecture comparison remains an optional standalone command through `workflow_cli.py arch-compare --project-to-compare <project_name>`; it is separate from numbered Stage 6 Digital IPOS and does not block the numbered pipeline.
- Stage 2 micro-architecture activities are implemented as a dedicated flow and are mandatory upstream evidence for Stage 3 and Stage 4 spec generation.
- Later long-horizon stages (numeric core, vectors, RTL, synthesis, optimization) remain defined in agent catalog but are outside this Stage 0 to 6 execution profile.
- Full-flow stage runner scripts print startup output banners with expected artifact paths to improve run transparency.
- Source-read contract: only Stage 1 may read the initial specification file directly. Stage 2+ activities must be artifact-driven.
- Supplementary source review is additive and occurs after the primary source completes Stage 2. Approved rows are added to the updated integrated source baseline. The loop is an incremental refresh/recompute of dependent stages, not a destructive restart: the current canonical corpus, architecture review mapping, approved mapping snapshot, hierarchical specifications, and SysML traceability outputs are invalidated and regenerated from the updated baseline.
- Existing approval records, source-review workbooks, workflow manifests, and generated artifact history remain preserved for audit. Because the evidence inputs changed, the regenerated architecture mapping and approved mapping snapshot require fresh reviewer approval and hashes; previous approvals remain historical and are not silently promoted to current approval.
- Hard enforcement: `scripts/guard_stage2_plus_spec_independence.py` is executed by Stage 2+ generation entrypoints and blocks direct source-spec coupling.
- Source-fidelity contract: Stage 1 preserves the exact source statement and its identifier when present. For non-tagged sources, it assigns a stable generated ID plus source file/page/section/table/line provenance, extraction method, and review disposition. Any deterministic recovery of a missed requirement must retain equivalent source-backed provenance.
- Downstream-authoring contract: SRS, ARS, and DRS consume the Stage 1 artifact and Stage 2A ownership only. They may normalize presentation but must not infer project-specific behavior or suppress a source requirement by its identifier.
- Shared descriptive-authority contract: SRS, ARS, and DRS may reuse source-backed descriptive sentences and capability statements from the Stage 1/source-spec catalog. The reviewed `artifacts/stage1_specs/architecture_mapping_preview.csv` supplies approved mapping, ownership, and structural context. SRS, ARS, and DRS are parallel derivations; none becomes the semantic authority for another.
- Hierarchy-coverage contract: Stage 5 generates `artifacts/stage5_drs/requirements_hierarchy_coverage_report.md` by joining each document traceability matrix to the full Stage 1 source ID catalog through `source_req_id`. The report shall show Source-to-SRS coverage, document and end-to-end coverage, and explicit gap IDs.
- Applicability rule: a scoped lower-level document is not applicable when its traceability matrix contains no authored requirement in its declared scope. Context-only rows must be reported separately and excluded from coverage percentages. Coverage rules are driven by document scope and artifact fields, with no project-specific source IDs, paths, or block-name exceptions.
- Downstream traceability rule: Stages 3, 4, 5, 6, and 7 each retain their own generated document, traceability matrix, crosscheck reports, and deterministic statistics. GUI status and traceability rendering refresh from those stage outputs, while aggregate reports remain supplemental.
- SysML timing rule: the Stage 3 SysML review performs structural checks only. Full requirement coverage, allocation, ownership, partition, and end-to-end coherence are deferred to the dedicated final SysML phase, which uses the same approved snapshot-bound downstream contract and calls `scripts/validate_downstream_coherence.py`.

## Workflow GUI Operations

- Launch with `python scripts/workflow_gui.py`.
- `Architecture Map Review` remains available before, during, and after Stage 2. It opens `architecture_mapping_preview.csv` and `.md`, offers Excel launch for CSV review, and displays live row counts by `review_decision` with the recorded Stage 2A approval decision and reviewer.
- The workflow-diagram review node uses the same `Architecture Map Review` wording as this dedicated reviewer workspace; selecting it opens the review dialog.
- The Stage 2 approval dialog is the write path for CSV review: reviewers may edit in Excel, mark all rows approved when appropriate, and record the reviewed CSV hash to enable Stage 2A.
- Supplementary requirement rule: map each supplementary source ID only to an existing Stage 2 architecture block. When source metadata is incomplete, normalized source-ID matching may propose an existing block; no new block may be invented. Classification uses explicit source/category metadata, optional block classification metadata, or deterministic evidence from the requirement and block definition. Use `System` only when Analog/Digital evidence is insufficient, and require user approval before Stage 2A.
- Secondary actions, including Architecture Map Review and the Stage 2A-to-Stage 5 requirements-only path, occupy a separate visible control row.
- Every stage box shows a hover popup. It displays stage intent in normal operation and the captured failure reason when a stage fails; the visible diagram hint mirrors that text.
- The central `workflow_cli.py validate --all` runs `scripts/validate_workflow_diagram_rendering.py` after the numbered stage validators. It renders both GUI workflow canvases and fails validation if a node label leaves its block, overlaps another block, selectable full-diagram nodes lose their click bindings, or rendered content is clipped. Gray identifies only actions present in the workflow CLI stage order or its `arch-compare` command; automatic intermediate nodes remain informational and cannot launch from diagram clicks.
- Every button, control, and stage-hover popup is placed from runtime widget geometry and current screen bounds so it remains fully visible; when the preferred below-control location would overflow, the popup flips above or clamps within the visible screen margin.
- Larger default fonts apply to controls, viewers, tables, chat/log consoles, and diagram labels for review readability.

## Stage Activity Map And Runners

### Stage 0 Activity
- Runner: `scripts/run_stage0_gate0.py`
- Steps:
	- `scripts/sync_repo_memory_local.py --quiet`
	- `scripts/init_stage0_artifacts.py`
	- `scripts/generate_stage0_ontology_outputs.py`
	- `scripts/generate_stage0_ontology_report.py`
	- `scripts/run_ontology_crosscheck_agent.py`
	- `scripts/validate_stage0_gate.py`
- Required outputs:
	- `artifacts/stage0_ontology/ontology.md`
	- `artifacts/stage0_ontology/glossary.csv`
	- `artifacts/stage0_ontology/ontology_requirement_links.csv`
	- `artifacts/stage0_ontology/semantic_issues.md`
	- `artifacts/orchestrator/stage_00_report.md`
	- `artifacts/orchestrator/stage_00_result.md`

### Stage 1 Activity
- Runner: `scripts/run_stage1_requirements_gate1.py`
- Steps:
	- OCR extraction
	- taxonomy cross-check/update (`scripts/run_taxonomy_crosscheck_update.py`)
	- RAG index build
	- Stage 1 requirements generation
	- RAG sentence-quality crosscheck
	- requirements coverage crosscheck agent
	- `scripts/validate_stage1_gate.py`
- Required outputs:
	- `artifacts/stage1_requirements/ocr_extracts/index.csv`
	- `artifacts/stage1_requirements/taxonomy_crosscheck.md`
	- `artifacts/stage1_requirements/requirements_summary.csv`
	- `artifacts/stage1_requirements/requirements_summary.md`
	- `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
	- `artifacts/stage1_requirements/coverage_crosscheck.md`
	- `artifacts/stage1_requirements/missing_requirements_candidates.csv`
	- `artifacts/orchestrator/stage_01_report.md`
	- `artifacts/orchestrator/stage_01_result.md`

### Stage 2 Activity
- Runner: `scripts/run_stage1_specs_gate2.py`
- Steps:
	- `scripts/generate_stage2_specs.py`
	- Generate `artifacts/stage1_specs/architecture_profile_draft.json` and `architecture_profile_approval_request.md`.
	- Generate editable `artifacts/stage1_specs/architecture_mapping_preview.csv` with preliminary requirement-ID-to-candidate-block assignments, source classification, editable approved classification, generated block paragraph previews, review decisions, approved block, and reviewer notes.
	- Generate final architecture-profile summary tables and requirement-to-candidate-block traceability outputs.
	- Require user review and approval of `config/stage2_mirco_arc_profile.json` before Stage 2A mapping, including matching evidence hashes, reviewed draft hash, reviewed mapping-preview CSV hash, and resolved/waived critical or major ambiguity dispositions.
	- Do not enforce text, table, and figure extraction completeness as an approval prerequisite.
	- `scripts/run_specs_crosscheck_agent.py`
	- `scripts/validate_stage2_gate.py`
- Required outputs:
	- `artifacts/stage1_specs/specs.md`
	- `artifacts/stage1_specs/traceability_seed.csv`
	- `artifacts/stage1_specs/architecture_profile_draft.json`
	- `artifacts/stage1_specs/architecture_profile_approval_request.md`
	- `artifacts/stage1_specs/architecture_mapping_preview.csv`
	- `artifacts/stage1_specs/architecture_profile_requirements_summary.csv`
	- `artifacts/stage1_specs/architecture_profile_block_summary.csv`
	- `artifacts/stage1_specs/architecture_profile_traceability.csv`
	- `artifacts/stage1_specs/architecture_profile_ambiguity_dispositions.csv`
	- `artifacts/orchestrator/stage_02_report.md`
	- `artifacts/orchestrator/stage_02_crosscheck_report.md`
	- `artifacts/orchestrator/stage_02_result.md`

### Stage 2 Micro-Architecture Activity (Required Upstream Evidence)
- Runner: `scripts/run_stage2_micro_arc_gate.py`
- Steps:
	- Load the Stage 1 requirement summary and the configured Stage 2 architecture profile.
	- Identify the concrete block inventory from configured block definitions, source architecture actors, and interaction evidence.
	- Determine explicit source-section ownership and configured aliases before generic classification.
	- Identify non-specific source paragraphs by paragraph title: if the title does not identify a configured block or alias, retain the requirement as `Unassigned` source-function context.
	- Map only the remaining requirements to block inventory items using explicit ownership, mapping rules, and supported function evidence.
	- Write both `requirement_to_block_traceability.csv` and `unmapped_requirement_routing.csv`.
	- `scripts/run_stage2_micro_arch_and_crosscheck.py`
	- `scripts/validate_stage2_micro_arc_gate.py`
- Required outputs:
	- `artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv`
	- `artifacts/stage2_mirco_arc/block_inventory.csv`
	- `artifacts/stage2_mirco_arc/interface_catalog.csv`
	- `artifacts/stage2_mirco_arc/interaction_matrix.csv`
	- `artifacts/stage2_mirco_arc/function_decomposition.md`
	- `artifacts/stage2_mirco_arc/micro_architecture_report.md`
	- `artifacts/stage2_mirco_arc/architecture_crosscheck_report.md`
	- `artifacts/stage2_mirco_arc/architecture_crosscheck_report.md`
	- `artifacts/stage2_mirco_arc/stage2_mapping_crosscheck_report.md`
	- `artifacts/stage2_mirco_arc/unmapped_requirement_routing.csv`
	- `artifacts/orchestrator/stage_02_micro_arch_report.md`
	- `artifacts/orchestrator/stage_02_micro_arch_result.md`

### Stage 3 Activity (SRS)
- Runner: `scripts/run_stage3_srs_gate.py`
- Steps:
	- `scripts/run_srs_gen_spec_agent.py`
	- `scripts/run_srs_md_to_latex_agent.py`
	- `scripts/run_srs_crosscheck_agent.py`
	- `scripts/run_srs_latex_crosscheck_agent.py`
	- `scripts/validate_stage3_srs_gate.py`
- Required outputs:
	- `artifacts/stage3_srs/system_requirements_specification.md`
	- `artifacts/stage3_srs/system_requirements_specification.docx`
	- `artifacts/stage3_srs/srs_traceability_matrix.csv`
	- `artifacts/stage3_srs/stage2_srs_combined.tex`
	- `artifacts/orchestrator/stage_srs_report.md`
	- `artifacts/orchestrator/stage_srs_crosscheck_report.md`
	- `artifacts/orchestrator/stage_srs_latex_crosscheck_report.md`
	- `artifacts/orchestrator/stage_03_srs_result.md`

### Stage 4 Activity (ARS)
- Runner: `scripts/run_stage4_ars_gate.py`
- Steps:
	- `scripts/run_ars_gen_spec_agent.py`
	- `scripts/run_ars_crosscheck_agent.py`
	- `scripts/validate_stage4_ars_gate.py`
- Required outputs:
	- `artifacts/stage4_ars/analog_requirements_specification.md`
	- `artifacts/stage4_ars/analog_requirements_specification.docx`
	- `artifacts/stage4_ars/ars_traceability_matrix.csv`
	- `artifacts/orchestrator/stage_ars_report.md`
	- `artifacts/orchestrator/stage_ars_crosscheck_report.md`
	- `artifacts/orchestrator/stage_04_ars_result.md`

### Stage 5 Activity (DRS)
- Runner: `scripts/run_stage5_drs_gate.py`
- Steps:
	- `scripts/run_drs_gen_spec_agent.py`
	- `scripts/run_drs_crosscheck_agent.py`
	- `scripts/validate_stage5_drs_gate.py`
- Required outputs:
	- `artifacts/stage5_drs/digital_requirements_specification.md`
	- `artifacts/stage5_drs/digital_requirements_specification.docx`
	- `artifacts/stage5_drs/drs_traceability_matrix.csv`
	- `artifacts/stage5_drs/requirements_hierarchy_coverage_report.md`
	- `artifacts/orchestrator/stage_drs_report.md`
	- `artifacts/orchestrator/stage_drs_crosscheck_report.md`
	- `artifacts/orchestrator/stage_05_drs_result.md`

### Stage 6 Activity (Mixed-Signal Architecture Comparison)
- Runner: `scripts/run_stage6_architecture_comparison.py`
- CLI wrapper: `scripts/workflow_cli.py arch-compare --project-to-compare <project_name>`
- Steps:
	- Resolve sibling comparison project (`--project-to-compare`)
	- Read Stage 2A artifacts for both projects
	- Normalize block/interface names and map equivalent blocks
	- Compare interactions, hierarchy structure, and modularization quality
	- Emit scorecard and final consolidated report
- Required outputs:
	- `artifacts/comparison/block_inventory_comparison.csv`
	- `artifacts/comparison/block_interaction_matrix.csv`
	- `artifacts/comparison/hierarchy_comparison.csv`
	- `artifacts/comparison/modularization_assessment.md`
	- `artifacts/comparison/efficiency_scorecard.csv`
	- `artifacts/comparison/final_report.md`

## Stage 0 Phased Model (Mandatory)
- Phase 0: source baseline and scope lock
- Phase 1: structural parsing and segmentation
- Phase 2: concept harvesting
- Phase 3: taxonomy classification (`Comment`, `Definition`, `Assumption`, `Requirement`)
- Phase 4: relation/dependency modeling (`is-a`, `part-of`, `depends-on`, `drives`, `constrains`)
- Phase 5: non-narrative coverage expansion (tables, images, modes, numeric constraints)
- Phase 6: semantic risk and blocker analysis (`critical`, `major`, `minor`)
- Phase 7: Gate 0 packaging and Stage 1 handoff recommendation (`go`/`no-go`)

## Ontology-Driven Forward Mapping (Mandatory)

The forward-only workflow shall implement this ordered mapping:

1. Ontological analysis: extract source-backed concepts, entities, attributes, functions, properties, and relationships.
2. Generic role assignment: classify discovered source elements using the configured role taxonomy and source evidence.
3. Requirement mapping: map requirements to roles and architectural blocks through validated relationships and function/property evidence.

Stage 0 publishes `artifacts/stage0_ontology/ontology_requirement_links.csv`. Stage 2A must validate and consume that artifact before applying lexical fallback rules. No later stage may reverse this flow or create a feedback loop into Stage 0.

## Stage 0 Ontology Study Definition And Method (Mandatory)

- Ontology study means identifying and formalizing key concepts, properties, and relationships so mixed-signal behavior is unambiguous and consistently modeled.
- Stage 0 ontology coverage must include text, tables, figures/diagrams, captions/references, and evidence-bearing footnotes.

Comparison-for-completion workflow:
1. Read textual description.
2. Extract concepts and constraints from tables and visual artifacts.
3. Compare sources crosswise.
4. Use one source to complete gaps in another.
5. Record unresolved inconsistencies, duplications, and conflicts in semantic issues.

Required practical ontology outputs:
- Glossary of terms
- Concept map
- Requirements model
- Formal schema
- Automatic checks and traceability basis

## SRS, ARS, And DRS Generation Policy (Enforced)

## Architectural Mapping Order (Enforced)

Stage 2A follows this order for every Stage 1 requirement:

1. Build the concrete block inventory from the current project profile and architecture evidence.
2. Resolve explicit source-section ownership, including configured aliases such as `FIFO_CTRL` to `Smart FIFO`.
3. Build the source heading cascade. Keep the nearest meaningful parent paragraph title active while reading its numbered child items, including continuation pages.
4. Treat generic clock/reset paragraphs and requirements as synonyms for the PMU/power-management clock-reset unit when the current project profile defines `PMU` and the source or statement carries PMU, clock, reset, resetn, rst_n, POR, or clock/reset parent-title evidence.
5. Classify the active parent title. A title that does not identify a configured block or alias is non-block context; child titles such as `TIME SLOT LENGTH` inherit the parent context `ECG and BIA`.
6. Map eligible requirements to inventory blocks using explicit ownership first, then profile mapping rules and supported block `Function` evidence. Explicit ownership overrides the generic cascade.
7. Group non-block requirements by their cascaded parent title and preserve each complete source paragraph in `unmapped_requirement_routing.csv` with status `retained_as_non_block_function_context`.
8. SRS, ARS, and DRS consume these Stage 2A decisions; they do not remap requirements from the original specification. Each document renders one source-function context group per cascaded parent title. Equivalent local labels for one requirement family may be rendered as one normalized child paragraph beneath that parent, while preserving the parent title, source wording, and source IDs. A dedicated requirement moves to a concrete block paragraph only when current Stage 2A `Function` evidence supports that owner; otherwise it remains in the dedicated context.

The generic paragraph rule never overrides explicit Stage 1 ownership. The placeholder `Unassigned` is a routing state, not an authored architecture block.

Example cascade:

- `14.3.2 ECG and BIA` -> generic parent context
- `1. TIME SLOT LENGTH` -> inherits `ECG and BIA`
- `2. SELECT CHANNEL` -> inherits `ECG and BIA`
- a requirement explicitly owned by `ADSP` -> remains under `ADSP`, even if its local child title is generic

## Reset And Clock Table Derivation Rules (Enforced)

- Reset tables with columns named `req_id`, `source`, and `destination` or `target` (including equivalent OCR or naming variants) shall produce a derived requirement for every populated `req_id` row.
- Each reset-table derived requirement shall state that the signal identified in the `source` column shall be connected to the signal identified in the `destination` or `target` column.
- Clock tables with columns named `req_id`, `source`, and `destination` or `target`, plus an `F max`, `Frequency`, or equivalent frequency column, shall produce a derived requirement for every populated `req_id` row.
- Each clock-table derived requirement shall state both the source-to-destination/target connection and that the source signal shall have the frequency specified in the frequency column.
- The derived requirement shall preserve the source table paragraph, table title or figure identity, page/line provenance, and the upstream `req_id` in `covered_source_req_id` or equivalent traceability metadata.
- A table `req_id` row shall not be discarded merely because its row is structural rather than narrative; reset and clock connectivity/frequency rows are normative derived requirements.
- Reset and clock table derivations shall flow through Stage 2A block mapping and shall be rendered in SRS, ARS, and DRS with a single `Covers: <source req_id>` link.

### Common rules
- Requirement statements are normative (`shall`).
- Explicit Stage 1 domain classification is authoritative for downstream selection. Heuristic keyword matches must not route an explicitly Digital requirement into ARS.
- Missing System, Analog, or Digital categories are coverage diagnostics, not failures that justify creating requirements without source evidence.
- Stage 4 may skip ARS generation only when the current Stage 1 requirement summary has zero Analog-category rows with non-empty source requirement IDs. The runner must record the skip and the gate must independently recheck the condition.
- Clock/reset and power-sequencing summaries in generated specifications must be artifact-derived from current structural connection rows and normative source requirements. They must preserve source identifiers and may not rely on project-specific literals in reusable logic.
- OCR numbered-list labels without an explicit parent-section reference are list content, not dedicated source sections. Render any retained non-block item with neutral unheaded context rather than promoting the list label into a heading.
- Deprecated wording `Linked requirements` is not allowed in generated specs.
- Every authored SRS/ARS/DRS requirement header must use bold Markdown: `**[<PREFIX>-REQ-xxx] Requirement:**`. DOCX conversion independently applies bold Word runs to these headers after conversion.
- Before every authored SRS/ARS/DRS requirement header, emit a blank line, the portable empty paragraph `<p>&nbsp;</p>`, and a blank line. DOCX generation also applies visible paragraph spacing at the same boundary.
- Authored IDs must be unique in each document.
- General requirement catalogs are residual-only: mapped items belong in project-specific sub-block requirement paragraphs.
- Requirements that cannot be mapped to a concrete block must retain their complete original specification paragraph, the source paragraph reference, and the requirement statement in the Stage 2A unmapped routing ledger.
- SRS, ARS, and DRS must render each retained non-block requirement under a source-function context section, preserving its Stage 1 requirement statement and source reference. Requirements-only specifications must exclude tagged source `Comment`, `Definition`, and `Assumption` content from all rendered excerpts.
- A non-block context entry must never be silently dropped, converted into a block requirement, or represented only by a shortened summary; its ledger routing status must be `retained_as_non_block_function_context`. In every generated SRS, ARS, or DRS it is an atomic local requirement under `Source Function Context`, with the local `**[<PREFIX>-REQ-xxx] Requirement:**` header, complete source body, exactly one `Covers:` link, `[End]`, and source paragraph reference.
- Every authored requirement in a generated specification uses the portable boundary `blank line`, `<p>&nbsp;</p>`, `blank line`, `**[<PREFIX>-REQ-xxx] Requirement:**`. This rule is project-agnostic and is applied by the shared formatter; DOCX conversion preserves the boundary as visible paragraph spacing and bold header runs.
- SRS/ARS/DRS documents include `0. Document Navigation` with table of contents, internal indexes, document control tables, and table of tables.
- Table numbering starts at `Table 1` and remains sequential.
- Internal indexes include project-specific sub-block sub-paragraph entries.

### Stage 3 SRS rules
- Project-specific block sections use atomic entries.
- Non-block requirements are rendered in `Source Function Context` sections using the complete original specification paragraph and source paragraph reference from the Stage 2A ledger.
- Each atomic entry must include a bold `**[SRS-REQ-xxx] Requirement:**` header, its statement, and `Covers: <single upstream requirement ID>`.
- Crosscheck and gate fail on duplicate IDs, missing entries, or non-atomic Covers linkage.

### Stage 4 ARS rules
- The general requirements section is context plus residual unmapped requirements only.
- Mapped requirement details are captured only in project-specific analog sub-block requirement paragraphs.
- Non-block requirements are rendered in `Source Function Context` sections using the complete original specification paragraph and source paragraph reference from the Stage 2A ledger.
- Each atomic entry must include a bold `**[ARS-REQ-xxx] Requirement:**` header, its statement, and `Covers: <single upstream requirement ID>`.
- Crosscheck and gate fail if a redundant mapped-summary subsection appears in the general requirements section.

### Stage 5 DRS rules
- The general requirements section is context plus residual unmapped requirements only.
- Mapped requirement details are captured only in project-specific digital sub-block requirement paragraphs.
- Non-block requirements are rendered in `Source Function Context` sections using the complete original specification paragraph and source paragraph reference from the Stage 2A ledger.
- Each atomic entry must include a bold `**[DRS-REQ-xxx] Requirement:**` header, its statement, and `Covers: <single upstream requirement ID>`.
- Project-specific digital sub-block statement style is enforced as: `The <BlockName> block shall implement: <original requirement statement>.`
- Project-specific digital sub-block requirement statements must not use the phrase `the following atomic functionality`.
- Project-specific digital block sections include only digital or system-control blocks.
- Deprecated wording `Linked requirements` is forbidden.

## Crosscheck And Gate Policy
- A stage is `pass` only when required generation outputs and required crosscheck/gate artifacts exist.
- A stage activity is complete only when its crosscheck report is present and has no unresolved `critical` findings.
- If gate status is fail, orchestration must loop to that stage and rework before progression.

## Crosscheck Mapping (Stage 0 to 6)
- Stage 0 ontology -> `.github/agents/ontology-crosscheck.agent.md`
- Stage 1 requirements -> `.github/agents/requirements-coverage-crosscheck.agent.md`
- Stage 2 specs -> `.github/agents/specs-crosscheck.agent.md`
- Stage 2 micro-architecture -> `.github/agents/architectural-crosscheck.agent.md`
- Stage 3 SRS generation -> `.github/agents/srs-crosscheck.agent.md`
- Stage 3 SRS markdown-to-latex -> `.github/agents/srs-latex-crosscheck.agent.md`
- Stage 4 ARS generation -> `.github/agents/ars-crosscheck.agent.md`
- Stage 5 DRS generation -> `.github/agents/drs-crosscheck.agent.md`
- Stage 6 mixed-signal architecture comparison -> `.github/agents/architecture-comparison.agent.md`

## Handoff Contract
- Covered requirements and traceability status
- Executed validations and crosschecks
- Metrics and counts
- Open risks and blockers
- Severity labels (`critical`, `major`, `minor`)
- Next-stage `go` or `no-go` decision

