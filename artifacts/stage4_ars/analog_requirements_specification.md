# Analog Requirements Specification {#analog-requirements-specification}

## STBIO {#stbio}

Author: Alessandro Lucio IANNUZZI

<p>&nbsp;</p>

Date: 2026-10-06

<p>&nbsp;</p>

Snapshot ID: snap-b2e8101b00dc6909feaed885

<p>&nbsp;</p>

Source specification: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/Deterministic_Reqs_workflow/specs/DDS_STBIO1.pdf

<p>&nbsp;</p>

## 0. Document Navigation {#0-document-navigation}

### 0.1 Table of contents {#01-table-of-contents}

- [STBIO](#stbio)
- [0. Document Navigation](#0-document-navigation)
- [1. Introduction](#1-introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Scope](#12-scope)
  - [1.3 Intended audience](#13-intended-audience)
  - [1.4 References](#14-references)
- [2. Definitions and terminology](#2-definitions-and-terminology)
- [3. System context for analog behavior](#3-system-context-for-analog-behavior)
  - [3.1 Analog Main Functions](#31-analog-main-functions)
- [4. Analog requirements](#4-analog-requirements)
  - [4.1 Analog block list](#41-analog-block-list)
  - [4.2 Analog I/O characteristics](#42-analog-io-characteristics)
  - [4.3 Sampling and conversion](#43-sampling-and-conversion)
  - [4.4 Analog operating modes](#44-analog-operating-modes)
  - [4.5 Analog calibration and test requirements](#45-analog-calibration-and-test-requirements)
  - [4.6 Analog performance requirements](#46-analog-performance-requirements)
- [5. Validation and qualification requirements](#5-validation-and-qualification-requirements)
- [6. Requirement identification and traceability](#6-requirement-identification-and-traceability)
  - [6.1 Numbering convention](#61-numbering-convention)
  - [6.2 Traceability contract](#62-traceability-contract)
  - [6.3 Requirement catalog](#63-requirement-catalog)
  - [6.4 Source Function Context](#64-source-function-context)
    - [6.4.1 Section 1 TIME SLOT LENGTH: (under Section 15.3.3 PPG Only), paragraph 010 (page 152)](#641-section-1-time-slot-length-under-section-1533-ppg-only-paragraph-010-page-152)
    - [6.4.2 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)](#642-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-017-page-34)
    - [6.4.3 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)](#643-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-018-page-34)
    - [6.4.4 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)](#644-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-019-page-34)
    - [6.4.5 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34)](#645-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-020-page-34)
    - [6.4.6 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)](#646-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-021-page-34)
    - [6.4.7 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)](#647-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-022-page-34)
    - [6.4.8 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130)](#648-section-1331-requirements-under-section-133-ispu-integration-paragraph-007-page-130)
    - [6.4.9 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130)](#649-section-1331-requirements-under-section-133-ispu-integration-paragraph-008-page-130)
    - [6.4.10 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130)](#6410-section-1331-requirements-under-section-133-ispu-integration-paragraph-009-page-130)
    - [6.4.11 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130)](#6411-section-1331-requirements-under-section-133-ispu-integration-paragraph-011-page-130)
    - [6.4.12 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130)](#6412-section-1331-requirements-under-section-133-ispu-integration-paragraph-013-page-130)
    - [6.4.13 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131)](#6413-section-1331-requirements-under-section-133-ispu-integration-paragraph-023-page-131)
    - [6.4.14 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131)](#6414-section-1331-requirements-under-section-133-ispu-integration-paragraph-027-page-131)
    - [6.4.15 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131)](#6415-section-1331-requirements-under-section-133-ispu-integration-paragraph-031-page-131)
    - [6.4.16 Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159)](#6416-section-181-scan-mode-under-section-18-digital-dft-paragraph-011-page-159)
    - [6.4.17 Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159)](#6417-section-182-debug-mode-under-section-18-digital-dft-paragraph-024-page-159)
    - [6.4.18 Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160)](#6418-section-183-adc-test-low-noise-under-section-18-digital-dft-paragraph-006-page-160)
    - [6.4.19 Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160)](#6419-section-183-adc-test-low-noise-under-section-18-digital-dft-paragraph-023-page-160)
    - [6.4.20 Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161)](#6420-section-184-adc-test-fast-under-section-18-digital-dft-paragraph-010-page-161)
    - [6.4.21 Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161)](#6421-section-185-bist-mode-under-section-18-digital-dft-paragraph-030-page-161)
    - [6.4.22 Section 2 SELECT CHANNEL: (under Section 15.3.3 PPG Only), paragraph 014 (page 152)](#6422-section-2-select-channel-under-section-1533-ppg-only-paragraph-014-page-152)
    - [6.4.23 Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: (under Section 15.3.3 PPG Only), paragraph 018 (page 152)](#6423-section-3-select-division-index-for-configured-channels-under-section-1533-ppg-only-paragraph-018-page-152)
    - [6.4.24 Section 4 CONFIGURE ADC SAMPLING PERIOD: (under Section 15.3.3 PPG Only), paragraph 022 (page 152)](#6424-section-4-configure-adc-sampling-period-under-section-1533-ppg-only-paragraph-022-page-152)
    - [6.4.25 Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152)](#6425-section-5-ppg-frames-config-under-section-1533-ppg-only-paragraph-026-page-152)
    - [6.4.26 Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153)](#6426-section-6-select-operative-mode-under-section-1533-ppg-only-paragraph-008-page-153)
    - [6.4.27 Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153)](#6427-section-7-check-data-under-section-1533-ppg-only-paragraph-011-page-153)
- [7. Project-specific analog block sections](#7-project-specific-analog-block-sections)
- [8. Assumptions and TBD](#8-assumptions-and-tbd)
- [9. Missing Inputs](#9-missing-inputs)

### 0.2 Internal index for paragraphs and pages {#02-internal-index-for-paragraphs-and-pages}

#### Table 3. Section navigation index {#table-3-section-navigation-index}

| Section | Paragraph anchor | Internal link | Page (rendered PDF) |
|---|---|---|---|
| STBIO | 0 | [Jump](#stbio) | Auto |
| 0. Document Navigation | 0 | [Jump](#0-document-navigation) | Auto |
| 1. Introduction | 1 | [Jump](#1-introduction) | Auto |
| 1.1 Purpose | 1.1 | [Jump](#11-purpose) | Auto |
| 1.2 Scope | 1.2 | [Jump](#12-scope) | Auto |
| 1.3 Intended audience | 1.3 | [Jump](#13-intended-audience) | Auto |
| 1.4 References | 1.4 | [Jump](#14-references) | Auto |
| 2. Definitions and terminology | 2 | [Jump](#2-definitions-and-terminology) | Auto |
| 3. System context for analog behavior | 3 | [Jump](#3-system-context-for-analog-behavior) | Auto |
| 3.1 Analog Main Functions | 3.1 | [Jump](#31-analog-main-functions) | Auto |
| 4. Analog requirements | 4 | [Jump](#4-analog-requirements) | Auto |
| 4.1 Analog block list | 4.1 | [Jump](#41-analog-block-list) | Auto |
| 4.2 Analog I/O characteristics | 4.2 | [Jump](#42-analog-io-characteristics) | Auto |
| 4.3 Sampling and conversion | 4.3 | [Jump](#43-sampling-and-conversion) | Auto |
| 4.4 Analog operating modes | 4.4 | [Jump](#44-analog-operating-modes) | Auto |
| 4.5 Analog calibration and test requirements | 4.5 | [Jump](#45-analog-calibration-and-test-requirements) | Auto |
| 4.6 Analog performance requirements | 4.6 | [Jump](#46-analog-performance-requirements) | Auto |
| 5. Validation and qualification requirements | 5 | [Jump](#5-validation-and-qualification-requirements) | Auto |
| 6. Requirement identification and traceability | 6 | [Jump](#6-requirement-identification-and-traceability) | Auto |
| 6.1 Numbering convention | 6.1 | [Jump](#61-numbering-convention) | Auto |
| 6.2 Traceability contract | 6.2 | [Jump](#62-traceability-contract) | Auto |
| 6.3 Requirement catalog | 6.3 | [Jump](#63-requirement-catalog) | Auto |
| 6.4 Source Function Context | 6.4 | [Jump](#64-source-function-context) | Auto |
| 6.4.1 Section 1 TIME SLOT LENGTH: (under Section 15.3.3 PPG Only), paragraph 010 (page 152) | 6.4.1 | [Jump](#641-section-1-time-slot-length-under-section-1533-ppg-only-paragraph-010-page-152) | Auto |
| 6.4.2 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34) | 6.4.2 | [Jump](#642-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-017-page-34) | Auto |
| 6.4.3 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34) | 6.4.3 | [Jump](#643-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-018-page-34) | Auto |
| 6.4.4 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34) | 6.4.4 | [Jump](#644-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-019-page-34) | Auto |
| 6.4.5 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34) | 6.4.5 | [Jump](#645-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-020-page-34) | Auto |
| 6.4.6 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34) | 6.4.6 | [Jump](#646-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-021-page-34) | Auto |
| 6.4.7 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34) | 6.4.7 | [Jump](#647-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-022-page-34) | Auto |
| 6.4.8 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130) | 6.4.8 | [Jump](#648-section-1331-requirements-under-section-133-ispu-integration-paragraph-007-page-130) | Auto |
| 6.4.9 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130) | 6.4.9 | [Jump](#649-section-1331-requirements-under-section-133-ispu-integration-paragraph-008-page-130) | Auto |
| 6.4.10 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130) | 6.4.10 | [Jump](#6410-section-1331-requirements-under-section-133-ispu-integration-paragraph-009-page-130) | Auto |
| 6.4.11 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130) | 6.4.11 | [Jump](#6411-section-1331-requirements-under-section-133-ispu-integration-paragraph-011-page-130) | Auto |
| 6.4.12 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130) | 6.4.12 | [Jump](#6412-section-1331-requirements-under-section-133-ispu-integration-paragraph-013-page-130) | Auto |
| 6.4.13 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131) | 6.4.13 | [Jump](#6413-section-1331-requirements-under-section-133-ispu-integration-paragraph-023-page-131) | Auto |
| 6.4.14 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131) | 6.4.14 | [Jump](#6414-section-1331-requirements-under-section-133-ispu-integration-paragraph-027-page-131) | Auto |
| 6.4.15 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131) | 6.4.15 | [Jump](#6415-section-1331-requirements-under-section-133-ispu-integration-paragraph-031-page-131) | Auto |
| 6.4.16 Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159) | 6.4.16 | [Jump](#6416-section-181-scan-mode-under-section-18-digital-dft-paragraph-011-page-159) | Auto |
| 6.4.17 Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159) | 6.4.17 | [Jump](#6417-section-182-debug-mode-under-section-18-digital-dft-paragraph-024-page-159) | Auto |
| 6.4.18 Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160) | 6.4.18 | [Jump](#6418-section-183-adc-test-low-noise-under-section-18-digital-dft-paragraph-006-page-160) | Auto |
| 6.4.19 Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160) | 6.4.19 | [Jump](#6419-section-183-adc-test-low-noise-under-section-18-digital-dft-paragraph-023-page-160) | Auto |
| 6.4.20 Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161) | 6.4.20 | [Jump](#6420-section-184-adc-test-fast-under-section-18-digital-dft-paragraph-010-page-161) | Auto |
| 6.4.21 Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161) | 6.4.21 | [Jump](#6421-section-185-bist-mode-under-section-18-digital-dft-paragraph-030-page-161) | Auto |
| 6.4.22 Section 2 SELECT CHANNEL: (under Section 15.3.3 PPG Only), paragraph 014 (page 152) | 6.4.22 | [Jump](#6422-section-2-select-channel-under-section-1533-ppg-only-paragraph-014-page-152) | Auto |
| 6.4.23 Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: (under Section 15.3.3 PPG Only), paragraph 018 (page 152) | 6.4.23 | [Jump](#6423-section-3-select-division-index-for-configured-channels-under-section-1533-ppg-only-paragraph-018-page-152) | Auto |
| 6.4.24 Section 4 CONFIGURE ADC SAMPLING PERIOD: (under Section 15.3.3 PPG Only), paragraph 022 (page 152) | 6.4.24 | [Jump](#6424-section-4-configure-adc-sampling-period-under-section-1533-ppg-only-paragraph-022-page-152) | Auto |
| 6.4.25 Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152) | 6.4.25 | [Jump](#6425-section-5-ppg-frames-config-under-section-1533-ppg-only-paragraph-026-page-152) | Auto |
| 6.4.26 Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153) | 6.4.26 | [Jump](#6426-section-6-select-operative-mode-under-section-1533-ppg-only-paragraph-008-page-153) | Auto |
| 6.4.27 Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153) | 6.4.27 | [Jump](#6427-section-7-check-data-under-section-1533-ppg-only-paragraph-011-page-153) | Auto |
| 7. Project-specific analog block sections | 7 | [Jump](#7-project-specific-analog-block-sections) | Auto |
| 8. Assumptions and TBD | 8 | [Jump](#8-assumptions-and-tbd) | Auto |
| 9. Missing Inputs | 9 | [Jump](#9-missing-inputs) | Auto |

<p>&nbsp;</p>

#### Table 4. Analog block navigation index {#table-4-analog-block-navigation-index}

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
| 1.1 | 2026-10-06 | Snapshot snap-b2e8101b00dc6909feaed885 ARS baseline generated from Stage 1 and Stage 2 artifacts | Alessandro Lucio IANNUZZI |

<p>&nbsp;</p>

#### Table 2. Reference documents {#table-2-reference-documents}

| Doc name | Version | Author |
|---|---|---|
| artifacts/stage3_srs/system_requirements_specification.md | 0.1 | SRS Gen Spec Agent |
| artifacts/stage1_requirements/requirements_summary.csv | 0.1 | Requirements Extraction Agent |
| artifacts/stage2_mirco_arc/micro_architecture_report.md | 0.1 | Micro-Architectural Analysis Agent |
| artifacts/stage2_mirco_arc/requirement_to_block_traceability.csv | 0.1 | Micro-Architectural Analysis Agent |
| templates/ARS_gen_AI_template_prompt.md | 0.1 | Project template maintainers |

<p>&nbsp;</p>

#### Table 6. Category convention {#table-6-category-convention}

| Category | Naming rule / prefix | Scope | Notes / example |
|---|---|---|---|
| Analog authored requirement | ARS-REQ-xxx | Project-specific ARS atomic entries | Covers one upstream requirement per row |
| Source analog/system/cross-domain requirement | source_req_id | Stage 1 source requirement catalog | Linked to authored SRS upstream ID |
| ARS upstream reference in Covers | SRS-REQ-xxx | Authored SRS requirement catalog | Required for every ARS authored requirement |

<p>&nbsp;</p>

### 0.4 Table of tables {#04-table-of-tables}

| Table | Title | Link |
|---|---|---|
| Table 1 | Version history | [Go to Table 1](#table-1-version-history) |
| Table 2 | Reference documents | [Go to Table 2](#table-2-reference-documents) |
| Table 3 | Section navigation index | [Go to Table 3](#table-3-section-navigation-index) |
| Table 4 | Analog block navigation index | [Go to Table 4](#table-4-analog-block-navigation-index) |
| Table 5 | Requirement paragraph index by block | [Go to Table 5](#table-5-requirement-paragraph-index-by-block) |
| Table 6 | Category convention | [Go to Table 6](#table-6-category-convention) |

<p>&nbsp;</p>

## 1. Introduction {#1-introduction}

### 1.1 Purpose {#11-purpose}
This document defines verifiable analog requirements derived from Stage 1 and micro-architecture artifacts.

<p>&nbsp;</p>

### 1.2 Scope {#12-scope}
This ARS covers analog subsystem behavior, analog interfaces, cross-domain dependencies, and verification hooks.

<p>&nbsp;</p>

### 1.3 Intended audience {#13-intended-audience}
Architecture, analog design, validation, and verification stakeholders.

<p>&nbsp;</p>

### 1.4 References {#14-references}
Reference documents are listed in [Table 2. Reference documents](#table-2-reference-documents).

<p>&nbsp;</p>

## 2. Definitions and terminology {#2-definitions-and-terminology}

- Analog terminology follows source requirements and micro-architecture artifacts.

## 3. System context for analog behavior {#3-system-context-for-analog-behavior}

- System context is summarized to scope analog requirements and mixed-signal interfaces.

### 3.1 Analog Main Functions {#31-analog-main-functions}

#### Sensing and signal paths {#sensing-and-signal-paths}

- Section 1 TIME SLOT LENGTH: (under Section 15.3.3 PPG Only), paragraph 010 (page 152)
- Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: (under Section 15.3.3 PPG Only), paragraph 018 (page 152)
- Section 4 CONFIGURE ADC SAMPLING PERIOD: (under Section 15.3.3 PPG Only), paragraph 022 (page 152)
- Section 2 SELECT CHANNEL: (under Section 15.3.3 PPG Only), paragraph 014 (page 152)
- Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152)
- Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153)

#### Sampling and conversion {#sampling-and-conversion}

- Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160)
- Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160)
- Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161)

#### General architecture {#general-architecture}

- Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34)
- Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34)
- Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34)
- Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34)
- Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34)
- Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34)

## 4. Analog requirements {#4-analog-requirements}

General analog requirements that are not mapped to any included analog block are listed below.

<p>&nbsp;</p>

All non-dedicated analog-relevant requirements are mapped to at least one analog block section.

<p>&nbsp;</p>

### 4.1 Analog block list {#41-analog-block-list}
Analog block list shall be derived from block inventory evidence.

<p>&nbsp;</p>

### 4.2 Analog I/O characteristics {#42-analog-io-characteristics}
Relevant analog interfaces include SENSOR_ANALOG_INPUT.

<p>&nbsp;</p>

Applicable source context tables include PMU I/O List and Sensor Hub I/O List; detailed port definitions remain in the owning Analog IPOS specification.

<p>&nbsp;</p>

Source context ports for PMU I/O List: clk_16m, clk_64k, POR1V2_1V2, START_CLK_16M, PDClockF, i_bio_divider, EN_LDO, PD_CLK_REG, EN_LDO1V8_REG, bist_mode, debug_mode, scan_mode, scan_enable, scan_clk, scan_rstn, clk_bistctlr, rst_bistctlr_n, clk_ext_en, clk_ext_slow, i_en_sh_clk, i_senshub_clk_sel, i_test_clk_fast, i_half_charge_ldo, mask_en_ldo_pdclkf, clk_en_s0, clk_en_s1, clk_en_s2_i2c, clk_en_s2_on, clk_en_s2_off, clk_en_s3, clk_en_s4, clk_en_s5, clk_en_m0, clk_en_m1, clk_en_m2, clk_en_m22, clk_en_m3, iso_i, vdden_i, i_start_operative_16MHz, main_ctrl_sw_resetn, stmc_sw_resetn, fifo_sw_resetn, masterblaze_sw_resetn, regmap_sw_resetn, adsp_run, adsp_xbar_sw_en, i_en_clk_gsr_16M, i_en_ck_m_p_q, i_en_clk_mod_debug, i_en_chop_ref, i_en_ck_chop_imp, i_en_ck_hc2_10k, i_freq_bia_m_p_q, i_en_clk_16MHz_sleep, EN_ADC_TEST_LOW_NOISE, EN_ADC_TEST_FAST, if_sh_ck_in, o_EN_LDO1V8, o_PD_CLKF, o_CLK_16M_READY, o_DIS_RC_VIREF, pd_osc_clk32k, tst_clk_32k, tst_clk_16m, tst_clk_bistctlr, tst_rst_bistctlr_n, clk_stredl, clk_xbar, clk_intf, clk_main_ctrl, clk_stmc, clk_stmc_ahb, clk_fifo, clk_masterblaze_m, clk_masterblaze_s, clk_regmap, o_clk_ext_en, resetn_stredl, resetn_xbar, resetn_intf, resetn_main_ctrl, resetn_32k_main_ctrl, resetn_stmc, resetn_fifo, resetn_masterblaze, resetn_regmap, o_trimming_clk_fast, iso_o, vdden_o, o_ck_bg, o_sh_clk, o_ck_chop_imp, o_ck_m, o_ck_hc2_10k, o_ck_p, o_ck_q, o_clk_16M_mc, o_clk_dft_adc, o_clk_gsr_16M, o_ADC_clk_serial_dft, o_sh_clk_gate.

<p>&nbsp;</p>

Source context ports for Sensor Hub I/O List: scan_mode, scan_enable, scan_rstn, HCLKM, HCLKS, sys_clk, HRESETn, DEBUG_MODE_i, scl_master_in, sda_master_in, scl_master_out, sda_master_out, dvalid_masterblaze_ext, dvalid_masterblaze_ext_enable, sleep_master, master_end_op_pulse, SH_SMARTFIFO_OCCUPATION, fifo_mode, fifo_offset, HSELS, HADDRS, HTRANSS, HSIZES, HWRITES, HREADYS, HWDATAS, HREADYOUTS, HRESPS, HRDATAS, ahb_master_on, HRDATAM, HREADYM, HRESPM, HGRANTM, HSELM, HADDRM, HTRANSM, HWRITEM, HSIZEM, HBURSTM, HPROTM, HWDATAM, HBUSREQM, HLOCKM.

<p>&nbsp;</p>

Detailed analog block inputs, outputs, ports, and source I/O tables are maintained only in the owning Analog IPOS specification.

<p>&nbsp;</p>

### 4.3 Sampling and conversion {#43-sampling-and-conversion}
Sampling, conversion, and resolution behavior shall satisfy timing and accuracy constraints from source requirements.

<p>&nbsp;</p>

### 4.4 Analog operating modes {#44-analog-operating-modes}
Analog operating behavior shall remain consistent across manual, schedule, off, and fault-degraded scenarios.

<p>&nbsp;</p>

### 4.5 Analog calibration and test requirements {#45-analog-calibration-and-test-requirements}
Calibration and observability requirements shall be defined for offset/gain handling and verification access.

<p>&nbsp;</p>

### 4.6 Analog performance requirements {#46-analog-performance-requirements}
Performance requirements shall cover noise, accuracy, range, drift, and response constraints.

<p>&nbsp;</p>

## 5. Validation and qualification requirements {#5-validation-and-qualification-requirements}

- Verification shall combine inspection, analysis, and test with measurable acceptance criteria.

## 6. Requirement identification and traceability {#6-requirement-identification-and-traceability}
### 6.1 Numbering convention {#61-numbering-convention}
ARS IDs use domain-prefixed numbering: ANA-RQ-### and XDN-RQ-###. Newly authored requirements in project-specific sub-block requirement paragraphs use ARS-REQ-###.

<p>&nbsp;</p>

### 6.2 Traceability contract {#62-traceability-contract}
ARS requirement catalog entries include statement only; full traceability details are maintained in artifacts/stage4_ars/ars_traceability_matrix.csv.

<p>&nbsp;</p>

### 6.3 Requirement catalog {#63-requirement-catalog}

#### Analog requirements {#analog-requirements}

- No residual unmapped requirements for this domain (mapped items are captured in project-specific analog sub-block requirement paragraphs).

#### Cross-domain requirements {#cross-domain-requirements}

- No residual unmapped requirements for this domain (mapped items are captured in project-specific analog sub-block requirement paragraphs).

#### Use case, user specific {#use-case-user-specific}

- None

## 7. Project-specific analog block sections {#7-project-specific-analog-block-sections}

## 6.4 Source Function Context {#64-source-function-context}

### 6.4.1 Section 1 TIME SLOT LENGTH: (under Section 15.3.3 PPG Only), paragraph 010 (page 152) {#641-section-1-time-slot-length-under-section-1533-ppg-only-paragraph-010-page-152}

### 6.4.2 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 017 (page 34) {#642-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-017-page-34}

### 6.4.3 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 018 (page 34) {#643-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-018-page-34}

### 6.4.4 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 019 (page 34) {#644-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-019-page-34}

### 6.4.5 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 020 (page 34) {#645-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-020-page-34}

### 6.4.6 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 021 (page 34) {#646-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-021-page-34}

### 6.4.7 Section 11.1 XBAR Connection Matrix (under Section 11 Interconnect), paragraph 022 (page 34) {#647-section-111-xbar-connection-matrix-under-section-11-interconnect-paragraph-022-page-34}

### 6.4.8 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 007 (page 130) {#648-section-1331-requirements-under-section-133-ispu-integration-paragraph-007-page-130}

### 6.4.9 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 008 (page 130) {#649-section-1331-requirements-under-section-133-ispu-integration-paragraph-008-page-130}

### 6.4.10 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 009 (page 130) {#6410-section-1331-requirements-under-section-133-ispu-integration-paragraph-009-page-130}

### 6.4.11 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 011 (page 130) {#6411-section-1331-requirements-under-section-133-ispu-integration-paragraph-011-page-130}

### 6.4.12 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 013 (page 130) {#6412-section-1331-requirements-under-section-133-ispu-integration-paragraph-013-page-130}

### 6.4.13 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 023 (page 131) {#6413-section-1331-requirements-under-section-133-ispu-integration-paragraph-023-page-131}

### 6.4.14 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 027 (page 131) {#6414-section-1331-requirements-under-section-133-ispu-integration-paragraph-027-page-131}

### 6.4.15 Section 13.3.1 Requirements (under Section 13.3 ISPU integration), paragraph 031 (page 131) {#6415-section-1331-requirements-under-section-133-ispu-integration-paragraph-031-page-131}

### 6.4.16 Section 18.1 Scan mode (under Section 18 Digital DFT), paragraph 011 (page 159) {#6416-section-181-scan-mode-under-section-18-digital-dft-paragraph-011-page-159}

### 6.4.17 Section 18.2 Debug mode (under Section 18 Digital DFT), paragraph 024 (page 159) {#6417-section-182-debug-mode-under-section-18-digital-dft-paragraph-024-page-159}

### 6.4.18 Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 006 (page 160) {#6418-section-183-adc-test-low-noise-under-section-18-digital-dft-paragraph-006-page-160}

### 6.4.19 Section 18.3 ADC TEST LOW NOISE (under Section 18 Digital DFT), paragraph 023 (page 160) {#6419-section-183-adc-test-low-noise-under-section-18-digital-dft-paragraph-023-page-160}

### 6.4.20 Section 18.4 ADC TEST FAST (under Section 18 Digital DFT), paragraph 010 (page 161) {#6420-section-184-adc-test-fast-under-section-18-digital-dft-paragraph-010-page-161}

### 6.4.21 Section 18.5 BIST MODE (under Section 18 Digital DFT), paragraph 030 (page 161) {#6421-section-185-bist-mode-under-section-18-digital-dft-paragraph-030-page-161}

### 6.4.22 Section 2 SELECT CHANNEL: (under Section 15.3.3 PPG Only), paragraph 014 (page 152) {#6422-section-2-select-channel-under-section-1533-ppg-only-paragraph-014-page-152}

### 6.4.23 Section 3 SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: (under Section 15.3.3 PPG Only), paragraph 018 (page 152) {#6423-section-3-select-division-index-for-configured-channels-under-section-1533-ppg-only-paragraph-018-page-152}

### 6.4.24 Section 4 CONFIGURE ADC SAMPLING PERIOD: (under Section 15.3.3 PPG Only), paragraph 022 (page 152) {#6424-section-4-configure-adc-sampling-period-under-section-1533-ppg-only-paragraph-022-page-152}

### 6.4.25 Section 5 PPG FRAMES CONFIG: (under Section 15.3.3 PPG Only), paragraph 026 (page 152) {#6425-section-5-ppg-frames-config-under-section-1533-ppg-only-paragraph-026-page-152}

### 6.4.26 Section 6 SELECT OPERATIVE MODE: (under Section 15.3.3 PPG Only), paragraph 008 (page 153) {#6426-section-6-select-operative-mode-under-section-1533-ppg-only-paragraph-008-page-153}

### 6.4.27 Section 7 CHECK DATA: (under Section 15.3.3 PPG Only), paragraph 011 (page 153) {#6427-section-7-check-data-under-section-1533-ppg-only-paragraph-011-page-153}

## 8. Assumptions and TBD {#8-assumptions-and-tbd}

- ASSUME-001: Analog validation environments provide representative sensor and load stimulus.
- TBD-001: Unassigned requirements in ARS traceability matrix require architectural owner review.

## 9. Missing Inputs {#9-missing-inputs}

- None

