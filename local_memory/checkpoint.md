# STBIO_AI Restore Checkpoint

## Latest checkpoint: 2026-10-05 - System Traceability

Approved snapshot: `snap-b2e8101b00dc6909feaed885` (unchanged). The current
System Traceability state is documented in the newest
`local_memory/chat_handoff.md` entry and `README.md` section. The new Primary
and integrated source XLSX exports are derived Stage 1 catalog views; the
inclusive all-levels XLSX remains approved-snapshot-linked and includes
generated requirements. Integrated `source_type` is column D. Supplementary
boxes/table rows show approved target-side coverage toward the Primary where
present; table rows, blocks, and arrows now share selection/highlighting.
The README contains a single nine-runner workflow step-by-step matching
`workflow_cli.py STAGE_ORDER`; review/merge/snapshot controls are separate,
and the redundant legacy stage table/list was removed.
It also names the pre-Stage-3 SysML architecture generation/structural review
and the separate post-Stage-7 `final-sysml` generation plus central coherence
check. Neither is an extra CLI run-stage key, and the final phase is not
included automatically in a `run --to-stage 7` range.

Project-agnostic within the touched feature: source provenance is compared to
the Primary name from the Stage 1 OCR index, and dynamic payload node IDs
control coverage and selection. Existing
unrelated STBIO-specific SysML/architecture references remain in the GUI and
validator; no full cross-project qualification is claimed. Current STBIO data:
271 Primary catalog rows; integrated 191 Primary + 123 Supplementary; one
approved Supplementary coverage of 123 / 123 (100.0%).

Verification: 16 focused tests PASS, Python compile and diagnostics clean.
An expanded 58-test run had two unrelated report-filter/snapshot-fixture
failures detailed in `local_memory/chat_handoff.md`; no full Stage 0-7 rerun
or manual GUI click-through is claimed. No Git commit was made; this is a
local-memory checkpoint. To restore: read the newest chat handoff, then run
`python.exe -m unittest tests.test_srs_downstream_coherence` from this folder.

## Latest checkpoint: 2026-10-01 - SRS System Overview Audit-Backed Rollout

Approved snapshot remains `snap-b2e8101b00dc6909feaed885`. The SRS-only
System Overview pilot was regenerated from the same approved in-scope SRS
authority, Stage 1 descriptive evidence, approved Stage 2 decomposition and
interface catalog. DRS, ARS and IPOS were not regenerated or used as authority.

SRS `3.1-3.7` now contains system identity, projected external sensing and
ECG/BIA capabilities, aggregated architectural-domain prose, interface-boundary
narrative plus catalog, approved operating modes, approved power behavior, and
engineering scope/allocation boundaries. Raw normative, block-local,
register/address/port/signal and malformed OCR/table fragments remain excluded.
Audit candidates previously rejected only for `topic output limit` were
reconsidered without changing authority.

SRS generation, LaTeX conversion, SRS crosscheck, LaTeX crosscheck, independent
System Overview validation and Stage 3 SRS gate pass. The last full Stage 0-7
validation before the final SRS-only renderer edits passed; after these final
edits only Stage 3 was rerun. Requirements generated/mapped remain 0/0; no
normative authority, `Covers`, allocation, mapping or snapshot values changed.

Current readable artifact SHA-256:
- SRS Markdown: `A9019D4914F84D379E5B82FDD1FC7BC2CABE321D1807BB9600E41B84CBA79A90`
- SRS traceability CSV: `825EB29B1366A9CCC2A5B2B077045767A5F9F62C3065AF2919E3FB38D1A98DBE`
- SRS descriptive audit: `E6172A89546C47F6CE8761B2978E77D269D02A9EFC8D2AA266E73E70FFE20557`
- DOCX regenerated at `2026-10-01 17:44:08`; its current hash was not read because Word held the file open during checkpointing.

Files changed include `scripts/run_srs_gen_spec_agent.py`,
`scripts/workflow_routing.py`, `scripts/validate_stage3_srs_gate.py`,
`scripts/validate_downstream_coherence.py`, `scripts/spec_document_contract.py`,
`templates/SRS_gen_AI_template_prompt.md`, and regenerated Stage 3 artifacts.
Do not broaden this rollout to ARS, DRS or IPOS without separate authorization.

## Latest checkpoint: 2026-10-01 - DRS Descriptive Evidence And Readability PASS

Approved snapshot remains `snap-b2e8101b00dc6909feaed885`. Stage 1
descriptive overview and explicit block-local descriptions are incorporated in
the DRS from OCR artifacts with continuation/TOC filtering, provenance, and
source-subject ownership checks. Descriptive prose remains separate from
normative requirements, `Covers`, and snapshot lineage. The audit check retained
5 overview records and 6 block-source descriptions, with 0 overview rejects.

