# IPOS Descriptive Rendering

IPOS descriptive rendering is deterministic, local-only, and non-authoritative. It uses the complete set of accepted same-block evidence already recorded in the descriptive audit.

For each supported internal function or capability family, the shared renderer:

- preserves every distinct supported responsibility and explicit local interaction;
- deduplicates only equivalent responsibility phrases;
- orders contributors by accepted evidence order;
- omits unsupported relationships and unsafe raw implementation detail; and
- records contributor IDs, deterministic aggregation order, selection mode, and suppression reasons in `descriptive_summary_audit.csv`.

RRF is not used for IPOS descriptive rendering, facet selection, or audit fields. RRF remains restricted to Hybrid RAG retrieval/query fusion and retrieval benchmark paths.

## Shared rollout (2026-09-29)

The same `1.2` role-first materialization and quality checks now apply through
the shared composer and validators to every materialized Digital and Analog IPOS
block. Generation, the IPOS gates, and downstream coherence use the same complete
approved snapshot candidate set; no additional authority inputs or block-specific
rendering rules are introduced. A block with truncated action text, procedural
filler, or a weak standalone title must be reported as failing the descriptive
quality contract even when its traceability and document structure pass.

## Main Controller 1.2 pilot baseline (2026-09-29)

This historical pilot baseline applied to Digital IPOS Main Controller at approved snapshot
`snap-b2e8101b00dc6909feaed885`. Shared final-materialization and validation
rules are in `.github/skills/workflow-stage-gate/SKILL.md`; this record fixes the
pilot identity and output; the later authorized all-block prose rollout supersedes
these artifact hashes. The shared rollout does not alter Stage 2a,
the snapshot candidate universe, or authored requirements.

- `1.2` has 12 function bullets: 52 accepted candidates merged, 4 standalone,
	and 2 intentionally suppressed atomic candidates in the descriptive audit.
- The ALC compensation handoff belongs to PPG FSM, not a standalone function.
	Soft reset (`DDS_STBIO1_1114`) and chopper clock
	(`IPOS_STBIO1_MAIN_CONTROLLER_077`) remain suppressed atomic candidates.
- Standalone function bullets require independent behavior; the shared validator
	rejects raw-identifier headings and incomplete action fragments. Display names
	are readable, openings describe roles, interactions are source-backed, and
	Markdown/DOCX preserve the same audited semantic-unit order.
- SHA-256 of `artifacts/stage6_digital_ipos/blocks/main-controller/digital_ipos_main-controller.md`:
	`6B4B5D3D89F91AA9227AA8A203B183BCF44C7FD1A1DE1D250FFA525B7B79754B`
- SHA-256 of `artifacts/stage6_digital_ipos/blocks/main-controller/descriptive_summary_audit.csv`:
	`CDAD4C078F97A153766AD6AC88AEA7B7417DCE717A98DF55CAB00298B4DFAB05`

The old hashes are retained only for comparison; the current shared renderer
does not reproduce the pre-rollout pilot Markdown from this snapshot. For a
full rollout, gate all blocks without `--block` and run the central downstream
validator against the same snapshot. Regeneration may remain scoped to the
outliers, but scoped gate results cannot substitute for a full gate.

### Full rollout validation

At snapshot `snap-b2e8101b00dc6909feaed885`, all eight Digital block documents
were regenerated with the shared composer. The Analog partition regenerated as
valid-empty (0 requirements, 0 blocks) and its gate passed. Focused descriptive
tests passed (57). The full Digital gate is **blocked** by descriptive quality;
downstream coherence reports `BLOCK_DOWNSTREAM` with six quality findings across
five blocks:

| Digital block | Descriptive quality findings |
| --- | --- |
| ADSP | `Local copy function`; `Operation control and data routing` |
| I2C_SPI_AHB | `Operation control and data routing` |
| PMU | `Local manage function` |
| Sensor-Hub | `Local reset function` |
| Smart FIFO | `State and processing synchronization` |

Main Controller, PAD MUX, and Regmap had no descriptive findings at this point;
the latter two have no accepted 1.2 refinement bullets. No new authority inputs
or block-specific rendering rules are permitted for this repair.

### Five-block quality repair

Only ADSP, I2C_SPI_AHB, PMU, Sensor-Hub, and Smart FIFO were regenerated from
the same approved snapshot. The shared final renderer now names a behavior and
retains its supported guard or destination from accepted local statements. The
six earlier weak summaries became:

| Block | Before | After |
| --- | --- | --- |
| ADSP | `Operation control and data routing` | `Operation start conditions`: quokka_run low, selected OTP bit set, and BOOT initiation |
| ADSP | `Local copy function` | `OTP memory transfer`: OTP memory to registers and regmap to memory |
| I2C_SPI_AHB | `Operation control and data routing` | `Read data preloading`: AHB preload after double-byte address write, ahead of master read |
| PMU | `Local manage function` | `Power-on start-up`: POR release, LDO1V8 turn-on, and clock start-up sequence |
| Sensor-Hub | `Local reset function` | `Register reset on operation start`: registers reset at each new I2C operation |
| Smart FIFO | `State and processing synchronization` | `Memory mode entry`: HMASTER value condition retained |

Sections 1.1 and 1.2 in these five documents now use the inventory function and
I/O as natural introductory prose instead of the earlier `approved macro-purpose`
and `approved ... function` scaffolding. The 58 focused tests and all five scoped
Digital IPOS gates pass. The read-only full downstream check no longer reports
any of the original six quality findings, but remains `BLOCK_DOWNSTREAM` with
six `scope_mismatch_with_block_authority` findings on the unchanged Main
Controller, Pad Mux, and Regmap 1.1/1.2 openings. Those documents were not
regenerated during the five-block repair; Main Controller retained the pilot
hashes at that point. This was a scoped result, not a global PASS.

### All-block natural-prose rollout decision

The approved follow-up decision was to retire the Main Controller pilot freeze
and regenerate only the three remaining outliers (Main Controller, Pad Mux, and
Regmap) against `snap-b2e8101b00dc6909feaed885`. General Rules, the central
workflow execution contract, the orchestrator, and the shared output validator
now require natural technical prose in `1.1` and `1.2` in every current and
future materialized IPOS block. The shared validator independently rejects
approval/process wording even when a document agrees with composer output;
the IPOS gate also checks final DOCX fidelity. No new authority inputs,
block-specific wording rules, or changed candidate decisions were introduced.

The three regenerated documents replace `approved macro-purpose` and `local
scope covers the approved ... function` with inventory-bounded technical
sentences. Pad Mux now preserves the compound `register-map controls` in its
1.2 opening. The current Main Controller SHA-256 values after the Windows
display-name author refresh are:

- Markdown: `64A4256BCD353F44BAA693102B19663BA86414BC29017349ECCACCDEDC8C3F89`
- Descriptive audit: `46231A50CF86466142438A29165448E78FADD2C75FDC8EE24BCC9D7B358101C5`

The pre-author-refresh Markdown hash was
`37E0C4030514B3A982638A4AB758107193078DBB93B5178C5B7FF6CE2ABD2FE3`.

At this snapshot the 60 focused descriptive tests PASS; the full Digital IPOS
gate PASSes (259 requirements, 8 blocks); the Analog IPOS gate PASSes as
valid-empty (0 requirements, 0 blocks); and full read-only downstream coherence
PASSes with zero findings. This is the global rollout result, not a scoped
waiver of the earlier six mismatch findings.