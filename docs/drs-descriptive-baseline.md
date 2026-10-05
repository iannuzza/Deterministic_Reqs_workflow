# DRS Descriptive Baseline (2026-09-29)

## DRS Conventions In Section 2.1 (2026-10-01)

The embedded DRS contract now places the four literal YAML definitions in
`2.1 Conventions`, immediately under `2. Definitions and terminology` and before
section 3. The generator, final Markdown/DOCX validator, TOC and internal index
agree on that numbered placement. `Table 6. Category convention` remains a
separate document-control table and its rows are preserved. The old placement
after Table 2 is rejected by both contract loading and final-artifact checks.

Seven focused contract tests pass. DRS-only generation, crosscheck, Stage 5 and
central downstream coherence pass. Native Word 16.0 opened the regenerated DOCX
with `OpenAndRepair=False`; 42 tables were available and the post-open hash was
unchanged. Approved snapshot remains `snap-b2e8101b00dc6909feaed885`.

## Word Open-Without-Repair Fix (2026-10-01)

Microsoft Word 16.0 reproduced `The file appears to be corrupted` with
`OpenAndRepair=False` on the pilot DOCX. Raw Pandoc output and the table-grid
and authored-requirement post-processors opened normally. The shared common
formatter reserialized `docProps/core.xml`, changing the `dcterms` prefix to
`ns2` while leaving `xsi:type="dcterms:W3CDTF"` on creation/modified dates.
Registering the original namespace before serialization preserves this QName.
The new focused regression checks both date types' declared prefix.

Only the DRS DOCX was re-exported from unchanged Markdown. Word 16.0 opened
the **final** DOCX with `OpenAndRepair=False`, `ReadOnly=True`, macros disabled
and no conversion dialogs; 42 editable tables and 7213 paragraphs were visible
to Word. The file was closed without saving and its SHA-256 remained unchanged.
Evidence: `logs/drs_word_open_verification_20261001.json`; original DOCX and
metadata: `logs/drs_word_fix_before_20261001/`.

Final DOCX SHA-256: `67737877a7316512eb329b81177d59762a7ed99ee1e0182a4eebbd62f957933d`.
Contract metadata was refreshed for that output; Markdown, DRS CSVs and
canonical SQLite remained byte-identical during this fix. DRS crosscheck,
Stage 5 gate and central downstream coherence PASS (zero findings). The fix
does not constitute a visual pagination review or certification of all other
generated DOCX documents. Older DOCX hashes and unreadability notes below
describe the pre-fix state.

## Executable DRS Template Pilot (2026-10-01)

This entry supersedes the current-output hashes and section-order statements below.
Only DRS was regenerated on `snap-b2e8101b00dc6909feaed885`.

`templates/DRS_gen_AI_template_prompt.md` now contains the version-1 YAML document
contract and merged DRS structure/writing guidance. General Rules remain superior;
the approved snapshot remains technical authority. The actual orchestrator file is
`.github/agents/workflow-orchestrator.agent.md`; it coordinates DRS gates and references
the contract rather than duplicating its rendering instructions.

The generator loads the contract before generating artifacts, rejects missing/malformed
templates, unsupported versions, missing/unknown mandatory rules and unsupported section
renderers, and uses it for section arrangement and literal Conventions content.
The pilot uses canonical repository template/output paths. It requires an explicit
pre-pilot preservation baseline for the same snapshot; it never silently rebases it.
`--regenerate-downstream` permits DRS output repairs only, not other coherence failures.

Shared implementation: `scripts/spec_document_contract.py`. DRS generation, crosscheck,
Stage 5 gate and `validate_downstream_coherence.py` call the shared final-artifact contract.
Existing evidence/provenance and natural-prose checks remain mandatory. The seven rules
are structure, conventions, navigation, table_preservation, technical_prose,
evidence_fidelity and artifact_fidelity. Rule results and template/baseline/artifact hashes
are in `artifacts/stage5_drs/drs_document_contract.json`; the generation report records
the executed version, template hash and rule outcomes.

### Document Changes

- Exactly one Conventions paragraph after the Reference documents table, before the
    unchanged ID-family convention table. Comment, Definition, Assumption and Requirement
    definitions come only from YAML and retain their complete original wording.
- Existing TOC, internal index, document-control tables and table index are preserved;
    Conventions is added to navigation. Internal Markdown/DOCX targets and shared DOCX
    title/TOC/footer layout are checked.