The DRS top-level overview now uses short paragraphs of at most two sentences.
The generator and DRS crosscheck PASS; `tests/test_descriptive_summary.py`
passes 74 tests. Current DRS counts are 55 requirements, 13 mapped, and 42
unassigned. The separate Stage 5 gate and central downstream coherence had
passed in the preceding full descriptive rollout, but were not rerun after this
formatting-only change. No snapshot, authored normative requirement, `Covers`,
SRS, ARS, or IPOS output was changed by this latest update.

Earlier in this descriptive rollout, the workflow GUI and canonical v4 PPTX
were updated for Stage 1 descriptive evidence, parallel specification
generation, and approved IPOS lineage. The deck has 19 slides; slide 14 shows
the distinct descriptive-evidence and normative-lineage paths. Recorded GUI
validation: 20 nodes, 24 edges, 10 selectable nodes, PASS.

Preservation-locked DRS section 4.1 still labels the ISPU role `need
clarification`, while section 3.1 includes Stage 1 ISPU prose. Do not edit the
table or its preservation baseline without explicit authorization.

Current SHA-256 fingerprints:
- DRS Markdown: `e1a39bd4bb0bccd7ccae4e0148ec0125afe7852f72cd57804278f1e0f2f0dfde`
- DRS DOCX: `89d4c15ab6161bae715d99cb79c1aa38bb009af2e98b3b883be66555b01c8681`
- Descriptive audit: `585d9cbdc206aaafa752fa70c9b3671b4f644b3aa3a99635e1caa8a26dfd2452`
- Traceability matrix: `d8132195d71c7cbe8fac899dda5263181d7954589b8b844478cc7dd51d54b93c`
- Workflow PPTX: `b3a952c6cbd6fb49d4c3561b40614e202b71b9c1c02da5e0d76e532e994ef635`

## Latest checkpoint: 2026-10-01 - DRS Conventions In Section 2.1

The four literal convention definitions from the DRS YAML now render exactly
once as `2.1 Conventions` under `2. Definitions and terminology`, before section
3. Table 6 remains separate in document control. The shared final Markdown/DOCX
contract and navigation checks reject the former after-Table-2 placement. Seven
focused contract tests PASS; DRS generation, crosscheck, Stage 5 and central
coherence PASS. Native Word opened the regenerated DOCX without repair (42
tables, unchanged hash). Approved snapshot remains
`snap-b2e8101b00dc6909feaed885`; only DRS was regenerated.

## Latest checkpoint: 2026-10-01 - DRS Word Readability PASS

Native Word 16.0 opened the final DRS DOCX without repair. Shared DOCX core
metadata serialization now retains `dcterms` for date `xsi:type` attributes;
new focused regression verifies the prefix. DRS DOCX only was re-exported;
hash and preservation details are in the latest descriptive baseline entry.
DRS crosscheck, Stage 5 and central coherence PASS. No snapshot, Markdown,
CSV or canonical SQLite changes during this fix. Earlier unreadability caveats
and DOCX hashes below describe the older output.

## Latest checkpoint: 2026-10-01 - Executable DRS Template Contract PASS

Use the newest chat handoff and descriptive-baseline entries. The DRS template now
contains the authoritative document-only YAML contract (version 1); generation and
all DRS/central gates execute it. General Rules and approved snapshot authority remain
unchanged. Conventions, section placement, TOC/indexes, table preservation and descriptive
ordering are enforced on final Markdown and DOCX. 87 tests PASS; DRS generation,
crosscheck, Stage 5 and central coherence PASS. Only DRS regenerated on the same snapshot.
291 protected files and all 55 requirement bodies/Covers are unchanged. Database changes
are confined to allocation created_at timestamps. Preserve the explicit pre-pilot baseline;
do not rebase from generated output. Word readability is still independently unverified.

## Latest checkpoint: 2026-10-01 - DRS Behavior-First Cleanup PASS

Use the newest `local_memory/chat_handoff.md` and
`docs/drs-descriptive-baseline.md` entries. Snapshot remains
`snap-b2e8101b00dc6909feaed885`; only DRS was regenerated. Shared composers
and independent final Markdown/DOCX checks now reject evidence/path counts
and approval/audit prose in the targeted section types. No new name-specific
rules or authority/mapping/evidence changes. DRS generation/crosscheck,
Stage 5 and central coherence PASS; 73 descriptive tests PASS. Tables,
section 9 onward, and provenance CSVs are unchanged. The existing derived
allocation refresh updates DB `created_at` timestamps, not allocation values.
Current hashes and residual limits are in the baseline report; all earlier
output hashes below are historical.

## Latest checkpoint: 2026-09-30 - DRS Section-Level Synthesis PASS

