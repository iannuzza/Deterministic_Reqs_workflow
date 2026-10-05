# DRS Generation Template Prompt

Use this template to generate a project-specific DRS (Digital Requirements Specification) document for a mixed-signal device after micro-architectural analysis is completed.

## Executable DRS document contract

This template is the sole DRS-specific document contract, subordinate to the General Rules.
The approved snapshot remains the only technical-content authority; approved structural artifacts
retain their existing evidence eligibility and cannot change requirements, ownership or allocation.
The orchestrator coordinates generation and gates. The generator and central validator execute
the versioned contract below. Unknown mandatory rules fail closed. The whole template SHA-256
and contract version are recorded separately from snapshot identity. This pilot applies only to DRS.

```yaml drs-document-contract
version: 1
document_type: DRS
mandatory_rules: [structure, conventions, navigation, table_preservation, technical_prose, evidence_fidelity, artifact_fidelity]
sections: ["1. Introduction", "2. Definitions and terminology", "3. Top Level Overview", "4. Digital requirements", "5. Validation and qualification requirements", "6. Requirement identification and traceability", "7. Interfaces and mixed-signal interactions", "8. Assumptions and TBD", "9. Top-level integration requirements", "10. Missing Inputs"]
navigation: ["0. Document Navigation", "0.1 Table of contents", "0.2 Internal index for paragraphs and pages", "0.3 Document control", "Table 1. Version history", "Table 2. Reference documents", "Table 6. Category convention", "0.4 Table of tables"]
conventions: {
heading: "2.1 Conventions",
after: "2. Definitions and terminology",
before: "3. Top Level Overview",
categories: [
{name: Comment, definition: "This category denotes that the content of the object text is a general comment. For example, this may be an explanation why the requirement demands certain items when there would also be other possibilities. A comment should not be necessary to understand the related requirements"},
{name: Definition, definition: "This category is used for the definition of terms, wordings, technical expressions etc. It is a documentation of design decisions and general instructions that belong to the document itself, e.g. owner of the document, structure of the document. It is needed to understand a related requirement. It is not linked to any test case."},
{name: Assumption, definition: "This category is used for requirements this document provide upstream to another document, indicating what this IP/block/system needs to work properly."},
{name: Requirement, definition: "This category denotes a requirement that has to be implemented and verified. Accordingly, it is necessary to establish traces from the different requirement levels to the test cases for this category."}
]}
writing: evidence_bounded_technical_prose_v1
```

The YAML definitions are literal output content, not classification or requirement-generation rules.
Whitespace may change for layout; definition wording, order and meaning must not change.

## Document objective

Generate a complete, review-ready DRS document that is:
- structured
- traceable
- unambiguous
- verification-oriented
- aligned with project artifacts

## Required input artifacts

Read and use these artifacts before generating the DRS:
- artifacts/stage1_requirements/requirements_summary.csv
- artifacts/stage1_requirements/requirements_rag_crosscheck.md
- artifacts/stage2_mirco_arc/micro_architecture_report.md
- artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv
- artifacts/stage2_mirco_arc/block_inventory.csv
- artifacts/stage2_mirco_arc/interface_catalog.csv
- artifacts/stage2_mirco_arc/interaction_matrix.csv
- artifacts/stage2_mirco_arc/architecture_crosscheck_report.md
- config/project_context.json

Missing authoritative inputs or an invalid document contract block generation. Report missing
supporting inputs explicitly; continue only where the existing snapshot-bound gates permit it.

## Generation rules

0. Top-digital coverage and Digital IPOS boundary:
- Keep the main DRS readable as a top-level digital/integration specification. Do not turn its descriptive body into a Covered/Partial/Missing audit report.
- Generate `artifacts/stage5_drs/top_digital_coverage_audit.csv` as the separate deterministic category-coverage artifact. It shall contain one row for each approved top-digital category, status, matched terms, evidence, provenance, and evidence scope.
- Assess only approved snapshot evidence with scope `top_digital`, `integration`, `architecture`, or `lifted_integration`. Block-local Digital IPOS evidence is not eligible to make a category Covered.
- For Partial or Missing categories, emit no invented filler and synthesize no requirements. Category coverage status remains audit-only; an expected descriptive topic may end with a targeted `need clarification` after its known technical behavior and supporting tables.
- Covered means approved top-level or integration evidence exists, or an approved mapping explicitly lifts block evidence into a top-level constraint, interface, shared-resource rule, interaction, visibility rule, or integration-level timing/sequencing constraint.
- The DRS shall retain top-level integration behavior, shared resources, interconnect, shared clock/reset/power, interface contracts, system-visible status/configuration/modes/errors, and integration-level sequencing/performance constraints.
- Detailed internal behavior, local algorithms, local state machines, local register detail, and block-private requirements remain in the corresponding Digital IPOS specification. If relevant at top level, render only the integration constraint or visible contract, not the block-local requirement body.
- Coverage evidence must preserve source provenance and must not contain copied Digital IPOS detail or block-local normative text.

