# SysML Readiness Checklist

## Purpose

The project-agnostic checklist in `config/readiness_checklist.json` protects downstream AI use. A generated file, structural PASS, port count, protocol acronym or successful document publication does not establish sufficient evidence for trustworthy RTL or high-level-model generation.

`scripts/validate_downstream_coherence.py` remains the sole readiness assessor. `scripts/readiness_checklist.py` contains its checklist/report mechanics, not an independent authority, evidence admission path or approval workflow. The integrated v2 catalog preserves the original rule IDs and extends their technical coverage. Required conditional items need evidence of applicability or non-applicability. Absence of a keyword is not proof of non-applicability.

## Integrated Sections

The single catalog covers scope and intent; interfaces; clocks and resets; FSMs and control behavior; functional behavior; datapath and data semantics; configuration, CSR, memory and registers; timing, ordering and performance constraints; internal structure and composition; consistency and conflict checks; traceability and governed evidence support; residual gaps and readiness blockers; and the final READY or NOT READY decision. Optional DFT, DFX and diagnostics remain a clearly identified conditional section, not another checklist.

Explicit additions include signal grouping and clock domains, asynchronous signals, CDC and reset-domain crossings, post-reset and recovery behavior, fixed/floating formats, overflow/underflow, CSR maps and access permissions, FIFO/RAM/ROM behavior, throughput, and behaviorally relevant gating, isolation and retention. Register maps do not become I/O evidence. Unresolved, ambiguous, conflicting, omitted, outside-scope and source-update-needed gaps retain their classification, provenance and readiness impact.

## Standard Interface Coverage

`io.standard` centrally defines the rule for all interface and timing checks. A clearly identified recognized standard, such as AMBA AHB/APB/AXI, I2C, SPI, LIN, UART or another unambiguous standard, can cover its defined signal semantics, value interpretation, handshakes and timing without local restatement or redundant revalidation. The reference and its applicability must be admitted, governed and traceable. Identify a version or revision where needed to remove ambiguity, not by guessing.

The same catalog still verifies standard identification, the block role, applicable subset or mode, local deviations, sidebands or extra signals, and local integration constraints. Applicability includes the exact local interface/signal mapping and behavior covered. Non-standard or partly identified interfaces, and undocumented deviations, require full custom checks for affected behavior; a protocol acronym cannot produce READY.

Central evidence adapters may mark covered results with `Coverage basis: standard` and a nonempty `Standard-defined scope`, retaining their evidence references. Checklist construction and decision validation reject that coverage unless `io.standard`, `io.role`, `io.mode`, `io.deviations`, `io.sideband` and `io.integration` are supported. Standard identification and role require a pass; other local checks may use evidence-backed non-applicability. Standard coverage cannot waive widths, clock domains, resets, CDC, local constraints or custom signals. This is not a new evidence admission or approval path: only the existing central assessor supplies evaluated checks from the selected governed snapshot. Unsupported extraction remains visible uncertainty, not a demand to rewrite the standard.

## Optional Diagnostics

`diagnostics.behavior` is informational by default. Its unassessed status remains visible but does not universally block readiness. The master policy's `required_optional_rule_ids` can explicitly require this rule; then missing or uncertain support blocks READY, even if a result attempts to label it informational. A central assessment may also escalate it to blocking. Optional status does not waive diagnostic requirements already admitted as mandatory functional behavior.

`readiness.decision` is derived from the required obligations, never accepted as a manually supplied pass. Central scope, coherence, dependency and residual findings override it to failure. Changing the rule catalog invalidates old fingerprint-bound assessments; no model or snapshot authority is changed.

## Editable Rule Reference

`config/readiness_checklist.xlsx` is the user-readable checklist reference to be satisfied by every centrally scoped hierarchy-level model and block. The Markdown, JSON and Excel summaries identify this reference. This rules workbook is separate from the generated assessment workbooks below.

Users may edit categories and rule descriptions, or add rules with unique dotted IDs such as `custom.integration`, in its **Checklist Rules** sheet. Keep the three headers and **Policy Metadata** intact. Save and close the workbook. The final SysML phase validates and synchronizes these saved changes into the adjacent JSON before generation or assessment. For report-only assessment, first run from the repository root:

```powershell
python -B scripts/readiness_checklist.py --sync-from-excel
```