The current DRS-only pilot supersedes the older clock-gating-output hashes
below; authority remains approved snapshot `snap-b2e8101b00dc6909feaed885`.
Sections 3, 3.1, 4.2-4.7 and PMU/domain-control prose now group approved
evidence by theme without copying block-purpose text into section narratives
or treating signal endpoints as blocks. Twelve selected concrete digital
blocks have named 3.1 paragraphs; eight approved PMU-source clock routes,
nine reset outputs, and all 11 clock routes remain source-linked in tables.
Broader destination-block coverage and missing implementation details are
explicitly unclear. `docs/drs-descriptive-baseline.md` is the current
before/after and residual-gap record. Markdown SHA-256:
`5889DCC4125F2E9568004A095C1A2D1A7517E4B1FDDBAD212517ED13CD500E98`;
DOCX SHA-256: `DEAD4854966F178422862F42B3B787BEF65086910684C32055BBBCC42DB8A69C`.
DRS crosscheck, Stage 5 gate, and central coherence PASS (zero findings);
71 focused tests PASS. Only DRS was regenerated; no approval or other
specification outputs changed. Restore from this entry and the latest
descriptive baseline, not historical hashes below.

## Latest checkpoint: 2026-09-30 - DRS Shared Architecture, Reset, And Clock-Gating PASS

This is a local checkpoint, not a commit or a new approval snapshot. The
approved authority remains `snap-b2e8101b00dc6909feaed885`. Only DRS was
regenerated; SRS/ARS/IPOS, Stage 1/2 inputs, canonical authority, allocation,
and snapshot approval were not changed.

Completed DRS changes:
- Sections 3.1/4.2 merge arbitration/control and shared-resource treatment.
  They describe approved FIFO ownership, register/memory and bus exchanges,
  reset/boot and power/clock roles, with unsupported facets explicitly marked
  `need clarification`. No policy or behavior is inferred from generic SoC
  expectations. Endpoints that are not inventory blocks remain endpoint labels.
- Section 4.6 reports eight approved PMU clock routes with frequency/gating,
  nine approved PMU reset outputs with source pages, and the reset route
  `DDS_STBIO1_2054`: `PMU.resetn_32k_main_ctrl -> Main Controller.i_rstn_sync_32`.
- Clock gating expressions from the approved snapshot are retained verbatim
  in both 4.6 and 4.7. Markdown `|` operators are escaped; DOCX retains each
  route as a five-cell row. OCR-split signal tokens are not normalized and
  carry `signal spelling: need clarification`. `DDS_STBIO1_2024` source/target
  route endpoints remain `need clarification`, separate from its available
  gate expression.
- The existing central DRS descriptive validator checks route rows and
  gating expressions against the selected approved snapshot in Markdown and
  DOCX. A mutation test confirms an altered gate term is rejected. Existing
  General Rules already require including available clock-gating column data.

Generated DRS remains 55 requirements. Current SHA-256:
- Markdown: `8137106AB19277AAADAE24C82BCB1595C87F20CDC805A71DBD166B6C6F23C861`
- DOCX: `A09D9CE68C6405F9601EC0E0E9BF689F751E0A7C6141F150A779CD9B7F3263A3`
- Other DRS artifacts and historical hashes are recorded in
  `docs/drs-descriptive-baseline.md`.

Validation: DRS generation/crosscheck PASS; focused descriptive tests 70
PASS; Stage 5 DRS gate PASS; central downstream coherence PASS (0 findings).
No full workflow run is claimed.

Remaining evidence gaps: OCR-broken control signal spelling; `DDS_STBIO1_2024`
clock endpoints; gating-control interpretation where source text is ambiguous;
reset release/synchronization mechanics; measured latency, bandwidth, or
interrupt response; concurrent-access ordering and requester priority; flow
control/backpressure where no approved specific behavior exists.

Replay from workspace root:
```powershell
python -B -m unittest discover -s STBIO_AI/tests -p test_descriptive_summary.py
python -B STBIO_AI/scripts/run_drs_gen_spec_agent.py --snapshot-id snap-b2e8101b00dc6909feaed885 --regenerate-downstream
python -B STBIO_AI/scripts/validate_stage5_drs_gate.py --snapshot-id snap-b2e8101b00dc6909feaed885
python -B STBIO_AI/scripts/validate_downstream_coherence.py --snapshot-id snap-b2e8101b00dc6909feaed885
```

Restore prompt: Read the newest handoff, this checkpoint, the project activity
log, and `docs/drs-descriptive-baseline.md`. Preserve the pinned snapshot,
source provenance, OCR uncertainty, and DRS-only scope; do not edit generated
DRS by hand or modify upstream authority without explicit approval.

## Latest checkpoint: 2026-09-29 - DRS Introductory Sections Populated

The current DRS output at `snap-b2e8101b00dc6909feaed885` extends the
validated descriptive pilot to introductory architecture context. Existing
approved top-digital interaction evidence now yields source-linked prose and
structural tables in sections 3, 4, and 7, with section 1 scoped to the
selected digital blocks and paths. Section 9 concrete-block I/O tables and
SRS/ARS outputs are unchanged. See the **Current DRS Introductory Rollout**
entry in `docs/drs-descriptive-baseline.md` for before/after, current hashes,
and commands; its earlier frozen hashes are historical. DRS crosscheck, Stage
5 gate, and central downstream validator PASS (0 findings); focused suite 63
PASS. Do not promote interaction endpoints to blocks or expand to SRS/ARS
without separate approval.

