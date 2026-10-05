# Stage-Gate Checklist

Note:
- Stage 6 mixed-signal architecture comparison is executed via `scripts/run_stage6_architecture_comparison.py` or `workflow_cli.py arch-compare` and produces artifacts under `artifacts/comparison/`.
- Gate numbering below (`Gate 6` and higher) belongs to long-horizon continuation stages (RTL and beyond), not to the Stage 6 architecture comparison activity.

## Gate 0
- Ontology baseline completed
- Glossary and semantic issues documented
- Semantic blockers classified
- Stage 0 phases 0-7 completed and recorded in `artifacts/orchestrator/stage_00_report.md`
- Ontology crosscheck completed and recorded in `artifacts/orchestrator/stage_00_crosscheck_report.md`
- Taxonomy classification complete (`Comment`/`Definition`/`Assumption`/`Requirement`)
- Relation/dependency graph complete (`is-a`, `part-of`, `depends-on`, `drives`, `constrains`)
- Stage 1 handoff decision explicit (`go`/`no-go`)
- Ontology study uses cross-source evidence (text + tables + figures/diagrams + captions/references)
- Comparison-for-completion analysis performed and reflected in ontology artifacts
- Ontology practical outputs present:
	- glossary of terms
	- concept map
	- requirements model
	- formal schema
	- automatic checks and traceability basis
- Placeholder/template ontology content rejected by crosscheck and gate validation

## Gate 1
- Functional requirements extracted
- Requirement IDs reused or assigned
- Summary table and sources validated
- Domain coverage reported without synthesizing requirements for an absent domain
- OCR index generated (`artifacts/stage1_requirements/ocr_extracts/index.csv`)
- Deterministic taxonomy crosscheck/update completed (`artifacts/stage1_requirements/taxonomy_crosscheck.md`)
- Requirements crosscheck completed (`artifacts/stage1_requirements/coverage_crosscheck.md`)
- Tagged mode hard checks:
	- No `generated_standard` rows when tagged mode is enabled
	- No missing `source_req_id` rows in tagged mode
- Table Req-ID extraction checks:
	- Notes include `table_line_info=pageX:lines[...]` for table-derived IDs
	- Context does not jump to next table row (no forward row contamination)
	- Standalone Req-ID lines bind only to previous-line row context

## Gate 2
- Formal specification artifacts completed
- Acceptance tests and assertions defined
- Specs crosscheck completed and recorded in `artifacts/orchestrator/stage_02_crosscheck_report.md`

## Gate 3
- Reference model implemented
- Core unit tests pass
- Python core crosscheck completed and recorded in `artifacts/orchestrator/stage_03_crosscheck_report.md`

## Gate 4
- Micro-architecture analysis completed
- Saved and closed `architecture_mapping_preview.xlsx` synchronized to `architecture_mapping_preview.csv` before execution; CSV/workbook requirement IDs and approved-block values match
- Requirement-to-block traceability generated
- Interface and interaction models documented
- Architectural crosscheck completed (post-Step-4)
- Crosscheck report available at `artifacts/stage2_mirco_arc/architecture_crosscheck_report.md`

## Stage 4 ARS Gate
- ARS generation is performed when one or more Analog-category source requirement IDs are present.
- When no such IDs are present, the runner records `ARS generation status: skipped`; the validator independently confirms the zero-row condition before passing.
- Explicit Digital classification prevents incidental power, clock, POR, or analog-domain wording from selecting a requirement for ARS.

## Stage 3 and Stage 5 Specification Content
- Clock/reset and power-sequencing summaries are source-backed by Stage 1 structural and normative evidence.
- OCR numbered-list labels without a parent-section reference are not rendered as dedicated source paragraphs.

## Gate 5
- Regression completed
- Golden vectors generated
- Vectors crosscheck completed and recorded in `artifacts/orchestrator/stage_05_crosscheck_report.md`

## Gate 6
- Design implementation traceable
- Lint-ready status achieved
- RTL design crosscheck completed and recorded in `artifacts/orchestrator/stage_06_crosscheck_report.md`

## Gate 7
- Verification regression complete
- No critical mismatches
- RTL verification crosscheck completed and recorded in `artifacts/orchestrator/stage_07_crosscheck_report.md`

## Gate 8
- Synthesis baseline available
- No must-fix blockers
- Synthesis crosscheck completed and recorded in `artifacts/orchestrator/stage_08_crosscheck_report.md`

## Gate 9
- Optimization plan prioritized
- Expected metric deltas quantified
- Optimization crosscheck completed and recorded in `artifacts/orchestrator/stage_09_crosscheck_report.md`