- Source Function Context is subsection 6.4 inside section 6, not a top-level heading
    after section 9. Its requirements and source references are unchanged.
- Descriptive sections retain known technical behavior before tables, with targeted
    clarification last. Engineering values remain; audit/count summaries and raw snippet
    markers are rejected. Tables retain their contents and owner/section association.

### Verification

- 73 descriptive regression tests and 14 shared/template-contract tests PASS.
- Negative cases cover missing/malformed/unsupported contracts, unknown/missing mandatory
    rules, missing/moved/duplicated conventions, altered definitions/category order,
    DOCX-only definition divergence, table loss, section order, missing navigation/TOC,
    non-numerical index order, counting prose, raw paths and clarification before tables.
- DRS generation/crosscheck, Stage 5 gate and final central coherence PASS (zero findings).
- 291 protected configuration/upstream/SRS/ARS/IPOS files are unchanged. All 55 authored
    requirement bodies and Covers references are identical ignoring layout whitespace.
    Traceability and all three existing descriptive/coverage CSV audits are byte-identical.
- All 24 canonical DB tables were compared with the pre-pilot backup. Only
    `requirement_allocations.created_at` changes through existing ledger refresh; no
    technical allocation, requirement, mapping or snapshot changes were found.
- Initial attempts caught merged adjacent tables and a late zero-number navigation row.
    The Markdown table parser was corrected, and the preservation inventory was rebuilt
    from hash-verified untouched pre-pilot files, never from regenerated outputs.

Evidence: `logs/drs_contract_pilot_before_20261001/`,
`logs/drs_contract_pilot_preservation_20261001.json`,
`logs/drs_contract_pilot_coherence_20261001.json`.

Current hashes:
- Template: `5d71381ef3fb4cd2ae71898506f3d906e67f20011c991869497acc4f9eeb3fac`
- Markdown: `c181b14f3a08291e92e6ea164404e4efa1c0083c942f29e675b42dc97f8bf46e`
- DOCX: `8bea0fc109e0b3eca5bcf5192341042e77d19ac34e0c684f9e0077667f20c501`

### Maintenance And Limits

Change DRS document policy in its template. Implement new rule semantics in the shared
contract/composer and tests before declaring them supported; prose instructions are not
automatically interpreted by Python. Keep orchestration changes in workflow guidance.
Do not change snapshot authority or extend to IPOS/SRS/ARS without separate authorization.
For a new snapshot or authorized table change, preserve and review a new baseline explicitly.
The current baseline intentionally blocks unreviewed table changes, including control-table
values; future metadata-only changes need an explicit baseline/policy decision.

Checks cover deterministic structural/content predicates and existing evidence-backed
synthesis, not a universal proof of human writing quality. Word opening without repair
has not been tested; the earlier unreadable-content issue remains a separate investigation.
No full Stage 0-7 rerun or whole-repository hardcoding cleanup was performed.

Reproduction from the existing baseline:
```powershell
python -B -m unittest discover -s STBIO_AI/tests -p test_*contract.py
python -B -m unittest discover -s STBIO_AI/tests -p test_descriptive_summary.py
python -B STBIO_AI/scripts/run_drs_gen_spec_agent.py --snapshot-id snap-b2e8101b00dc6909feaed885 --regenerate-downstream
python -B STBIO_AI/scripts/validate_stage5_drs_gate.py --snapshot-id snap-b2e8101b00dc6909feaed885
python -B STBIO_AI/scripts/validate_downstream_coherence.py --snapshot-id snap-b2e8101b00dc6909feaed885
```

## Current Behavior-First Cleanup (2026-10-01)

DRS-only regeneration uses approved snapshot `snap-b2e8101b00dc6909feaed885`.
This entry supersedes the output hashes below. The shared deterministic
composers in `scripts/workflow_routing.py` now express named roles and directed
relationships, not evidence/path/endpoint counts or approval/audit prose.
The existing central orchestrator-validator invokes independent final prose
checks for Markdown and DOCX through the DRS descriptive validator. General
Rules and the existing orchestrator/stage-gate guidance carry the same rule.
No pilot block names, aliases, or capability cases were added to shared rules.

### Section Before/After