## Latest checkpoint: 2026-09-29 - IPOS And DRS Descriptive Baseline

The shared document-neutral natural-prose contract is validated for the existing
IPOS rollout and the DRS-only pilot at approved snapshot
`snap-b2e8101b00dc6909feaed885`. This local checkpoint does not create a new
approval snapshot or authorize SRS/ARS regeneration. Their output and literal
inventory-function checks remain unchanged pending separate pilot decisions.

The frozen DRS Markdown/DOCX, audit, traceability, and report fingerprints,
PASS reports, 62 focused tests, Stage 5 DRS gate PASS, downstream coherence
PASS (0 findings), and workspace-root replay commands are in
`docs/drs-descriptive-baseline.md`. The DOCX hash was obtained via Python read
while PowerShell's `Get-FileHash` could not access the open document.
Preserve approved authority, exact DRS audit provenance, owner-scoped I/O
tables, and existing IPOS baseline; do not rerun generation just to verify.

Restore prompt:
> Read this newest checkpoint, `local_memory/chat_handoff.md`,
> `docs/drs-descriptive-baseline.md`, and `docs/ipos-descriptive-rendering.md`.
> Use the pinned snapshot and read-only gates; keep SRS/ARS descriptive output
> unchanged until a separate pilot decision.

## Latest checkpoint: 2026-09-29 - Global IPOS Prose Contract, All Gates PASS

This is a local file checkpoint, not a git commit or a new approval snapshot. It supersedes the blocked-rollout and frozen-pilot instructions below. The user authorized applying one project-agnostic natural technical prose rule to every materialized Digital/Analog IPOS `1.1 Functionality` and `1.2 Supported functions and scope`, including regeneration of the remaining Main Controller, Pad Mux, and Regmap documents. Approved snapshot: `snap-b2e8101b00dc6909feaed885`.

Current state:
- `scripts/workflow_routing.py` is the shared deterministic inventory-bound composer and descriptive output validator. Final 1.1/1.2 Markdown rejects `approved` and analogous governance/process wording independently of composer parity; existing IPOS/central gates check final DOCX through the shared materialization chain. `register-map controls` is kept intact as a compound input label. No new authority inputs, block-specific logic, candidate decision changes, Stage 2a changes, or edits to authored requirements.
- General Rules (`.github/copilot-instructions.md`), `.github/agents/workflow-orchestrator.agent.md`, and `.github/skills/workflow-stage-gate/SKILL.md` state the same rule for future projects. `tests/test_descriptive_summary.py` includes negative governance-prose and register-map regressions.
- The five earlier weak-summary blocks (ADSP, I2C_SPI_AHB, PMU, Sensor-Hub, Smart FIFO) were repaired first. Main Controller, Pad Mux, and Regmap were subsequently regenerated from the same snapshot. Historical pilot and intermediate FAIL findings are retained in `docs/ipos-descriptive-rendering.md` as history only. The old Main Controller hash freeze was explicitly retired for this rollout; new Markdown/audit SHA-256 hashes are recorded there.

Final verification from workspace root:
```text
python -B -m unittest discover -s STBIO_AI/tests -p test_descriptive_summary.py
python -B STBIO_AI/scripts/validate_ipos_gate.py --kind digital --snapshot-id snap-b2e8101b00dc6909feaed885
python -B STBIO_AI/scripts/validate_ipos_gate.py --kind analog --snapshot-id snap-b2e8101b00dc6909feaed885
python -B STBIO_AI/scripts/validate_downstream_coherence.py --snapshot-id snap-b2e8101b00dc6909feaed885
```
- Focused descriptive tests PASS (60); the nearby source-port coverage tests also PASS (2). Full Digital IPOS gate PASS (259 requirements, 8 blocks), Analog gate PASS as valid-empty (0 requirements, 0 blocks), full read-only downstream coherence PASS (0 findings). No full S0-Stage 7 rerun is claimed.

Restore prompt:
> Load `local_memory/chat_handoff.md`, this checkpoint, `local_memory/project_activity_log.md`, and `docs/ipos-descriptive-rendering.md`. Use the newest 2026-09-29 global PASS entry, not the historical blocked or pilot-only instructions below. Preserve the approved snapshot and project-agnostic shared natural-prose contract, contributor provenance, and normative text; do not widen authority or infer new behavior from source specs.

## Latest checkpoint: 2026-09-29 - All-IPOS Shared Descriptive Rollout

The newest user request authorizes extending the frozen Main Controller `1.2` rule to all IPOS generation without new authority inputs or block-specific logic. The Main Controller hash-pinned pilot baseline below remains historical; its pilot-only rollout instruction is superseded.

Current result at approved snapshot `snap-b2e8101b00dc6909feaed885`: all eight Digital IPOS block documents regenerated; Analog valid-empty regenerated and gate PASS (0/0). `tests/test_descriptive_summary.py` PASS (57). Full Digital gate FAIL on descriptive quality; full downstream coherence `BLOCK_DOWNSTREAM` with six findings across ADSP, I2C_SPI_AHB, PMU, Sensor-Hub, and Smart FIFO. Main Controller, PAD MUX, and Regmap have no descriptive findings. Exact block findings are in `docs/ipos-descriptive-rendering.md`. Do not claim a full rollout PASS or suppress the findings.

