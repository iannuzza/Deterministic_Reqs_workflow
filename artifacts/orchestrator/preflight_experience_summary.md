# Preflight Experience Extract

- Keywords: stage1, rag, pypdf, pandoc, ssl, path

### 1) Python command not found in terminal
- Attempt: run scripts with `python ...`
- Error: `python : The term 'python' is not recognized ...`
- Cause: python executable not exposed in terminal PATH.
- Working fix:
  - Use `py -3` for CLI tasks.
  - Keep VS Code tasks aligned to `py -3` for RAG scripts.
- Prevention:
  - Before first run, execute: `py -3 --version`

### 2) OCR failed because module missing in launcher runtime
- Attempt: `py -3 scripts/extract_requirements_ocr.py ...`
- Error: `ModuleNotFoundError: No module named 'pypdf'`
- Cause: package installed in another Python env, not in `py -3` runtime.
- Working fix:
  - Install for launcher runtime:
  - `py -3 -m pip install pypdf --trusted-host pypi.org --trusted-host files.pythonhosted.org`
- Prevention:
  - After install, run quick import:
  - `py -3 -c "import pypdf; print('ok')"`

### 3) pip SSL failure behind corporate certificate chain
- Attempt: install packages with plain pip.
- Error: `SSLCertVerificationError ... self signed certificate in certificate chain`
- Cause: corporate TLS interception.
- Working fix:
  - Add trusted hosts for pip installs:
  - `--trusted-host pypi.org --trusted-host files.pythonhosted.org`
- Prevention:
  - Use trusted-host flags by default when SSL issues appear.

### 4) Pandoc missing from machine
- Attempt: `pandoc ...`
- Error: `pandoc : The term 'pandoc' is not recognized ...`
- Cause: pandoc not installed.
- Working fix used:
  - Installed local pandoc and validated with `pandoc --version`.
- Additional note:
  - If package managers are unavailable (`winget`, `choco`, `scoop`), use local binary installation fallback.

### 5) Input path mismatch during conversion
- Attempt: `pandoc output/spec.md doc/spec.docx`
- Error: `output/spec.md: ... does not exist`
- Cause: source file was in docs/, not output/.
- Working fix:
  - `pandoc docs/spec.md -o docs/spec.docx`
- Prevention:
  - Verify file exists before conversion.

### 6) RAG automation initially not chained in standard pipeline
- Attempt: run normal first steps and expect RAG to refresh automatically.
- Issue: RAG build was separate from normal gate pipeline.
- Working fix:
  - Added composed task `stage1-ocr-refresh-rag`.
  - Wired pipelines to depend on composed task:
    - `pipeline-early-up-to-requirements`
    - `pipeline-first-3-gates`
- Result:
  - Each new run now refreshes OCR output and RAG index.

### 7) Stage1 text quality control for split/truncated requirements
- Need: Ensure requirement sentence in requirements_summary.csv is complete and source-faithful.
- Working fix:
  - Run `scripts/crosscheck_stage1_requirements_rag.py` after Stage1 generation.
  - Script repairs split/truncated phrases from OCR context and verifies each requirement against RAG chunks.
  - Cross-check evidence: `artifacts/stage1_requirements/requirements_rag_crosscheck.md`.
- Enforcement:
  - Added to first-3-steps pipeline and required by Stage 1 gate validator.

### 9) ARS deduplication between Section 4 and block sections
- Attempt: summarize mapped requirements in Section 4 and also list atomic entries in Section 7.
- Issue: duplicate coverage narrative creates review noise and inconsistency risk.
- Working fix:
  - Keep Section 4 as context + residual unmapped only.
  - Keep mapped requirement details only in Section 7 atomic block entries.
  - Add validator checks that fail if "Mapped requirements by analog block" appears in ARS markdown.
- Prevention:
  - Validate ARS output with:
    - `python scripts/run_stage4_ars_gate.py`

