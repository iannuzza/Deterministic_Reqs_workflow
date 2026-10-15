# SysML Model View Status Legend

Reference documentation only; authority is false. This file does not configure
classification, approve evidence, waive gates, or change readiness. The shared
implementation is [sysml_relations.py](../scripts/sysml_relations.py); the
[central downstream validator](../scripts/validate_downstream_coherence.py)
owns scope, snapshot coherence and readiness.

## Where To Read Each Assessment

| View or report | Assessment | Interpretation |
| --- | --- | --- |
| Hierarchy | Containment | Approved materialized system/subsystem/block structure, not signal wiring. |
| Block Relations | Block-to-block evidence and current model representation | Includes documented clocks, resets, buses, data/control/status exchanges and interactions, including admitted XBAR matrix cells. |
| Signal Connections / Connections | Port-connection representation and unresolved candidates | A physical connector requires exact scoped endpoints and compatible directions. Block-only evidence cannot establish remote pins. |
| Signal Connections / Signal Details | Per-I/O description and peer resolution | Local Port identifies the inspected I/O. Documented Peer can be a block or a qualified endpoint. Peer Role distinguishes its role relative to the local block. |
| Relation reports | Inventory, integrity and view coverage | Derived accounting, not architectural approval or implementation certification. |
| Readiness reports | Complete checklist and central gates | Separate from connection presence or endpoint resolution. |

## Connection And Model Row Statuses

The GUI uses a specific `resolution_status` when available; otherwise it shows
the underlying `status` or `connection_status`. Thus a report can retain
`status=unresolved` while the GUI displays a more precise cause.

Connections and Signal Details expose two independent assessments for clocks,
resets and other connections: **Endpoint Status** describes identity/port/direction
resolution; **Model Status** describes the current serialized connector. Thus
`resolved` and `missing` can correctly occur together on the same row in both
tabs. A `not_established` model status means no supported connector assessment
was linked, not that a physical wire is missing. Signal Details uses the same
central model assessment as Connections, not a separate GUI inference.

| Status | Classification | Meaning | Limit or follow-up |
| --- | --- | --- | --- |
| `serialized` | Current model representation | A connector exists in the selected-snapshot model, has governed metadata, and has no connector-specific findings in the central comparison. | Does not certify whole-model completeness or READY. |
| `missing` | Representation gap | A documented, resolved inventory relation is not serialized under its expected identity in the current model. | Not evidence that the primary source lacks the connection. In the Name Status column, this same word instead means the I/O name is missing. |
| `invalid` | Integrity failure | A serialized connector has findings in the central model-to-inventory comparison. | Read Reason for the exact mismatch; presence alone is not compliance. |
| `unverified` | Unverified representation | A parsed connector lacks governed relation metadata. | Its declaration is not proof of admitted evidence or validated wiring. This value may also appear in Kind when typed metadata is absent. |
| `historical/unverified` | Snapshot mismatch | The connector's model snapshot is different from the selected snapshot, or its snapshot header is unknown. | Historical visibility is not current-snapshot acceptance. |
| `resolved` | Endpoint or inventory resolution | Required identities are resolved at the assessed level; a signal relation also requires explicit ports and compatible directions. | In Signal Details this is not a claim that the connection is serialized. A resolved block relationship does not establish pins. |
| `block_only` | Documented block relationship | Evidence identifies the peer block or block interaction, but does not establish a complete pin-level contract. | Valid block-level information, not a missing-wire claim. Use Block Relations; retain the unknown peer port explicitly. |
| `unmapped_instance` | Endpoint identity gap | Neither an explicit snapshot binding nor the shared case-insensitive, complete-name instance-segment rule identifies a scoped model block. | The signal connection may be explicit in the source. This label does not mean the source connection is absent; do not guess substrings or ancestor identities. |
| `port_not_found` | Port identity gap | A block identity is known, but its referenced port is not uniquely established in the approved port inventory. | Do not substitute a similarly named port. |
| `identity_conflict` | Ambiguous identity | More than one admitted identity matches an endpoint. | Resolve the identity conflict; do not choose a candidate silently. |
| `direction_missing` | Direction gap | Available I/O or peer-role evidence does not establish the required directed relationship. | A retained association is not proof of source-to-target direction. |
| `direction_conflict` | Direction contradiction | Approved port directions do not support the described source-to-target relationship. | Check the original direction and reference; do not reverse wiring automatically. |
| `connection_conflict` | Rejected signal candidate | Endpoint lookup succeeded, but the candidate did not survive central connection validation. | No resolved physical connector may be claimed from that candidate. |
| `incomplete_reference` | Incomplete source reference | A documented peer path lacks a port suffix, for example `u_fabric.`. | Preserve the literal text; do not complete the name by guessing. |
| `unsupported_reference` | Reference projection gap | The reference is conditional, ambiguous, split, or outside the supported reference grammar. | Parser inability is not proof of absent source information. |
| `evidence_unbound` | Evidence binding gap | An interaction lacks complete selected-snapshot evidence or required admitted endpoint/exchange fields. | A derived matrix entry alone cannot establish a governed relation. |
| `outside_scope` | Scope boundary | The referenced peer is not resolved within the current materialized block scope. | Retain the boundary label; do not create a block or infer a canonical identity. The peer may exist elsewhere in the source architecture. |
| `non_materializable` | Statement projection gap | The admitted statement or derived matrix cannot be projected by the supported relation grammar with independently supported endpoints and type. | Does not by itself establish a source defect or require new approval. |
| `conflicting` | General conflict | The underlying inventory reports incompatible evidence, metadata, direction, drivers, or snapshot binding. | A specific resolution cause may replace this generic label in the GUI. Read Reason. |
| `unresolved` | General unresolved candidate | The relation lacks enough established identity, port, direction or evidence support for the assessed level. | Read Reason; this generic label does not identify the root cause by itself. |
| `not_established` | No established peer projection | The current adapter did not establish a peer from the retained I/O description. | The source may still contain useful information; a blank target is not proof of no connection. |
| `incomplete` | Raw I/O-check status | The source peer reference ends before its port name. | Raw report counterpart of the more specific incomplete-reference diagnosis. |
| `unsupported` | Raw I/O-check status | The reference parser cannot project the retained details unambiguously. | Raw report counterpart of unsupported-reference handling. |
| `stale` | I/O snapshot mismatch | The I/O row explicitly belongs to a different snapshot. | It cannot establish a current-snapshot connector. |
| `candidate` | Intermediate I/O-check state | A qualified peer token was extracted before endpoint and connection validation. | Candidate extraction alone is not a validated connection. |