Root cause fixed during rollout: the central downstream validator previously passed derived IPOS trace rows as its candidate universe; generation and the IPOS gates passed all approved snapshot-scoped candidates. The candidate projection now lives once in `scripts/workflow_routing.py` and is reused by both paths. The remaining failures concern incomplete or generic rendered summaries, not input parity or snapshot authority.

Next-session prompt:
> Read the newest handoff and `docs/ipos-descriptive-rendering.md`. Repair the five named Digital 1.2 quality failures with accepted evidence and shared rules only, preserve Main Controller baseline and Stage 2a boundaries, then rerun full Digital/Analog IPOS gates and downstream coherence.

## Latest checkpoint: 2026-09-29 - Main Controller 1.2 Pilot Frozen

Approved scope: Digital IPOS Main Controller only, snapshot `snap-b2e8101b00dc6909feaed885`. Stage 2a and approved inputs are unchanged. `docs/ipos-descriptive-rendering.md` fixes the pilot identity, hashes of the generated Markdown/audit, 12-bullet result, and reproduction commands. The shared, project-agnostic rendering and validation rule lives in `.github/skills/workflow-stage-gate/SKILL.md`; it must not be read as approval to regenerate other blocks. The restriction is operational/governance-only; there is no runtime feature gate for other blocks.

State to preserve:
- `scripts/workflow_routing.py` composes role-first, normalized Main Controller 1.2 summaries with source-backed conditions and useful external interactions; validator rejects low-quality standalone entries and checks provenance and Markdown/DOCX semantic units.
- Current accepted local candidate audit: 52 `merged`, 4 `standalone`, 2 `suppressed_atomic`; orphaned ALC handoff `IPOS_STBIO1_MAIN_CONTROLLER_099` merges into PPG FSM. `DDS_STBIO1_1114` (soft reset) and `IPOS_STBIO1_MAIN_CONTROLLER_077` (chopper clock) remain atomic suppressions. No unsupported PPG interaction was restored to local configuration.
- The supplementary OCR block description of Elab_FSM was identified, but not added to the approved snapshot or Stage 2+ inputs. Do not import it in a presentation-only pass. Older checkpoints below are historical; this checkpoint governs the current 1.2 pilot.
- Do not expand rollout, change Stage 2a, reopen broad parsing, use new source-spec reads downstream, or modify approved snapshot authority for cosmetic wording.

Verification from workspace root: `python -B -m unittest discover -s STBIO_AI/tests -p test_descriptive_summary.py` PASS (57); `python -B STBIO_AI/scripts/validate_ipos_gate.py --kind digital --snapshot-id snap-b2e8101b00dc6909feaed885 --block main-controller` PASS (259 requirements, 8 blocks, descriptive block=Main Controller). Regeneration used `--regenerate-downstream --block main-controller` before the baseline freeze; governance-only edits afterward did not regenerate artifacts.

Next-session prompt:
> Load `STBIO_AI/local_memory/chat_handoff.md`, `STBIO_AI/local_memory/checkpoint.md`, and `STBIO_AI/local_memory/project_activity_log.md`. Start with the frozen Main Controller baseline in `docs/ipos-descriptive-rendering.md`. Preserve accepted-evidence accounting, 52/4/2 audit, role-first 1.2 output, and the shared project-agnostic rule; gate only Main Controller unless a new rollout is authorized. Note that other-block rollout is governed by instructions, not enforced by a runtime selector.

## Latest checkpoint: 2026-09-28 - Shared Deterministic IPOS Aggregation

Current verified state:
- Every materialized IPOS block uses the shared `deterministic_aggregation` renderer. Each emitted function summary combines only accepted same-block evidence into its responsibility and explicit supported local interactions.
- Do not over-compress generated descriptions: `scripts/workflow_routing.py` preserves every distinct accepted action phrase, while still normalizing source noise and duplicate wording. RRF, ranked facet selection, and fixed facet-count truncation are prohibited in IPOS rendering.
- RRF remains restricted to Hybrid RAG retrieval/query fusion and retrieval benchmark paths. Do not add inferred functional clauses merely to make prose more specific.
- Authority boundaries are unchanged: no evidence extraction, acceptance/suppression, ownership, allocation, traceability, or snapshot semantics changed. Unsupported cross-function relationships remain omitted.

