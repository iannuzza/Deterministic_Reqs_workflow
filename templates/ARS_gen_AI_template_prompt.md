# ARS Generation Template Prompt

Use this template to generate a project-specific ARS (ANalog Requirements Specification) document for a mixed-signal device after micro-architectural analysis is completed.

## Objective

Generate a complete, review-ready ARS document that is:
- structured
- traceable
- unambiguous
- verification-oriented
- aligned with project artifacts

## Required input artifacts

Read and use these artifacts before generating the ARS:
- `artifacts/stage1_requirements/requirements_summary.csv`
- `artifacts/stage1_requirements/requirements_rag_crosscheck.md`
- `artifacts/stage2_micro_arch/micro_architecture_report.md`
- `artifacts/stage2_micro_arch/requirement_to_block_traceability.csv`
- `artifacts/stage2_micro_arch/block_inventory.csv`
- `artifacts/stage2_micro_arch/interface_catalog.csv`
- `artifacts/stage2_micro_arch/interaction_matrix.csv`
- `artifacts/stage2_micro_arch/architecture_crosscheck_report.md`
- `config/project_context.json`

If any required artifact is missing, report it under an explicit "Missing Inputs" section and continue using available evidence.

## Generation rules

1. Preserve requirement traceability:
	- Keep original requirement IDs where available.
	- Do not rewrite source IDs into new unrelated IDs.
	- For newly authored block-section requirements, start each atomic entry with `[ARS-REQ-xxx] Requirement:`.
	- In project-specific analog block sections, split mapped behavior into atomic entries and use one-to-one traceability as `Covers: <single upstream requirement ID>`.
2. Use normative language:
	- Requirement statements must use "shall".
3. Keep facts and assumptions separated:
	- Mark assumptions as `ASSUME-<NNN>`.
4. Do not invent unsupported behavior:
	- If evidence is weak, mark as `TBD` with rationale.
5. Provide verification hooks:
	- Each requirement must include verification method and acceptance criteria.
6. Keep terminology consistent with project artifacts.
7. Keep the general requirement catalog residual-only: requirements already mapped in project-specific block sections shall not be repeated in a separate mapped-summary subsection.
8. Add a `0. Document Navigation` section with table of contents, internal paragraph index, document control tables, and table of tables.
9. Table numbering must start at `Table 1` and remain sequential.
10. Internal indexes must include project-specific analog sub-block paragraph entries (for example `7.x` entries such as `ADCInterface`).
11. Formatting reference baseline:
	- Use `templates/MPT_IPOS_template.docx` as the primary style reference for table of contents structure, internal indexes, and table formatting conventions.
	- Even when generating Markdown first, keep section ordering, navigation tables, and table layout aligned with that reference template.
12. Page formatting parity (template-aligned):
	- Mirror the same document-control presentation style used by the template for navigation and control tables.
	- Keep heading hierarchy, section titling style, and table caption/number style consistent across the document.
	- Use consistent table column naming and ordering conventions for similar table types.
13. Category Convention tables:
	- Include explicit category-convention tables in the document navigation/control area for requirement categories and ID-family conventions used by the specification.
	- Category convention tables must define category name, naming rule/prefix, scope, and notes/example.
14. Connection Matrix requirements:
	- When a source artifact contains a `Source`-row/`Destination`-column connection matrix, inspect each populated cross-cell.
	- Use the exact source-row and destination-column labels from the matrix; do not invent, alias, normalize, or substitute block names.
	- Rewrite each populated cell as `The <Source label> block shall be connected to the <Destination label> block.` and keep all cell requirement IDs only in `Covers:`.

## Required output artifacts

Generate:
- `artifacts/stage4_ars/analog_requirements_specification.md`
- `artifacts/stagea_ars/ars_traceability_matrix.csv`
- `artifacts/orchestrator/stage_ars_report.md`

## ARS document format

Use the following structure.

### Title page

Place these fields below the `Analog Requirements Specification` title, following the first-page presentation convention in `templates/MPT_IPOS_template.docx`:
- Project subtitle: the project name from `config/project_context.json`.
- Author: the current Windows user's full display name, resolved at generation time.
- Date and source specification.

### 0. Document Navigation

#### 0.1 Table of contents
Provide internal markdown links to all top-level sections.

#### 0.2 Internal index for paragraphs and pages
Include section/paragraph navigation tables and analog block navigation tables with links.

#### 0.3 Document control
Include a version history table and a reference documents table.

#### 0.4 Table of tables
List all tables with links.

### 1. Introduction

#### 1.1 Purpose
Define the purpose of the ARS and device scope.

#### 1.2 Scope
Cover:
- system-level and anaog-level functionality
- analog subsystem behavior
- interfaces and configuration model
- power, timing, performance constraints
- validation expectations

