# System Requirements Specification {#system-requirements-specification}

## STBIO {#project-name}

Author: Alessandro Lucio IANNUZZI

<p>&nbsp;</p>

Date: 2026-10-07

<p>&nbsp;</p>

Snapshot ID: snap-b2e8101b00dc6909feaed885

<p>&nbsp;</p>

Downstream contract fingerprint: 8d22eb86b9a584c32e1fedacf6d98a199b8f93896143054eb1c8b2075b0ea372

<p>&nbsp;</p>

Source specification: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/Deterministic_Reqs_workflow/specs/DDS_STBIO1.pdf

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
  - [10.1 Descriptive content review findings](#101-descriptive-content-review-findings)
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
| 10.1 Descriptive content review findings | 10.1 | [Jump](#101-descriptive-content-review-findings) | Auto |

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
| 1.1 | 2026-10-06 | Snapshot snap-b2e8101b00dc6909feaed885 SRS baseline generated from Stage 1 and Stage 2 artifacts | Alessandro Lucio IANNUZZI |

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

This document presents the system-level requirements and supporting context for STBIO included in the selected approved baseline. Descriptive content does not add requirements or change their allocation.

<p>&nbsp;</p>

### 1.2 Scope {#12-scope}

The scope is limited to system-level requirements allocated to this document and the supporting system context. Analog and digital behavior, interfaces, operating conditions and verification information are described only to the extent supported by the approved content. This description does not extend subsystem or block-level allocations.

<p>&nbsp;</p>

### 1.3 Intended audience {#13-intended-audience}

This document is intended for system architects, analog and digital design engineers, firmware engineers, verification and validation engineers, test and product engineers, and program and customer stakeholders.

<p>&nbsp;</p>

### 1.4 References {#14-references}

Reference documents are listed in Table 2. Source links for any included requirements are recorded in the associated traceability matrix. Listing a document or standard does not itself establish applicability or add obligations.

<p>&nbsp;</p>

## 2. Definitions and terminology {#2-definitions-and-terminology}

### 2.1 System terminology {#21-system-terminology}

These definitions aid interpretation of the system descriptions and document abbreviations. They do not establish capabilities, ownership or allocation; specific meanings follow the approved content.

**System:** The device or functional scope identified in the approved descriptions.

**Subsystem:** A grouping of related functions identified in the approved architecture context.

**Block:** A concrete unit identified in the approved architecture context.

**SRS:** System Requirements Specification; the system-level requirements and context document.

**ARS:** Analog Requirements Specification; the analog and mixed-signal integration document.

**DRS:** Digital Requirements Specification; the digital integration document.

**IPOS:** The block-local implementation requirements specification.

### 2.2 Analog terminology {#22-analog-terminology}

Analog terms are descriptive. Ranges, operating conditions and performance limits are those stated in the applicable approved content.

**Input/output range:** The span of input or output values considered under stated operating conditions.

**Gain:** The ratio of a change in output to the corresponding change in input.

**Offset:** The deviation from the specified reference response at a reference input.

**Noise:** Unwanted variations superimposed on a signal or measurement.

**Bandwidth:** The frequency interval over which a response meets a defined criterion.

**Full-scale:** The reference magnitude or span corresponding to the specified measurement range.

**ODR:** Output data rate; the rate at which new output samples become available.

**Sensitivity:** The change in output per unit change in the measured quantity.

### 2.3 Digital terminology {#23-digital-terminology}

Digital terms aid interpretation of configuration and control descriptions. Their inclusion does not imply a particular implementation or supported feature.

**Register:** A named storage element used to expose data, configuration or status.

**Bit field:** A defined subset of bits within a register or data word.

**Mode:** An operating configuration described in the applicable content.

**State:** A condition of control logic identified within a described operating sequence.

**Reset:** Initialization of affected logic as described in the applicable content.

**Interrupt:** An event notification that requests attention from a controller or processor.

**Boot sequence:** An initialization sequence described in the applicable content.

**Interface:** A defined boundary through which components exchange data, control or status.

### 2.4 Measurement and acceptance terms {#24-measurement-and-acceptance-terms}

Measurement terms aid interpretation of verification information. Test conditions, limits and acceptance criteria remain those specified in the applicable approved requirements.

**RMS noise:** The root-mean-square amplitude of noise over a stated measurement interval and bandwidth.

**SNR:** Signal-to-noise ratio; the ratio of signal power to noise power, commonly expressed in decibels.

**Latency:** The elapsed time between a defined initiating event and its corresponding response.

**Precision:** The repeatability of measurement results under stated conditions.

**Tolerance:** A permitted deviation where specified relative to a reference value or condition.

**GR&R:** Gage repeatability and reproducibility; the evaluation of measurement-system variation.

**Guard band:** A margin between acceptance and specification limits where such a margin is specified.

**Pass/fail:** An assessment against acceptance criteria specified by the applicable requirements.

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

The system can acquire external sensor measurements through I2C master protocol with data collection and embedded processing of external measurements.

<p>&nbsp;</p>

The system provides collected external sensor measurements for sensor-fusion processing.

<p>&nbsp;</p>

The system provides the real and the imaginary parts of the body and the breathing impedance.

<p>&nbsp;</p>

The system supports body impedance and human breathing measurements with a configurable excitation path and measurement path.

<p>&nbsp;</p>

The system supports ECG measurement.

<p>&nbsp;</p>

### 3.3 Main Architectural Domains and Subsystems {#33-main-architectural-domains-and-subsystems}

- **Sensing and measurement**
  - The measurement paths support ECG measurement.
  - The measurement paths support body impedance and human breathing measurements with a configurable excitation path and measurement path.
- **External acquisition and data handling**
  - The acquisition and data paths can acquire external sensor measurements through I2C master protocol with data collection and embedded processing of external measurements.
  - The acquisition and data paths provide collected external sensor measurements for sensor-fusion processing.
  - The acquisition and data paths provide the real and the imaginary parts of the body and the breathing impedance.
- **Embedded processing**
  - In Normal Mode, the processing function processes ECG, BIA or GSR measurements.

### 3.4 External Interfaces and System Boundaries {#34-external-interfaces-and-system-boundaries}

The interfaces provide sensing input, measurement data exchange, serial communication, interrupt reporting and power supply roles. External versus internal placement is not specified for every interface.

| Boundary role | Direction | Medium |
|---|---|---|
| Sensing input | input | analog |
| Measurement data exchange | output | digital |
| Serial communication | input, bidirectional, output | digital |
| Interrupt reporting | output | digital |
| Power supply | input | power |

<p>&nbsp;</p>

### 3.5 Operating Concept {#35-operating-concept}

- **Data Storage Mode**
  - In Data Storage Mode, the system acquires ECG and BIA measurements, averages the samples and stores the sampled data.
  - In Data Storage Mode, the system acquires GSR measurements and stores the raw sampled data.
  - In Data Storage Mode, the system acquires PPG measurements, averages the samples according to the user's configuration and stores the sampled data.
- **Normal Mode**
  - In Normal Mode, the system acquires ECG, BIA or GSR measurements, averages the samples and stores the sampled data.
  - In Normal Mode, the system processes ECG, BIA or GSR measurements.

### 3.6 Power, Clock, and Reset Overview {#36-power-clock-and-reset-overview}

An always-on domain remains powered.

<p>&nbsp;</p>

A switchable domain can enter a powered-down state in idle when its associated logic is not in use.

<p>&nbsp;</p>

State retention across system power transitions is not specified.

| Domain | Type | Control | Functional Role | Power Conditions |
|---|---|---|---|---|
| PD_TOP1V2 | Always-On | HW | Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub acquisition, FIFO read and write data, Elaboration Mode with ADSP only). Associated blocks: ADSP, multi_channel_fifo, i2c_spi_slave, main_controller_top, senshub_mst_i2c, pad_mux, pmu, stbio1_regmap, scan_out_mux, xbar_afe | Always active. Never powered down |
| PD_STREDL | Switchable | SW | Powers the STREDL core and associated cache. Associated blocks: STREDL | Can be powered down in idle. Can be powered down when STREDL is not in use |
| PD_TOP3V3 | Always-On | HW | power supply to the OTP memory block. Associated blocks: H9A_MEM_OTP_ PUMP_85AL05_2 | Always active. Never powered down. It provides 4.7V of power supply to the OTP memory block during programming (write) operations |
| PD_TOPIO | Always-On | HW | Powers communication PAD. Associated blocks: level_shifter_sel | Never powered down |

<p>&nbsp;</p>

- **Clock and reset**
  - Top-level clock and reset coordination are not specified.

### 3.7 Assumptions, Scope Limits, and Allocation Boundaries {#37-assumptions-scope-limits-and-allocation-boundaries}

System-level scope covers product capabilities and externally observable behavior. Subsystem implementation remains within its engineering allocation.

- **Assumptions**
  - Additional system-level assumptions are not described in the available descriptions.

## 4. Analog sub-system {#4-analog-sub-system}

### 4.1 Analog block list {#41-analog-block-list}

No analog block catalog entries have a resolved classification in the selected architecture context.

<p>&nbsp;</p>

### 4.2 Analog I/O characteristics {#42-analog-io-characteristics}

### 4.3 Sampling and conversion {#43-sampling-and-conversion}

### 4.4 Analog operating modes {#44-analog-operating-modes}

### 4.5 Analog calibration {#45-analog-calibration}

### 4.6 Analog performance {#46-analog-performance}

## 5. Digital sub-system {#5-digital-sub-system}

### 5.1 Digital block list {#51-digital-block-list}

- **Sensor-Hub**

  The Sensor-Hub block is designed to operate the Sensor Hub I2C master for external targets, including trigger/control, pad enable, data collection, and FIFO multi-mode coordination.

- **ADSP**

  The ADSP block is designed to execute ADSP firmware for OTP boot/write/test and signal elaboration, using mapped program/data/register memory and soft-reset handling.

- **Main Controller**

  The Main Controller block is designed to generate and receive Analog Domain control signals, perform DSP elaboration on ADC outputs, and write elaborated results to the defined addresses.

- **Smart FIFO**

  The Smart FIFO block is designed to provide FIFO storage and AHB/memory access in mutually exclusive Unique or Multiple modes, including sub-FIFO depth/addressing and tagged Sensor Hub data formatting.

- **Regmap**

  The Regmap block is designed to implement the mapped AFE, system, and OTP registers, exposing configuration/status while enforcing reset and OTP write-protection rules.

- **PMU**

  The PMU block is designed to sequence POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clocks, clock-ready signaling, and digital-reset release for boot and power modes.

- **I2C_SPI_AHB**

  The I2C_SPI_AHB block is designed to accept I2C/SPI accesses and translate them as needed into AHB transactions for device configuration and readback, including ISPU access.

- **OTP**

  The OTP block is designed to provide the source-specified one-time-programmable memory interface used by ADSP boot, programming, and test routines.

<p>&nbsp;</p>

### 5.2 Control and register requirements {#52-control-and-register-requirements}

### 5.3 Mode control requirements {#53-mode-control-requirements}

### 5.4 Communication requirements {#54-communication-requirements}

### 5.5 Digital timing requirements {#55-digital-timing-requirements}

### 5.6 Digital data-path requirements {#56-digital-data-path-requirements}

Digital data-path requirements shall state the conditions for full, empty, overflow, underflow, throughput limits, and backpressure, including the involved blocks and required response.

<p>&nbsp;</p>

Data-path conditions and involved blocks:

- Main Controller -> Smart FIFO via sample stream and FIFO mode control (trigger: FIFO enabled)
- Smart FIFO -> IRQ logic via watermark/overrun/empty flags (trigger: FIFO status change)
- Main Controller -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- ADSP -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- I2C_SPI_AHB -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- SENSOR HUB -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- ISPU -> FIFO via XBAR connection (trigger: XBAR matrix cell)
- ISPU debug -> FIFO via XBAR connection (trigger: XBAR matrix cell)
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

Supply-domain functions and operating conditions are described in [section 3.6](#36-power-clock-and-reset-overview).

<p>&nbsp;</p>

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

### 10.1 Descriptive content review findings {#101-descriptive-content-review-findings}

- SRS_CATALOG_CLASSIFICATION_MISSING: IRQ logic
- SRS_CATALOG_CLASSIFICATION_MISSING: BIST Controller
- SRS_CATALOG_CLASSIFICATION_CONFLICT: PAD MUX
- SRS_CATALOG_APPROVAL_MISSING: ISPU
- SRS_POWER_VOLTAGE_UNRELIABLE: Stage 1 OCR power-domain table/description (PD_TOP3V3): 3A
- SRS_POWER_NOTE_UNREADABLE: Stage 1 OCR power-domain table/description (PD_TOPIO): Always active 32 10.4

