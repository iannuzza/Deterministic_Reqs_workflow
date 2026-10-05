# Deterministic_Reqs_workflow
Requirement-driven design flow implemented through a deterministic pipeline chain

# STBIO_AI

Generic reusable scaffold for a multi-stage engineering workflow driven by specialized agents.

## Workflow Abstract

This workflow converts tagged or untagged engineering specifications into validated, traceable system documentation. It is organized as an agentic AI pipeline in which each stage has a focused mission, explicit input/output artifacts, and an independent gate before the next stage can consume its results. The agentic structure is used at design time to separate specialized responsibilities such as ontology analysis, requirement extraction, formalization, architecture mapping, SRS generation, ARS generation, DRS generation, and crosschecks. Runtime execution is deterministic: the executable workflow is driven by Python scripts and local artifact files, and the standard CLI stage flows do not make AI/LLM calls.

The pipeline extracts requirements, semantics, functions, properties, and relationships while preserving source IDs or assigning stable generated IDs with provenance. It identifies architectural roles and functions and generates a Stage 2 architecture profile review package with a preliminary requirement-ID-to-block mapping preview, generated block paragraph previews, summary tables, and traceability outputs. Stage 2A requirement-to-block mapping starts only after explicit approval linked to current evidence hashes, the reviewed draft fingerprint, and resolved or waived critical and major ambiguities. Independent gates verify coverage, mapping correctness, semantic evidence, approval freshness, and forward-only traceability across the resulting system requirements specification (SRS), analog requirement specification (ARS), and digital requirement specification (DRS) hierarchy.

The main advantages of this structure are modularity, auditability, repeatability, and flexibility. Individual stages can be rerun or improved without redesigning the full workflow, artifacts create reviewable handoffs, and project-specific behavior is supplied through configuration and generated evidence rather than hardcoded source-document assumptions. The tradeoffs are stricter artifact contracts, more intermediate files to maintain, and explicit approval points that slow execution when source evidence or architecture ownership is ambiguous. These tradeoffs are intentional: they favor deterministic engineering traceability over opaque automatic regeneration.

## Current Project Status (2026-10-01)

- Approved snapshot: `snap-b2e8101b00dc6909feaed885`.
- The DRS uses Stage 1 OCR-backed overview and explicitly block-attributed descriptions with source provenance and an audit trail. Descriptive prose remains separate from normative requirements and `Covers` traceability.
- Current DRS: 55 requirements, 13 mapped, and 42 unassigned. The descriptive audit retained 5 overview records and 6 block descriptions, with 0 overview rejects.
- The generated Top Level Overview is formatted in paragraphs of at most two sentences. The latest DRS generation and crosscheck passed; `tests/test_descriptive_summary.py` passed 74 tests.
- The dedicated Stage 5 gate and central downstream coherence passed in the preceding descriptive rollout. They were not rerun after the latest formatting-only update.
- The workflow GUI and v4 presentation show Stage 1 descriptive evidence, parallel specification generation, and approved IPOS lineage. The deck has 19 slides; slide 14 shows separate descriptive-evidence and normative-lineage paths.
- Open boundary: baseline-protected DRS section 4.1 still says `need clarification` for the ISPU role, while section 3.1 includes Stage 1 ISPU prose. Do not revise that table or its preservation baseline without explicit authorization.

For the restore checkpoint, artifact fingerprints, and handoff notes, see [`local_memory/checkpoint.md`](local_memory/checkpoint.md), [`local_memory/chat_handoff.md`](local_memory/chat_handoff.md), and [`docs/drs-descriptive-baseline.md`](docs/drs-descriptive-baseline.md).

### System Traceability (2026-10-05)

- In the GUI, **Traceability Reports** offers **Primary source requirements** (`requirements_summary.csv` exported to `primary_source_requirements.xlsx`) and **Source spec integrated reqs** (`integrated_requirements.csv` exported to `source_spec_integrated_reqs.xlsx`). Successful generation opens the selected workbook in Excel. The integrated workbook adds `source_type` in column D (`Primary` or `Supplementary`). These two XLSX files reproduce Stage 1 extracted catalogs and are labeled as derived catalogs, not approved snapshot authority. The snapshot is still selected to generate/register them.
- **All levels** produces the hierarchy reports and `all_requirements_traceability.xlsx`, including both imported and generated requirements. The inclusive workbook uses approved snapshot lineage; generated requirement statements must not be read from generated Markdown as upstream authority.
- **System Traceability Diagram** shows approved Primary-to-Supplementary coverage in the Supplementary box and table when that relationship exists, using the Supplementary requirement denominator. Downstream specification boxes and rows show coverage only for their named upstreams. Selecting a table row highlights its diagram block and connected arrows in blue; selecting a block or arrow selects the corresponding table row (the arrow selects its target block). Redraws retain the selection; the explicit Refresh action clears it.
- The new report classification compares catalog provenance with the Primary specification identified by the Stage 1 OCR index; relationship matching and table/diagram selection use payload node IDs rather than STBIO-specific requirement IDs or document names. This is a scoped claim about these features; older SysML/architecture paths elsewhere in the GUI and central validator still contain project-specific names.
- For the current approved snapshot (`snap-b2e8101b00dc6909feaed885`), the Primary catalog has 271 rows; the integrated catalog has 191 Primary and 123 Supplementary rows. Its Supplementary-to-Primary relationship reports 123 / 123 (100.0%). These counts describe this project's artifacts, not hardcoded thresholds. The latest focused traceability suite has 16 passing tests; this is not a full Stage 0-7 gate rerun. See the latest System Traceability checkpoint for verification boundaries.