| Section | Before | After |
| --- | --- | --- |
| 1.2 Scope | Source/destination/path totals described the scope. | States digital integration and interface relationships, with block-local implementation outside the integration scope. |
| 3 System digital context | `The approved integration evidence groups...` followed by totals. | Describes ADC samples reaching Main Controller, sample/control delivery to Smart FIFO, flags to IRQ logic, register configuration/readback, host transactions, status, and named XBAR relationships. |
| 3.1 Power and clock islands | `Approved clock routes reach...` counted destinations; status was described as an architecture record. | Describes 16 MHz operation with and without gating, ungated 32 kHz operation, and PMU power/clock status delivered to Main Controller. |
| 3.1 Buses and interconnects | Counted register/host-interface paths and endpoints. | Explains SPI/I2C register transactions to Regmap, read responses to the interfaces, and I2C_SPI_AHB host transactions with their actual destinations. |
| 3.1 Arbitration, control, and shared resources | Counted grouped exchange types. | Describes sample, configuration, status, host and shared-resource exchanges using their actual names; requester priority remains a targeted clarification after known behavior. |
| 3.1 Digital processing blocks | XBAR connection totals stood in for processing behavior. | Leads with ADSP firmware/signal elaboration and Main Controller DSP elaboration on ADC outputs, then describes XBAR relationships. Connectivity does not establish an ISPU algorithm. |
| 3.1 Sequencing and domain control | Repeated destination counts and audit-shaped status wording. | Describes PMU boot/power-mode sequencing, clock behavior and status delivery, followed by a targeted gap for domain ordering and reset-release dependencies. |
| 3.1 Low-power responsibility | Supply-interface table alone. | Explains PMU's VDD core-supply and VDD_IO digital-I/O-supply interfaces before the unchanged supporting table. |
| 4.2 Arbitration/control/shared resources | Path totals, matched keyword lists (`Approved block functions identify...`), and interleaved unsupported facets. | Describes storage/access roles, configuration and register visibility, host-to-bus translation, boot/reset and clock status. Exact repeated sentences are removed across facets; unsupported flow control, synchronization, performance and priority follow known behavior. |
| 4.3 Register/configuration | Counted register/host paths. | Explains Regmap configuration writes to Main Controller, incoming SPI/I2C transactions and outgoing read responses. |
| 4.4 Interfaces/communication | Counted paths and endpoints. | Describes SPI/I2C register transactions and the corresponding host transactions from I2C_SPI_AHB. |
| 4.5 Data path/buffering | Counted sample/FIFO paths. | Describes ADC sample delivery, Main Controller sample-stream/FIFO-mode delivery, and Smart FIFO status to IRQ logic. |
| 4.6 Digital performance | Counted clock destinations and used approval-shaped table introductions. | Describes supported clock rates and gating first; measured latency and cross-domain synchronization remain explicitly unresolved. Clock/reset tables retain exact details. |
| 4.7 Clock/synchronization | Counted destination endpoints and unresolved routes. | Describes gated/ungated 16 MHz, ungated 32 kHz and ungated 64 kHz distribution, then flags incomplete clock labels. Exact gating expressions, reset connections and interrupt wake-up context remain. |
| 7 Interfaces/mixed-signal interactions | Repeated selected block-purpose descriptions before the boundary table. | Describes actual boundary exchanges and XBAR relationships from the same boundary rows; interface/debug labels are not promoted to blocks. |

The named concrete-block paragraphs in 3.1 and the power-domain architecture
paragraph/table were already evidence-bound and remain unchanged. Incomplete
processing-role inputs in future projects retain known connectivity first,
then `Processing behavior: need clarification`; no missing algorithm is inferred.

### Verification And Preservation

- DRS generation and crosscheck: PASS; 55 authored requirements. Only DRS was regenerated.
- Focused suite: 73 tests PASS, including generic renamed-entity, directed-association,
    duplicate-input, coordinated-verb, incomplete-evidence and independent Markdown/DOCX
    rejection tests. Composer inputs use stable local ordering, without model or network calls.
- Stage 5 DRS gate: PASS. Central downstream coherence: PASS, zero findings.
- All supporting Markdown/DOCX table content is identical to the saved baseline,
    excluding the generated version-history date. Markdown from section 9 onward is
    byte-identical, preserving authored integration content, block boundaries and I/O.
- `drs_traceability_matrix.csv`, `descriptive_summary_audit.csv`, and
    `descriptive_low_power_audit.csv` are byte-identical to the pre-cleanup versions.
- Of 107 protected files fingerprinted before execution, 106 remain byte-identical,
    including configuration, mapping/Stage 2 evidence and SRS/ARS/IPOS outputs. The
    canonical SQLite file changed because the existing generator refreshes its derived
    allocation ledger. A read-only comparison around the final run checked all 24 DB
    tables: only `requirement_allocations.created_at` changed; row counts, allocation
    values, requirements, mappings and snapshots did not. Do not claim DB byte identity.