1. Preserve requirement traceability:
- Keep original requirement IDs where available.
- Do not rewrite source IDs into unrelated IDs.
- For newly authored block-section requirements, start each atomic entry with `[DRS-REQ-xxx] Requirement:`.
- In project-specific digital block sections, split mapped behavior into atomic entries and use one-to-one traceability as Covers: <single upstream requirement ID>.
- Preserve approved authored requirement text and placement; block paragraphs contain only approved integration requirements, not newly promoted block-local requirements.
- Do not use the phrase the following atomic functionality.
2. Use normative language:
- Requirement statements must use shall.
3. Keep facts and assumptions separated:
- Mark assumptions as ASSUME-<NNN>.
4. Do not invent unsupported behavior:
- If evidence is weak, mark as TBD with rationale.
5. Provide verification hooks:
- Each requirement must include verification method and acceptance criteria.
6. Keep terminology consistent with project artifacts.
7. Keep the general requirement catalog residual-only: requirements already mapped in project-specific block sections shall not be repeated in a separate mapped-summary subsection.
8. Formatting reference baseline:
- Use templates/MPT_IPOS_template.docx as the primary style reference for table of contents structure, internal indexes, and table formatting conventions.
- Even when generating Markdown first, keep section ordering, navigation tables, and table layout aligned with that reference template.
9. Page formatting parity (template-aligned):
- Mirror the same document-control presentation style used by the template for navigation and control tables.
- Keep heading hierarchy, section titling style, and table caption/number style consistent across the document.
- Use consistent table column naming and ordering conventions for similar table types.
10. Conventions and existing ID convention table:
- Render exactly one `2.1 Conventions` paragraph under `2. Definitions and terminology`, using the four literal YAML definitions in their declared order.
- Keep `Table 6. Category convention` in document control as the separate existing ID-family table, with its columns and rows unchanged.
- Add 2.1 Conventions to the TOC and internal navigation index without removing existing entries or tables.
11. Connection Matrix requirements:
- When a source artifact contains a `Source`-row/`Destination`-column connection matrix, inspect each populated cross-cell.
- Use the exact source-row and destination-column labels from the matrix; do not invent, alias, normalize, or substitute block names.
- Apply the General Rules DRS matrix rendering and traceability rules. Preserve exact source/destination labels and the approved upstream reference; do not introduce raw source IDs as DRS Covers values or remap approved allocations.

12. Evidence-bounded technical prose (`evidence_bounded_technical_prose_v1`):
- Explain known behavior, responsibilities and directed relationships in natural, non-normative technical prose. Synthesize admitted evidence by section theme; do not concatenate raw snippets, source tags, path lists or copied requirement bodies.
- Within each descriptive paragraph/section, present known behavior first, supporting tables second, and targeted `need clarification` statements last. Retain numerical engineering values such as frequency, latency and width; counts of evidence, paths, endpoints or grouped items are not a technical explanation.
- Reject approval/audit/process prose, including `approved integration evidence groups`, `approved block functions identify` and `approved clock routes reach`, in descriptive content. Keep coverage statistics in audit/report artifacts.
- Use existing shared deterministic composers and independent Markdown/DOCX prose checks. Complete inventory Function meaning and approved I/O remain evidence-bound; never infer a block, capability, timing or synchronization behavior from a signal label.
- Emit one 3.1 purpose paragraph per approved concrete digital block, without duplicating it across topic summaries. Preserve exact provenance in existing descriptive audits and complete owner-scoped I/O tables.
- For arbitration/control/shared resources, synthesize resource responsibility, access and integration behavior only where supported. For clock/reset/power, retain every supported route, frequency, gating status and reset output in tables. Mark unsupported facets precisely without inventing a policy.
- Reusable code, guidance and tests must not contain project-specific block names, aliases or capability catalogues. Snapshot content and admitted structural evidence provide project values.