#### 1.3 Intended audience
List relevant stakeholders (architecture, design, verification, test, product, customer).

#### 1.4 References
List all related documents:
•	system requirement specification
•	architecture specification
•	block-level specification
•	electrical specifications
•	validation plan
•	customer requirements


### 2. Definitions and terminology

#### 2.1 System terminology
Define project-specific analog terms and abbreviations.

#### 2.2 Analog terminology
Define analog terms (input/output range, gain, offset, noise, bandwidth, full-scale, ODR, sensitivity).
•	input range
•	output range
•	gain
•	offset
•	sensitivity
•	bandwidth
•	noise
•	full-scale
•	settling time
#### 2.3 Signal quality terminology
Define:
•	RMS noise
•	SNR
•	distortion
•	linearity
•	crosstalk
•	drift
•	quantization error
#### Conversion terminology
If applicable, define:
•	sampling rate
•	ODR
•	resolution
•	latency
•	conversion time
•	aliasing
•	filter response
#### Calibration terminology
Define:
•	offset calibration
•	gain calibration
•	trim
•	self-test
•	runtime calibration
•	factory calibration
•	temperature compensation

#### 2.4 Measurement and acceptance terms
Define terms such as RMS noise, SNR, latency, precision, tolerance, GR&R, guard band, pass/fail.

#### 2.5 Category Convention
### 2.5.1 Comment
This category denotes that the content of the object text is a general comment. For example, this may be an explanation why the requirement demands certain items when there would also be other possibilities. A comment should not be necessary to understand the related requirements

### 2.5.2 Definition
This category is used for the definition of terms, wordings, technical expressions etc. It is a documentation of design decisions and general instructions that belong to the document itself, e.g. owner of the document, structure of the document. It is needed to understand a related requirement. It is not linked to any test case. 

### 2.5.3 Assumption
This category is used for requirements this document provide upstream to another document, indicating what this IP/block/system needs to work properly.

### 2.5.4 Requirement
This category denotes a requirement that has to be implemented and verified. Accordingly, it is necessary to establish traces from the different requirement levels to the test cases for this category. 


### 3. System-level requirements

#### 3.1 General system description
This section is generated from current Stage 1 and Stage 2A artifacts.

#### 3.2 Operating modes
For each mode define:
- active blocks
- disabled blocks
- power target
- latency and throughput behavior
- register accessibility
- allowed transitions

#### 3.3 Power states
Define power-up, normal, low-power, standby, shutdown, and debug/factory behavior.
Use the shared project-agnostic low-power descriptive contract with analog/mixed-signal/power scope filtering. Distinguish supply and bias domains, analog power islands, sequencing, low-power entry/exit, retention, isolation, wake-up, restore, and hardware/software responsibility. Exclude unrelated generic digital or marketing power text. Write `descriptive_low_power_audit.csv` beside the ARS Markdown.

#### 3.4 System interfaces
Define supply, reset, clock, host communication, interrupt, and test interfaces.

#### 3.5 System constraints
Define environmental, electrical, timing, packaging, reliability, and safety constraints.

#### 3.6 System performance targets
Define measurable system KPIs with units and acceptance limits.

### 4. Analog requirements

#### 4.1 Analog block list
List the project-dependent analog block names from the current architecture-analysis block inventory; generic block names in this template are rules, not output values.

#### Block descriptions
For each analog block, describe:
•	purpose
•	function
•	dependencies
•	linked operating modes
•	expected behavior

### Analog functional requirements
### 4.1 Input characteristics
For each input channel, define:
•	input signal type
•	input range
•	common-mode range
•	absolute maximum ratings
•	protection requirements
### 4.2 Output characteristics
For each output path, define:
•	output signal type
•	output range
•	load conditions
•	drive capability
•	output impedance
### 4.3 Gain and offset
Each analog block shall define:
•	nominal gain
•	gain accuracy
•	gain setting options
•	offset error
•	offset drift
### 4.4 Noise and signal quality
Each analog block shall define:
•	RMS noise target
•	noise bandwidth
•	distortion limits
•	linearity targets
•	SNR target
### 4.5 Frequency response
Each analog block shall define:
•	bandwidth
•	cutoff frequency
•	filter behavior
•	roll-off
•	flatness
### 4.6 Timing requirements
Each analog block shall define:
•	startup time
•	settling time
•	response time
•	recovery time
•	mode-switch latency

### Analog configuration requirements
### Configurable analog parameters
List configurable parameters such as:
•	full-scale range
•	gain
•	bandwidth
•	filter setting
•	bias current
•	calibration trim
•	operating mode
### Configuration rules
Define:
•	valid settings
•	forbidden combinations
•	default values
•	reset values
•	update timing
#### 4.2 Analog I/O characteristics
Define ranges, linearity, noise, bandwidth, saturation, settling, and constraints per block.