Validation:
```powershell
C:/Users/syslocadm1906/AppData/Local/Programs/Python/Python311/python.exe -m unittest tests.test_descriptive_summary
C:/Users/syslocadm1906/AppData/Local/Programs/Python/Python311/python.exe scripts/generate_ipos_specs.py --kind digital --snapshot-id snap-b2e8101b00dc6909feaed885 --regenerate-downstream --block main-controller
C:/Users/syslocadm1906/AppData/Local/Programs/Python/Python311/python.exe scripts/validate_ipos_gate.py --kind digital --snapshot-id snap-b2e8101b00dc6909feaed885 --block main-controller
C:/Users/syslocadm1906/AppData/Local/Programs/Python/Python311/python.exe scripts/validate_downstream_coherence.py --snapshot-id snap-b2e8101b00dc6909feaed885 --ipos-kind digital --ipos-block main-controller
```
Result: 47 focused tests PASS; full Digital IPOS gate PASS (259 requirements, 8 blocks); downstream coherence PASS with 0 findings.

Next-session prompt:
> Load `local_memory/chat_handoff.md`, `local_memory/project_activity_log.md`, and this checkpoint. Preserve shared deterministic full-evidence aggregation for every IPOS block. Preserve every distinct accepted action in readable deterministic summaries, but do not invent evidence or change the authority pipeline.

## Latest checkpoint: 2026-09-23 - Central IPOS Quality And Shared DOCX Layout

Current verified state:
- Current approved snapshot: `snap-b2e8101b00dc6909feaed885`.
- Only mapped concrete blocks materialize IPOS documents. Digital: 259 requirements across 8 blocks. Analog: valid-empty, 0 requirements and 0 block documents. OTP and ISPU have no IPOS artifacts because no IPOS requirements are mapped to them.
- Central shared IPOS synthesis in `scripts/workflow_routing.py` uses approved inventory function evidence for high-level purpose/scope and omits unsupported sections. It rejects raw/near-raw requirements, IDs/tags, low-level implementation fragments, isolated keyword classification, and unsupported DRS themes.
- Topic safety protects ADSP, Regmap, Main Controller, and Smart FIFO from prior weak keyword inference. Sensor-Hub now has a source-supported local purpose/scope summary.
- Shared DOCX formatting and the existing IPOS gate enforce: document title and metadata on page 1, TOC first on page 2, Document Navigation after the TOC, and a bottom-right PAGE footer.
- No snapshot, allocation, ownership, partition, requirement, ID, traceability, or central-contract semantics changed.

Validation:
```powershell
C:\Users\syslocadm1906\AppData\Local\Programs\Python\Python311\python.exe -m py_compile scripts\workflow_routing.py scripts\generate_ipos_specs.py scripts\validate_ipos_gate.py
C:\Users\syslocadm1906\AppData\Local\Programs\Python\Python311\python.exe scripts\validate_ipos_gate.py --kind digital --snapshot-id snap-b2e8101b00dc6909feaed885
C:\Users\syslocadm1906\AppData\Local\Programs\Python\Python311\python.exe scripts\validate_downstream_coherence.py --snapshot-id snap-b2e8101b00dc6909feaed885
```
Result: Digital IPOS gate PASS (259 requirements, 8 blocks); Analog IPOS gate PASS (0 requirements, 0 blocks); downstream coherence PASS with 0 findings.

Next-session prompt:
> Load `local_memory/chat_handoff.md`, `local_memory/project_activity_log.md`, and this checkpoint. Preserve central orchestrator-governed IPOS evidence admissibility, topic assignment, scope, omission, gate expectations, zero-mapped-block omission, and shared DOCX layout. Do not promote requirement detail into descriptive overview text.

## Latest checkpoint: 2026-09-17

Current focus and verified state:
- Stage 2 Architecture Map Review is explicitly user-controlled. Workbook-authoritative fields are `approved_classification`, `approved_block`, `review_decision`, `allocation_class`, `owning_target`, `allocation_rationale`, `lineage_mode`, and `reviewer_notes`.
- `review_decision` is editable and literal, with dropdown values `pending_review`, `approved`, `reassigned`, `rejected`, and `needs_clarification`. It is never inferred from `approved_block`, classification, or any other edit.
- `pending_review` is the canonical unresolved state. Existing reviewed CSV values are preserved across Stage 2 regeneration by `requirement_id`; deterministic prefill applies only to clearly supported empty allocation fields.
- Workbook review fields are red when incomplete or invalid and green only when explicitly reviewed (`approved` or `reassigned`) and currently valid, including a consistent allocation class/owning target pair.
- Enable Gate from Workbook saves/closes Excel, synchronizes XLSX to CSV, validates only the synchronized CSV, and records the CSV hash only after validation passes.
- No Stage 2A or downstream stage was executed for this checkpoint.

Validation:
```powershell
python -m unittest discover -s STBIO_AI\tests -p test_mapping_review_sync.py
python -m py_compile STBIO_AI\scripts\mapping_review_sync.py STBIO_AI\scripts\generate_stage2_specs.py STBIO_AI\scripts\workflow_gui.py
```
Result: 5 focused tests passed; compilation and diagnostics passed.

Open work:
- Regenerate Stage 2 to replace any older XLSX containing formula-driven review behavior.
- Review, explicitly decide, save, and close the workbook; enable the gate from the workbook before running Stage 2A.

