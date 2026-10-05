# Stage 1 Runbook (Requirements Extraction)

## Inputs
- Source specifications in `specs/` folder (initial file example: `specs/i3g4250d.pdf`)
- Project scope and constraints

## Steps
1. Read initial specification source from `specs/` (HTML or PDF) and generate OCR index artifacts.
2. Run deterministic taxonomy cross-check/update from OCR index (`scripts/run_taxonomy_crosscheck_update.py`).
3. Build RAG index from OCR/source evidence.
4. This Stage 1 read is the only direct source-spec read in the Stage 0 to 6 baseline.
5. Extract explicit functional requirements by category (System, Analog, Digital).
6. Enforce requirement ID policy:
	- Tagged source mode: preserve source requirement IDs (`source_req_id`) as final IDs.
	- Non-tagged mode: assign generated IDs (`SYS-RQ-###`, `ANA-RQ-###`, `DIG-RQ-###`) when needed.
	- In non-tagged mode, derive candidates from normative/constraint language, numbered-list and table structure, and source-section context. Preserve source file, page, section, table, line, extraction method, and reviewer disposition for every generated ID.
	- Prefer native text or HTML to OCR where available; reconstruct page/table-boundary continuations before classification, and exclude metadata, headings, references, glossary-only text, and illustrative examples.
	- Reconcile candidate coverage by section and table and compare deterministic reruns to identify unexpected losses. Send ambiguous candidates to review before Stage 2 mapping.
7. Extract table-linked requirement IDs with table trace metadata:
	- Persist `table_line_info=pageX:lines[...]` in notes.
	- Avoid forward row jumps when reconstructing context.
	- For standalone Req-ID lines, use previous-line row context only.
8. Derive reset-table requirements from rows containing `req_id`, `source`, and `destination` or `target` columns, including equivalent OCR or naming variants. State the required source-to-destination/target connection.
9. Derive clock-table requirements from rows containing the same connectivity columns plus `F max`, `Frequency`, or equivalent. State the required connection and frequency constraint.
10. Preserve the table title/figure identity, source paragraph, page/line information, original `req_id`, and derivation kind in the summary and traceability metadata.
11. Produce summary table with source paragraph references and notes.
12. Produce stage report and handoff artifacts for Stage 2+ artifact-driven flows.

## Approved Recovery Of Extraction Misses

An approved recovery may add a missed source requirement only when it has a source-backed statement, a stable source or generated identifier, and precise location provenance. Record the recovery method in the notes so Gate 1 can verify it. The recovery rule must be deterministic and source-agnostic; downstream stages consume the resulting Stage 1 artifact and must not infer new source behavior.

## Source Paragraph Cascade

Stage 1 source metadata must preserve the paragraph hierarchy used by downstream mapping:

1. Detect a meaningful parent heading such as `ECG and BIA`, `BOOT Phase`, or `Configuration Phase`.
2. Keep that parent active while extracting numbered child paragraphs and while the source continues on the next page.
3. Store the child location together with the inherited parent context in the `source` field.
4. Do not infer a block from requirement keywords when the inherited parent is generic; Stage 2A will route it to source-function context.
5. Preserve explicit source owners separately so Stage 2A can override the generic cascade when the source identifies a concrete block.

The resulting mapping relationship is: `source parent -> child paragraph -> requirement ID -> concrete block or non-block context`. SRS, ARS, and DRS consume this relationship from Stage 2A artifacts.

## Gate 1 tagged-ID integrity checks

- In tagged mode, `generated_standard` rows are not allowed.
- In tagged mode, each requirement row must carry `source_req_id`.
- ID extraction should support configured/custom families such as `DDS_STBIO1_XXXXX`.

## Outputs
- `artifacts/stage1_requirements/ocr_extracts/index.csv`
- `artifacts/stage1_requirements/taxonomy_crosscheck.md`
- `artifacts/stage1_requirements/requirements_raw.md`
- `artifacts/stage1_requirements/requirements_summary.csv`
- `artifacts/stage1_requirements/requirements_summary.md`
- `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
- `artifacts/stage1_requirements/coverage_crosscheck.md`
- `artifacts/stage1_requirements/missing_requirements_candidates.csv`
- `artifacts/orchestrator/stage_01_report.md`
