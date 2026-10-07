- Active project directory: repository root (`.`), wherever this clone is located.
- Active source specification: specs/DDS_STBIO1.pdf
- Use python scripts/... commands in this workspace.

- Latest restart checkpoint: `2026-10-06-local-fixes-snapshot-history` at
  2026-10-06 16:35:30. Read the newest `local_memory/chat_handoff.md` and
  `local_memory/checkpoint.md` entries before older records below.
- Active Git clone: `C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/Deterministic_Reqs_workflow`.
  The separate original `../STBIO_AI` is reference-only. Preserve the dirty
  worktree; no commit or rollback backup has been created.
- Verified Windows interpreter:
  `C:/Users/syslocadm1906/AppData/Local/Programs/Python/Python311/python.exe`.
  Existing terminals can still use original STBIO_AI as cwd; set the clone root
  or use absolute script/test paths to avoid running the wrong project.
- Current authority: snapshot `snap-b2e8101b00dc6909feaed885`, project `STBIO`,
  314 approved rows; SRS/ARS/Analog IPOS valid-empty, DRS 55, Digital IPOS 259.
- Final history contract across all specification types: new approved snapshot
  appends a dated minor-version row and preserves old rows; same snapshot leaves
  all history rows, dates, authors and version unchanged.
- Latest checks: history/contract/descriptive tests 90 PASS; GUI 46 PASS;
  fingerprint/coherence suite 19 PASS; central coherence 0 findings; Stage 2+
  independence guard exit 0. These were separate checks, not a full pipeline run.
- DRS repair/gate passed at 15:47:22 before the final shared-history code change.
  Current artifacts still pass coherence after the change; no full regeneration
  or newly approved production snapshot was exercised for the final history edit.
- Unfixed unrelated DRS classifier issue: `_is_non_normative_table_row` references
  undefined `text`. Dynamic test imports also have editor resolution warnings;
  verified interpreter imports/tests pass.
- PowerShell may run in constrained language mode; avoid generic collection
  construction and unsafe shell writes. Use the existing tools and verified Python.

- Current downstream restore state (2026-09-29): approved snapshot `snap-b2e8101b00dc6909feaed885`; full Digital IPOS gate PASS (259/8), Analog IPOS gate PASS valid-empty (0/0), full downstream coherence PASS (0 findings). Focused descriptive tests PASS (60). The newest `local_memory/checkpoint.md` and `chat_handoff.md` supersede older pilot/blocked notes; `docs/ipos-descriptive-rendering.md` retains historical and current Main Controller hashes. Keep IPOS 1.1/1.2 natural technical prose via the common composer/validator, with no new authority inputs.

- Current ontology mapping artifacts:
  - Role catalog: config/ontology_role_taxonomy.json
  - Ontology-to-requirement links: artifacts/stage0_ontology/ontology_requirement_links.csv
  - Independent Stage 2A mapping report: artifacts/stage2_mirco_arc/stage2_mapping_crosscheck_report.md

- Current Stage 2A validation sequence:
  - scripts/validate_stage2_profile.py
  - scripts/validate_stage2_mapping.py
  - scripts/validate_stage2_micro_arc_gate.py

- Current execution invariant: workflow_cli invokes exactly one runner and one gate validator per selected stage, in forward order, with immediate stop on failure and no retry/loop behavior.

- Stage source-read contract:
  - Stage 1 only may read the source spec directly.
  - Stage 2+ must be artifact-driven.
  - Enforcement guard: scripts/guard_stage2_plus_spec_independence.py

- Active artifact context:
  - OCR index: artifacts/stage1_requirements/ocr_extracts/index.csv
  - RAG DB: artifacts/rag_DDS_STBIO1/rag_index.sqlite
  - RAG manifest: artifacts/rag_DDS_STBIO1/index_manifest.json
  - RAG last query output: artifacts/rag_DDS_STBIO1/last_query_results.md

- Canonical stage order:
  - S0 -> S1 -> S2 -> S2A -> S2B -> S2C -> S2D -> S2E -> S2F -> S2G -> S2H -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7
  - Stage 2A is mandatory before Stage 3. Approved snapshots and profiles govern authoritative downstream actions.