## Workflow Step-by-Step

`workflow_cli.py run` accepts nine ordered stage keys: `0 -> 1 -> 2 -> 2a -> 3 -> 4 -> 5 -> 6 -> 7`. Each stage runs its own crosschecks and gate before the next stage; an ascending contiguous range stops at the first failure.

1. **Stage 0 (`0`, S0): Ontology baseline.** Extract source-backed concepts, functions, properties, relationships, and ontology links; validate Gate 0.
2. **Stage 1 (`1`, S1): Source requirements.** Read the primary specification, extract and tag requirements by OCR/parsing, preserve source IDs or assign stable IDs with provenance, and run duplicate-ID, text, RAG, and coverage checks before Gate 1. Only Stage 1 reads the initial specification directly.
3. **Stage 2 (`2`, S2): Formalization and review package.** Consume Stage 0/1 artifacts to build the specs baseline, architecture-profile draft, requirement-to-block mapping preview, block paragraph previews, traceability seed, and review summaries; validate Gate 2. The preview is a review surface, not approved canonical authority.
4. **Stage 2A (`2a`, S2A): Approved micro-architecture mapping.** After review of the profile and synchronization/approval of the mapping preview, map requirements to approved blocks, produce block inventory, interaction and traceability artifacts, and run independent semantic checks plus the Stage 2A gate. Approval hashes and ambiguity dispositions must be current.

**SysML architecture handoff (after Stage 2A, before Stage 3; not a CLI stage key):** From the validated Stage 2A mapping and an approved snapshot, the GUI generates architecture `.sysml` files under `artifacts/stage2_mirco_arc/sysml/` and runs a structural-only review. The model review must pass before Stage 3; full requirement coverage is checked in the final SysML phase, not here.

5. **Stage 3 (`3`): SRS.** Consume the approved immutable mapping snapshot and validated Stage 2A artifacts; generate the System Requirements Specification, traceability, crosschecks, and gate.
6. **Stage 4 (`4`): ARS.** Generate and validate analog requirements and traceability against the approved snapshot and Stage 2A ownership. Stage order does not make SRS prose normative authority for ARS.
7. **Stage 5 (`5`): DRS.** Generate and validate digital requirements, hierarchy traceability, and consistency/coverage against the approved snapshot. Generated Markdown is not source authority.
8. **Stage 6 (`6`): Digital IPOS.** Generate implementation-oriented requirements for approved digital allocations and run the Digital IPOS gate.
9. **Stage 7 (`7`): Analog IPOS.** Generate and gate the analog implementation scope; an empty analog partition is valid when no requirements apply.

**Final SysML phase (after Stage 7; not a CLI stage key):** Run `python scripts/workflow_cli.py final-sysml --use-latest-approved` (or select a snapshot explicitly). This generates the complete snapshot-bound `.sysml` set under `artifacts/stage2_mirco_arc/sysml/`, runs structural review, and validates downstream coverage, allocations, ownership, partition, and end-to-end coherence. It is a separate command, not included automatically in `workflow_cli.py run --to-stage 7`.

Review, merge impact/approval, taxonomy/retrieval refresh, Architecture Map Review, mapping approval, and immutable snapshot creation are separate GUI/canonical-service operations between runners. Diagram labels such as S2B-S2H are **not** extra CLI run stages or a second mandatory stage chain. A supplementary-source merge requires refreshed dependent Stage 0/1/2 evidence and fresh mapping approval and snapshot before downstream regeneration. Stages 3-7 use one approved snapshot. Optional cross-project architecture comparison is another separate command.

The canonical workflow store is `data/canonical/canonical_store.sqlite`. Retrieval/index SQLite is derived and rebuildable; CSV, JSON, Markdown, XLSX, and SysML files are derived or compatibility artifacts only. The current SQLite/FTS5 retrieval backend is replaceable and must not become workflow authority. Downstream generation, reports, SysML, and authoritative GUI actions consume approved immutable snapshots with approved vocabulary, taxonomy, and architecture context. The authoritative path is deterministic, local-only, and does not require LLM, network, or cloud services.