13. Preservation and validation:
- Preserve every existing table, including contents, columns, source attribution and owner/section association. The internal navigation table may gain entries; existing entries must remain. Capture a pre-pilot Markdown/DOCX table baseline explicitly and never refresh it silently during generation.
- Keep title/metadata on page 1, TOC first on page 2, Document Navigation after the TOC and the right-aligned PAGE footer through the existing shared formatter. Preserve TOC hierarchy, internal index, document-control tables and table index. Markdown navigation retains its existing structure.
- Keep requirements, IDs, allocation, provenance and the approved snapshot unchanged. Move Source Function Context into section 6 as subsection 6.4 without rewriting authored content.
- The shared final-document validator checks both formats against this contract and the preservation baseline. Existing descriptive/evidence checks remain mandatory; composer self-comparison alone cannot pass.
- Record the whole template hash, contract version, baseline hash, final artifact hashes and rule results in `drs_document_contract.json` and summarize execution in the stage report.

## Required output artifacts

Generate:
- artifacts/stage5_drs/digital_requirements_specification.md
- artifacts/stage5_drs/digital_requirements_specification.docx
- artifacts/stage5_drs/drs_document_contract.json
- artifacts/stage5_drs/drs_traceability_matrix.csv
- artifacts/stage5_drs/top_digital_coverage_audit.csv
- artifacts/orchestrator/stage_drs_report.md

## DRS document format

Use the YAML section order. The following guidance explains those sections; it does not
authorize additional technical content. Preserve existing topic and owner-scoped tables.

### Title page

Place these fields below the `Digital Requirements Specification` title, following the first-page presentation convention in `templates/MPT_IPOS_template.docx`:
- Project subtitle: the project name from `config/project_context.json`.
- Author: the current Windows user's full display name, resolved at generation time.
- Date and source specification.

### 0. Document Navigation

Preserve 0.1 Table of contents, 0.2 Internal index for paragraphs and pages,
0.3 Document control and 0.4 Table of tables. Retain Table 1 Version history,
Table 2 Reference documents, Table 3 Section navigation index and Table 6 Category convention.
Keep Table 6 in document control, separate from the definitions under 2.1.
Use consistent heading levels and working internal targets.

### 1. Introduction

#### 1.1 Purpose
Define the purpose of the DRS and device scope.

#### 1.2 Scope
Describe approved digital integration, shared behavior and externally visible contracts.
Detailed block-private implementation remains in Digital IPOS.

#### 1.3 Intended audience
This document is intended for:
- digital design engineers
- system architects
- verification engineers
- firmware engineers
- test engineers
- product engineers
- program and customer stakeholders

#### 1.4 References
Keep the reference file list exclusively in `Table 2. Reference documents`.
Do not repeat the file paths as a second list in this paragraph.


### 2. Definitions and terminology

#### 2.1 Conventions
Render Comment, Definition, Assumption and Requirement from the YAML definitions above,
in order, exactly once. Do not duplicate them in document control.

#### 2.2 Digital terminology
Define digital terms such as register, bit field, mode, state, reset, interrupt, FIFO, packet, handshake, and watchdog.

#### 2.3 Data handling terminology
Define word length, data format, alignment, endianness, throughput, latency, buffering, overflow, and underflow.

#### 2.4 Communication terminology
If applicable, define SPI, I2C, UART, command and response framing, status words, chip select behavior, and timing constraints.

#### 2.5 Timing terminology
Define setup time, hold time, propagation delay, response time, interrupt latency, synchronization, and clock-domain crossing constraints.

### 3. Top Level Overview
Describe the approved Digital Top at a high level: its purpose, its explicitly approved
system or application role, and the major top-level digital capabilities it enables.
Use source-backed architectural capability statements from the Stage 1 catalog when
they describe this role. Use the reviewed `artifacts/stage1_specs/architecture_mapping_preview.csv`
for approved mapping and ownership context. Stage 1/source-spec content remains authoritative;
SRS and ARS are parallel downstream derivations and neither is authoritative over the other.
Do not repeat the later `3.1 Digital Main Functions` block descriptions, add low-level
implementation detail, or infer application context that is not explicitly approved.

Summarize relevant architecture context and mixed-signal dependencies required to understand digital requirements.

#### 3.1 Digital Main Functions

Describe approved concrete digital block purposes and distinct integration themes:
power/clock islands, buses/interconnects, arbitration/control/shared resources,
digital processing, power-domain architecture, sequencing and low-power responsibility.
Use admitted inventory functions and integration evidence; retain supporting tables and audits.

### 4. Digital requirements

#### 4.1 Digital block list
List the project-dependent digital block names from the current architecture-analysis block inventory; generic block names in this template are rules, not output values.