- The required authority-consistency diagnostic reports legacy findings in untouched
    scripts, including the central validator. It reports none in the two edited Python
    implementation files. This cleanup does not certify or rewrite the whole repository.
- DOCX verification covered final XML prose and editable table content, not a visual
    inspection of Word's paginated layout.

Before artifacts: `logs/drs_cleanup_before_20261001/`. Protected-file fingerprints:
`logs/drs_cleanup_protected_before_20261001.csv`. The comparison DB immediately
before the final run is `logs/drs_cleanup_before_final_run_20261001.sqlite`.

| Current artifact | SHA-256 |
| --- | --- |
| DRS Markdown | `58942716910e70c7da7bba8762a8888575f4315548c8e08c5817e175586d7d88` |
| DRS DOCX | `990f0e9be10b0472d7ed9e074cdbbe78c9ae2be2ef583fa565d694fe46639ebf` |

### Residual Limits

Within the enforced sections, missing approved information remains explicit:
ISPU local processing beyond interrupt wake-up; arbitration priority and concurrent
access ordering; backpressure; detailed domain/reset-release sequencing; CDC/RDC;
measured latency, bandwidth and interrupt response. OCR-split gating tokens and
`DDS_STBIO1_2024` endpoints remain unrepaired. A clock endpoint is not evidence of
an additional concrete block or an approved destination-block alias.

Outside this section-prose cleanup, 4.1 still has exact-label relationship gaps
and tabular inventory roles; section 5 retains generic verification wording;
section 8 retains existing assumptions/TBD wording; 6.4 source-function context
and section 9 source/I/O descriptions retain their prior rendering. These were
not rewritten or certified as natural section summaries. The independent prose
scan covers 1.2, 3, 3.1 and its subsections, 4.2-4.7, and 7; other existing
authority, provenance and block/I/O checks remain active outside that set.

## Current Section-Level Synthesis Pilot (2026-09-30)

Authority remains `snap-b2e8101b00dc6909feaed885`. This DRS-only pilot
regenerated Markdown and DOCX; SRS/ARS/IPOS, approved mappings, canonical DB,
authored requirements, I/O ownership, and snapshot approval were unchanged.
The existing central orchestrator-validator checks section summaries,
interaction provenance, clock routes, reset outputs, domain tables, and final
Markdown/DOCX. General Rules now require thematic synthesis and clarification
boundaries for future projects.

| Section | Before | After |
| --- | --- | --- |
| 3 System context | A single ADC-to-Main-Controller exchange obscured the broader digital paths. | The approved 33 paths are grouped into interconnect, sample/FIFO, register/host-interface, power/clock-status, and test/status families; endpoint labels remain distinct from approved blocks. |
| 3.1 Digital Main Functions | Named block paragraphs were followed by repeated block-purpose prose and a one-edge PMU table. | All 12 selected concrete digital blocks retain dedicated named paragraphs; non-block labels have none. Thematic subsections summarize approved paths, with power/clock destinations represented by the complete route evidence in 4.6/4.7. Singleton power/clock status is a sentence, not a misleading destination table. |
| 4.2 Arbitration/control/shared resources | Concatenated block `Function` summaries and individual `source -> target` strings produced long facet paragraphs. | Facets identify approved owners with supported function terms; the section groups exchanges by evidence family and retains the full audited interaction table. Unsupported priority, ordering, flow control, synchronization and performance remain `need clarification`. |
| 4.6 Digital performance | Repeated the PMU block description and presented a lone status edge before the route table. | Summarizes approved PMU-source clock destinations at 16 MHz and 32 kHz, then preserves all eight clock routes with gating expressions and nine owner-scoped reset outputs with source pages. A malformed route remains unresolved; release behavior is not inferred. |
| 4.7 Clock/synchronization | Repeated PMU block text ahead of the 11 raw clock paths. | Summarizes ten named destination clock endpoints and frequency groups, then retains 11 source-linked routes (including one with unresolved endpoints) and the corroborated reset connection. CDC/RDC and interrupt response remain open. |
| PMU/power-domain control | Domain tables were present but domain-control prose repeated PMU block purpose and emphasized one status edge. | Always-on/switchable-domain descriptions and the domain table remain evidence-bound; sequencing references documented clock-route coverage and records the status edge as a sentence. No additional PMU destination-block mapping is inferred. |