Optional continuation stages (defined by agents but outside the current executable baseline): numeric/model core; vectors/verification; RTL design/verification; synthesis; optimization.

## Repository Structure

- `.github/agents/` and `.github/skills/`: agent definitions, shared instructions, and stage-gate guidance.
- `.vscode/`: editor settings and task shortcuts.
- `artifacts/`: generated stage outputs, source-ingestion records, RAG indexes, audits, validation reports, and IPOS block documents. These are organized by stage or artifact purpose.
- `config/`: project context, approved architecture profile, ontology taxonomy, and retrieval configuration.
- `data/canonical/canonical_store.sqlite`: canonical workflow store and approval/snapshot state.
- `docs/`: architecture/workflow documentation, runbooks, generated-specification guidance, and presentation assets.
- `local_memory/`: project-local checkpoints, handoffs, environment notes, and sync manifest.
- `logs/`: runner and workflow execution logs.
- `retrieval/`: reusable local retrieval and semantic-index modules.
- `scripts/`: workflow CLI/GUI, stage runners, generators, crosschecks, services, and validators.
- `specs/`: source specifications and reviewed project inputs.
- `templates/`: prompt templates, document templates, and artifact templates.
- `tests/`: Python unit and contract tests.
- `requirements.txt`: Python runtime dependencies.

Generated stage artifacts are not interchangeable with canonical authority. In particular, RAG indexes and most files under `artifacts/` are derived outputs; the approved snapshot and canonical workflow store control downstream generation.

## Runtime

- Python: 3.11 (64-bit)

## Workflow GUI

Run `python scripts/workflow_gui.py` for the desktop workflow interface.

- `Architecture Map Review` is the reviewer workspace for approving or changing preliminary architecture mappings. It opens the editable mapping-preview CSV and Markdown, opens the CSV in Excel, and reports live `review_decision` counts plus the recorded Stage 2A gate decision and reviewer. For each source requirement ID, the reviewer confirms or changes the candidate/approved block, the approved classification, and the decision (`approved`, `reassigned`, `rejected`, or `needs_clarification`), with optional reviewer notes.
- The reviewed mapping establishes the approval gate for the next workflow steps: Stage 2A can proceed only after every row has an approved decision (`approved` or `reassigned`), reassigned rows have an approved block, and the GUI records the reviewed CSV hash together with the approver and approval time in the architecture profile.
- The Stage 2 approval dialog retains CSV review actions, including opening the preview in Excel, approving all rows, and recording the reviewed CSV hash to enable Stage 2A.
- **Mandatory mapping synchronization:** the saved and closed `architecture_mapping_preview.xlsx` is synchronized to `architecture_mapping_preview.csv` before Stage 2A approval/execution or Stage 2B snapshot freezing. The flow blocks on unsaved, duplicate, missing, unknown, or mismatched rows; a stale CSV cannot be used instead.
- Workflow action controls are arranged in visible rows so review, diagnostics, table review, DRS shortcut, SysML, snapshot reports, and conflict actions remain visible without relying on horizontal scrolling.
- The single-stage and range selectors use executable keys `0, 1, 2, 2a, 3, 4, 5, 6, 7`; the GUI offers a separate Architecture Map Review action (`S2F`). Review and approval operations are not CLI stage-range members.
- GUI fonts are enlarged across controls, artifact viewers, CSV tables, chat, logs, and the workflow diagram.
- Hovering any workflow stage box displays a popup with its purpose. A failed stage instead displays its captured failure reason; the diagram hint line retains the same message.
- Button, control, and stage-hover popups are positioned from the live widget location and screen bounds so the full popup remains visible; if there is not enough room below the control, the popup flips above or clamps inside the visible display margin.

## Core Runner Scripts

All commands are run from repository root.

Each stage full-flow runner prints a startup artifact banner to the console so users can see expected outputs and locations before execution.

### Stage runners

- `python scripts/run_stage0_gate0.py`
  - Stage 0 init, concrete ontology artifact generation, Stage 0 report generation, ontology crosscheck, Gate 0 validation.
- `python scripts/run_stage1_requirements_gate1.py`
  - OCR extraction, taxonomy cross-check/update, RAG build, requirements generation, RAG crosscheck, coverage crosscheck, Gate 1 validation.
- `python scripts/run_stage1_specs_gate2.py`
  - Specs generation, specs crosscheck, Gate 2 validation.
- `python scripts/run_stage2_micro_arc_gate.py`
  - Micro-architecture generation/crosscheck and micro-architecture gate validation.
- `python scripts/validate_stage2_profile.py`
  - Validates source-backed interaction mappings, source-ID uniqueness/coverage, and profile-to-source edge agreement before Stage 2A generation.
- `python scripts/run_stage3_srs_gate.py`
- `python scripts/run_stage3_srs_gate.py --use-latest-approved`
  - SRS generation, md->LaTeX conversion, SRS crosschecks, Stage 3 gate validation. DOCX export is optional and is skipped when pandoc is not available on PATH.