Locked workbooks, formulas, duplicate IDs, missing mandatory built-in IDs and conflicting independent JSON edits are rejected without importing the rules. Read-only assessment rejects unsynchronized workbook edits rather than using stale JSON. The JSON fingerprint changes after import, invalidating prior assessments. Modified and new rule descriptions remain blocking `uncertain` until a matching central evidence adapter supports them; edits cannot inherit old automatic passes, approve source evidence or override readiness gates. Do not delete mandatory built-in rules or edit JSON and Excel independently.

## Assessment Table

Every model report includes one row per catalog item, with:

| Field | Allowed values or content |
| --- | --- |
| Category | Catalog category |
| Checklist item | Exact catalog item |
| Assessment result | `pass`, `fail`, `not_applicable`, `uncertain` |
| Evidence status | `supported`, `partially_supported`, `missing`, `contradictory` |
| Reason | Item-specific explanation, including evaluator limitations |
| Readiness impact | `blocking`, `non_blocking`, `informational` |

Rows additionally contain a stable checklist ID and separate verified and candidate evidence references. Candidate references never establish a pass. Unsupported non-applicability, missing/duplicate rows, invalid enum values, contradictory evidence and unsupported passes fail closed. Required obligations remain blocking; changing their impact field cannot waive an unresolved obligation. Only the centrally declared optional diagnostics rule may remain informational without proof of applicability.

## Decision And Sticker

READY requires a complete supported checklist, no blocking fail or uncertainty, no material coherence or snapshot issue and no unresolved material residual gap. Missing, stale or inconsistent assessment defaults to NOT READY. A valid non-applicability result needs explicit governed evidence and an item-specific reason.

Each generated SysML starts with exactly one valid comment declaration:

```text
// READY for RTL or high-level model generation
```

or:

```text
// NOT READY for RTL or high-level model generation
```

The `//` preserves SysML syntax. Generation initially uses the central NOT READY default. Only central recomputation and stamping may promote it. Checklist policy, evaluator implementation, snapshot, contract, semantic model bodies, relevant inputs and residual reviews are freshness-bound. Editing a report cannot authorize READY. Publication eligibility and implementation readiness remain distinct.

## Reports

The final SysML phase writes one JSON file per centrally scoped model under `artifacts/validation/readiness_checklists/`. Each includes the checklist, overall declaration, blocking-item summary, residual gaps, model identity and assessment binding. Successful central stamping also writes the aggregate `artifacts/validation/final_readiness.json`. Missing, changed or stale per-model reports invalidate a persisted assessment.

The same central writer produces `readiness_summary.md` and `readiness_summary.json` in that directory. Their block table separates official blocks from system/shared models and includes readiness, per-result counts, blocking obligations and detailed report links. This is the current assessment, not a claim that existing file stickers were updated. Isolated demo exports are not promoted or substituted for official files.

Excel equivalents are also written: `readiness_summary.xlsx` contains block/system status tables and relative links to each detailed workbook. Every per-model workbook contains Checklist, Blocking Items, Residual Gaps and Metadata sheets. They are presentation-only exports; edits are never consumed as readiness evidence or approval. Keep the workbooks closed while regenerating reports to avoid Excel file locks.

## GUI Execution

In the SysML tab, **Generate SysML + Checklist** invokes only `run_final_sysml_phase.py` with the selected approved snapshot. This is the separate final phase after Digital IPOS and applicable Analog IPOS, not a Stage 2 preview. It does not rerun or modify upstream specification stages and does not consume isolated demo exports.

The central checklist and Excel reports run automatically immediately after the generation attempt. On a failed generation or validation gate, reports describe available official artifacts; they do not certify a successful new model set. Structural/coherence gates and final stamping remain enforced. Execution-log lines beginning `[REPORT] Open SysML readiness Excel:` are clickable and open the summary or individual reports in Excel through the existing GUI opener. Readiness NOT READY is distinct from generation failure; both are logged explicitly.

Final SysML failures use a dedicated dialog, not the generic Stage 3-7 JSON viewer. Its **Open Excel summary** action requires a `[SYSML_READINESS]` receipt emitted by the same run, with matching selected snapshot and exact JSON/Excel summary hashes. Missing, changed or wrong-snapshot reports cannot be opened through that action. Opening the summary never runs an upstream repair. The existing generic validation report dialog remains available for upstream stage failures.

For report-only evaluation, without model regeneration, declaration stamping, manifest updates or authority changes:

```powershell
python -B scripts/validate_downstream_coherence.py --snapshot-id <explicit-approved-snapshot-id> --readiness-report
```