Residual weak/evidence-limited areas: the ISPU local processing function in
3.1 is not established; the Digital processing blocks topic has only XBAR
connection evidence, not a processing contract; a complete destination-block
map beyond the documented clock endpoints is not approved. The OCR-damaged
`DDS_STBIO1_2024` endpoints and OCR-split gating signal spelling remain
unclear. Priority, concurrent-access ordering, backpressure, reset-release
sequencing, CDC/RDC implementation, measured latency/bandwidth and interrupt
response remain `need clarification`. Sections 4.3-4.5 now group approved
exchange families, but detailed policies beyond their audited paths are not
available; section 7 retains its existing interface narrative and was not
rewritten in this pilot. No unsupported behavior was filled in to improve prose.

Verification: DRS regeneration/crosscheck PASS (55 requirements); focused
descriptive tests 71 PASS; Stage 5 DRS gate PASS; central read-only downstream
coherence PASS (0 findings). This is not an S0-Stage 7 rerun. Previous DRS
Markdown/DOCX hashes are recorded below; current SHA-256:

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `5889DCC4125F2E9568004A095C1A2D1A7517E4B1FDDBAD212517ED13CD500E98` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `DEAD4854966F178422862F42B3B787BEF65086910684C32055BBBCC42DB8A69C` |

## Previous Clock-Gating Controls (2026-09-30)

The approved snapshot `snap-b2e8101b00dc6909feaed885` is unchanged.
Before this DRS-only pass, 4.6 and 4.7 said `Gated; control expression:
need clarification` on every gated route, despite the approved DB retaining
the source-table expressions. After: both sections show each approved gating
expression, with Boolean `|` operators preserved as one Markdown/DOCX cell.
OCR-split signal tokens remain verbatim with `signal spelling: need
clarification`; no hierarchy or gate terms were inferred. The damaged source
and destination of `DDS_STBIO1_2024` remain independently unresolved while
its available gating expression is retained in 4.7. The central DRS validator
checks the rows against the selected snapshot in Markdown and DOCX, including
a regression that rejects altered control terms. DRS generation/crosscheck:
PASS (55 requirements); 70 focused tests, Stage 5 gate, and downstream
coherence: PASS (zero findings). No SRS/ARS/IPOS specification or authority
input was regenerated.

Current SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `8137106AB19277AAADAE24C82BCB1595C87F20CDC805A71DBD166B6C6F23C861` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `A09D9CE68C6405F9601EC0E0E9BF689F751E0A7C6141F150A779CD9B7F3263A3` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `BC74E71FDB9A27D366AFC399567C956C598AD9C8880461A566278575AE56299A` |
| `artifacts/stage5_drs/descriptive_low_power_audit.csv` | `8AE72DCFDA1AF63B3C5C4ABAB4313449D144B7BB43924427EF5CA83F4F44E8D6` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |

## Previous Shared-Resource and Power/Clock Pass (2026-09-30)

The approved snapshot `snap-b2e8101b00dc6909feaed885` is unchanged.
Before this DRS-only pilot, 3.1 separated arbitration/control from shared
resources; 4.2 reduced control to two block roles and a small exchange table;
4.6 showed only PMU -> Main Controller power/clock status. After: 3.1 combines
the approved arbitration/control and shared-resource interaction records under
one heading. Section 4.2 presents approved resource ownership, register/memory
access roles and interactions, reset/boot roles, and power/clock context, with
the full selected interaction table and explicit evidence gaps. Section 4.6
retains status, lists eight approved PMU-source clock routes with frequency
and gating status, nine approved owner-scoped PMU reset outputs with source
pages, and the
corroborated 32 kHz Main Controller reset connection. Non-block endpoints
retain source labels; malformed clock route `DDS_STBIO1_2024` is not promoted.
The shared DRS validator invoked by the central orchestrator checks the
Markdown and DOCX against approved Stage 2 and snapshot evidence. No
SRS/ARS/IPOS specification or authority input was regenerated.

Remaining `need clarification`: simultaneous-request priority, concurrent
register/memory access ordering, flow control/backpressure, synchronization
mechanisms, reset release sequence, measured latency/bandwidth/interrupt
response, damaged clock-route endpoints (`DDS_STBIO1_2024`), and exact gated
clock control expressions. DRS generation/crosscheck: PASS (55 requirements);
70 focused tests, Stage 5 gate, and central downstream coherence: PASS
(zero findings).