- `python scripts/run_stage4_ars_gate.py --use-latest-approved`
  - ARS generation, ARS crosscheck, Stage 4 gate validation. DOCX export is optional and is skipped when pandoc is not available on PATH.
- `python scripts/run_stage5_drs_gate.py --use-latest-approved`
  - DRS generation, DRS crosscheck, Stage 5 gate validation. DOCX export is optional and is skipped when pandoc is not available on PATH.
- `python scripts/run_stage6_digital_ipos_gate.py --use-latest-approved`
  - Generate and validate Digital IPOS from an approved snapshot.
- `python scripts/run_stage7_analog_ipos_gate.py --use-latest-approved`
  - Generate and validate Analog IPOS from an approved snapshot; a valid-empty partition is supported when there are no applicable requirements.

### Snapshot and optional operations

- `python scripts/workflow_cli.py freeze-stage2b --reviewer <name>`
  - Freeze the explicitly reviewed and approved architecture mapping as a downstream snapshot.
- `python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>`
  - Run the optional cross-project architecture comparison. It is separate from the executable Stage 0-7 pipeline, despite the legacy `run_stage6_architecture_comparison.py` script name.
- `python scripts/workflow_cli.py final-sysml --use-latest-approved`
  - Generate and centrally validate the complete final SysML set from one approved snapshot.

## Stage 1 Tagged Req-ID Policy (2026-08-11)

Stage 1 now enforces stricter tagged-source behavior for requirement IDs preserved from source tables and text.

- Tagged mode integrity:
  - If tagged mode is enabled, generated IDs are rejected for tagged rows.
  - Missing `source_req_id` for tagged rows is treated as a rule failure.
- Req-ID detection:
  - Supports configured/custom families (for example `DDS_STBIO1_XXXXX`) across OCR text, including non-bracketed cases.
  - Supports table header variants (`Req_id`, `REQ_ID`, `Req ID`, `ID`, plus configured aliases).
- Table row extraction:
  - Captures `table_line_info=pageX:lines[...]` in notes for traceability.
  - Prevents cross-row contamination by avoiding forward/next-row jumps.
  - For standalone Req-ID lines, row context is resolved from previous lines only (same logical row intent).
- Crosscheck/gate behavior:
  - Strict tagged checks remain hard-fail conditions.
  - Non-policy ontology completeness checks are warnings and do not block Gate 1.

### Stage 1 Non-Tagged Source Discovery Policy

When a source specification has no usable requirement tags, Stage 1 identifies requirements through a deterministic, reviewable sequence:

1. Prefer the highest-fidelity available representation (native text or HTML before OCR), retaining source file, page, section, table, and line provenance.
2. Detect normative and constraint language such as `shall`, `must`, `should`, `will`, `required`, prohibitions, limits, ranges, and conditional obligations; include structurally equivalent numbered-list and table statements.
3. Reconstruct statements split across page and table boundaries before classifying them, while excluding document metadata, headings, references, glossary-only entries, and illustrative examples.
4. Allocate stable generated requirement IDs from source location and preserve the verbatim source statement separately from any normalized form.
5. Classify each candidate and record extraction method, provenance, and review decision; require reviewer disposition for ambiguous candidates before architecture mapping.
6. Crosscheck candidate counts by source section and table, and compare deterministic reruns to detect silent requirement loss.

Approved recovery of an extraction miss is permitted only when a source-backed statement, stable identifier, and precise provenance are recorded. Recovery must be generic, deterministic, and reviewed; it must not introduce source-specific behavior into downstream SRS, ARS, or DRS generation.

### Supporting scripts

- `python scripts/run_taxonomy_crosscheck_update.py --index-csv artifacts/stage1_requirements/ocr_extracts/index.csv`
  - Deterministic taxonomy rules update from OCR index and source spec; writes `artifacts/stage1_requirements/taxonomy_crosscheck.md`.

- `python scripts/run_step0_preflight.py`
  - Reads `docs/execution-experience-log.md` and writes `artifacts/orchestrator/preflight_experience_summary.md`.
- `python scripts/run_until_step3.py`
  - Runs preflight + first three gates sequence and stops on first failure.
- `python scripts/run_stage2_micro_arch_and_crosscheck.py`
  - Produces Stage 2 micro-architecture artifacts and architectural crosscheck report.
- `python scripts/sync_repo_memory_local.py`
  - Syncs local memory metadata to `local_memory/sync_manifest.json`.

## Deterministic Local CLI (No LLM Calls)

Use the local CLI to run stage flows and validations using only Python scripts.

### Strict Forward Pipeline Rule

The executable workflow CLI supports a single-pass, forward-only stage range:

`Stage 0 -> Stage 1 -> Stage 2 -> Stage 2A -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 Digital IPOS -> Stage 7 Analog IPOS`

