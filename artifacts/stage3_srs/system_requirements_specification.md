# System Requirements Specification {#system-requirements-specification}

## STBIO {#project-name}

Author: Alessandro Lucio IANNUZZI

<p>&nbsp;</p>

Date: 2026-10-01

<p>&nbsp;</p>

Snapshot ID: snap-b2e8101b00dc6909feaed885

<p>&nbsp;</p>

Downstream contract fingerprint: 5424834735474f3f97ba3357e63e8703bd7f341f5995c19ba9e75bcba49d8157

<p>&nbsp;</p>

Source specification: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf

<p>&nbsp;</p>

## 0. Document Navigation {#0-document-navigation}

### 0.1 Table of contents {#01-table-of-contents}

- [STBIO](#project-name)
- [0. Document Navigation](#0-document-navigation)
- [1. Introduction](#1-introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Scope](#12-scope)
  - [1.3 Intended audience](#13-intended-audience)
  - [1.4 References](#14-references)
- [2. Definitions and terminology](#2-definitions-and-terminology)
  - [2.1 System terminology](#21-system-terminology)
  - [2.2 Analog terminology](#22-analog-terminology)
  - [2.3 Digital terminology](#23-digital-terminology)
  - [2.4 Measurement and acceptance terms](#24-measurement-and-acceptance-terms)
  - [2.5 Category Convention](#25-category-convention)
    - [2.5.1 Comment](#251-comment)
    - [2.5.2 Definition](#252-definition)
    - [2.5.3 Assumption](#253-assumption)
    - [2.5.4 Requirement](#254-requirement)
- [3. System Overview](#3-system-overview)
  - [3.1 General System Description](#31-general-system-description)
  - [3.2 Main System Capabilities](#32-main-system-capabilities)
  - [3.3 Main Architectural Domains and Subsystems](#33-main-architectural-domains-and-subsystems)
  - [3.4 External Interfaces and System Boundaries](#34-external-interfaces-and-system-boundaries)
  - [3.5 Operating Concept](#35-operating-concept)
  - [3.6 Power, Clock, and Reset Overview](#36-power-clock-and-reset-overview)
  - [3.7 Assumptions, Scope Limits, and Allocation Boundaries](#37-assumptions-scope-limits-and-allocation-boundaries)
- [4. Analog sub-system](#4-analog-sub-system)
  - [4.1 Analog block list](#41-analog-block-list)
  - [4.2 Analog I/O characteristics](#42-analog-io-characteristics)
  - [4.3 Sampling and conversion](#43-sampling-and-conversion)
  - [4.4 Analog operating modes](#44-analog-operating-modes)
  - [4.5 Analog calibration](#45-analog-calibration)
  - [4.6 Analog performance](#46-analog-performance)
- [5. Digital sub-system](#5-digital-sub-system)
  - [5.1 Digital block list](#51-digital-block-list)
  - [5.2 Control and register requirements](#52-control-and-register-requirements)
  - [5.3 Mode control requirements](#53-mode-control-requirements)
  - [5.4 Communication requirements](#54-communication-requirements)
  - [5.5 Digital timing requirements](#55-digital-timing-requirements)
  - [5.6 Digital data-path requirements](#56-digital-data-path-requirements)
- [6. Cross-domain mixed-signal requirements](#6-cross-domain-mixed-signal-requirements)
  - [6.1 Analog-digital interactions](#61-analog-digital-interactions)
  - [6.2 Transition behavior across domains](#62-transition-behavior-across-domains)
  - [6.3 Clock and synchronization across domains](#63-clock-and-synchronization-across-domains)
  - [6.4 Power sequencing across domains](#64-power-sequencing-across-domains)
- [7. Validation and qualification requirements](#7-validation-and-qualification-requirements)
  - [7.1 Verification scope](#71-verification-scope)
  - [7.2 Pass/fail criteria](#72-passfail-criteria)
  - [7.3 GR&R and guard band](#73-grr-and-guard-band)
  - [7.4 Validation configurations](#74-validation-configurations)
- [8. Requirement identification and traceability](#8-requirement-identification-and-traceability)
  - [8.1 Numbering convention](#81-numbering-convention)
  - [8.2 Traceability contract](#82-traceability-contract)
  - [8.3 Residual requirement catalog by domain](#83-residual-requirement-catalog-by-domain)
- [9. Project-specific block sections](#9-project-specific-block-sections)
- [10. Missing Inputs](#10-missing-inputs)
- [Assumptions and TBD](#assumptions-and-tbd)

### 0.2 Internal index for paragraphs and pages {#02-internal-index-for-paragraphs-and-pages}

#### Table 3. Section navigation index {#table-3-section-navigation-index}

| Section | Paragraph anchor | Internal link | Page (rendered PDF) |
|---|---|---|---|
| 0. Document Navigation | 0 | [Jump](#0-document-navigation) | Auto |
| 1. Introduction | 1 | [Jump](#1-introduction) | Auto |
| 1.1 Purpose | 1.1 | [Jump](#11-purpose) | Auto |
| 1.2 Scope | 1.2 | [Jump](#12-scope) | Auto |
| 1.3 Intended audience | 1.3 | [Jump](#13-intended-audience) | Auto |
| 1.4 References | 1.4 | [Jump](#14-references) | Auto |
| 2. Definitions and terminology | 2 | [Jump](#2-definitions-and-terminology) | Auto |
| 2.1 System terminology | 2.1 | [Jump](#21-system-terminology) | Auto |
| 2.2 Analog terminology | 2.2 | [Jump](#22-analog-terminology) | Auto |
| 2.3 Digital terminology | 2.3 | [Jump](#23-digital-terminology) | Auto |
| 2.4 Measurement and acceptance terms | 2.4 | [Jump](#24-measurement-and-acceptance-terms) | Auto |
| 2.5 Category Convention | 2.5 | [Jump](#25-category-convention) | Auto |
| 2.5.1 Comment | 2.5.1 | [Jump](#251-comment) | Auto |
| 2.5.2 Definition | 2.5.2 | [Jump](#252-definition) | Auto |
| 2.5.3 Assumption | 2.5.3 | [Jump](#253-assumption) | Auto |
| 2.5.4 Requirement | 2.5.4 | [Jump](#254-requirement) | Auto |
| 3. System Overview | 3 | [Jump](#3-system-overview) | Auto |
| 3.1 General System Description | 3.1 | [Jump](#31-general-system-description) | Auto |
| 3.2 Main System Capabilities | 3.2 | [Jump](#32-main-system-capabilities) | Auto |
| 3.3 Main Architectural Domains and Subsystems | 3.3 | [Jump](#33-main-architectural-domains-and-subsystems) | Auto |
| 3.4 External Interfaces and System Boundaries | 3.4 | [Jump](#34-external-interfaces-and-system-boundaries) | Auto |
| 3.5 Operating Concept | 3.5 | [Jump](#35-operating-concept) | Auto |
| 3.6 Power, Clock, and Reset Overview | 3.6 | [Jump](#36-power-clock-and-reset-overview) | Auto |
| 3.7 Assumptions, Scope Limits, and Allocation Boundaries | 3.7 | [Jump](#37-assumptions-scope-limits-and-allocation-boundaries) | Auto |
| 4. Analog sub-system | 4 | [Jump](#4-analog-sub-system) | Auto |
| 4.1 Analog block list | 4.1 | [Jump](#41-analog-block-list) | Auto |
| 4.2 Analog I/O characteristics | 4.2 | [Jump](#42-analog-io-characteristics) | Auto |
| 4.3 Sampling and conversion | 4.3 | [Jump](#43-sampling-and-conversion) | Auto |
| 4.4 Analog operating modes | 4.4 | [Jump](#44-analog-operating-modes) | Auto |
| 4.5 Analog calibration | 4.5 | [Jump](#45-analog-calibration) | Auto |
| 4.6 Analog performance | 4.6 | [Jump](#46-analog-performance) | Auto |
| 5. Digital sub-system | 5 | [Jump](#5-digital-sub-system) | Auto |
| 5.1 Digital block list | 5.1 | [Jump](#51-digital-block-list) | Auto |
| 5.2 Control and register requirements | 5.2 | [Jump](#52-control-and-register-requirements) | Auto |
| 5.3 Mode control requirements | 5.3 | [Jump](#53-mode-control-requirements) | Auto |
| 5.4 Communication requirements | 5.4 | [Jump](#54-communication-requirements) | Auto |
| 5.5 Digital timing requirements | 5.5 | [Jump](#55-digital-timing-requirements) | Auto |
| 5.6 Digital data-path requirements | 5.6 | [Jump](#56-digital-data-path-requirements) | Auto |
| 6. Cross-domain mixed-signal requirements | 6 | [Jump](#6-cross-domain-mixed-signal-requirements) | Auto |
| 6.1 Analog-digital interactions | 6.1 | [Jump](#61-analog-digital-interactions) | Auto |
| 6.2 Transition behavior across domains | 6.2 | [Jump](#62-transition-behavior-across-domains) | Auto |
| 6.3 Clock and synchronization across domains | 6.3 | [Jump](#63-clock-and-synchronization-across-domains) | Auto |
| 6.4 Power sequencing across domains | 6.4 | [Jump](#64-power-sequencing-across-domains) | Auto |
| 7. Validation and qualification requirements | 7 | [Jump](#7-validation-and-qualification-requirements) | Auto |
| 7.1 Verification scope | 7.1 | [Jump](#71-verification-scope) | Auto |
| 7.2 Pass/fail criteria | 7.2 | [Jump](#72-passfail-criteria) | Auto |
| 7.3 GR&R and guard band | 7.3 | [Jump](#73-grr-and-guard-band) | Auto |
| 7.4 Validation configurations | 7.4 | [Jump](#74-validation-configurations) | Auto |
| 8. Requirement identification and traceability | 8 | [Jump](#8-requirement-identification-and-traceability) | Auto |
| 8.1 Numbering convention | 8.1 | [Jump](#81-numbering-convention) | Auto |
| 8.2 Traceability contract | 8.2 | [Jump](#82-traceability-contract) | Auto |
| 8.3 Residual requirement catalog by domain | 8.3 | [Jump](#83-residual-requirement-catalog-by-domain) | Auto |
| 9. Project-specific block sections | 9 | [Jump](#9-project-specific-block-sections) | Auto |
| 10. Missing Inputs | 10 | [Jump](#10-missing-inputs) | Auto |

<p>&nbsp;</p>

#### Table 4. Block navigation index {#table-4-block-navigation-index}

| Block | Paragraph anchor | Internal link | Requirement IDs |
|---|---|---|---|
| N/A | N/A | N/A | N/A |

<p>&nbsp;</p>

#### Table 5. Requirement paragraph index by block {#table-5-requirement-paragraph-index-by-block}

| Requirement group | Paragraph anchor | Internal link | Page (rendered PDF) |
|---|---|---|---|
| N/A | N/A | N/A | N/A |

<p>&nbsp;</p>

### 0.3 Document control {#03-document-control}

#### Table 1. Version history {#table-1-version-history}

| Version | Date | Description | Author |
|---|---|---|---|
| 1.1 | 2026-10-01 | Snapshot snap-b2e8101b00dc6909feaed885 SRS baseline generated from Stage 1 and Stage 2 artifacts | Alessandro Lucio IANNUZZI |

<p>&nbsp;</p>

#### Table 2. Reference documents {#table-2-reference-documents}

| Doc name | Version | Author |
|---|---|---|
| artifacts/stage1_requirements/requirements_summary.csv | 0.1 | Requirements Extraction Agent |
| artifacts/stage2_mirco_arc/micro_architecture_report.md | 0.1 | Micro-Architectural Analysis Agent |
| artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv | 0.1 | Micro-Architectural Analysis Agent |
| artifacts/stage2_mirco_arc/block_inventory.csv | 0.1 | Micro-Architectural Analysis Agent |
| artifacts/stage2_mirco_arc/interface_catalog.csv | 0.1 | Micro-Architectural Analysis Agent |
| artifacts/stage2_mirco_arc/interaction_matrix.csv | 0.1 | Micro-Architectural Analysis Agent |
| templates/SRS_gen_AI_template_prompt.md | 0.1 | Project template maintainers |

<p>&nbsp;</p>

#### Table 6. Category convention {#table-6-category-convention}

| Category | Naming rule / prefix | Scope | Notes / example |
|---|---|---|---|
| System authored requirement | SRS-REQ-xxx | Project-specific SRS atomic entries | Covers one upstream requirement per row |
| Source system requirement | SYS-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |
| Source analog requirement | ANA-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |
| Source digital requirement | DIG-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |
| Cross-domain requirement | XDN-RQ-xxx or source_req_id | Upstream Stage 1 requirement catalog | Referenced through Covers linkage |

<p>&nbsp;</p>

### 0.4 Table of tables {#04-table-of-tables}

| Table | Title | Link |
|---|---|---|
| Table 1 | Section navigation index | [Go to Table 1](#table-3-section-navigation-index) |
| Table 2 | Block navigation index | [Go to Table 2](#table-4-block-navigation-index) |
| Table 3 | Requirement paragraph index by block | [Go to Table 3](#table-5-requirement-paragraph-index-by-block) |
| Table 4 | Version history | [Go to Table 4](#table-1-version-history) |
| Table 5 | Reference documents | [Go to Table 5](#table-2-reference-documents) |
| Table 6 | Category convention | [Go to Table 6](#table-6-category-convention) |

<p>&nbsp;</p>

## 1. Introduction {#1-introduction}

### 1.1 Purpose {#11-purpose}

### 1.2 Scope {#12-scope}

### 1.3 Intended audience {#13-intended-audience}

### 1.4 References {#14-references}

## 2. Definitions and terminology {#2-definitions-and-terminology}

### 2.1 System terminology {#21-system-terminology}

### 2.2 Analog terminology {#22-analog-terminology}

### 2.3 Digital terminology {#23-digital-terminology}

### 2.4 Measurement and acceptance terms {#24-measurement-and-acceptance-terms}

### 2.5 Category Convention {#25-category-convention}

<p>&nbsp;</p>

#### 2.5.1 Comment {#251-comment}

This category denotes that the content of the object text is a general comment. For example, this may be an explanation why the requirement demands certain items when there would also be other possibilities. A comment should not be necessary to understand the related requirements

<p>&nbsp;</p>

#### 2.5.2 Definition {#252-definition}

This category is used for the definition of terms, wordings, technical expressions etc. It is a documentation of design decisions and general instructions that belong to the document itself, e.g. owner of the document, structure of the document. It is needed to understand a related requirement. It is not linked to any test case.

<p>&nbsp;</p>

#### 2.5.3 Assumption {#253-assumption}

This category is used for requirements this document provide upstream to another document, indicating what this IP/block/system needs to work properly.

<p>&nbsp;</p>

#### 2.5.4 Requirement {#254-requirement}

This category denotes a requirement that has to be implemented and verified. Accordingly, it is necessary to establish traces from the different requirement levels to the test cases for this category.

<p>&nbsp;</p>

## 3. System Overview {#3-system-overview}

### 3.1 General System Description {#31-general-system-description}

The system is an analog front end with embedded processing capabilities.

<p>&nbsp;</p>

### 3.2 Main System Capabilities {#32-main-system-capabilities}

The system supports external sensor acquisition through an I2C master protocol, enabling data collection in FIFO and embedded elaboration also on external data domain.


<p>&nbsp;</p>

The ECG signal chain has several complementary features supporting ECG measurement, such as driven reference for common-mode rejection and lead off detection to identify a fallen electrode.


<p>&nbsp;</p>

The system supports body impedance and human breathing measurements with a configurable excitation path and measurement path. BIA channel delivers both the real and the imaginary parts of the body and the breathing impedance.


<p>&nbsp;</p>

This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively.


<p>&nbsp;</p>

This configuration generates each time slot, two averaged ECG data, which are ECG AC and ECG DC, respectively and four averaged BIA data which are BIA_AC_P, BIA_DC_P, BIA_AC_Q and BIA_DC_Q.


<p>&nbsp;</p>

This configuration generates each time slot, a number of PPG DATA according to user configuration.

### 3.3 Main Architectural Domains and Subsystems {#33-main-architectural-domains-and-subsystems}

The approved architecture includes a digital processing and control domain.

### 3.4 External Interfaces and System Boundaries {#34-external-interfaces-and-system-boundaries}

The approved system boundary includes analog, digital, power interface roles for sensing, communication, control, and supply exchange.

<p>&nbsp;</p>

Approved system-boundary evidence identifies the following interfaces:

| Interface | Direction | Type | Owner |
|---|---|---|---|
| SENSOR_ANALOG_INPUT | input | analog | Sensor-Hub |
| ADC_DATA | output | digital | ADC |
| FIFO_DATA | output | digital | Smart FIFO |
| SERIAL_CLK | input | digital | SPI interface |
| SERIAL_SELECT | input | digital | SPI interface |
| SERIAL_DATA_IN | input | digital | SPI interface |
| SERIAL_DATA_OUT | output | digital | SPI interface |
| ALT_SERIAL_CLK | input | digital | I2C interface |
| ALT_SERIAL_DATA | bidirectional | digital | I2C interface |
| INT1 | output | digital | IRQ logic |
| INT2 | output | digital | IRQ logic |
| VDD | input | power | PMU |
| VDD_IO | input | power | PMU |

<p>&nbsp;</p>

### 3.5 Operating Concept {#35-operating-concept}

The approved operating concept includes the following system modes: Data Storage Mode, Normal Mode.

<p>&nbsp;</p>

### 3.6 Power, Clock, and Reset Overview {#36-power-clock-and-reset-overview}

Approved evidence identifies always-on power domains that remain active for system continuity.


<p>&nbsp;</p>

Approved evidence also identifies switchable power domains that may be powered down when their associated activity is idle.


<p>&nbsp;</p>

Retention behavior is defined for preserving state across an applicable low-power transition.

### 3.7 Assumptions, Scope Limits, and Allocation Boundaries {#37-assumptions-scope-limits-and-allocation-boundaries}

The system scope covers approved sensing, processing, data exchange, operating-mode, and power-domain behavior. Detailed implementation remains outside this overview and follows the approved allocation boundaries.

<p>&nbsp;</p>

## 4. Analog sub-system {#4-analog-sub-system}

### 4.1 Analog block list {#41-analog-block-list}

Analog behavior is summarized at system level here. Detailed analog block ownership, requirements, and I/O are maintained in ARS and the corresponding analog IPOS specifications.

<p>&nbsp;</p>

### 4.2 Analog I/O characteristics {#42-analog-io-characteristics}

### 4.3 Sampling and conversion {#43-sampling-and-conversion}

### 4.4 Analog operating modes {#44-analog-operating-modes}

### 4.5 Analog calibration {#45-analog-calibration}

### 4.6 Analog performance {#46-analog-performance}

## 5. Digital sub-system {#5-digital-sub-system}

### 5.1 Digital block list {#51-digital-block-list}

Digital behavior is summarized at system level here. Detailed digital block ownership, requirements, and I/O are maintained in DRS and the corresponding digital IPOS specifications.

<p>&nbsp;</p>

Digital blocks in the approved architecture: Sensor-Hub, ADSP, Main Controller, Smart FIFO, Regmap, IRQ logic, PMU, BIST Controller, I2C_SPI_AHB, OTP, PAD MUX, ISPU.

- Sensor-Hub: Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination.
- ADSP: Execute ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling.
- Main Controller: Generate and receive Analog Domain control signals, perform DSP elaboration on ADC outputs, and write elaborated results to the defined addresses.
- Smart FIFO: Provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting.
- Regmap: Implement the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules.
- IRQ logic: Aggregate and route FIFO, Sensor Hub, ISPU sample-ready, software, and timer interrupt status to configured GPIO/interrupt outputs.
- PMU: Sequence POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clocks, clock-ready signaling, and digital-reset release for boot and power modes.
- BIST Controller: Control BIST operating modes and coordinate ADC/OTP test operations and their register-visible results.
- I2C_SPI_AHB: Accept I2C/SPI accesses and translate them as needed into AHB transactions for device configuration and readback, including ISPU access.
- OTP: Provide the source-specified one-time-programmable memory interface used by ADSP boot, programming, and test routines.
- PAD MUX: Route source-specified functional, scan, BIST, debug, and ISPU-debug signals to and from device pads.
- ISPU: Represent the ISPU digital architecture block and its source/destination responsibilities described by Stage 2 interaction evidence.

### 5.2 Control and register requirements {#52-control-and-register-requirements}

### 5.3 Mode control requirements {#53-mode-control-requirements}

### 5.4 Communication requirements {#54-communication-requirements}

### 5.5 Digital timing requirements {#55-digital-timing-requirements}

### 5.6 Digital data-path requirements {#56-digital-data-path-requirements}

Digital data-path requirements shall state the conditions for full, empty, overflow, underflow, throughput limits, and backpressure, including the involved blocks and required response.

<p>&nbsp;</p>

Data-path conditions and involved blocks:

- Sensor-Hub: Operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination.
- Smart FIFO: Provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting.
- IRQ logic: Aggregate and route FIFO, Sensor Hub, ISPU sample-ready, software, and timer interrupt status to configured GPIO/interrupt outputs.
- Main Controller -> Smart FIFO via sample stream and FIFO mode control (trigger: FIFO enabled)
- Smart FIFO -> IRQ logic via watermark/overrun/empty flags (trigger: FIFO status change)
- Main Controller -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- ADSP -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- I2C_SPI_AHB -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- Overflow: when a write arrives while storage is full, the producing and buffering blocks shall define whether the write is blocked, flagged, or otherwise handled without silent data loss.
- Underflow: when a read is requested while storage is empty, the consuming and buffering blocks shall define the returned status/data and recovery behavior.
- Throughput and backpressure: when the offered data rate exceeds the available transfer capacity, the producer, buffer, and consumer shall define flow control and recovery behavior.

## 6. Cross-domain mixed-signal requirements {#6-cross-domain-mixed-signal-requirements}

### 6.1 Analog-digital interactions {#61-analog-digital-interactions}

Cross-domain orchestration shall be implemented through interaction paths:

- ADC -> Main Controller via digital samples (trigger: sample cycle)
- Main Controller -> Smart FIFO via sample stream and FIFO mode control (trigger: FIFO enabled)
- Smart FIFO -> IRQ logic via watermark/overrun/empty flags (trigger: FIFO status change)
- Regmap -> Main Controller via configuration writes (trigger: register update)
- SPI interface -> Regmap via SPI register transactions (trigger: host SPI access)
- I2C interface -> Regmap via I2C register transactions (trigger: host I2C access)
- Regmap -> SPI interface via register read response (trigger: SPI read)
- Regmap -> I2C interface via register read response (trigger: I2C read)

### 6.2 Transition behavior across domains {#62-transition-behavior-across-domains}

### 6.3 Clock and synchronization across domains {#63-clock-and-synchronization-across-domains}

### 6.4 Power sequencing across domains {#64-power-sequencing-across-domains}

#### Power-domain architecture {#power-domain-architecture}

- Domain: PD_TOP1V2
- Included blocks: ADSP,  multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe.
- Domain type: Always-On.
- Control mode: HW.
- Notes: Always active. -.
- Functions: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). -.
- Characteristics: Never powered down. -.
- Domain: PD_STREDL
- Included blocks: STREDL.
- Domain type: Switchable.
- Control mode: SW.
- Notes: Can be powered down in idle. -.
- Functions: Powers the STREDL core and associated cache. -.
- Characteristics: Can be powered down when STREDL is not in use. -.
- Domain: PD_TOP3V3
- Included blocks: H9A_MEM_OTP_ PUMP_85AL05_2.
- Domain type: Always-On.
- Voltage: 3A.
- Control mode: HW.
- Notes: Always active. -.
- Functions: power supply to the OTP memory block. -.
- Characteristics: Never powered down. It provides 4.7V of power supply to the OTP memory block during programming (write) operations -.
- Domain: PD_TOPIO
- Included blocks: level_shifter_sel.
- Domain type: Always-On.
- Control mode: HW.
- Functions: Powers communication PAD -.
- Characteristics: Never powered down. -.

## 7. Validation and qualification requirements {#7-validation-and-qualification-requirements}

### 7.1 Verification scope {#71-verification-scope}

### 7.2 Pass/fail criteria {#72-passfail-criteria}

### 7.3 GR&R and guard band {#73-grr-and-guard-band}

### 7.4 Validation configurations {#74-validation-configurations}

## 8. Requirement identification and traceability {#8-requirement-identification-and-traceability}

### 8.1 Numbering convention {#81-numbering-convention}

### 8.2 Traceability contract {#82-traceability-contract}

### 8.3 Residual requirement catalog by domain {#83-residual-requirement-catalog-by-domain}

#### System requirements {#system-requirements}

- No residual unmapped requirements for this domain (mapped items are captured in project-specific sub-block requirement paragraphs).

#### Analog requirements {#analog-requirements}

- No residual unmapped requirements for this domain (mapped items are captured in project-specific sub-block requirement paragraphs).

#### Digital requirements {#digital-requirements}

- No residual unmapped requirements for this domain (mapped items are captured in project-specific sub-block requirement paragraphs).

#### Cross-domain requirements {#cross-domain-requirements}

- No residual unmapped requirements for this domain (mapped items are captured in project-specific sub-block requirement paragraphs).

#### Use case, user specific {#use-case-user-specific}

- None

## 9. Project-specific block sections {#9-project-specific-block-sections}

This section summarizes system-level functions and digital/analog interactions. Block-specific requirements, source I/O tables, ports, pins, clocks, and resets are owned by DRS or ARS and the corresponding IPOS specifications.

<p>&nbsp;</p>

## Assumptions and TBD {#assumptions-and-tbd}

- ASSUME-001: Verification environments include controllable stimulus for all listed operating modes.
- TBD-001: Unassigned requirements in traceability matrix need architectural owner review.

## 10. Missing Inputs {#10-missing-inputs}

- None

