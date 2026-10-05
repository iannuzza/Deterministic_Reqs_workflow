# OCR and RAG Pipeline File Map

## 1. Source Input and Conversion

- `specs/DDS_STBIO1.pdf`
  - Candidate primary source specification. It becomes the approved primary bootstrap context only after explicit S0 selection and approval; it is not the canonical workflow store.

- `scripts/s0_source_bootstrap.py`
  - Performs deterministic tagged/untagged/ambiguous assessment before OCR.
  - Preserves source evidence and proposes a req-ID prefix without silently mutating approved metadata.
  - Approved primary-source metadata drives applicable OCR, RAG, vocabulary, and taxonomy processing. Supplementary sources remain additive and approval-gated.

- `scripts/pdf_to_html.py`
  - Converts the source PDF into page-structured HTML.
  - Provides cleaner text and table context for later processing.

- `scripts/extract_requirements_ocr.py`
  - Main source extraction entry point after primary-source bootstrap approval.
  - Selects the configured PDF, HTML, or DOCX source.
  - Extracts text page by page.
  - Writes one text file per page.
  - Creates the OCR index.
  - Updates taxonomy terms from the source.

## 2. OCR Page Artifacts

- `artifacts/stage1_requirements/ocr_extracts/index.csv`
  - Page-level OCR manifest containing the source file, page number, extracted text path, and extraction status.

- `artifacts/stage1_requirements/ocr_extracts/DDS_STBIO1_p001.txt` through `DDS_STBIO1_p163.txt`
  - Individual page text files generated from the source document.
  - Preserve page-local OCR text.
  - Used as fallback evidence by Stage 1 and RAG.

## 3. Requirement Reconstruction

- `scripts/generate_stage1_requirements.py`
  - Converts OCR page text into structured requirements.
  - Detects normative statements such as `shall`, `must`, and `required`.
  - Detects source requirement IDs.
  - Reconstructs split OCR lines.
  - Reconstructs table rows and table headers.
  - Preserves source IDs such as `DDS_STBIO1_0201`.
  - Extracts clock, reset, interrupt, timing, measurement, and explicit table requirements.
  - Adds source page and line provenance.
  - Assigns requirement category and type.
  - Creates requirement summaries and review artifacts.

- `artifacts/stage1_requirements/requirements_summary.csv`
  - Main structured Stage 1 requirement output.

- `artifacts/stage1_requirements/requirements_raw.md`
  - Human-readable raw requirement extraction.

- `artifacts/stage1_requirements/requirements_summary.md`
  - Formatted requirement summary.

- `artifacts/stage1_requirements/table_row_review.csv`
  - Unified review list for explicit and structurally reconstructed table rows.

- `artifacts/stage1_requirements/table_row_review_request.md`
  - Manual-review request generated when table rows are ambiguous.

- `artifacts/stage1_requirements/source_matrix_edges.csv`
  - Exact structural edges extracted from source connection tables.
  - Example: `DDS_STBIO1_0201,Main Controller,Regmap`.

- `artifacts/stage1_requirements/stage1_report.md`
  - Stage 1 extraction and classification report.

## 4. OCR Quality Control and RAG Cross-Check

- `scripts/crosscheck_stage1_requirements_rag.py`
  - Checks extracted requirements against OCR and RAG evidence.
  - Finds likely truncated or split requirements.
  - Repairs statements using source context.
  - Compares requirement text with retrieved chunks.
  - Checks source provenance.
  - Rewrites corrected requirement summaries.
  - Produces the RAG cross-check report.