Stage keys are `0`, `1`, `2`, `2a`, `3`, `4`, `5`, `6`, and `7`. Stage 2B snapshot freezing and the related review/approval operations are explicit commands/services outside ordinary stage ranges. Stages 3-7 require one approved snapshot selected with `--snapshot-id` or `--use-latest-approved`. Each run validates after every stage and stops on the first failure; retries, loops, and backward transitions are not supported. Stage 4 can be skipped only when its runner and validator confirm there are no applicable Analog source requirement IDs. The `drs-after-stage2a` command is the approved forward shortcut from Stage 2A to Stage 5.

- Help:
  - `python scripts/workflow_cli.py --help`
- Status:
  - `python scripts/workflow_cli.py status`
- Run standalone taxonomy update (deterministic):
  - `python scripts/workflow_cli.py taxonomy-update`
- Run the optional architecture comparison against another workspace project:
  - `python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>`
  - `python scripts/workflow_cli.py arch-compare --project-to-compare <project_name> --output-dir artifacts/comparison`
- Run the top-down pipeline through Stage 3:
  - `python scripts/workflow_cli.py run --from-stage 0 --to-stage 3`
- Run the complete top-down pipeline:
  - First run through mapping: `python scripts/workflow_cli.py run --from-stage 0 --to-stage 2a`
  - Review and freeze the mapping: `python scripts/workflow_cli.py freeze-stage2b --reviewer <name>`
  - Then run snapshot-backed stages: `python scripts/workflow_cli.py run --from-stage 3 --to-stage 7 --use-latest-approved`
- Generate and validate only Digital IPOS:
  - `python scripts/workflow_cli.py digital-ipos --use-latest-approved`
- Generate and validate only Analog IPOS:
  - `python scripts/workflow_cli.py analog-ipos --use-latest-approved`
- Generate and centrally validate final SysML:
  - `python scripts/workflow_cli.py final-sysml --use-latest-approved`
- Run advisory downstream retrieval/mapping validation:
  - `python scripts/workflow_cli.py validate-downstream`
- Run the approved forward Stage 2A-to-DRS shortcut:
  - `python scripts/workflow_cli.py drs-after-stage2a`
- Validate all gates:
  - `python scripts/workflow_cli.py validate --all --use-latest-approved`

Operational notes:
- Stage ranges are inclusive and follow: `0 -> 1 -> 2 -> 2a -> 3 -> 4 -> 5`.
- Ranges may start at any stage but must remain ascending and contiguous; Stage `2a` is mandatory before Stage `3` when included.
- Use `--dry-run` to print commands without executing them.
- Each stage is attempted once; any failure stops the run.
- `taxonomy-update` is a standalone command and can be run before Stage 1 full flow when switching spec sources.
- Stage 6 is Digital IPOS. The optional architecture comparison is a standalone `arch-compare` command and is not part of stage ranges.
- Comparison output defaults to `artifacts/comparison/`; override with `--output-dir` or set a custom final report path with `--output-path`.

## Quick Run Guide

### Run first three gates

`python scripts/run_until_step3.py`

Sequence:
1. `run_step0_preflight.py`
2. `run_stage1_requirements_gate1.py`
3. `run_stage0_gate0.py`
4. `run_step3_gate1_gate2.py`

### Run the complete workflow after mapping approval

Run Stages 0-2A, complete Architecture Map Review and freeze the Stage 2B snapshot, then run Stages 3-7 with that approved snapshot. See the commands above; snapshot-backed stages must not be run from unapproved mapping artifacts.

Single-stage example:
- `python scripts/workflow_cli.py run --stage 3 --use-latest-approved`

Ascending range example:
- `python scripts/workflow_cli.py run --from-stage 3 --to-stage 5 --use-latest-approved`

### Run optional architecture comparison after Stage 5

1. `python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>`
2. Optional custom output folder:
  - `python scripts/workflow_cli.py arch-compare --project-to-compare <project_name> --output-dir artifacts/comparison`

## SRS/ARS/DRS Policy Highlights

### Source-Baselined Hierarchy Coverage

Stage 5 produces `artifacts/stage5_drs/requirements_hierarchy_coverage_report.md` from the current traceability matrices. It measures each document against the complete unique Stage 1 source-requirement ID catalog using `source_req_id`, reports Source-to-SRS coverage explicitly, and lists source IDs absent from the SRS or every applicable lower-level document.

Lower-level documents are evaluated only for their declared requirement scope. A document with no in-scope authored requirements is reported as not applicable; retained source-function context rows do not inflate coverage. The ARS and DRS union measures applicable lower-level coverage, while end-to-end coverage requires an SRS link and a link in at least one applicable lower-level document. These rules are artifact-driven and apply to all projects without requirement-ID, source-file, or block-name exceptions.