Exit code 0 means READY; exit code 1 means NOT READY, including a successfully produced blocked assessment. Report-only evaluation never waives production gates. Snapshot resolution must succeed; invalid authority is an error, not permission to infer scope. A stale but resolvable materialization scope can be reported as NOT READY, while production stamping still rejects it. Unsafe external model addresses are not consumed as readiness inputs.

## Three Governed Views

The central downstream contract owns one snapshot-bound relation inventory using
`scripts/sysml_relations.py`. Extraction, exact endpoint resolution, typing,
serialization, actual-model parsing and representation checks are shared. The GUI
does not repair models or infer relations. **Model Views** opens one window with
three tabs and shared snapshot/block context:

- **Hierarchy** shows actual serialized containment only, never interaction or wiring arrows.
- **Block Relations** retains documented dependencies/interactions and distinct clock/reset distribution, without requiring port identities.
- **Signal Connections** shows only explicitly supported directed port-to-port connections. Unresolved ports preserve a supported block relation but cannot create wiring.

Within **Signal Connections**, **Signal Details** inspects every approved source-I/O
catalog row for the centrally materialized digital and analog blocks. Select a
hierarchy block and enable **Selected block** to inspect its signals; selecting
the digital subsystem filters its descendants, while the system scope includes
all blocks. The **Connections** mode remains the actual-model/gap projection.

The shared inventory retains names, directions, literal descriptions, specified
width expressions, clock/reset/bus classification, peer endpoints, table/page/file
provenance and snapshot. Description presence is not proof of semantic sufficiency.
Explicit single peer references in table details support connection candidates;
incomplete paths, conditional or ambiguous forms and unmapped instances remain
visible gaps with their original details. No instance aliases, pin names, widths
or timing are guessed. Rows without an established peer are still listed, not
silently skipped; this is not proof that the primary specification lacks one.
Zero-row blocks remain visible in the report and are not certified complete.

Explicit prose I/O descriptions may identify block-level peers without naming
remote ports: clock/reset descriptions, directed bus/interconnect exchanges,
data/control/status transfers and interactions are retained centrally. Labels
use only the approved central normalizer and aliases. Ambiguous, conditional or
negated descriptions do not establish a connection; references outside the
materialized scope remain visible boundaries, not new blocks. An interaction
expressed as "with" retains unspecified directionality rather than inventing
a producer/consumer direction.

Use **Block Relations** for these documented block-to-block exchanges, including
the admitted XBAR source/destination cells. **Signal Details** retains the local
port, documented peer, peer role, reference level and missing remote-port status.
**Signal Connections** does not promote block-only evidence to pin-level wiring.
Documented relations absent from current model files remain marked `missing`
(documented, not serialized); inspection does not regenerate the models.
Hierarchy remains containment-only. Both scrollbar axes remain present in each
visible model-view pane, including source text and the port map.

Connection projections distinguish `unmapped_instance`, `port_not_found`,
`identity_conflict`, `direction_missing`, `direction_conflict`,
`incomplete_reference`, `unsupported_reference` and `block_only` rather than
displaying every case as unresolved. `block_only` is an interaction without a
pin-level contract, not evidence of a missing wire. The filter accepts these
statuses as well as relation types. Canonical validation statuses remain intact;
the separate `resolution_status` and exact reason are exported in the reports.
Logical block-label comparisons use the central approved normalizer. Qualified
connection paths additionally use `connection_instance_block_keys` from the
central downstream validator: the immediate instance segment must contain one
unique scoped block name or approved alias as complete normalized tokens.
Comparison is case-insensitive and equates whitespace, hyphens and underscores;
prefix/suffix tokens may surround the complete name. Ancestor segments, arbitrary
substrings, port-name similarity and longest-match guesses cannot establish
identity. Multiple matching scoped blocks remain `identity_conflict`; no match
remains `unmapped_instance`. Explicit snapshot endpoint bindings take precedence.
Port spelling remains exact, and directions and snapshot eligibility are checked
separately. The original hierarchical path is retained as evidence. This rule is
project-agnostic, connection-only and cannot expand materialization scope or
change ownership, allocation or approval. Endpoint resolution does not establish
that a connection is serialized in the current model.

Both Connections and Signal Details display separate **Endpoint Status** and
**Model Status** columns for clocks, resets and every other connection type.
For example, `resolved` plus `missing` means the documented endpoints are known
but their governed connector is absent from the current SysML serialization.
Signal Details obtains model status from the same central connector assessment
as Connections, linked by governed relation identity and retained I/O evidence.
`not_established` model status means no supported connector assessment was linked;
it must not be treated as a missing wire. The relation workbook's **Signal Status
Crosscheck** sheet exports both statuses for every scoped I/O row.