Previous output SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `E591F73492242A62644F1050E0DA1BD938668876542D292D710E04F334040E66` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `0E7A41023252CA8A3C3DD716BBE95ABA60690D4290256B9DF9458B2AAF885B25` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `BC74E71FDB9A27D366AFC399567C956C598AD9C8880461A566278575AE56299A` |
| `artifacts/stage5_drs/descriptive_low_power_audit.csv` | `8AE72DCFDA1AF63B3C5C4ABAB4313449D144B7BB43924427EF5CA83F4F44E8D6` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |

## Previous DRS Clock Routes (2026-09-30)

The frozen approved snapshot is unchanged. DRS 4.7 now lists 11 approved
source-to-destination clock connection requirements from the canonical DB,
with their documented frequency and gated/not-gated status. One route has an
incomplete OCR hierarchy; its endpoints are marked `need clarification` rather
than corrected by inference. The DB text for the approved
reset/synchronization-labelled connection `DDS_STBIO1_2054` truncates its
source hierarchy and joins it to the destination. The OCR table splits the
`_32` suffix across lines; approved output/input port records corroborate
`PMU.resetn_32k_main_ctrl -> Main Controller.i_rstn_sync_32`. Its
synchronization implementation remains `need clarification`. Exact gating
control expressions, CDC/RDC mechanisms, and measured interrupt response time
also remain `need clarification`.
The central validator checks the route table against the approved snapshot in
both Markdown and DOCX. DRS generation and crosscheck: PASS (55 requirements);
69 focused tests, Stage 5 gate, and downstream coherence: PASS (zero findings).

Previous output SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `F481E50F840AFAF7E988FC07540883AE56C61ED127BDBCC3A672803BA9075E68` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `8D92311C2E89AEF8A9F776B1B0D8BBA58AB2B64DD8FF5C9121EA001F83D54B92` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `BC74E71FDB9A27D366AFC399567C956C598AD9C8880461A566278575AE56299A` |
| `artifacts/stage5_drs/descriptive_low_power_audit.csv` | `8AE72DCFDA1AF63B3C5C4ABAB4313449D144B7BB43924427EF5CA83F4F44E8D6` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |

## Previous DRS Narrative Cleanup (2026-09-30)

Snapshot `snap-b2e8101b00dc6909feaed885` is unchanged. Before this DRS-only
pass, section 3.1 grouped block roles into unheaded paragraphs and introduced
most architecture tables by echoing one exchange. Sections 4.2-4.6 repeated
those exchange summaries, 4.5 used traceability-only prose, and 4.7 labeled
interrupt-status connections as response-time evidence. After: each selected
concrete digital block has a named 3.1 paragraph; relevant inventory roles
introduce the architecture, low-power, shared-resource, bus, control, and
processing tables. Sections 4.2-4.7 and 7 use functional descriptions before
their retained evidence tables. Selected DRS requirements support the ISPU
interrupt-wake-up description; table-only connections do not stand in for a
local processing function. The central DRS validator checks named paragraphs,
topic narratives, the clarification boundaries, and existing table provenance
in Markdown and DOCX. Only the DRS was regenerated; SRS, ARS, IPOS, their
authority inputs, and section 9 approved I/O tables remain unchanged.

Previous output SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `941E5BA1FB13029C58666458AF88EA20B00CEE2EC6DD6DB4EB98CE7108BF107B` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `A0D299497A5BC736962BAF4238F8A9C2FFA1EE324259B2C0F2DBA370E82F8204` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `BC74E71FDB9A27D366AFC399567C956C598AD9C8880461A566278575AE56299A` |
| `artifacts/stage5_drs/descriptive_low_power_audit.csv` | `8AE72DCFDA1AF63B3C5C4ABAB4313449D144B7BB43924427EF5CA83F4F44E8D6` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |

DRS generation/crosscheck: PASS (55 requirements). Focused descriptive tests:
68 PASS. Residual `need clarification`: ISPU local processing beyond its
approved interrupt-triggered wake-up, priority among concurrent shared-resource
requesters, direct integration for blocks without an exact matrix endpoint,
cross-domain synchronization and measured latency. Source labels that differ
from inventory block names are not silently equated. Numeric clock frequencies
and supported power-domain roles are retained; no unsupported CDC, voltage, or
arbitration policy is inferred.

## Previous DRS Functions, Domains, and Author (2026-09-30)