Stage 2A profile validation runs before interaction-matrix generation. It compares the active profile with `artifacts/stage1_requirements/source_matrix_edges.csv` and blocks endpoint mismatches, duplicate requirement IDs, duplicate source/destination cells, missing Stage 1 IDs, empty endpoints, and missing source edges. The duplicate-cell rule is data-driven and applies to every declared connection matrix; it prevents multiple requirement IDs from being silently coalesced into one source/destination cell.

### Stage 2A Architecture Mapping Order

The architecture analysis uses the following deterministic order:

1. Identify the concrete block inventory from the project profile and architecture evidence.
2. Apply explicit source-section ownership and configured aliases first.
3. Maintain a cascading source-heading context through numbered child items and continuation pages.
4. Classify the active parent title. A parent without a configured block or alias is generic source-function context; its child items inherit that context.
5. Map eligible requirements to block inventory items using profile mapping rules and block `Function` support. Explicit ownership always overrides the generic cascade.
6. Group and record non-block requirements in `unmapped_requirement_routing.csv` with `retained_as_non_block_function_context`.
7. Pass the Stage 2A traceability and routing artifacts to SRS, ARS, and DRS without rereading or remapping the source specification.

For example, `ECG and BIA` is the parent context inherited by `TIME SLOT LENGTH`, `SELECT CHANNEL`, and similar child items. `BOOT Phase` and `Configuration Phase` are handled the same way. Explicit ownership such as `ADSP` or the configured `FIFO_CTRL` alias is preserved. `Unassigned` is a routing state and is never authored as a real block.

- Requirement statements use normative wording (`shall`).
- SRS, ARS, and DRS generators/crosscheckers are project-agnostic: they must load project-specific names, requirement IDs, signal paths, and ownership only from current runtime artifacts; no project-specific literal, alias, or special-case branch is allowed in reusable scripts.
- `Linked requirements` wording is deprecated and rejected by checks.
- Project-specific block sections use atomic authored entries.
- Authored IDs are unique:
  - `SRS-REQ-xxx` in SRS
  - `ARS-REQ-xxx` in ARS
  - `DRS-REQ-xxx` in DRS
- `Covers` is one-to-one: each atomic entry maps to a single upstream requirement ID.
- General requirement catalogs are residual-only; mapped items are captured in project-specific sub-block requirement paragraphs.
- Each SRS/ARS/DRS document includes a `0. Document Navigation` section with:
  - table of contents
  - internal section/paragraph index
  - document control tables (version history and reference documents)
  - table of tables
- Table numbering starts at `Table 1` and remains sequential.
- Internal index tables include project-specific sub-block sub-paragraph entries (for example `GPIO`, `ADCInterface`).
- In project-specific sub-block paragraphs, `Inputs`, `Outputs`, `Requirement ID`, `Statement`, and `Covers` are plain field lines (no markdown bullet prefix).
- For DRS project-specific digital sub-block requirement statements, enforced style is:
  - `The <BlockName> block shall implement: <original requirement statement>.`
- Reset/clock connectivity-table rows containing a requirement ID plus source and destination/target are structural derived requirements. Their statement preserves exact source and destination/target paths, includes exact `F max`/frequency when present, and includes the clock-gating text; `No` or absent gating is rendered as `without clock gating`.
- Generic clock/reset paragraphs and requirements are treated as synonyms for the PMU/power-management clock-reset unit when the current project profile defines `PMU` and the source or statement carries PMU, clock, reset, resetn, rst_n, POR, or clock/reset parent-title evidence. Block-specific reset behavior remains with its explicit owner.
- Interrupt-table rows use the table fields directly: `The <Interrupt label> interrupt shall be connected to the <Destination label> block.` when a destination exists, otherwise `The <Interrupt label> interrupt shall be connected to <Description label> to bit <bit label>.` Original table IDs remain in `Covers:`.
- Stage 1 retains table title, headers, and continuation-page context for rows carrying requirement IDs. SRS/ARS/DRS consume those structural Stage 1 statements without rereading the source specification.
- Domain classification is authoritative downstream: an explicitly Digital requirement is not selected for ARS solely because its wording mentions power, clocks, POR, or an analog domain. Category coverage reports missing domains as a warning; it must not create artificial requirements.
- Stage 4 is validly skipped when the current Stage 1 summary contains no Analog-category rows with source requirement IDs. The runner records `ARS generation status: skipped`; the Stage 4 validator independently verifies the same condition before passing the skip.
- SRS and DRS clock/reset and power-sequencing summaries must be derived from current Stage 1 structural clock/reset rows and source requirements, preserving signal paths, timing, enables, resets, and source IDs. Do not invent sequence details.
- A numbered OCR list item is not a source paragraph. Downstream dedicated-source and source-context rendering requires a real parent-section reference; otherwise it must retain a neutral unheaded-context label.

## Stage 0 Phases

Stage 0 uses a mandatory phased model:

- Phase 0: source baseline and scope lock
- Phase 1: structural parsing and segmentation
- Phase 2: concept harvesting
- Phase 3: taxonomy classification
- Phase 4: relation/dependency modeling
- Phase 5: non-narrative coverage expansion
- Phase 6: semantic risk and blocker analysis
- Phase 7: gate packaging and handoff recommendation

## Stage 0 Ontology Study Mission

Ontology study is defined as identifying and formalizing key concepts, properties, and relationships so mixed-signal behavior is unambiguous and consistently modeled.

Stage 0 ontology analysis is cross-source by design and must include:
- textual description
- tables and mode/register tables
- figures/diagrams (including timing and block diagrams)
- captions, references, and evidence-bearing footnotes

Required comparison-for-completion workflow:
1. Read textual description.
2. Extract concepts/constraints from tables and visual artifacts.
3. Compare cross-source semantics.
4. Use one source to complete gaps in another.
5. Report inconsistencies/duplications/conflicts in semantic issues.

Mandatory practical outputs:
- glossary of terms
- concept map
- requirements model
- formal schema
- automatic checks and traceability basis

Stage 0 full-flow script sequence:
1. `python scripts/init_stage0_artifacts.py`
2. `python scripts/generate_stage0_ontology_outputs.py`
3. `python scripts/generate_stage0_ontology_report.py`
4. `python scripts/run_ontology_crosscheck_agent.py`
5. `python scripts/validate_stage0_gate.py`

Gate hardening notes:
- Stage 0 fails on placeholder/template artifacts.
- Stage 0 fails if ontology-study sections are missing.
- Crosscheck includes quality counters (concepts, glossary rows, table/image/mode evidence).

## Main Artifact Targets

- Stage 0:
  - `artifacts/stage0_ontology/ontology.md`
  - `artifacts/stage0_ontology/glossary.csv`
  - `artifacts/stage0_ontology/ontology_requirement_links.csv`
  - `artifacts/stage0_ontology/semantic_issues.md`
  - `artifacts/orchestrator/stage_00_report.md`
