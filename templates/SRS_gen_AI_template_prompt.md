# SRS Generation Template Prompt

Use this template to generate a project-specific SRS (System Requirements Specification) document for a mixed-signal device after micro-architectural analysis is completed.

## Objective

Generate a complete, review-ready SRS document that is:
- structured
- traceable
- unambiguous
- verification-oriented
- aligned with project artifacts

## Required input artifacts

Read and use these artifacts before generating the SRS:
- `artifacts/stage1_requirements/requirements_summary.csv`
- `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
- `artifacts/stage2_mirco_arc/micro_architecture_report.md`
- `artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv`
- `artifacts/stage2_mirco_arc/block_inventory.csv`
- `artifacts/stage2_mirco_arc/interface_catalog.csv`
- `artifacts/stage2_mirco_arc/interaction_matrix.csv`
- `artifacts/stage2_mirco_arc/architecture_crosscheck_report.md`
- `config/project_context.json`

If any required artifact is missing, report it under an explicit "Missing Inputs" section and continue using available evidence.

## Generation rules

1. Preserve requirement traceability:
	- Keep original requirement IDs where available.
	- Do not rewrite source IDs into new unrelated IDs.
	- For newly authored SRS requirements that reference upstream IDs via `Covers`, start each atomic entry with `[SRS-REQ-xxx] Requirement:`.
	- In project-specific block sections, split mapped behavior into atomic entries.
	- For each atomic entry, use one-to-one traceability as `Covers: <single upstream requirement ID>`.
2. Use normative language:
	- Requirement statements must use "shall".
3. Keep facts and assumptions separated:
	- Mark assumptions as `ASSUME-<NNN>`.
4. Do not invent unsupported behavior:
	- If evidence is weak, mark as `TBD` with rationale.
5. Provide verification hooks:
	- Each requirement must include verification method and acceptance criteria.
6. Keep terminology consistent with project artifacts.
7. Group system requirements by argument-related paragraphs; do not collapse all system requirements into a single paragraph.
8. Keep the requirement catalog residual-only: requirements already mapped in project-specific block sections shall not be repeated in the general catalog.
9. Add a `0. Document Navigation` section with table of contents, internal paragraph index, document control tables, and table of tables.
10. Table numbering must start at `Table 1` and remain sequential.
11. Internal indexes must include project-specific sub-block paragraph entries (for example `9.x` entries such as `SerialSPI` or `SerialI2C`).
12. Formatting reference baseline:
	- Use `templates/MPT_IPOS_template.docx` as the primary style reference for table of contents structure, internal indexes, and table formatting conventions.
	- Even when generating Markdown first, keep section ordering, navigation tables, and table layout aligned with that reference template.
13. Page formatting parity (template-aligned):
	- Mirror the same document-control presentation style used by the template for navigation and control tables.
	- Keep heading hierarchy, section titling style, and table caption/number style consistent across the document.
	- Use consistent table column naming and ordering conventions for similar table types.
14. Category Convention:
	- Render `2.5 Category Convention` with the same four literal definitions and order as the DRS `2.1 Conventions` section: Comment, Definition, Assumption, Requirement.
	- Keep the four definitions as descriptive document convention text, not as requirement-generation or classification rules.
	- Keep `Table 6. Category convention` in document control as the separate SRS authored/source ID-family table; do not replace the four definitions with that table.
15. Connection Matrix requirements:
	- When a source artifact contains a `Source`-row/`Destination`-column connection matrix, inspect each populated cross-cell.
	- Use the exact source-row and destination-column labels from the matrix; do not invent, alias, normalize, or substitute block names.
	- Rewrite each populated cell as `The <Source label> block shall be connected to the <Destination label> block.` and keep all cell requirement IDs only in `Covers:`.

## Required output artifacts

Generate:
- `artifacts/stage3_srs/system_requirements_specification.md`
- `artifacts/stage3_srs/srs_traceability_matrix.csv`
- `artifacts/orchestrator/stage_srs_report.md`

## SRS document format

Use the following structure.

### Title page

Place these fields below the `System Requirements Specification` title, following the first-page presentation convention in `templates/MPT_IPOS_template.docx`:
- Project subtitle: the configured `<project_name>` value from the common `config/project_context.json` file.
- Author: the current Windows user's full display name, resolved at generation time.
- Date and source specification.

### 0. Document Navigation

#### 0.1 Table of contents
Provide internal markdown links to all top-level sections.

#### 0.2 Internal index for paragraphs and pages
Include section/paragraph navigation tables and block navigation tables with links.

#### 0.3 Document control
Include a version history table and a reference documents table.

#### 0.4 Table of tables
List all tables with links.

### 1. Introduction

Apply the frozen SRS introductory writing rule `srs-introductory-authority-bounded-v1` from the shared general rules and `SRS_INTRODUCTORY_WRITING_RULE` in `scripts/workflow_routing.py`. Use concise professional prose bounded by the selected approved content, without extending coverage, allocation, performance or implementation claims. Terminology is descriptive context, not independent authority. This preference is SRS-specific and does not alter other document profiles.

#### 1.1 Purpose
Present the document purpose and included approved system-level requirements/context; do not promise completeness or create allocation.

#### 1.2 Scope
State the limits of this document's allocated system-level requirements and supported system context. Mention behavior, interfaces, operating conditions and verification information only to the extent supported by approved content; do not extend subsystem or block-level allocations.

#### 1.3 Intended audience
List relevant stakeholders (architecture, design, verification, test, product, customer).

#### 1.4 References
Refer to existing document-control references and requirement traceability; listing a document or standard does not establish applicability or obligations.

### 2. Definitions and terminology

Use the same frozen SRS introductory writing rule. Definitions aid interpretation; specific meanings, operating conditions, limits and acceptance criteria remain bounded by approved content. Do not infer supported features, implementation, ownership or coverage from glossary entries. Keep the existing literal category conventions unchanged.

#### 2.1 System terminology
Describe system and document terms; project-specific meanings require support in the approved content.

#### 2.2 Analog terminology
Define analog terms (input/output range, gain, offset, noise, bandwidth, full-scale, ODR, sensitivity).

#### 2.3 Digital terminology
Define digital terms (register, bit field, mode, state, reset, interrupt, boot sequence, interface).

#### 2.4 Measurement and acceptance terms
Define terms such as RMS noise, SNR, latency, precision, tolerance, GR&R, guard band, pass/fail.

#### 2.5 Category Convention
Render this section with the shared four literal definitions used by DRS `2.1 Conventions`, in this order: Comment, Definition, Assumption, Requirement. These definitions are document convention text only; they are not classification or requirement-generation rules.


## 3. System Overview

Use the shared deterministic fact-to-prose core and the explicit SRS system/architecture profile for supported constructions. Aggregate compatible factual relationships only; retain modal strength, polarity, alternatives, conditions, mode and functional qualifiers. Record all contributors and unsupported projection gaps in the descriptive audit, never in the technical prose. Check selected facts against final Markdown and DOCX independently. Do not use an LLM or infer authority from vocabulary; identity, interface and scope projections retain their existing scoped rules.

### 3.1 General System Description
Describe the product or system itself and its explicitly supported application role; do not describe the purpose of this document. Use natural system-level prose and do not infer an application role.

### 3.2 Main System Capabilities
Summarize top-level capabilities only. Exclude implementation detail, registers, signals, data-name lists, block-local descriptions, and copied normative requirement text.

### 3.3 Main Architectural Domains and Subsystems
Aggregate supported functions into top-level domains or subsystems. Do not produce a block inventory or infer a domain role from the presence of blocks, ports, signals, or connections.

### 3.4 External Interfaces and System Boundaries
Explain the system boundary and supported external or cross-domain interface roles. A table may support that explanation but must not become a raw port/interface dump or imply behavior from interface presence alone.

### 3.5 Operating Concept
Explain the system role of supported operating modes and transitions. Mode names alone are not an operating concept; do not promote block-local states.

### 3.6 Power, Clock, and Reset Overview
Describe only safe top-level power, clock, and reset structure supported by clean evidence. Keep unsupported facets as narrow technical gaps; do not infer behavior from route or signal presence.

### 3.7 Assumptions, Scope Limits, and Allocation Boundaries
State engineering scope, supported assumptions, and allocation boundaries. Do not use generator disclaimers or audit language; identify only the specific unsupported technical points and do not change allocation authority.

Use prose before supporting tables. Keep each section focused on its role and deduplicate meaning across sections. For repeated structured items, bold the item name and place its attributes on indented sub-items. Do not render OCR fragments, table/path dumps, raw source stitching, or evidence counts. Consider all scoped candidates before treating a section as unsupported; a topic/output limit alone is not authority absence. Keep descriptive provenance in audit artifacts and normative traceability in its approved artifacts. Do not use parallel-document authority unless the approved workflow contract explicitly allows it.

### 4. Analog sub-system

#### 4.1 Analog block list
List the project-dependent analog block names from the current architecture-analysis block inventory as standard Markdown bullets, one block per line; generic block names in this template are rules, not output values.

#### 4.2 Analog I/O characteristics
Define ranges, linearity, noise, bandwidth, saturation, settling, and constraints per block.

#### 4.3 Sampling and conversion
Define ODR, conversion latency, synchronization, filtering, and resolution expectations.

#### 4.4 Analog operating modes
Define normal, low-power, high-performance, calibration, test, and shutdown behavior.

#### 4.5 Analog calibration
Define offset/gain calibration, compensation, and self-test behavior if applicable.

#### 4.6 Analog performance
Define noise, distortion, sensitivity, drift, crosstalk, and PSRR/CMRR requirements as applicable.

### 5. Digital sub-system

#### 5.1 Digital block list
List the project-dependent digital block names from the current architecture-analysis block inventory as standard Markdown bullets, one block per line; generic block names in this template are rules, not output values.

#### 5.2 Control and register requirements
Define register model, reset defaults, access policy, reserved bit behavior, and boot defaults.

#### 5.3 Mode control requirements
Define mode select/switch/retention behavior, transitions, and debug access constraints.

#### 5.4 Communication requirements
Define protocol-level behavior for applicable interfaces (for example UART, I2C, SPI).

#### 5.5 Digital timing requirements
Define clocking, setup/hold, propagation, response, interrupt latency, and synchronization.

#### 5.6 Digital data-path requirements
Define data format, alignment, buffering/FIFO, overflow/underflow, and framing rules.

### 6. Cross-domain mixed-signal requirements

#### 6.1 Analog-digital interactions
Define enable/disable controls, measurement triggers, update timing, data-ready signaling, and calibration control.

#### 6.2 Transition behavior across domains
Define data retention/flush behavior and accessibility during mode transitions.

#### 6.3 Clock and synchronization across domains
Define source dependencies, sample alignment, timestamping, and reset synchronization.

#### 6.4 Power sequencing across domains
Define startup ordering, brownout handling, reset dependencies, and shutdown ordering.

### 7. Validation and qualification requirements

#### 7.1 Verification scope
Define simulation, emulation, silicon validation, characterization, final test, qualification scope.

#### 7.2 Pass/fail criteria
Define thresholds, tolerance bands, confidence/population criteria, and acceptance rules.

#### 7.3 GR&R and guard band
Define GR&R expectations, uncertainty handling, and guard-banding approach.

#### 7.4 Validation configurations
Define approved modes/settings/conditions for validation execution.

### 8. Requirement identification and traceability

#### 8.1 Numbering convention
Use consistent IDs, for example:
- `SYS-RQ-001`
- `ANA-RQ-001`
- `DIG-RQ-001`
- `XDN-RQ-001`
- `SRS-REQ-001` (for newly authored SRS requirements that include `Covers` links)

#### 8.2 Traceability contract
For each requirement include:
- ID
- statement
- rationale
- source
- verification method
- acceptance criteria
- owning block(s)

#### 8.3 Residual requirement catalog by domain
List only residual requirements not already represented in project-specific atomic sub-block requirement entries.

### 9. Project-specific block sections

#### 9.1 Analog block details
One subsection per analog block with:
- general functional description (copy the matching `block_inventory.csv` `Function` field exactly; do not paraphrase or derive it from requirements)
- requirement ownership (place a non-matrix requirement under a block only when its behavior is supported by that block's `Function`; do not use source headings, source-specific tags, signal/IP names, broad mappings, or `Linked requirements` lists)
- inputs (plain field line, no bullet prefix)
- outputs (plain field line, no bullet prefix)
- function
- interfaces
- modes
- electrical/timing/performance constraints
- verification method
- atomic requirement entries: `[SRS-REQ-xxx] Requirement:`, followed directly by `The <BlockName> block shall implement: <original requirement statement>.`, the complete original bullet list when present, `Covers: <single upstream requirement ID>` when available, a blank line, and `[End]`

#### 9.2 Digital block details
One subsection per digital block with:
- general functional description (copy the matching `block_inventory.csv` `Function` field exactly; do not paraphrase or derive it from requirements)
- requirement ownership (place a non-matrix requirement under a block only when its behavior is supported by that block's `Function`; do not use source headings, source-specific tags, signal/IP names, broad mappings, or `Linked requirements` lists)
- inputs (plain field line, no bullet prefix)
- outputs (plain field line, no bullet prefix)
- function
- state machine/control model
- register/interface model
- timing/performance constraints
- verification method
- Keep a lead requirement plus its bullets as one atomic entry; do not create separate SRS-REQ headers for bullet items, and do not place upstream IDs in the statement.

Readability rule:
- add one additional empty line after each `Covers: <single upstream requirement ID>` line.

## Required CSV output format

`srs_traceability_matrix.csv` must contain these columns in this exact order:

1. `srs_req_id`
2. `source_req_id`
3. `domain`
4. `requirement_statement`
5. `owning_block`
6. `source_artifact`
7. `verification_method`
8. `acceptance_criteria`
9. `status`
10. `notes`

## Stage SRS report format

`stage_srs_report.md` must contain:
- SRS generation status (`pass` or `fail`)
- input artifact coverage summary
- count of generated SRS requirements by domain
- count of requirements with full traceability
- open TBD/assumptions list
- blocking issues list

## Final quality checklist

Before finalizing outputs, confirm:
- all requirement statements use normative wording
- all requirements have verification method and acceptance criteria
- all requirements map to at least one source artifact
- cross-domain interactions are explicitly captured
- unresolved ambiguity is marked and tracked
