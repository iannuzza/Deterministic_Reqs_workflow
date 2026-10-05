# CLI Quick Card

Fast command reference for deterministic local workflow execution.

## Help And Status

```bash
python scripts/workflow_cli.py --help
python scripts/workflow_cli.py status
python scripts/workflow_cli.py taxonomy-update
```

## Daily Stable Runs

```bash
# Run an ascending range from Stage 0 through Stage 3
python scripts/workflow_cli.py run --from-stage 0 --to-stage 3

# Run one stage
python scripts/workflow_cli.py run --stage 3

# Run an ascending range from Stage 3 through Stage 5
python scripts/workflow_cli.py run --from-stage 3 --to-stage 5

# Generate and centrally validate the complete final SysML set
python scripts/workflow_cli.py final-sysml --snapshot-id <approved_snapshot_id>

# Run full Stage 0 through Stage 5
python scripts/workflow_cli.py run --from-stage 0 --to-stage 5

# Approved forward shortcut from Stage 2A to Stage 5
python scripts/workflow_cli.py drs-after-stage2a
```

Each run executes one stage or an ascending contiguous range, executes each selected stage once, validates before advancing, and stops on the first failure. Retries, loops, skipped stages, and backward transitions are not supported.

## Validation

```bash
# Validate one gate
python scripts/workflow_cli.py validate --stage 4

# Validate all gates
python scripts/workflow_cli.py validate --all
```

## Taxonomy Update (Deterministic, No LLM)

```bash
# Standalone taxonomy update from OCR index
python scripts/run_taxonomy_crosscheck_update.py --index-csv artifacts/stage1_requirements/ocr_extracts/index.csv

# Same action via workflow CLI
python scripts/workflow_cli.py taxonomy-update
```

## Stage 6 Mixed-Signal Architecture Comparison

```bash
# Run Stage 6 comparison through the single-stage workflow command
python scripts/workflow_cli.py run --stage 6 --project-to-compare <project_name>

# Equivalent standalone Stage 6 comparison command
python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>

# Custom output directory for comparison artifacts
python scripts/workflow_cli.py arch-compare --project-to-compare <project_name> --output-dir artifacts/comparison

# Direct script entrypoint
python scripts/run_stage6_architecture_comparison.py --project-to-compare <project_name>
```

Expected Stage 6 outputs:
- `artifacts/comparison/block_inventory_comparison.csv`
- `artifacts/comparison/block_interaction_matrix.csv`
- `artifacts/comparison/hierarchy_comparison.csv`
- `artifacts/comparison/modularization_assessment.md`
- `artifacts/comparison/efficiency_scorecard.csv`
- `artifacts/comparison/final_report.md`

## Safe Preview Mode

```bash
# Show commands only (no execution)
python scripts/workflow_cli.py run --from-stage 0 --to-stage 3 --dry-run
python scripts/workflow_cli.py validate --all --dry-run
```

## Stage Keys

- Canonical order: `0 -> 1 -> 2 -> 2a -> 3 -> 4 -> 5`
- Stage `2a` is mandatory before Stage `3`
- Stage 6 comparison is a standalone command after Stage 5 (`arch-compare`)
- Accepted aliases include values such as `stage2`, `2-a`, and `2_a`

## Execution Policy

- Canonical order: `0 -> 1 -> 2 -> 2a -> 3 -> 4 -> 5`
- Start: any stage, when run as a single stage or ascending range
- Attempts: one per stage
- Failure: stop immediately
- Correction: rerun the affected stage or an ascending range