The central relation JSON includes `signal_checks`; its Excel report has a
**Signal Checks** sheet and per-block signal/description/reference counts in
**Block Matrix**. These are projections of the same inventory, not a separate
validator or approval lane. Actual model files are not regenerated by inspection.

The relation contract forbids promotion based on compatible ports, similar names,
topology or co-occurrence. Unknown RTL paths are unresolved, not proof of an
outside-model block. Explicitly governed outside-scope entities remain boundary
references in gap rows; they do not create block files or model-open actions.
Missing/unsupported extraction grammar is a projection gap, not missing approval
or proof that the specification lacks a relation.

When already admitted architecture metadata explicitly identifies an RTL instance
or endpoint, the existing approved architecture profile can carry
`relation_endpoint_bindings`, a list of objects with exact `endpoint`, approved
`block`, and optional exact source `port`. Bindings are consumed only from the
selected immutable snapshot profile, never mutable GUI configuration. An instance
binding can resolve block identity while its port remains unresolved. Ambiguous
or overlapping bindings do not select a winner. Missing parser support for
existing approved mappings must be addressed before requesting new metadata;
this field is not a separate approval lane and does not authorize snapshot edits.

Supported adapters currently cover explicit signal-connection sentences,
block-level provision/transfer, dependency and communication statements, and exact directed source-I/O peer references.
Derived matrix entries require selected-snapshot requirement evidence and corroborated
endpoint grammar; they cannot establish new relationships independently. Exact
structured interaction cells already admitted in the selected immutable architecture
profile are also central evidence, including source-to-destination crossbar/bus cells
whose flattened requirement text retains only a table heading. The central contract
resolves their block labels using approved normalization and preserves requirement
IDs, profile-row provenance and exchange qualifiers. It does not reread DRS tables
as authority or require reapproval of those admitted cells. Bus relationships do not
imply physical signal connections, and a protocol label is retained only when
explicit in the admitted cell. Outside-scope endpoints remain typed boundary gaps
visible under the Bus filter; they never create extra block models. Current model
files lacking those relationships show documented-but-not-serialized gaps until
ordinary gated regeneration. Other candidate constructions remain explicit central gaps.
The inventory is not a claim that every possible natural-language relationship
can already be extracted.

Block and signal relations use distinct serialized types and identity-bound
provenance. The central validator compares actual endpoints, direction, type,
qualifiers and metadata; signal checks also require the actual port declarations.
Deleting a connector while retaining its requirement sentence is a failure.
Existing legacy connectors remain visible as unverified or historical, never
silently upgraded to governed current connections.

Automatic final-phase reporting also writes
`artifacts/validation/sysml_relations/relation_summary.json` and
`relation_summary.xlsx`, with separate view coverage, an all-block matrix,
integrity findings, full relations and unresolved/conflicting/outside-scope or
non-materializable gaps. `REPRESENTED` describes resolved obligations only;
`PARTIAL` and `INCOMPLETE` disclose residuals and missing serialization. None
certifies a complete netlist. Tab filters show hidden counts and preserve each
tab's filter/scroll state. Tables retain parallel and opposite-direction links
as separate records rather than presenting a fabricated bidirectional net.

Authority, snapshot, readiness and downstream gates are unchanged. Reports and
workbooks never approve evidence. Official generation remains a separate gated
action; implementing these views does not regenerate production models.

## Conservative Assessment

The central assessor currently verifies snapshot/derived-structure consistency and owner-scoped IO identity, direction and widths through existing coherence checks. Legacy interface meaning, interpretation and timing patterns remain useful diagnostics, but matching phrases cannot prove completeness or absence of contradictory semantics.

Remaining semantic checklist items default to blocking `uncertain` until a completeness-capable central adapter can substantiate them from existing governed approved evidence. This includes clocks/resets, full FSM behavior, function triggers and sequencing, arithmetic precision, configuration constraints and cross-representation ambiguity. Existing evidence may contain this information: an unsupported assessment is not a demand for new source approval and not proof that the source lacks it.

This intentionally prevents automatic READY under the current limited semantic coverage. Future adapters must consume the same approved snapshot scope, retain exact provenance and conditions, detect contradiction, establish applicability and completeness, and pass independent mutation tests. Editable rules must not become readiness waivers. Do not implement keyword-based semantics, inferred implementation choices, a new approval lane or a project-specific exception to obtain READY.