The document-author refresh uses the signed-in Windows account's full display
name at generation time. SRS, ARS, DRS, eight materialized digital IPOS
documents, and the combined SRS LaTeX were regenerated from the same approved
snapshot; analog IPOS had no materialized blocks. Visible Author fields,
version-history Author cells, and DOCX creator properties agree across all
eleven generated specifications. The login remains reserved for technical
activity logs, never the document Author field. The central downstream
validator checks author-field consistency without assuming the verifier is the
original document author.

Snapshot `snap-b2e8101b00dc6909feaed885` remains the sole authority. Before
this DRS-only pass, section 3.1 had interaction tables but no coherent digital
function overview and displayed fragmentary power-domain/low-power bullets;
section 4.1 listed block names without roles or relationships. Now section
3.1 groups the selected inventory functions into prose and projects selected
Stage 1 structured power-domain evidence into one domain/type/control/function
table, with retention context alongside it. Section 4.1 shows roles from the
approved concrete-block inventory and only exact endpoint relationships from
the approved interaction matrix. Existing interaction and section 9 I/O tables
are retained. The DRS descriptive validator used by the crosscheck, Stage 5,
and downstream gates checks both Markdown and DOCX against those artifacts.

Previous output SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `084EC87F65E13EDD7FBB6AFF128E6FDF26730ACBC74E0DDA400C9741F93AE628` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `7B2A9D962CA196E8E1FC60BF8EAA94D6883585C276B0CAF601F3DC4F28CDF435` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `BC74E71FDB9A27D366AFC399567C956C598AD9C8880461A566278575AE56299A` |
| `artifacts/stage5_drs/descriptive_low_power_audit.csv` | `8AE72DCFDA1AF63B3C5C4ABAB4313449D144B7BB43924427EF5CA83F4F44E8D6` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |

At that point, focused descriptive tests: 67 PASS; DRS generation/crosscheck, Stage 5 gate,
and central downstream gate: PASS. Requirement count remains 55. Residual
limits: endpoint labels such as `SENSOR HUB` do not always exactly match
inventory labels such as `Sensor-Hub`; section 4.1 explicitly marks blocks
without a matching direct matrix path instead of inferring relationships.
OCR power-domain voltage and included-block fields are omitted where noisy;
the structured domain type, control, function, and audit provenance remain.
The preceding DRS descriptive pass did not regenerate SRS/ARS or IPOS; the
subsequent author refresh described above did.

## Previous DRS Introductory Rollout (2026-09-29)

The earlier fingerprints below are the **before** state for the separately
authorized DRS-only introductory rollout. The approved snapshot remains
`snap-b2e8101b00dc6909feaed885`; no SRS/ARS rendering or authority inputs
changed. DRS now projects existing top-digital interactions into natural
descriptive paragraphs and audited source/destination/exchange tables. These
endpoints remain integration context, not newly classified concrete blocks.
Approved concrete-block I/O tables in section 9 are unchanged.

Before: sections 1.1-1.2 and 3 had generic scope/context sentences, section
3.1 emitted raw `Interaction:` bullets, sections 4.2-4.6 used unsourced
`shall define` placeholders, 4.5 copied requirement statements into bullets,
4.7 repeated generic timing bullets, and section 7 speculated about interface
handshakes. After: section 1 identifies the selected digital scope and the
actual integration path count; section 3 summarizes the ADC-to-controller
sample path and supplies relationship tables for power/clock, buses, control,
shared resources, and processing; low-power interface evidence is tabular.
Sections 4.2-4.6 summarize evidenced control/mode, register, host protocol,
sample/FIFO, and power/clock-status paths in topic-specific tables. Section
4.7 lists timing source IDs and upstream references in a coverage table;
section 7 tabulates only evidenced integration endpoints outside the selected
concrete-block set. The authored requirement catalog remains authoritative.

Previous output SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `67B781F4B93399C92FE9D4BEB9C3457E5204972D5B2B036F48CB891C80E1F1F2` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `33433CA7A49B0A8961D557A8D0ADE8A90D29BA16B832DFCFDD34DC126A15EEEE` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `BC74E71FDB9A27D366AFC399567C956C598AD9C8880461A566278575AE56299A` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |

For that rollout, focused descriptive tests: 63 PASS. DRS generation and crosscheck: PASS
(55 requirements, 10/10 inputs). Stage 5 DRS gate: PASS; read-only central
downstream coherence: PASS, zero findings. The fingerprints in this section
are historical; use the current table above for the generated outputs.

## Historical Block-Description Baseline

