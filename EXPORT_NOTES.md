# MEMS_biosensor export notes

This package was trimmed to keep only project essentials for the MEMS_biosensor workflow.

## Included

- Agent definitions: `.github/agents/`
- VS Code tasks: `.vscode/tasks.json`
- Project config: `config/project_context.json`
- Source spec: `specs/st1vafe3bx.pdf`
- Pipeline scripts: `scripts/*.py`
- Documentation: `docs/*.md`
- Artifact templates: `templates/artifacts/**`
- Runtime artifact folders under `artifacts/` (including current generated stage outputs)
- Stage 6 mixed-signal comparison outputs under `artifacts/comparison/`

## Removed as non-essential

- Historical snapshots and archives
- Existing generated artifacts and logs
- Memory synchronization snapshots
- Non-target specs (Moro/Morag/iis2dlpc files)

## Environment setup

1. Use Python 3.11 (64-bit), or create and activate a Python 3.11 environment.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Run the workflow tasks from VS Code Tasks, or run scripts directly with Python.

## 2026-07-23 update summary

- SRS, ARS, and DRS generation now share a common readability/navigation baseline:
   - `0. Document Navigation` section
   - table of contents
   - internal section/paragraph index tables
   - document control tables (version history and reference documents)
   - table of tables
- Project-specific sub-block requirement paragraphs are normalized to plain field lines:
   - `Inputs`, `Outputs`, `Requirement ID`, `Statement`, `Covers`
   - no bullet prefix on those field lines
   - one-to-one `Covers` mapping per authored atomic entry
- Policy wording was made section-number agnostic for ARS/SRS/DRS checks and guidance.
- Updated layers include scripts (generator/crosscheck/gate), agent docs, templates, README, and workflow docs.
- Validated runs after update:
   - `python scripts/run_stage3_srs_gate.py` -> PASS
   - `python scripts/run_stage4_ars_gate.py` -> PASS
   - `python scripts/run_stage5_drs_gate.py` -> PASS

## 2026-08-11 update summary

- Stage1 tagged Req-ID extraction and validation were hardened for source-trace integrity.
- Table Req-ID detection now supports header variants (`Req_id`, `REQ_ID`, `Req ID`, `ID`) and custom ID families (for example `DDS_STBIO1_XXXXX`).
- Table-derived rows now carry explicit line provenance in notes (`table_line_info=pageX:lines[...]`).
- Cross-row contamination control:
   - No forward/next-row context jumps during table Req-ID reconstruction.
   - Standalone Req-ID lines reconstruct context from previous lines only.
- Tagged mode strict checks retained:
   - fail on generated IDs in tagged mode
   - fail on missing `source_req_id` in tagged mode