### 11) Stage 5 rerun failure due locked output CSV on cloud-synced storage
- Attempt: rerun Stage 5 DRS generation after prior execution.
- Error: `Permission denied` / `file is being used by another process` on `artifacts/stage5_drs/drs_traceability_matrix.csv`.
- Cause: external process lock (viewer/indexer/sync).
- Working fix:
  - Close external file viewers/editors using the CSV.
  - Rerun Stage 5 command.
- Prevention:
  - Avoid opening generated CSV in external tools during active reruns.
  - Prefer single-writer flow: complete run first, inspect artifacts after PASS.

### 13) New navigation/index formatting baseline for SRS/ARS/DRS
- Attempt: improve readability only in one generated spec family.
- Issue: inconsistent review experience across SRS, ARS, and DRS.
- Working fix:
  - Standardized generated markdown to include:
    - `0. Document Navigation`
    - table of contents
    - internal section/paragraph indexes
    - document control tables (version history + reference documents)
    - table of tables
  - Enforced plain-field project-specific sub-block paragraphs and one-to-one `Covers` links.
- Prevention:
  - Keep generator, crosscheck, gate validator, agent docs, templates, and README/workflow docs aligned.

### 14) Terminal parse error on unquoted paths containing `&`
- Attempt: run scripts using absolute paths that include `AMS_R&D` without full quoting.
- Error: `The ampersand (&) character is not allowed...`
- Cause: PowerShell tokenization on unquoted path segments containing `&`.
- Working fix:
  - Quote full executable and full script path when using absolute paths.
  - Example:
    - `& ".../.venv/Scripts/python.exe" ".../Req_spec_flow/scripts/run_stage3_srs_gate.py"`
- Prevention:
  - Always quote absolute paths in this workspace; prefer repo-relative script execution when possible.

### Run first 3 steps with automatic RAG refresh
- Via tasks:
  - `pipeline-first-3-gates`

### Manual equivalent
1. `py -3 scripts/extract_requirements_ocr.py --spec-folder specs --initial-spec "specs/i3g4250d.pdf"`
2. `py -3 scripts/build_rag_index.py --source-index artifacts/stage1_requirements/ocr_extracts/index.csv --db-path artifacts/rag/rag_index.sqlite`
3. `python scripts/init_stage0_artifacts.py`
4. `python scripts/validate_stage0_gate.py`
5. `python scripts/validate_stage1_gate.py`
6. `python scripts/validate_stage2_gate.py`

### RAG smoke query
- `py -3 scripts/query_rag_index.py --query "shall OR must OR requirement" --top-k 8 --db-path artifacts/rag/rag_index.sqlite`

## Validation Targets Per Run
- `artifacts/stage1_requirements/ocr_extracts/index.csv`
- `artifacts/rag/rag_index.sqlite`
- `artifacts/rag/index_manifest.json`
- `artifacts/orchestrator/stage_00_result.md`
- `artifacts/orchestrator/stage_01_result.md`
- `artifacts/orchestrator/stage_02_result.md`

## Update Rule
When a new failure pattern appears:
1. Add one entry in "Reusable Lessons" with exact error text.
2. Add the exact working command.
3. Add one prevention check.

### 17) Domain selection and empty ARS output
- Issue: incidental analog/power terminology could select an explicitly Digital requirement for ARS; after correction, a generic non-empty-ARS gate rejected the valid empty result.
- Working fix: use explicit Stage 1 domain classification before keyword heuristics. If no Analog-category source requirement IDs exist, record Stage 4 as skipped and have the validator independently verify that condition.
- Prevention: treat missing domain coverage as a warning and run `python scripts/workflow_cli.py run --stage 4` after domain-classification changes.

### 18) OCR numbered list promoted to a false source paragraph
- Issue: an OCR line such as a numbered routine name was treated as a section heading and appeared as a dedicated DRS paragraph.
- Working fix: require an explicit parent-section reference for dedicated-source rendering; retain incomplete OCR labels as neutral unheaded source context.
- Prevention: run `python scripts/workflow_cli.py run --stage 5` and confirm list items do not appear in DRS navigation as source paragraphs.