This is a local output baseline, not a new approval snapshot or a git commit.
Approved immutable snapshot: `snap-b2e8101b00dc6909feaed885`. The shared
document-neutral natural-prose rule is validated for IPOS and now DRS; SRS and
ARS retain their existing rendering and literal inventory-function checks until
each receives a separate pilot decision. The earlier IPOS baseline and its
historical hashes are in `docs/ipos-descriptive-rendering.md`.

The DRS pilot selects only approved concrete digital blocks, describes each
using the complete approved inventory `Function`, and records exact provenance
in the existing descriptive audit. Owner-scoped approved block I/O remains in
Markdown and final DOCX tables. Stage 5, DRS crosscheck, and the central
downstream validator share the final-artifact descriptive check. This freeze
does not change snapshot authority, Stage 2A, requirements, allocation, or
SRS/ARS artifacts.

## Frozen fingerprints

SHA-256 (relative to `STBIO_AI/`):

| Artifact | SHA-256 |
| --- | --- |
| `artifacts/stage5_drs/digital_requirements_specification.md` | `613DFF836D0B4AA90E3E2CAB3D3A6A4727723F0B93FC7A26F1E6B4AD6E48CFC6` |
| `artifacts/stage5_drs/digital_requirements_specification.docx` | `BE276014730CE48B555881CA6262132E54FD64AB8AFAA44F51B5899FB8F14E53` |
| `artifacts/stage5_drs/descriptive_summary_audit.csv` | `37F30E5E51905BF64186BABB7190B369B95DCDEBD9B4844BFA93F64D78FE760B` |
| `artifacts/stage5_drs/drs_traceability_matrix.csv` | `D8132195D71C7CBE8FAC899DDA5263181D7954589B8B844478CC7DD51D54B93C` |
| `artifacts/orchestrator/stage_drs_report.md` | `10D917E55DB2C3EDA08EE215741735742712E068FDBA87B2B5FEF1151F97BBB3` |
| `artifacts/orchestrator/stage_drs_crosscheck_report.md` | `6FAFBDC78F26D85D2A997E6236BD9DD9289EE96C5F4947515EC1293C60FA1921` |

The DOCX was open in another process when fingerprinted. `Get-FileHash` could
not read it; Python's read mode successfully hashed the existing file without
closing or regenerating it. Do not substitute the Markdown hash for DOCX bytes.

## Validation record

- DRS regeneration and crosscheck: PASS, full inputs (10 present, 0 missing),
  55 generated requirements, 13 assigned to an owning block and 42 unassigned.
  The unassigned rows remain visible in the Stage DRS report; the crosscheck
  reported no missing generated traceability rows and no findings.
- Focused descriptive regression suite: 62 tests PASS.
- Stage 5 DRS gate: PASS.
- Full read-only downstream coherence: PASS, 0 findings.
- No SRS/ARS regeneration and no whole-workflow S0-Stage 7 rerun is claimed.

## Reproduction from workspace root

Regeneration changes output bytes and should be performed only when an updated
DRS pilot is authorized. For the current outputs, run the read-only checks and
compare SHA-256 values in the current table above; the historical tables are
retained for before/after comparison:

```powershell
python -B -m unittest discover -s STBIO_AI/tests -p test_descriptive_summary.py
python -B STBIO_AI/scripts/validate_stage5_drs_gate.py --snapshot-id snap-b2e8101b00dc6909feaed885
python -B STBIO_AI/scripts/validate_downstream_coherence.py --snapshot-id snap-b2e8101b00dc6909feaed885
Get-FileHash STBIO_AI/artifacts/stage5_drs/digital_requirements_specification.md,STBIO_AI/artifacts/stage5_drs/descriptive_summary_audit.csv,STBIO_AI/artifacts/stage5_drs/drs_traceability_matrix.csv,STBIO_AI/artifacts/orchestrator/stage_drs_report.md,STBIO_AI/artifacts/orchestrator/stage_drs_crosscheck_report.md -Algorithm SHA256
python -B -c "import hashlib; from pathlib import Path; path=Path('STBIO_AI/artifacts/stage5_drs/digital_requirements_specification.docx'); print(hashlib.sha256(path.read_bytes()).hexdigest().upper())"
```

The command that produced this DRS-only baseline was:

```powershell
python -B STBIO_AI/scripts/run_drs_gen_spec_agent.py --snapshot-id snap-b2e8101b00dc6909feaed885 --regenerate-downstream
```

If an artifact is regenerated, compare its new fingerprints and validation
results before explicitly replacing this baseline. Do not roll the shared
descriptive rule into SRS or ARS merely because DRS passed.