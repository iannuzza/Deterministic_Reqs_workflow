# **Digital IPOS - PMU** {#digital-ipos---pmu}

- Snapshot: `snap-b2e8101b00dc6909feaed885`

Author: Alessandro Lucio IANNUZZI

## **0. Document Navigation** {#0-document-navigation}

### **0.1 Table of contents** {#01-table-of-contents}
- [1. Block overview](#1-block-overview)
- [2. Source I/O](#2-source-io)
- [3. Block requirements](#3-block-requirements)

### **0.2 Document control** {#02-document-control}
#### **Table 1. Version history** {#table-1-version-history}
| Version | Date | Description | Author |
|---|---|---|---|
| 0.1 | 2026-10-01 | Snapshot snap-b2e8101b00dc6909feaed885 digital IPOS block baseline | Alessandro Lucio IANNUZZI |

### **0.3 Requirement navigation** {#03-requirement-navigation}
| Requirement | Internal link |
|---|---|
| IPOS-PMU-001 | [Go to requirement](#ipos-pmu-001) |
| IPOS-PMU-002 | [Go to requirement](#ipos-pmu-002) |
| IPOS-PMU-003 | [Go to requirement](#ipos-pmu-003) |
| IPOS-PMU-004 | [Go to requirement](#ipos-pmu-004) |
| IPOS-PMU-005 | [Go to requirement](#ipos-pmu-005) |
| IPOS-PMU-006 | [Go to requirement](#ipos-pmu-006) |
| IPOS-PMU-007 | [Go to requirement](#ipos-pmu-007) |
| IPOS-PMU-008 | [Go to requirement](#ipos-pmu-008) |
| IPOS-PMU-009 | [Go to requirement](#ipos-pmu-009) |
| IPOS-PMU-010 | [Go to requirement](#ipos-pmu-010) |
| IPOS-PMU-011 | [Go to requirement](#ipos-pmu-011) |
| IPOS-PMU-012 | [Go to requirement](#ipos-pmu-012) |
| IPOS-PMU-013 | [Go to requirement](#ipos-pmu-013) |
| IPOS-PMU-014 | [Go to requirement](#ipos-pmu-014) |
| IPOS-PMU-015 | [Go to requirement](#ipos-pmu-015) |
| IPOS-PMU-016 | [Go to requirement](#ipos-pmu-016) |
| IPOS-PMU-017 | [Go to requirement](#ipos-pmu-017) |
| IPOS-PMU-018 | [Go to requirement](#ipos-pmu-018) |
| IPOS-PMU-019 | [Go to requirement](#ipos-pmu-019) |
| IPOS-PMU-020 | [Go to requirement](#ipos-pmu-020) |
| IPOS-PMU-021 | [Go to requirement](#ipos-pmu-021) |
| IPOS-PMU-022 | [Go to requirement](#ipos-pmu-022) |
| IPOS-PMU-023 | [Go to requirement](#ipos-pmu-023) |
| IPOS-PMU-024 | [Go to requirement](#ipos-pmu-024) |
| IPOS-PMU-025 | [Go to requirement](#ipos-pmu-025) |
| IPOS-PMU-026 | [Go to requirement](#ipos-pmu-026) |
| IPOS-PMU-027 | [Go to requirement](#ipos-pmu-027) |
| IPOS-PMU-028 | [Go to requirement](#ipos-pmu-028) |
| IPOS-PMU-029 | [Go to requirement](#ipos-pmu-029) |
| IPOS-PMU-030 | [Go to requirement](#ipos-pmu-030) |
| IPOS-PMU-031 | [Go to requirement](#ipos-pmu-031) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The PMU block is designed to sequence POR-driven LDO1V8 enable, 64/32 kHz and 16 MHz clocks, clock-ready signaling, and digital-reset release for boot and power modes.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The PMU accepts VDD/VDD_IO, power-on reset, clock references, clock-start requests, power-mode configuration and produces LDO and power-domain controls, clock enable/gating and ready status, reset-release signals, power-state status.
- **Power-on start-up.** On release of POR from the analog domain, coordinates LDO1V8 turn-on and the clock start-up sequence.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| clk_16m | input | wire Clock 16 MHz from analog ring oscillators | PMU I/O List | 37 |
| clk_64k | input | wire Clock 64kHz from analog ring oscillators | PMU I/O List | 37 |
| POR1V2_1V2 | input | wire POR Signal | PMU I/O List | 37 |
| START_CLK_16M | input | wire Clock ready for 16MHz | PMU I/O List | 37 |
| PDClockF | input | wire Power Down for 16MHz Ring Oscillator from main controller | PMU I/O List | 37 |
| i_bio_divider | input | wire Enable 32kHz geneartion from 16MHz when a Bio-Channel is activated | PMU I/O List | 37 |
| EN_LDO | input | wire enable LDO from main controller | PMU I/O List | 37 |
| PD_CLK_REG | input | wire power down 16MHz from Regmap 37 | PMU I/O List | 37 |
| EN_LDO1V8_REG | input | wire Enable LDO from regmap | PMU I/O List | 38 |
| bist_mode | input | wire enable bist mode | PMU I/O List | 38 |
| debug_mode | input | wire enable debug | PMU I/O List | 38 |
| scan_mode | input | wire enable scan mode | PMU I/O List | 38 |
| scan_enable | input | wire start scan mode | PMU I/O List | 38 |
| scan_clk | input | wire scan clk | PMU I/O List | 38 |
| scan_rstn | input | wire scan rst | PMU I/O List | 38 |
| clk_bistctlr | input | wire bist controller and collar clock | PMU I/O List | 38 |
| rst_bistctlr_n | input | wire bist controller and collar resetn | PMU I/O List | 38 |
| clk_ext_en | input | wire enable external clock from pad | PMU I/O List | 38 |
| clk_ext_slow | input | wire external clock 32kHz | PMU I/O List | 38 |
| i_en_sh_clk | input | wire enable sensor hub clock | PMU I/O List | 38 |
| i_senshub_clk_sel | input | wire [2:0] selector for sensor hub clock | PMU I/O List | 38 |
| i_test_clk_fast | input | wire enable test and trimming for 16MHz clock | PMU I/O List | 38 |
| i_half_charge_ldo | input | wire enable the low power mode for ldo when only ppg is selected | PMU I/O List | 38 |
| mask_en_ldo_pdclkf | input | wire mask the control of pdf and ldo control during boot | PMU I/O List | 38 |
| clk_en_s0 | input | wire clock gating logic inside stredl_afe_top | PMU I/O List | 38 |
| clk_en_s1 | input | wire if present should be HSEL STMC AHB Master | PMU I/O List | 38 |
| clk_en_s2_i2c | input | wire if present should be HSEL STMC AHB Master | PMU I/O List | 38 |
| clk_en_s2_on | input | wire clk gating ON from AHB I2C/SPI Interface | PMU I/O List | 38 |
| clk_en_s2_off | input | wire clk gating OFF from AHB I2C/SPI Interface | PMU I/O List | 38 |
| clk_en_s3 | input | wire clk gating from AHB Master Main Controller 38 | PMU I/O List | 38 |
| clk_en_s4 | input | wire clock gating logic inside stredl_afe_top | PMU I/O List | 39 |
| clk_en_s5 | input | wire clock gating logic inside masterblaze_ahb | PMU I/O List | 39 |
| clk_en_m0 | input | wire clock gating logic inside stredl_afe_top | PMU I/O List | 39 |
| clk_en_m1 | input | wire HSEL M1 from xbar to STMC AHB Slave | PMU I/O List | 39 |
| clk_en_m2 | input | wire HSEL M2 from xbar to FIFO | PMU I/O List | 39 |
| clk_en_m22 | input | wire HSEL M2 from xbar to MASTERBLAZE | PMU I/O List | 39 |
| clk_en_m3 | input | wire HSEL M3 from xbar to Regmap | PMU I/O List | 39 |
| iso_i | input | wire from register | PMU I/O List | 39 |
| vdden_i | input | wire enable ISPU Power Island | PMU I/O List | 39 |
| i_start_operative_16MHz | input | wire enable the lead of check | PMU I/O List | 39 |
| main_ctrl_sw_resetn | input | wire soft reset for main controller | PMU I/O List | 39 |
| stmc_sw_resetn | input | wire adsp soft reset | PMU I/O List | 39 |
| fifo_sw_resetn | input | wire fifo soft reset | PMU I/O List | 39 |
| masterblaze_sw_resetn | input | wire sensor hub soft reset | PMU I/O List | 39 |
| regmap_sw_resetn | input | wire regmap soft reset | PMU I/O List | 39 |
| adsp_run | input | wire adsp is running | PMU I/O List | 39 |
| adsp_xbar_sw_en | input | wire adsp clk ahb | PMU I/O List | 39 |
| i_en_clk_gsr_16M | input | wire enable the clock for gsr digital circuit | PMU I/O List | 39 |
| i_en_ck_m_p_q | input | wire enable quadrature and phase clock | PMU I/O List | 39 |
| i_en_clk_mod_debug | input | wire enable the clock modulation debug | PMU I/O List | 39 |
| i_en_chop_ref | input | wire enable chopper clock | PMU I/O List | 39 |
| i_en_ck_chop_imp | input | wire enable chopper clock for bia | PMU I/O List | 39 |
| i_en_ck_hc2_10k | input | wire enable health channel clock | PMU I/O List | 39 |
| i_freq_bia_m_p_q | input | wire [2:0] frequency selector for phase and quadrature 39 | PMU I/O List | 39 |
| i_en_clk_16MHz_sleep | input | wire enable clock in SLEEP mode when a bio- channel is selected | PMU I/O List | 40 |
| EN_ADC_TEST_LOW_NOISE | input | wire enable adc test low noise | PMU I/O List | 40 |
| EN_ADC_TEST_FAST | input | wire enable adc test fast | PMU I/O List | 40 |
| if_sh_ck_in | input | wire sensor hub clock interface | PMU I/O List | 40 |
| o_EN_LDO1V8 | output | wire enable ldo to analog domain | PMU I/O List | 40 |
| o_PD_CLKF | output | wire power down 16MHz clock to analog domain | PMU I/O List | 40 |
| o_CLK_16M_READY | output | wire clock ready to the digital domain | PMU I/O List | 40 |
| o_DIS_RC_VIREF | output | wire dis rc viref to the analog domain | PMU I/O List | 40 |
| pd_osc_clk32k | output | wire power down for clk 64kHz | PMU I/O List | 40 |
| tst_clk_32k | output | wire clock slow 32k to main_controller | PMU I/O List | 40 |
| tst_clk_16m | output | wire clock fast 16M | PMU I/O List | 40 |
| tst_clk_bistctlr | output | wire test clock for bist ctrl | PMU I/O List | 40 |
| tst_rst_bistctlr_n | output | wire test reset for bist ctrl | PMU I/O List | 40 |
| clk_stredl | output | wire clock gating logic inside stredl_afe_top | PMU I/O List | 40 |
| clk_xbar | output | wire xbar clock | PMU I/O List | 40 |
| clk_intf | output | wire interface clock | PMU I/O List | 40 |
| clk_main_ctrl | output | wire clock for main controller | PMU I/O List | 40 |
| clk_stmc | output | wire adsp clock | PMU I/O List | 40 |
| clk_stmc_ahb | output | wire adsp clk elaboration | PMU I/O List | 40 |
| clk_fifo | output | wire fifo clock | PMU I/O List | 40 |
| clk_masterblaze_m | output | wire sensor hub master clock | PMU I/O List | 40 |
| clk_masterblaze_s | output | wire sensor hub slave clock | PMU I/O List | 40 |
| clk_regmap | output | wire regmap clock | PMU I/O List | 40 |
| o_clk_ext_en | output | wire enable external clock 40 | PMU I/O List | 40 |
| resetn_stredl | output | wire reset mngmt inside stredl_afe_top | PMU I/O List | 41 |
| resetn_xbar | output | wire xbar reset | PMU I/O List | 41 |
| resetn_intf | output | wire reset interface | PMU I/O List | 41 |
| resetn_main_ctrl | output | wire reset main controller | PMU I/O List | 41 |
| resetn_32k_main_ctrl | output | wire reset 32kHz domain main controller | PMU I/O List | 41 |
| resetn_stmc | output | wire reset adsp | PMU I/O List | 41 |
| resetn_fifo | output | wire reset FIFO | PMU I/O List | 41 |
| resetn_masterblaze | output | wire reset sensor hub | PMU I/O List | 41 |
| resetn_regmap | output | wire reset regmap | PMU I/O List | 41 |
| o_trimming_clk_fast | output | wire trimming output clock fast | PMU I/O List | 41 |
| iso_o | output | wire left open . to be connected in synthesis | PMU I/O List | 41 |
| vdden_o | output | wire to be connected to psw_ctrl.VDDIEN | PMU I/O List | 41 |
| o_ck_bg | output | wire bg clock to analog domain | PMU I/O List | 41 |
| o_sh_clk | output | wire sensor hub clock | PMU I/O List | 41 |
| o_ck_chop_imp | output | wire chopper bia clock to analog domain | PMU I/O List | 41 |
| o_ck_m | output | wire modulation clock to analog domain | PMU I/O List | 41 |
| o_ck_hc2_10k | output | wire healt channel 10kHz clock to analog domain | PMU I/O List | 41 |
| o_ck_p | output | wire phase clock to analog domain | PMU I/O List | 41 |
| o_ck_q | output | wire quadrature clock to analog domain | PMU I/O List | 41 |
| o_clk_16M_mc | output | wire 16MHz clock for Main Controller | PMU I/O List | 41 |
| o_clk_dft_adc | output | wire 16MHz clock for ADC DFT | PMU I/O List | 41 |
| o_clk_gsr_16M | output | wire gsr clock to digital domain | PMU I/O List | 41 |
| o_ADC_clk_serial_dft | output | wire adc serial clock in dft | PMU I/O List | 41 |
| o_sh_clk_gate | output | wire status clk reg clk sh 16Mhz 41 | PMU I/O List | 41 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-PMU-001** {#ipos-pmu-001}
When the device is turned on, i_POR1V2_1V2 shall be high. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0104

[End]


#### **IPOS-PMU-002** {#ipos-pmu-002}
When i_POR1V2_1V2 is low, o_ EN_LDO1V8 shall be low. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0105

[End]


#### **IPOS-PMU-003** {#ipos-pmu-003}
When i_POR1V2_1V2 is low, o_PD_CLKF shall be high. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0106

[End]


#### **IPOS-PMU-004** {#ipos-pmu-004}
When i_POR1V2_1V2 is low, o_CLK_16M_READY shall be low. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0107

[End]


#### **IPOS-PMU-005** {#ipos-pmu-005}
When i_POR1V2_1V2 is low, o_DIS_RC_VIREF shall be high. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0108

[End]


#### **IPOS-PMU-006** {#ipos-pmu-006}
When i_POR1V2_1V2 rises, after at least 10 cycles of i_clk_64k (64kHz), o_ EN_LDO1V8 shall be high and the clk_64k_divided is considered stable. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0109

[End]


#### **IPOS-PMU-007** {#ipos-pmu-007}
When clk_64k_divided is stable, after at least 352 cycles of clk_64k_divided (32kHz), o_DIS_RC_VIREF shall be low. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0110

[End]


#### **IPOS-PMU-008** {#ipos-pmu-008}
When i_mask_en_ldo_pdclkf_reg and o_EN_LDO1V8 are set to 1, o_PD_CLKF shall be low after at least 40 cycles of the clk_64k_divided. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0111

[End]


#### **IPOS-PMU-009** {#ipos-pmu-009}
When i_START_CLK_16M is high, after at least 20 cycles of i_clk_16M (16MHz), o_CLK_16M_READY shall be high. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0112

[End]


#### **IPOS-PMU-010** {#ipos-pmu-010}
When i_START_CLK_16M is high for the first time, after at least 20 cycles of i_clk_16M (16MHz), o_main_resetn shall be high. [TO: IPOS_PMU]

Covers: DDS_STBIO1_0113

[End]


#### **IPOS-PMU-011** {#ipos-pmu-011}
At the release of the POR signal from the analog domain, the PMU shall manage the turn-on of the LDO1V8 and starts clocks Start-Up Sequence (reported in PMU IPOS) [TO: IPOS_PMU]

Covers: DDS_STBIO1_0114

[End]


#### **IPOS-PMU-012** {#ipos-pmu-012}
After At least 2 ms from the Release of the POR, the reset of the digital domain shall be de- asserted (an overlook on this part is described in the PMU IPOS) and the device shall start the Boot Phase [TO: IPOS_PMU]

Covers: DDS_STBIO1_0115

[End]


#### **IPOS-PMU-013** {#ipos-pmu-013}
The stbio1_top.clk_16m signal shall be connected to the stbio1_top.dig_wrapper_LV.u_pmu.clk_16m signal, with frequency 16 MHz and without clock gating.

Covers: DDS_STBIO1_1020

[End]


#### **IPOS-PMU-014** {#ipos-pmu-014}
The stbio1_top.clk_64k signal shall be connected to the stbio1_top.dig_wrapper_LV.u_pmu.clk_64k signal, with frequency 64 kHz and without clock gating.

Covers: DDS_STBIO1_1021

[End]


#### **IPOS-PMU-015** {#ipos-pmu-015}
The stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft signal shall be connected to the stbio1_top.dig_wrapper_LV.u_ADSP.stmc_clk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.adsp_run | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable.

Covers: DDS_STBIO1_1022

[End]


#### **IPOS-PMU-016** {#ipos-pmu-016}
The stbio1_top.dig_wrapper_LV.u_pmu.w_sh_clk signal shall be connected to the stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.sys_clk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.i_en_sh_clk | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable.

Covers: DDS_STBIO1_1023

[End]


#### **IPOS-PMU-017** {#ipos-pmu-017}
The stbio1_top.dig_wrapper_LV.u_pmu.clk_16m_dft signal shall be connected to the stbio1_top.dig_wrapper_LV.u_xbar_afe.hclk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_xbar_en | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable.

Covers: DDS_STBIO1_1024

[End]


#### **IPOS-PMU-018** {#ipos-pmu-018}
The u_stbio1_top.u_pmu.u_device_startup.tst_clk_32k signal shall be connected to the stbio1_top.dig_wrapper_LV.tst_clk_32k signal, with frequency 32 kHz and without clock gating.

Covers: DDS_STBIO1_1025

[End]


#### **IPOS-PMU-019** {#ipos-pmu-019}
The stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16m signal shall be connected to the stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_16MHz signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.i_en_clk_16MHz_sleep | stbio1_top.dig_wrapper_LV.u_pm u.scan_mode | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable.

Covers: DDS_STBIO1_1026

[End]


#### **IPOS-PMU-020** {#ipos-pmu-020}
The stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_32k signal shall be connected to the stbio1_top.dig_wrapper_LV.u_main_controller_top.i_clk_32kHz signal, with frequency 32 kHz and without clock gating.

Covers: DDS_STBIO1_1027

[End]


#### **IPOS-PMU-021** {#ipos-pmu-021}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_stmcu_stbio1_top.dig_wrapper_LV.u_ADSP.HRESETn signal.

Covers: DDS_STBIO1_1050

[End]


#### **IPOS-PMU-022** {#ipos-pmu-022}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_masterblazeu_stbio1_top.dig_wrapper_LV.u_masterblaze_ahb.HRESETn signal.

Covers: DDS_STBIO1_1051

[End]


#### **IPOS-PMU-023** {#ipos-pmu-023}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_regmapu_stbio1_top.dig_wrapper_LV.u_regmap_otp.hresetn signal.

Covers: DDS_STBIO1_1052

[End]


#### **IPOS-PMU-024** {#ipos-pmu-024}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_fifou_stbio1_top.dig_wrapper_LV.u_multi_channel_fifo_top.HRESETn signal.

Covers: DDS_STBIO1_1053

[End]


#### **IPOS-PMU-025** {#ipos-pmu-025}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_main_ctrlu_stbio1_top.dig_wrapper_LV.u_main_controller_top.i_rstn signal.

Covers: DDS_STBIO1_1054

[End]


#### **IPOS-PMU-026** {#ipos-pmu-026}
The stbio1_top.dig_wrapper_LV.u_pmuclk_xbar signal shall be connected to the stbio1_top.dig_wrapper_LV.u.fifo.HCLK signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m2_reg | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable.

Covers: DDS_STBIO1_2024

[End]


#### **IPOS-PMU-027** {#ipos-pmu-027}
The stbio1_top.dig_wrapper_LV.u_pmu.clk_stredl signal shall be connected to the stbio1_top.dig_wrapper_LV.u_ispu.clk signal, with frequency 16 MHz and without clock gating.

Covers: DDS_STBIO1_2025

[End]


#### **IPOS-PMU-028** {#ipos-pmu-028}
The stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar signal shall be connected to the stbio1_top.dig_wrapper_LV.u_regmap_otp.hclk signal, with frequency 16 MHz and with clock gating stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3 | stbio1_top.dig_wrapper_LV.u_pm u.all_test_mode | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_m3_reg | stbio1_top.dig_wrapper_LV.u_pm u.clk_en_s3 | ~stbio1_top.dig_wrapper_LV.u_p ad_mux.scan_enable.

Covers: DDS_STBIO1_2026

[End]


#### **IPOS-PMU-029** {#ipos-pmu-029}
The stbio1_top.dig_wrapper_LV.u_pmu. signal shall be connected to the u_device_startup.u_por_main_resetn.RST_N_FF[0]u_stbio1_top.dig_wrapper_LV.u_xbar_afe.hresetn signal.

Covers: DDS_STBIO1_2052

[End]


#### **IPOS-PMU-030** {#ipos-pmu-030}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_regmapu_stbio1_top.dig_wrapper_LV.u_ispu.main_rst_n signal.

Covers: DDS_STBIO1_2053

[End]


#### **IPOS-PMU-031** {#ipos-pmu-031}
The u_stbio1_top.dig_wrapper_LV.u_p signal shall be connected to the mu.resetn_32k_main_ctrlu_stbio1_top.dig_wrapper_LV.u_main_controller_top.i_rstn_sync_32 signal.

Covers: DDS_STBIO1_2054

[End]