- Crosscheck/gate runners:
  - Stage 0: python scripts/run_stage0_gate0.py
  - Stage 1: python scripts/run_stage1_requirements_gate1.py
  - Stage 2: python scripts/run_stage1_specs_gate2.py
  - Stage 2a: python scripts/run_stage2_micro_arc_gate.py
  - Stage 3: python scripts/run_stage3_srs_gate.py
  - Stage 4: python scripts/run_stage4_ars_gate.py
  - Stage 5: python scripts/run_stage5_drs_gate.py
  - Stage 6: python scripts/workflow_cli.py run --stage 6 --snapshot-id <approved_snapshot_id> (Digital IPOS)
  - Stage 7: python scripts/workflow_cli.py run --stage 7 --snapshot-id <approved_snapshot_id> (Analog IPOS)
  - Optional comparison, not a numbered stage: python scripts/workflow_cli.py arch-compare --project-to-compare <project_name>

- Deterministic local CLI mode:
  - Primary runner: python scripts/workflow_cli.py
  - Strict execution: run --stage N or run --from-stage N --to-stage M, with M >= N
  - One attempt per selected stage; validation runs before advancement and failure stops the pipeline
  - Approved forward shortcut: drs-after-stage2a

- Current authored requirement header convention:
  - SRS: [SRS-REQ-###] Requirement:, where ### is 001-999
  - ARS: [ARS-REQ-###] Requirement:, where ### is 001-999
  - DRS: [DRS-REQ-###] Requirement:, where ### is 001-999
  - The old field form `Requirement ID: *RS-REQ-###` is deprecated and rejected by crosschecks/gates.

- Current strengthened GUI stage selectors:
  - Single-stage and range menus expose S0, S1, S2, S2A, S2B, S2C, S2D, S2E, S2F, S2G, S2H, Stage 3, Stage 4, Stage 5, Stage 6 Digital IPOS, Stage 7 Analog IPOS, and Optional Architecture Comparison.
  - Optional Architecture Comparison is the final selectable menu entry.
  - CLI-supported contiguous ranges remain limited to the executable legacy runner keys; approval-only S2B-S2H selections route to GUI/service guidance.
  - Compact workflow diagram has vertical scrolling, horizontal Shift-wheel scrolling, and Ctrl-wheel zoom.
  - Tooltip popups dismiss on pointer exit, click, focus loss, popup entry/exit, and timeout.

- Stage 1 specs fix:
  - `scripts/generate_stage2_specs.py` must pass `_approved_classifications(repo_root)` into `_write_mapping_preview`.
  - Verified with `python scripts/run_stage1_specs_gate2.py`: generation, crosscheck, and Gate 2 PASS.

- GUI checkpoint:
  - Main GUI file: scripts/workflow_gui.py
  - Work Area viewer supports read-only text/CSV viewing, horizontal scrollbars, Markdown internal jumps, requirement-summary ID counts, and Ctrl+F search.

- Restoration timestamp:
  - 2026-08-11 (restored for STBIO_AI)
  - 2026-08-19 (updated with GUI, gate, and SRS/ARS/DRS format fixes)
  - 2026-08-21 (restored local memory and chat handoff from current artifacts)
  - 2026-09-08 (restored from latest canonical-authority, Stage 1 specs, and GUI checkpoint)

- Latest Stage 2 architecture note (2026-08-19):
  - `config/stage2_mirco_arc_profile.json` is the curated source for block function and interface descriptions emitted to `artifacts/stage2_mirco_arc/block_inventory.csv`.
  - After any profile correction, run `python scripts/run_stage2_micro_arch_and_crosscheck.py`, then the dependent SRS/ARS/DRS gate scripts as needed.

- Current downstream ownership and taxonomy contract (2026-08-20):
  - For non-matrix requirements, `block_inventory.csv` Function is the sole ownership authority; unsupported candidates remain `Unassigned`.
  - Connection-matrix requirements retain interaction-matrix source-row ownership and their downstream `Covers:` link targets the matching SRS-authored matrix requirement.
  - Protocol/bus terms (`I2C`, `SPI`, `AHB`, `AXI`, `APB`, `UART`, `JTAG`, `serial`, `protocol`, `bus`) and processor terms (`processor`, `CPU`, `microprocessor`, `core`, `digital`) are authoritative digital indicators.
  - Latest restored orchestrator pass records: Stage 3 PASS at 2026-08-20 17:53:14; Stage 4 PASS at 17:58:56; Stage 5 PASS at 17:59:01.

