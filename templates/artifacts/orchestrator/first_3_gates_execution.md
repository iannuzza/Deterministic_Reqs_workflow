# First 3 Gates Execution Playbook

Date: <YYYY-MM-DD>

## Objective
- Execute and validate the first three gates of the workflow:
  - Gate 0 (ontology baseline)
  - Gate 1 (requirements extraction)
  - Gate 2 (spec formalization)

## Prerequisites
- Python 3.11 (64-bit)
- `config/project_context.json` is present and contains valid `source_spec_path` and Stage 1/RAG defaults

## Step Sequence
1. Bootstrap OCR index from the initial specification source:
  - `python scripts/extract_requirements_ocr.py`
2. Refresh RAG index from OCR output:
  - `py -3 scripts/build_rag_index.py`
3. Generate and quality-check Stage 1 requirements outputs:
  - `python scripts/generate_stage1_requirements.py`
  - `python scripts/crosscheck_stage1_requirements_rag.py`
4. Integrate the micro-architectural analysis agent template in the project environment:
  - `python scripts/init_stage0_artifacts.py`
  - Expected integration target: `artifacts/stage2_mirco_arc/uArch_analysis.agent.md`
5. Validate Gate 0 artifacts:
   - `python scripts/validate_stage0_gate.py`
6. Validate Gate 1 artifacts:
   - `python scripts/validate_stage1_gate.py`
7. Validate Gate 2 artifacts:
   - `python scripts/validate_stage2_gate.py`

## Expected Artifacts
- Gate 0:
  - `artifacts/stage0_ontology/ontology.md`
  - `artifacts/stage0_ontology/glossary.csv`
  - `artifacts/stage0_ontology/semantic_issues.md`
  - `artifacts/stage2_mirco_arc/uArch_analysis.agent.md`
  - `artifacts/orchestrator/stage_00_report.md`
  - Phase evidence in Stage 00 report:
    - Phase 0 source baseline and scope lock
    - Phase 1 structure mapping
    - Phase 2 concept harvesting
    - Phase 3 taxonomy classification
    - Phase 4 relation/dependency map
    - Phase 5 non-narrative expansion
    - Phase 6 blocker analysis
    - Phase 7 handoff recommendation (`go`/`no-go`)
- Gate 1:
  - `artifacts/stage1_requirements/requirements_raw.md`
  - `artifacts/stage1_requirements/requirements_summary.csv`
  - `artifacts/stage1_requirements/requirements_summary.md`
  - `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
  - `artifacts/orchestrator/stage_01_report.md`
- Gate 2:
  - `artifacts/stage1_specs/specs.md`
  - `artifacts/stage1_specs/traceability_seed.csv`
  - `artifacts/orchestrator/stage_02_report.md`

## Result Log
- Gate 0: <pass|fail>
- Gate 1: <pass|fail>
- Gate 2: <pass|fail>

## Notes
- If any gate fails, fix missing artifacts and rerun the corresponding validator.
