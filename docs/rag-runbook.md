# RAG Runbook

## Objective
Create and query a local retrieval index for the initial specification to speed up requirements, ontology, and traceability work.

## Inputs
- OCR index: use `ocr_index_path` from `config/project_context.json`
- Source HTML/PDF referenced by index rows (preferred for quality)
- OCR page text files: artifacts/stage1_requirements/ocr_extracts/*.txt (fallback when source parsing is unavailable)

## Outputs
- SQLite index: use `rag_db_path` from `config/project_context.json`
- Build manifest: use `rag_manifest_path` from `config/project_context.json`
- Query results: use `rag_query_output_path` from `config/project_context.json`

## Build Index
python scripts/build_rag_index.py

Optional tuning:
- --chunk-size 1200
- --chunk-overlap 180

## Query Index
python scripts/query_rag_index.py --query "shall OR must OR requirement" --top-k 10

## Suggested Workflow
1. Run stage1 OCR extraction.
2. Run deterministic taxonomy cross-check/update from OCR index.
3. Build RAG index.
4. Query targeted concepts (mode names, registers, limits, timing, protocol).
5. Use retrieved chunks as evidence for downstream agents.

## Notes
- Query syntax uses SQLite FTS5.
- Keep top-k low (5-15) for focused evidence.
- Current builder uses HTML-clean mode when source is `.html` and records `html_clean_mode=true` in the configured manifest (`rag_manifest_path`).
- If `html_clean_mode` is false or missing, rebuild index before Stage 1 quality checks.