## Signal Detail Fields

| Field | Value | Meaning and limit |
| --- | --- | --- |
| Name Status | `present` / `missing` | Whether the retained local I/O name is nonempty; not semantic validation. |
| Direction Status | `valid` / `invalid_or_missing` | Whether the catalog direction is one of the accepted direction values; not validation of a remote connection. |
| Description Status | `present` / `not_established` | Whether the adapter retains more than a type/width-only description; presence does not prove complete semantics. |
| Width | Literal expression / `unspecified` | The retained width expression or bit count; no default one-bit width is inferred. |
| Reference Level | `block` | A prose description establishes a block-level peer, not a remote port. |
| Peer Role | `source` / `target` | The documented peer supplies the local block or receives from it, respectively. |
| Peer Role | `peer` / `unspecified` | An association without a producer/consumer direction, or a role not established by the adapter. |
| Peer Port Status | `not_established` | Block-level evidence does not identify the exact remote pin. |
| Any unpopulated detail field | Blank | The current adapter did not populate that field; blank is not a proven absence or automatic not-applicable decision. |

## Report Coverage And Readiness

| Status | Applies to | Meaning and limit |
| --- | --- | --- |
| `REPRESENTED` | Relation view coverage | All expected resolved obligations match serialized connectors, with no residual candidates counted for that view; not proof of source completeness. |
| `PARTIAL` | Relation view coverage | Expected resolved obligations are represented, but residual candidates remain. |
| `INCOMPLETE` | Relation view coverage | Not all expected resolved obligations match serialized connectors. |
| `PASS` | Containment coverage | No findings in the central containment check; not full functional or implementation readiness. |
| `FAIL` | Containment coverage | Central containment checking reported findings. |
| `READY` | Final readiness | The current bound central assessment satisfies required checklist obligations and applicable gates. A connection row alone cannot confer this state. |
| `NOT_READY` | Final readiness | Required obligations or gates are unsatisfied, uncertain, unavailable or stale. It is not a finding that every source requirement is defective. |

## Examples

- An approved description saying "fifo clock" can establish PMU to Smart FIFO
  through the central approved label alias. Its peer is visible as `block_only`
  even when the destination port is unknown.
- A literal `u_pmu.clk_fifo` reference resolves to the scoped PMU block through
  the shared complete-name instance-segment rule. Exact port spelling and
  compatible directions are still required; ambiguous identities are not chosen.
- An admitted XBAR source/destination cell can establish a bus block relation
  without establishing AHB pin connections. If that expected block relation is
  absent from the current SysML serialization, its row is `missing`.

Counts are inventory/projection records, not necessarily distinct physical
nets. Different evidence routes and assessment levels can produce several rows
for one described relationship. None of these labels changes source approval,
allocation, ownership, snapshot selection or production publication eligibility.