#### 4.3 Sampling and conversion
Define ODR, conversion latency, synchronization, filtering, and resolution expectations.

#### 4.4 Analog operating modes
Define normal, low-power, high-performance, calibration, test, and shutdown behavior.

### Mode behavior
For each mode, define:
•	active blocks
•	inactive blocks
•	expected power consumption
•	expected noise
•	expected bandwidth
•	expected latency
•	allowed transitions
### Mode transition rules
Define:
•	what happens during mode switching
•	whether outputs are preserved
•	whether measurements are interrupted
•	whether recalibration is required
•	whether data loss is allowed

### Analog interfaces
### External analog interfaces
For each external analog interface, define:
•	pin name
•	direction
•	description
•	electrical characteristics
•	operating range
•	special constraints
### Internal analog interfaces
For each internal analog connection, define:
•	source block
•	destination block
•	signal type
•	range
•	timing dependency
•	ownership
### Analog-digital interaction
Define the relationship between analog and digital functions, including:
•	mode control
•	enable/disable control
•	calibration control
•	status reporting
•	interrupt generation

#### 4.5 Analog calibration and test requirements
Define offset/gain calibration, compensation, and self-test behavior if applicable.
### Calibration
The analog subsystem shall support:
•	factory calibration
•	runtime calibration
•	offset correction
•	gain correction
•	temperature compensation
### Test access
Define:
•	observability points
•	controllability points
•	test modes
•	debug hooks
•	self-test features
### Validation constraints
Define:
•	validated configurations
•	measurement setup
•	GR&R expectations
•	guard band rules
•	acceptance criteria

#### 4.6 Analog performance requirements
Define noise, distortion, sensitivity, drift, crosstalk, and PSRR/CMRR requirements as applicable.
### Static performance
Define:
•	offset
•	gain error
•	drift
•	sensitivity
•	supply dependence
•	temperature dependence
### Dynamic performance
Define:
•	noise
•	bandwidth
•	latency
•	distortion
•	transient response
•	settling behavior
### Environmental performance
Define performance over:
•	supply voltage range
•	temperature range
•	process corners
•	aging conditions, if required

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
- `ANA-RQ-001`
- `XDN-RQ-001`
- `ARS-REQ-001` for newly authored requirements in project-specific block sections.

#### 8.2 Traceability contract
For each requirement include:
- ID
- statement
- rationale
- source
- verification method
- acceptance criteria
- owning block(s)

### 9. Project-specific block sections

#### 9.1 Analog block details
One subsection per analog block with:
- general functional description (copy the matching `block_inventory.csv` `Function` field exactly; do not paraphrase or derive it from requirements)
- requirement ownership (place a non-matrix requirement under a block only when its behavior is supported by that block's `Function`; do not use source headings, source-specific tags, signal/IP names, broad mappings, or `Linked requirements` lists)
- inputs (plain field line, no bullet prefix)
- outputs (plain field line, no bullet prefix)
- requirement header (`[ARS-REQ-xxx] Requirement:`, plain field line)
- statement (normative, uses shall; use: `The <BlockName> block shall implement: <original requirement statement>.`)
- function
- interfaces
- modes
- electrical/timing/performance constraints
- verification method
- covers (`Covers: <single upstream requirement ID>`, plain field line); place the direct normative statement and complete original bullet list before it, without a `Statement:` label

Atomic decomposition rule:
- split each block functionality into atomic functional items
- create one `[ARS-REQ-xxx] Requirement:` header per atomic item
- each atomic item must end with `Covers: <single upstream requirement ID>` when available (one-to-one traceability), followed by a blank line and `[End]`; keep a lead plus bullets as one item and keep upstream IDs out of authored prose
- add one additional empty line after each `Covers` line for readability
- do not aggregate multiple upstream requirement IDs into one atomic item

Selection rule:
- include only analog/power/mixed-signal blocks that directly realize analog behavior
- exclude pure digital/system-control blocks from ARS block sections (for example: SerialSPI, SerialI2C, FIFOController, InterruptController, RegisterControl, HostInterface)

## Required CSV output format

`ars_traceability_matrix.csv` must contain these columns in this exact order:

1. `ars_req_id`
2. `source_req_id`
3. `domain`
4. `requirement_statement`
5. `owning_block`
6. `source_artifact`
7. `verification_method`
8. `acceptance_criteria`
9. `status`
10. `notes`

## Stage ARS report format

`stage_ars_report.md` must contain:
- ARS generation status (`pass` or `fail`)
- input artifact coverage summary
- count of generated ARS requirements by domain
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