Next-session prompt:
> Load `local_memory/chat_handoff.md`, `local_memory/project_activity_log.md`, and this checkpoint. Preserve explicit workbook review authority, literal decisions, `pending_review` as the sole unresolved state, XLSX-to-CSV synchronization before validation, and reviewed-and-valid green semantics. Do not auto-approve or run downstream before the gate succeeds.

## Latest checkpoint: 2026-09-14

Current focus and verified state:
- Stage 1 concrete ownership inference is parent-section based. Block terms appearing only in paragraph titles no longer become concrete owners.
- DFT/test paragraphs such as `DDS_STBIO1_0701` and `DDS_STBIO1_0702` retain their original source text and route to `Unassigned` by default. A reviewer may explicitly promote them to a real approved hierarchy owner.
- Stage 2 preview distinguishes candidate evidence from approved ownership: candidate `ADC TEST LOW NOISE` may be visible for review, while approved block remains blank/pending until user action. Authoritative Stage 2 routing does not fabricate an ADC block.
- User-controlled Stage 2 approval hashes and snapshots were not refreshed automatically. The refreshed inputs require Architecture Map Review before Stage 2A can run.
- Work Area text/CSV search remains available with `Ctrl+F`. Main SysML source text and hierarchy-window SysML details/source text now support the same find workflow: case-insensitive matches, all/current highlighting, Enter and Shift+Enter navigation, Prev/Next, counters, Escape/Close, and hierarchy-window cleanup.

Validation:
```powershell
python.exe -m unittest discover -s STBIO_AI\\tests -p test_final_polish.py
python.exe -m py_compile STBIO_AI\\scripts\\workflow_gui.py
```
Result: 22 focused tests passed; GUI compilation passed; VS Code diagnostics were clean.

Open work:
- Review and explicitly approve the refreshed Stage 2 mapping.
- Rerun Stage 2A, freeze the approved snapshot, and regenerate Stage 3/downstream artifacts.
- Treat stale ADC associations in older generated reports as pending regeneration, not as current authoritative ownership.

Next-session prompt:
> Load `STBIO_AI/local_memory/chat_handoff.md`, `STBIO_AI/local_memory/project_activity_log.md`, and this checkpoint. Preserve source-context paragraphs and `Unassigned` default routing for non-specific DFT/test rows, keep approval metadata user-controlled, and verify SysML `Ctrl+F` search behavior before further GUI changes.

## Latest checkpoint: 2026-09-11

Current focus and verified state:
- SRS power-state renderer fills `Entry, exit, wake-up, and restore` from approved power-domain evidence and records unspecified restore timing explicitly.
- SRS keeps detailed power-domain records only under `3.3 Power states -> Power-domain architecture`; the general system overview contains a pointer rather than repeated domain descriptions, and Operating Modes excludes those records.
- Reusable policy was saved in `.github/copilot-instructions.md`, `.github/skills/workflow-stage-gate/SKILL.md`, and `.github/agents/{srs,ars,drs}_gen_spec.agent.md`.
- Policy: SRS interface summaries only; DRS complete digital block I/O tables under matching block paragraphs; single-block Digital/Analog IPOS owns detailed implementation I/O; do not duplicate complete block tables across outputs.
- Policy: SRS/ARS/DRS TOCs must follow numerical section depth in Markdown and retain the same nested list levels in DOCX.

Validation:
```powershell
python -m py_compile STBIO_AI/scripts/run_srs_gen_spec_agent.py STBIO_AI/scripts/run_ars_gen_spec_agent.py STBIO_AI/scripts/run_drs_gen_spec_agent.py STBIO_AI/scripts/workflow_gui.py
python -m unittest STBIO_AI.tests.test_descriptive_summary -q
```
Latest result: compilation passed and 13 focused tests passed.

Open work:
- Remove the existing SRS section 3.4 source-I/O-table rendering loop and regenerate SRS, leaving only the system interface summary.
- Validate nested TOC levels in generated DOCX files after DOCX regeneration succeeds.
- The empty approved snapshot remains a traceability blocker; approval metadata must remain user-controlled.

Restore prompt:
"Load `local_memory/chat_handoff.md`, `local_memory/project_activity_log.md`, and this checkpoint. Continue with SRS I/O-table ownership cleanup and DOCX TOC validation; preserve approved snapshot authority and the saved SRS/DRS/ARS/IPOS rules."

## Latest checkpoint: 2026-09-10