- `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
  - Reports exact matches, warnings, repaired statements, and failures between Stage 1 requirements and RAG evidence.

- `artifacts/stage1_requirements/coverage_crosscheck.md`
  - Reports requirement coverage and missing-source candidates.

- `artifacts/stage1_requirements/missing_requirements_candidates.csv`
  - Candidate requirements found in source evidence but not currently represented in the requirement summary.

## 5. RAG Configuration

- `config/project_context.json`
  - Defines the active project and pipeline paths, including the source specification, OCR index, RAG database, RAG manifest, query output, and domain vocabulary.

- `config/domain_vocabulary.json`
  - Provides deterministic RAG search expansion through protected acronyms, acronym expansions, synonym groups, phrase mappings, units, and terms that must not be merged.
  - These terms improve search recall but are not source evidence.

- `scripts/approved_vocabulary.py`
  - Loads the approved vocabulary profile used by deterministic retrieval and downstream authority checks.
  - Keeps stopwords, protected acronyms, synonym groups, and phrase mappings centralized instead of duplicated in retrieval modules.

- `data/canonical/canonical_store.sqlite`
  - Canonical SQLite authority for approved requirement revisions, provenance, classifications, mappings, profiles, audit events, and immutable snapshots.
  - RAG indexes and CSV/Markdown/XLSX exports are derived retrieval or presentation artifacts and are not authoritative requirement stores.

## 6. RAG Index Construction

- `scripts/build_rag_index.py`
  - Builds a separate local SQLite retrieval index from the approved primary-source OCR manifest and applicable supplementary evidence.
  - Reads `ocr_extracts/index.csv`.
  - Loads OCR page text.
  - Prefers cleaned HTML text when available.
  - Normalizes text.
  - Detects text, table, figure, and section boundaries.
  - Creates overlapping chunks.
  - Generates normalized terms.
  - Writes SQLite metadata and FTS5 indexes.
  - Writes the build manifest.
  - Does not replace canonical SQLite authority or silently change approved source metadata.
  - SQLite/FTS5 is the current default retrieval backend and remains replaceable; authoritative workflow code must not depend on its schemas or query internals.

  Important internal functions:
  - `_load_index`: loads OCR page metadata.
  - `_extract_clean_html_pages`: reads cleaned HTML pages.
  - `_chunk_text`: creates overlapping text chunks.
  - `_chunk_page_text`: identifies text, table, and figure chunks.
  - `_controlled_terms`: creates normalized search terms.
  - `_prepare_db`: creates the SQLite schema.

- `artifacts/rag_DDS_STBIO1/rag_index.sqlite`
  - Local RAG database containing:
    - `chunks`: raw text and provenance metadata.
    - `chunk_fts`: original-text lexical FTS5 index.
    - `chunk_terms_fts`: normalized-term FTS5 index.

- `artifacts/rag_DDS_STBIO1/index_manifest.json`
  - Records index configuration and statistics, including chunk size, overlap, source, page count, and HTML-clean mode.

## 7. RAG Querying

- `scripts/query_rag_index.py`
  - Queries the SQLite RAG index.
  - Supports `lexical` BM25 search over original text.
  - Supports `normalized` search over normalized terms and approved vocabulary expansions.
  - Supports `hybrid` Reciprocal Rank Fusion of lexical and normalized results.
  - Retrieval is deterministic, local, and evidence-preserving. Semantic retrieval is optional, local-only, version-pinned, and never required for the authoritative workflow.
  - Retrieval results are evidence candidates only; they do not become workflow truth or replace the approved snapshot boundary.

  Important internal functions:
  - `_fetch_lexical`: performs BM25 retrieval.
  - `_fetch_normalized`: searches normalized terms.
  - `_rrf_fuse`: combines rankings.
  - `_controlled_terms`: expands the user query.
  - `_fts_or_query`: creates a safe FTS5 `OR` query.

- `artifacts/rag_DDS_STBIO1/last_query_results.md`
  - Markdown export of the latest retrieved evidence chunks, including page, chunk, score, and source metadata.

## 8. Downstream Consumers

- `scripts/generate_stage0_ontology_outputs.py`
  - Uses OCR-indexed source evidence to create ontology and role mappings.

- `scripts/run_stage2_micro_arch_and_crosscheck.py`
  - Uses Stage 1 requirements and source evidence to generate the architecture interaction model.

- `artifacts/stage2_mirco_arc/interaction_matrix.csv`
  - Architecture-level representation of structural edges such as `Main Controller -> Regmap`.

- `scripts/run_srs_gen_spec_agent.py`
  - Consumes approved snapshot materialization, Stage 1 requirements, OCR provenance, and cross-check results to generate the SRS.

- `scripts/approved_snapshot_resolver.py`
  - Requires an explicit snapshot ID or explicit latest-approved selection for authoritative downstream generation.
  - Rejects incomplete, impacted, or project-mismatched snapshots.

- `scripts/generate_snapshot_reports.py` / `scripts/generate_architecture_sysml.py`
  - Produce derived XLSX and SysML artifacts from approved snapshots only.
  - Preserve snapshot and provenance metadata; SysML requires full approved block requirement coverage unless explicit partial export is requested.

## 9. End-to-End Flow

```text
DDS_STBIO1.pdf
  -> s0_source_bootstrap.py (select + approve primary bootstrap)
  -> pdf_to_html.py
  -> extract_requirements_ocr.py
  -> ocr_extracts/index.csv + page text files
  -> generate_stage1_requirements.py
  -> requirements_summary.csv
  -> build_rag_index.py
  -> rag_index.sqlite
  -> query_rag_index.py
  -> evidence chunks
  -> crosscheck_stage1_requirements_rag.py
  -> canonical_store.sqlite + approved snapshot
  -> validated requirements and snapshot-derived architecture/SRS/ARS/DRS/SysML outputs
```