- Stage 1:
  - `artifacts/stage1_requirements/taxonomy_crosscheck.md`
  - `artifacts/stage1_requirements/requirements_summary.csv`
  - `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
  - `artifacts/stage1_requirements/coverage_crosscheck.md`
- Stage 2 specs:
  - `artifacts/stage1_specs/specs.md`
  - `artifacts/stage1_specs/traceability_seed.csv`
  - `artifacts/stage1_specs/architecture_profile_draft.json`
  - `artifacts/stage1_specs/architecture_profile_approval_request.md`
  - `artifacts/stage1_specs/architecture_mapping_preview.csv`
  - `artifacts/stage1_specs/architecture_profile_requirements_summary.csv`
  - `artifacts/stage1_specs/architecture_profile_block_summary.csv`
  - `artifacts/stage1_specs/architecture_profile_traceability.csv`
  - `artifacts/stage1_specs/architecture_profile_ambiguity_dispositions.csv`
- Stage 2 micro-architecture:
  - `artifacts/stage2_mirco_arc/block_inventory.csv`
  - `artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv`
  - `artifacts/stage2_mirco_arc/interface_catalog.csv`
  - `artifacts/stage2_mirco_arc/interaction_matrix.csv`
  - `artifacts/stage2_mirco_arc/architecture_crosscheck_report.md`
  - `artifacts/stage2_mirco_arc/stage2_mapping_crosscheck_report.md`
- Stage 3 SRS:
  - `artifacts/stage3_srs/system_requirements_specification.md`
  - `artifacts/stage3_srs/srs_traceability_matrix.csv`
  - `artifacts/orchestrator/stage_srs_crosscheck_report.md`
- Stage 4 ARS:
  - `artifacts/stage4_ars/analog_requirements_specification.md`
  - `artifacts/stage4_ars/ars_traceability_matrix.csv`
  - `artifacts/orchestrator/stage_ars_crosscheck_report.md`
- Stage 5 DRS:
  - `artifacts/stage5_drs/digital_requirements_specification.md`
  - `artifacts/stage5_drs/drs_traceability_matrix.csv`
  - `artifacts/orchestrator/stage_drs_crosscheck_report.md`
- Stage 6 Digital IPOS:
  - `artifacts/stage6_digital_ipos/ipos_traceability_matrix.csv`
  - `artifacts/stage6_digital_ipos/blocks/<block-slug>/` (Markdown, DOCX, descriptive audit, and materialization audit per materialized block)
- Stage 7 Analog IPOS:
  - `artifacts/stage7_analog_ipos/ipos_traceability_matrix.csv`
  - `artifacts/stage7_analog_ipos/blocks/<block-slug>/` (Markdown, DOCX, descriptive audit, and materialization audit per materialized block)
- Snapshot and traceability reports:
  - `artifacts/traceability_reports/`
  - `artifacts/traceability_reports/primary_source_requirements.xlsx`
  - `artifacts/traceability_reports/source_spec_integrated_reqs.xlsx`
  - `artifacts/traceability_reports/all_requirements_traceability.xlsx`
  - `data/canonical/canonical_store.sqlite`
- Optional architecture comparison:
  - `artifacts/comparison/block_inventory_comparison.csv`
  - `artifacts/comparison/block_interaction_matrix.csv`
  - `artifacts/comparison/hierarchy_comparison.csv`
  - `artifacts/comparison/modularization_assessment.md`
  - `artifacts/comparison/efficiency_scorecard.csv`
  - `artifacts/comparison/final_recommendation.md`
  - `artifacts/comparison/final_report.md`

## VS Code Task Pipelines

Common task labels:
- `pipeline-first-3-gates`
- `stage2-micro-arc-full-flow`
- `stage3-srs-full-flow`
- `stage4-ars-full-flow`
- `stage5-drs-full-flow`
- `pipeline-full-through-stage4-ars`
- `pipeline-full-through-stage5-drs`
- `pipeline-rag-bootstrap`

## References

- Workflow details: `docs/orchestration-spec.md`
- Diagram: `docs/workflow-diagram.md`
- CLI quick card: `docs/cli-quick-card.md`
- RAG runbook: `docs/rag-runbook.md`
- Execution lessons: `docs/execution-experience-log.md`

## Notes

- Source specification is configured in `config/project_context.json` and read directly only by Stage 1 OCR extraction.
- Stages 2 to 5 are artifact-driven and do not read the initial source specification file directly.
- Hard guard enforcement for Stage 2+ independence is implemented in `scripts/guard_stage2_plus_spec_independence.py`.
- Guard is executed by Stage 2+ generation entrypoints and fails fast if direct source-spec coupling is reintroduced.
- Stage 3/4/5 DOCX outputs depend on pandoc. If pandoc is not installed or not on PATH, SRS/ARS/DRS generation and gate validation continue without DOCX conversion.
- Replace placeholder values (`<...>`) before production use.
- On cloud-synced paths, transient file locks can block CSV overwrite during stage reruns; retry after closing external viewers/editors.

## Switching To A New PDF Spec

For a new project/specification file, update only Stage 1 source selection; Stage 2+ will consume regenerated artifacts.

Primary method (recommended):
1. Place the new PDF under `specs/`.
2. Update `config/project_context.json`:
  - `source_spec_path`: `specs/<your_new_file>.pdf`
3. Re-run Stage 1 to rebuild OCR + requirements artifacts:
  - `python scripts/run_stage1_requirements_gate1.py`
  - This run includes deterministic taxonomy cross-check/update and report generation.
4. Continue normal downstream flows (Stage 2+):
  - `python scripts/run_stage1_specs_gate2.py`
  - `python scripts/run_stage2_micro_arc_gate.py`
  - `python scripts/run_stage3_srs_gate.py`
  - `python scripts/run_stage4_ars_gate.py`
  - `python scripts/run_stage5_drs_gate.py`

One-shot override (without editing config):
- You can pass a source file directly to OCR extraction:
  - `python scripts/extract_requirements_ocr.py --initial-spec specs/<your_new_file>.pdf`
- `--initial-spec` takes precedence over `source_spec_path` for that run.

Optional explicit taxonomy-only refresh after OCR extraction:
- `python scripts/run_taxonomy_crosscheck_update.py --index-csv artifacts/stage1_requirements/ocr_extracts/index.csv`
- Or via CLI wrapper: `python scripts/workflow_cli.py taxonomy-update`

## Tagged Requirement ID Mode

Use this mode when the source specification already contains explicit requirement IDs in tagged form such as:

- `[DDS_STBIO1_0104] Requirement: The system shall ... [End]`

The Stage 1 generator and Stage 1 RAG crosscheck both read rules from `config/project_context.json` under `requirement_id_rules`.

Current STBIO_AI configuration:

- `tagged_source_mode`: `true`
- `source_req_id_patterns`: `"DDS_STBIO1_\\d{4}"`
- `tag_label`: `"Requirement"`
- `tag_terminator`: `"[End]"`
- `table_id_columns_priority`: `"Req_id"`, `"ID"`, `"Spec ID"`

How to adapt for a different project:

1. Update `source_req_id_patterns` to match your new source Req-ID format.
2. If your tag label changes (for example `Requirement` to `Req`), update `tag_label`.
3. If your requirement terminator differs from `[End]`, update `tag_terminator`.
4. Set `table_id_columns_priority` to the preferred table headers for requirement ID lookup.
5. Re-run Stage 1 full flow:
  - `python scripts/run_stage1_requirements_gate1.py`

Behavior notes:

- Tagged mode captures requirement text from the tag start through the terminator.
- The extracted source requirement ID is preserved in notes as `source_req_id=...`.
- If no source Req-ID is matched, generated IDs are still produced as fallback.