#### 4.2 Arbitration, control, and shared resources
Explain approved shared-resource responsibilities, integration control, mode coordination,
reset/boot and power transitions. Keep private state machines in IPOS.

#### 4.3 Register and configuration requirements
Explain system-visible register/configuration contracts, parameter dependencies, defaults,
update timing and locking where supported. Keep private register implementation in IPOS.

#### 4.4 Interface and communication requirements
Explain approved interface/protocol contracts, status and interrupt visibility, command/response
behavior and integration error handling. Preserve exact table details and provenance.

#### 4.5 Data-path and buffering requirements
Explain approved data exchanges, buffering contracts, validity and overflow/underflow behavior
at integration level. Do not promote private buffering implementation.

#### 4.6 Digital performance requirements
Describe supported timing/performance constraints, frequencies, startup/reset/wake-up behavior
and power/clock/reset relationships. Preserve all route and reset-output tables.

#### 4.7 Clock and synchronization across domains
Explain approved clock distribution, gating and synchronization contracts without inferring
implementation from labels. Preserve clock/reset, timing and upstream-reference tables.

Power/reset and operating-mode topics map to 3.1, 4.2, 4.6, 4.7 and the applicable approved
requirements in 6/9, not duplicate catalogs. Use shared low-power assembly and keep
`descriptive_low_power_audit.csv`; block-local evidence cannot establish top-level coverage.

### 5. Validation and qualification requirements

Describe supported validation/qualification, test, debug, observability and diagnostic contracts.
Retain source-topic grouping and authored requirements in their approved destination sections.

### 6. Requirement identification and traceability

Keep 6.1 Numbering convention, 6.2 Traceability contract and 6.3 residual Requirement catalog.
When present, 6.4 Source Function Context belongs here, before section 7; preserve its source
topic labels, authored statements and Covers links, including mode, test/debug and configuration topics.

### 7. Interfaces and mixed-signal interactions

Explain digital/mixed-signal exchanges, analog configuration/readout, status, calibration and
power-mode coordination where approved. Preserve all existing supporting interface tables.

### 8. Assumptions and TBD

Keep unresolved assumptions and evidence gaps distinct from approved requirements.

### 9. Top-level integration requirements

Render only approved top-digital/integration requirements here:
- shared-resource and interconnect constraints
- shared clock/reset and power coordination
- interface contracts to analog, pads, and external systems
- system-visible status, configuration, modes, errors, and firmware contracts
- integration-level sequencing, synchronization, and performance constraints

Each rendered normative entry uses `[DRS-REQ-xxx] Requirement:`, a normative top-level statement, and one `Covers: SRS-REQ-xxx` link. A matrix or structural source may be rewritten only into its approved integration constraint; preserve the exact source labels and provenance. Descriptive sentences and capability summaries may reuse Stage 1/source-spec wording without a normative `Covers` link; retain their source/provenance in the descriptive audit instead.

Digital IPOS separation is mandatory:
- Do not render detailed block-local algorithms, local state machines, private register fields, local buffering implementation, or block-private requirements in the DRS body.
- Do not copy `block_inventory.csv` Function text or Digital IPOS requirement bodies into DRS category evidence. The complete DRS traceability CSV remains available as an authoritative upstream mapping for Digital IPOS generation.
- If block behavior matters at top level, render only its shared interface, visibility, interaction, sequencing, or integration constraint.
- Detailed digital block requirements remain in the corresponding Digital IPOS specifications.

### 10. Missing Inputs

List missing supporting artifacts without fabricating replacements. Missing authority blocks generation.

## Required CSV output format

Preserve the existing traceability schema. Its initial columns are:
1. drs_req_id
2. source_req_id
3. domain
4. requirement_statement
5. owning_block
6. source_artifact
7. verification_method
8. acceptance_criteria
9. status
10. notes

Retain all existing snapshot/allocation/lineage/ownership columns after these fields; this pilot
must not remove metadata or change traceability rows.

## Stage DRS report format

stage_drs_report.md must contain:
- DRS generation status (pass or fail)
- input artifact coverage summary
- count of generated DRS requirements by domain
- count of requirements with full traceability
- open TBD and assumptions list
- blocking issues list

## Final quality checklist

Before finalizing outputs, confirm:
- all requirement statements use normative wording
- all requirements have verification method and acceptance criteria
- all requirements map to at least one source artifact
- cross-domain interactions are explicitly captured
- unresolved ambiguity is marked and tracked