Primary current state:
- Architecture Map Review workbook is `artifacts/stage1_specs/architecture_mapping_preview.xlsx`. It is user-editable and has data-validation dropdowns for `approved_classification` (`System`, `Digital`, `Analog`) and `approved_block` (top-level routes plus real names from `approved_block_list.xlsx`).
- `review_decision` is Excel formula-driven and tool-authoritative. A change to classification, block, or notes changes it to `reassigned`; the GUI importer recomputes that status and writes only `architecture_mapping_preview.csv`.
- The GUI importer must never save/rewrite the XLSX, because openpyxl rewriting strips Excel data validation dropdown metadata.
- A top-level selection must match `approved_classification`: `System` -> SRS only; `Digital` -> DRS only; `Analog` -> ARS only. These are routing choices, not concrete block owners, and remain `Unassigned` in SysML/block allocation.
- For block-level Digital/Analog IPOS, assign an exact real approved block. ADC is not an allowed approved block; it remains candidate/source evidence only.
- Stage 2A is verified PASS for 314 requirements, 0 uncovered. `validate_stage2_mapping.py` accepts exact reviewer-approved `reassigned` assignments as ownership evidence after checking real inventory/function/interactions.
- Live Chat is persisted to `logs/workflow_gui_chat.log`; GUI layout saves only on explicit user save or GUI close.

Restore commands:
```powershell
python -m py_compile scripts/generate_stage2_specs.py scripts/workflow_gui.py scripts/validate_stage2_mapping.py
python scripts/validate_stage2_mapping.py
python scripts/workflow_cli.py run --stage 2a
```

Next-session prompt:

> Load `STBIO_AI/local_memory/chat_handoff.md`, `STBIO_AI/local_memory/project_activity_log.md`, and this checkpoint. Preserve workbook dropdowns by never rewriting the XLSX during GUI import. Preserve `System`/`Digital`/`Analog` as top-level routing options, not fake blocks; keep ADC out of `approved_block`. Do not auto-refresh user approval hashes. Stage 2A currently passes; freeze a new Stage 2B snapshot only after the reviewed workbook is explicitly imported and approved.

## Latest checkpoint: 2026-09-08

Primary current state:
- Canonical workflow order is S0 -> S1 -> S2 -> S2A -> S2B -> S2C -> S2D -> S2E -> S2F -> S2G -> S2H -> Stage 3 -> Stage 4 -> Stage 5 -> Stage 6 -> Stage 7.
- `data/canonical/canonical_store.sqlite` is authoritative. Retrieval/index SQLite and all CSV, JSON, Markdown, XLSX, and SysML outputs are derived artifacts.
- Approved immutable snapshots and approved vocabulary, taxonomy, and architecture profiles are required for authoritative downstream generation, reports, SysML, and authoritative GUI actions.
- Stage 1 specs Gate 2 is repaired: `generate_stage2_specs.py` supplies approved canonical classifications to `_write_mapping_preview()`.
- The GUI selectors expose S0-S2H and Stage 3-7, with Optional Architecture Comparison last. Approval-only range selections provide GUI/service guidance rather than unsupported CLI execution.
- The compact workflow diagram supports vertical scrolling, Shift-wheel horizontal scrolling, and Ctrl-wheel zoom. Tooltips dismiss reliably.

Restore files:
- `local_memory/chat_handoff.md`
- `local_memory/project_activity_log.md`
- `local_memory/checkpoint.md`

Restore commands:
```powershell
python -m py_compile scripts\workflow_gui.py scripts\generate_stage2_specs.py
python -m unittest tests.test_final_polish tests.test_end_to_end_authority
python scripts\run_stage1_specs_gate2.py
python scripts\workflow_cli.py status
```

Next-session prompt:

> Load `STBIO_AI/local_memory/chat_handoff.md`, `STBIO_AI/local_memory/project_activity_log.md`, `.github/copilot-instructions.md`, and `.github/skills/workflow-stage-gate/SKILL.md`. Preserve canonical SQLite authority, derived retrieval/artifacts, approved snapshot/profile enforcement, the complete GUI stage vocabulary with Optional Architecture Comparison last, compact diagram scrolling, and dismissible tooltip behavior. Verify Stage 1 specs Gate 2 before changing workflow code.

## Latest checkpoint: 2026-09-04

The latest verified work covers GUI layout persistence, the SysML architecture workspace, and the rendered PyMuPDF/Pillow PDF Reader in `scripts/workflow_gui.py`.

Preserve:
- Save Window Layout persistence for window geometry and all registered paned-window sashes.
- SysML block selection, source-tree expansion, source-file viewing, and source zoom.
- Rendered PDF viewing with page navigation, scrollbars, zoom, and clean document shutdown.
- User-controlled values in `config/gui_state.json`.
- Stage 1-only direct source reads and Stage 2+ artifact-only execution.
- Reviewed deterministic architecture ownership; hybrid RAG remains advisory.

Restore files:
- `local_memory/chat_handoff.md`
- `local_memory/project_activity_log.md`
- `local_memory/environment.md`

Validation command:

```powershell
C:\Users\syslocadm1906\AppData\Local\Programs\Python\Python311\python.exe -m py_compile scripts\workflow_gui.py
```

Next-session prompt:

> Load `STBIO_AI/local_memory/chat_handoff.md`, `STBIO_AI/local_memory/project_activity_log.md`, and `STBIO_AI/local_memory/checkpoint.md`. Preserve the GUI layout persistence contract and rendered PyMuPDF/Pillow PDF Reader. Verify `scripts/workflow_gui.py` compilation before changing GUI behavior.
