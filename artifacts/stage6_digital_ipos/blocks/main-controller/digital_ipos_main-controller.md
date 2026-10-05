# **Digital IPOS - Main Controller** {#digital-ipos---main-controller}

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
| IPOS-MAIN-CONTROLLER-001 | [Go to requirement](#ipos-main-controller-001) |
| IPOS-MAIN-CONTROLLER-002 | [Go to requirement](#ipos-main-controller-002) |
| IPOS-MAIN-CONTROLLER-003 | [Go to requirement](#ipos-main-controller-003) |
| IPOS-MAIN-CONTROLLER-004 | [Go to requirement](#ipos-main-controller-004) |
| IPOS-MAIN-CONTROLLER-005 | [Go to requirement](#ipos-main-controller-005) |
| IPOS-MAIN-CONTROLLER-006 | [Go to requirement](#ipos-main-controller-006) |
| IPOS-MAIN-CONTROLLER-007 | [Go to requirement](#ipos-main-controller-007) |
| IPOS-MAIN-CONTROLLER-008 | [Go to requirement](#ipos-main-controller-008) |
| IPOS-MAIN-CONTROLLER-009 | [Go to requirement](#ipos-main-controller-009) |
| IPOS-MAIN-CONTROLLER-010 | [Go to requirement](#ipos-main-controller-010) |
| IPOS-MAIN-CONTROLLER-011 | [Go to requirement](#ipos-main-controller-011) |
| IPOS-MAIN-CONTROLLER-012 | [Go to requirement](#ipos-main-controller-012) |
| IPOS-MAIN-CONTROLLER-013 | [Go to requirement](#ipos-main-controller-013) |
| IPOS-MAIN-CONTROLLER-014 | [Go to requirement](#ipos-main-controller-014) |
| IPOS-MAIN-CONTROLLER-015 | [Go to requirement](#ipos-main-controller-015) |
| IPOS-MAIN-CONTROLLER-016 | [Go to requirement](#ipos-main-controller-016) |
| IPOS-MAIN-CONTROLLER-017 | [Go to requirement](#ipos-main-controller-017) |
| IPOS-MAIN-CONTROLLER-018 | [Go to requirement](#ipos-main-controller-018) |
| IPOS-MAIN-CONTROLLER-019 | [Go to requirement](#ipos-main-controller-019) |
| IPOS-MAIN-CONTROLLER-020 | [Go to requirement](#ipos-main-controller-020) |
| IPOS-MAIN-CONTROLLER-021 | [Go to requirement](#ipos-main-controller-021) |
| IPOS-MAIN-CONTROLLER-022 | [Go to requirement](#ipos-main-controller-022) |
| IPOS-MAIN-CONTROLLER-023 | [Go to requirement](#ipos-main-controller-023) |
| IPOS-MAIN-CONTROLLER-024 | [Go to requirement](#ipos-main-controller-024) |
| IPOS-MAIN-CONTROLLER-025 | [Go to requirement](#ipos-main-controller-025) |
| IPOS-MAIN-CONTROLLER-026 | [Go to requirement](#ipos-main-controller-026) |
| IPOS-MAIN-CONTROLLER-027 | [Go to requirement](#ipos-main-controller-027) |
| IPOS-MAIN-CONTROLLER-028 | [Go to requirement](#ipos-main-controller-028) |
| IPOS-MAIN-CONTROLLER-029 | [Go to requirement](#ipos-main-controller-029) |
| IPOS-MAIN-CONTROLLER-030 | [Go to requirement](#ipos-main-controller-030) |
| IPOS-MAIN-CONTROLLER-031 | [Go to requirement](#ipos-main-controller-031) |
| IPOS-MAIN-CONTROLLER-032 | [Go to requirement](#ipos-main-controller-032) |
| IPOS-MAIN-CONTROLLER-033 | [Go to requirement](#ipos-main-controller-033) |
| IPOS-MAIN-CONTROLLER-034 | [Go to requirement](#ipos-main-controller-034) |
| IPOS-MAIN-CONTROLLER-035 | [Go to requirement](#ipos-main-controller-035) |
| IPOS-MAIN-CONTROLLER-036 | [Go to requirement](#ipos-main-controller-036) |
| IPOS-MAIN-CONTROLLER-037 | [Go to requirement](#ipos-main-controller-037) |
| IPOS-MAIN-CONTROLLER-038 | [Go to requirement](#ipos-main-controller-038) |
| IPOS-MAIN-CONTROLLER-039 | [Go to requirement](#ipos-main-controller-039) |
| IPOS-MAIN-CONTROLLER-040 | [Go to requirement](#ipos-main-controller-040) |
| IPOS-MAIN-CONTROLLER-041 | [Go to requirement](#ipos-main-controller-041) |
| IPOS-MAIN-CONTROLLER-042 | [Go to requirement](#ipos-main-controller-042) |
| IPOS-MAIN-CONTROLLER-043 | [Go to requirement](#ipos-main-controller-043) |
| IPOS-MAIN-CONTROLLER-044 | [Go to requirement](#ipos-main-controller-044) |
| IPOS-MAIN-CONTROLLER-045 | [Go to requirement](#ipos-main-controller-045) |
| IPOS-MAIN-CONTROLLER-046 | [Go to requirement](#ipos-main-controller-046) |
| IPOS-MAIN-CONTROLLER-047 | [Go to requirement](#ipos-main-controller-047) |
| IPOS-MAIN-CONTROLLER-048 | [Go to requirement](#ipos-main-controller-048) |
| IPOS-MAIN-CONTROLLER-049 | [Go to requirement](#ipos-main-controller-049) |
| IPOS-MAIN-CONTROLLER-050 | [Go to requirement](#ipos-main-controller-050) |
| IPOS-MAIN-CONTROLLER-051 | [Go to requirement](#ipos-main-controller-051) |
| IPOS-MAIN-CONTROLLER-052 | [Go to requirement](#ipos-main-controller-052) |
| IPOS-MAIN-CONTROLLER-053 | [Go to requirement](#ipos-main-controller-053) |
| IPOS-MAIN-CONTROLLER-054 | [Go to requirement](#ipos-main-controller-054) |
| IPOS-MAIN-CONTROLLER-055 | [Go to requirement](#ipos-main-controller-055) |
| IPOS-MAIN-CONTROLLER-056 | [Go to requirement](#ipos-main-controller-056) |
| IPOS-MAIN-CONTROLLER-057 | [Go to requirement](#ipos-main-controller-057) |
| IPOS-MAIN-CONTROLLER-058 | [Go to requirement](#ipos-main-controller-058) |
| IPOS-MAIN-CONTROLLER-059 | [Go to requirement](#ipos-main-controller-059) |
| IPOS-MAIN-CONTROLLER-060 | [Go to requirement](#ipos-main-controller-060) |
| IPOS-MAIN-CONTROLLER-061 | [Go to requirement](#ipos-main-controller-061) |
| IPOS-MAIN-CONTROLLER-062 | [Go to requirement](#ipos-main-controller-062) |
| IPOS-MAIN-CONTROLLER-063 | [Go to requirement](#ipos-main-controller-063) |
| IPOS-MAIN-CONTROLLER-064 | [Go to requirement](#ipos-main-controller-064) |
| IPOS-MAIN-CONTROLLER-065 | [Go to requirement](#ipos-main-controller-065) |
| IPOS-MAIN-CONTROLLER-066 | [Go to requirement](#ipos-main-controller-066) |
| IPOS-MAIN-CONTROLLER-067 | [Go to requirement](#ipos-main-controller-067) |
| IPOS-MAIN-CONTROLLER-068 | [Go to requirement](#ipos-main-controller-068) |
| IPOS-MAIN-CONTROLLER-069 | [Go to requirement](#ipos-main-controller-069) |
| IPOS-MAIN-CONTROLLER-070 | [Go to requirement](#ipos-main-controller-070) |
| IPOS-MAIN-CONTROLLER-071 | [Go to requirement](#ipos-main-controller-071) |
| IPOS-MAIN-CONTROLLER-072 | [Go to requirement](#ipos-main-controller-072) |
| IPOS-MAIN-CONTROLLER-073 | [Go to requirement](#ipos-main-controller-073) |
| IPOS-MAIN-CONTROLLER-074 | [Go to requirement](#ipos-main-controller-074) |
| IPOS-MAIN-CONTROLLER-075 | [Go to requirement](#ipos-main-controller-075) |
| IPOS-MAIN-CONTROLLER-076 | [Go to requirement](#ipos-main-controller-076) |
| IPOS-MAIN-CONTROLLER-077 | [Go to requirement](#ipos-main-controller-077) |
| IPOS-MAIN-CONTROLLER-078 | [Go to requirement](#ipos-main-controller-078) |
| IPOS-MAIN-CONTROLLER-079 | [Go to requirement](#ipos-main-controller-079) |
| IPOS-MAIN-CONTROLLER-080 | [Go to requirement](#ipos-main-controller-080) |
| IPOS-MAIN-CONTROLLER-081 | [Go to requirement](#ipos-main-controller-081) |
| IPOS-MAIN-CONTROLLER-082 | [Go to requirement](#ipos-main-controller-082) |
| IPOS-MAIN-CONTROLLER-083 | [Go to requirement](#ipos-main-controller-083) |
| IPOS-MAIN-CONTROLLER-084 | [Go to requirement](#ipos-main-controller-084) |
| IPOS-MAIN-CONTROLLER-085 | [Go to requirement](#ipos-main-controller-085) |
| IPOS-MAIN-CONTROLLER-086 | [Go to requirement](#ipos-main-controller-086) |
| IPOS-MAIN-CONTROLLER-087 | [Go to requirement](#ipos-main-controller-087) |
| IPOS-MAIN-CONTROLLER-088 | [Go to requirement](#ipos-main-controller-088) |
| IPOS-MAIN-CONTROLLER-089 | [Go to requirement](#ipos-main-controller-089) |
| IPOS-MAIN-CONTROLLER-090 | [Go to requirement](#ipos-main-controller-090) |
| IPOS-MAIN-CONTROLLER-091 | [Go to requirement](#ipos-main-controller-091) |
| IPOS-MAIN-CONTROLLER-092 | [Go to requirement](#ipos-main-controller-092) |
| IPOS-MAIN-CONTROLLER-093 | [Go to requirement](#ipos-main-controller-093) |
| IPOS-MAIN-CONTROLLER-094 | [Go to requirement](#ipos-main-controller-094) |
| IPOS-MAIN-CONTROLLER-095 | [Go to requirement](#ipos-main-controller-095) |
| IPOS-MAIN-CONTROLLER-096 | [Go to requirement](#ipos-main-controller-096) |
| IPOS-MAIN-CONTROLLER-097 | [Go to requirement](#ipos-main-controller-097) |
| IPOS-MAIN-CONTROLLER-098 | [Go to requirement](#ipos-main-controller-098) |
| IPOS-MAIN-CONTROLLER-099 | [Go to requirement](#ipos-main-controller-099) |
| IPOS-MAIN-CONTROLLER-100 | [Go to requirement](#ipos-main-controller-100) |
| IPOS-MAIN-CONTROLLER-101 | [Go to requirement](#ipos-main-controller-101) |
| IPOS-MAIN-CONTROLLER-102 | [Go to requirement](#ipos-main-controller-102) |
| IPOS-MAIN-CONTROLLER-103 | [Go to requirement](#ipos-main-controller-103) |
| IPOS-MAIN-CONTROLLER-104 | [Go to requirement](#ipos-main-controller-104) |
| IPOS-MAIN-CONTROLLER-105 | [Go to requirement](#ipos-main-controller-105) |
| IPOS-MAIN-CONTROLLER-106 | [Go to requirement](#ipos-main-controller-106) |
| IPOS-MAIN-CONTROLLER-107 | [Go to requirement](#ipos-main-controller-107) |
| IPOS-MAIN-CONTROLLER-108 | [Go to requirement](#ipos-main-controller-108) |
| IPOS-MAIN-CONTROLLER-109 | [Go to requirement](#ipos-main-controller-109) |
| IPOS-MAIN-CONTROLLER-110 | [Go to requirement](#ipos-main-controller-110) |
| IPOS-MAIN-CONTROLLER-111 | [Go to requirement](#ipos-main-controller-111) |
| IPOS-MAIN-CONTROLLER-112 | [Go to requirement](#ipos-main-controller-112) |
| IPOS-MAIN-CONTROLLER-113 | [Go to requirement](#ipos-main-controller-113) |
| IPOS-MAIN-CONTROLLER-114 | [Go to requirement](#ipos-main-controller-114) |
| IPOS-MAIN-CONTROLLER-115 | [Go to requirement](#ipos-main-controller-115) |
| IPOS-MAIN-CONTROLLER-116 | [Go to requirement](#ipos-main-controller-116) |
| IPOS-MAIN-CONTROLLER-117 | [Go to requirement](#ipos-main-controller-117) |
| IPOS-MAIN-CONTROLLER-118 | [Go to requirement](#ipos-main-controller-118) |
| IPOS-MAIN-CONTROLLER-119 | [Go to requirement](#ipos-main-controller-119) |
| IPOS-MAIN-CONTROLLER-120 | [Go to requirement](#ipos-main-controller-120) |
| IPOS-MAIN-CONTROLLER-121 | [Go to requirement](#ipos-main-controller-121) |
| IPOS-MAIN-CONTROLLER-122 | [Go to requirement](#ipos-main-controller-122) |
| IPOS-MAIN-CONTROLLER-123 | [Go to requirement](#ipos-main-controller-123) |
| IPOS-MAIN-CONTROLLER-124 | [Go to requirement](#ipos-main-controller-124) |
| IPOS-MAIN-CONTROLLER-125 | [Go to requirement](#ipos-main-controller-125) |
| IPOS-MAIN-CONTROLLER-126 | [Go to requirement](#ipos-main-controller-126) |
| IPOS-MAIN-CONTROLLER-127 | [Go to requirement](#ipos-main-controller-127) |
| IPOS-MAIN-CONTROLLER-128 | [Go to requirement](#ipos-main-controller-128) |
| IPOS-MAIN-CONTROLLER-129 | [Go to requirement](#ipos-main-controller-129) |
| IPOS-MAIN-CONTROLLER-130 | [Go to requirement](#ipos-main-controller-130) |
| IPOS-MAIN-CONTROLLER-131 | [Go to requirement](#ipos-main-controller-131) |
| IPOS-MAIN-CONTROLLER-132 | [Go to requirement](#ipos-main-controller-132) |
| IPOS-MAIN-CONTROLLER-133 | [Go to requirement](#ipos-main-controller-133) |
| IPOS-MAIN-CONTROLLER-134 | [Go to requirement](#ipos-main-controller-134) |
| IPOS-MAIN-CONTROLLER-135 | [Go to requirement](#ipos-main-controller-135) |
| IPOS-MAIN-CONTROLLER-136 | [Go to requirement](#ipos-main-controller-136) |
| IPOS-MAIN-CONTROLLER-137 | [Go to requirement](#ipos-main-controller-137) |
| IPOS-MAIN-CONTROLLER-138 | [Go to requirement](#ipos-main-controller-138) |

## **1. Block overview** {#1-block-overview}

### **1.1 Functionality** {#11-functionality}

The Main Controller block is designed to generate and receive Analog Domain control signals, perform DSP elaboration on ADC outputs, and write elaborated results to the defined addresses.

### **1.2 Supported functions and scope** {#12-supported-functions-and-scope}

- The Main Controller accepts configuration settings, sampled data and produces control state and data routing.
- **PPG saturation flag control.** Flags PPG saturation when at least half of the selected samples equal 0x8000 or 0x7FFF after signed conversion; clears at the start of the next frame or frame repetition.
- **Digital ramp control.** Advances the digital ramp first step (o_Tx_Vref) to the configured start value (i_N_start) at preset time (i_T_preset), then enters Rising Ramp when averaging completes in First ALC Samples.
  Interacts with ADC averaging completion.
- **ELAB FSM.** Coordinates elaboration across TIMER BUFFER, PPG, BIA, ECG, and start-up paths, with PPG start-up timing.
  Sequences TIMER BUFFER then PPG ALC STORAGE states.
  Interacts with PPG frame sequencing, PPG operation control, ADC phase acquisition, and ADC mux, acquisition-enable, and buffer outputs.
- **Measurement setup and initiation.** Selects GSR, ECG0, BIA, PPG, and ECG1/ECG2 channels and Data Storage Mode, then starts measurement.
- **GSR acquisition and processing.** Enables GSR current (GSR curr on) in every time slot when CDS is disabled (GSR_CTRL bit 3), averages 16 samples for GSR, and subtracts the separately averaged GSR SNS and GSR CDS values from 16 acquisitions each when CDS is enabled.
- **ADC phases.** Maintains ADC sampling until conversion completes.
  Enables the ADC clock for ECG, BIA, or GSR sampling when ADC acquisition is enabled.
- **PPG result computation.** Subtracts accumulated PPG raw data and PPG noise according to ALC Mask.
- **Device FSM.** Controls the device lifecycle across Idle, PPG, Error, Start-Up, Boot, Operative, and Sleep states.
  Waits for ADSP boot completion.
  Enters Operative state when in Sleep Mode if no error occurs and all the operations are ended.
  Interacts with Clock Generator block, ADSP boot completion, start-up delay control, PPG frame sequencing, PPG noise averaging, ALC compensation sequencing, ADC mux, acquisition-enable, and buffer outputs, Digital Top error interrupt, and device busy and status outputs.
- **Local configuration.** Selects channels and Data Storage Mode, limits configured channel values to 1024, and sets the GSR acquisition interval in time slots; the cited expression is retained without interpreting its arithmetic.
- **PPG FSM.** Coordinates PPG averaging, ramp timing, and ALC compensation start.
  Waits for ADC conversion completion across FIRST ALC SAMPLES, Measurement, Rising Ramp, Falling Ramp, and SECOND ALC SAMPLES paths.
  Waits for ALC compensation completion before PPG start-up.
  Interacts with ADC block, ALC Compensation block, and ADC averaging completion.
- **Frame repetition result computation.** Divides accumulated frame data by number of repetitions to produce a 20-bit result.
- **Main Controller FSM.** Stores time-slot results in the FIFO with a dedicated tag.

## **2. Source I/O** {#2-source-io}

The following approved source I/O entries are owned by this block.

| Port name | Direction | Type / details | Table | Source page |
|---|---|---|---|---|
| i_clk_32kHz | input | clk 32kHz from pmu | Main Controller I/O List | 76 |
| i_clk_16MHz | input | clk 16MHz from pmu | Main Controller I/O List | 76 |
| i_clk_gsr_16M | input | clk for gsr signal | Main Controller I/O List | 76 |
| i_clk_ahb_master | input | clock for ahb master | Main Controller I/O List | 76 |
| i_rstn | input | reset in 16MHz domain | Main Controller I/O List | 76 |
| i_rstn_sync_32 | input | reset in 32kz domain | Main Controller I/O List | 76 |
| i_wave_velocity_mode | input | enable of the wave velocity mode | Main Controller I/O List | 76 |
| i_ispu_end_elab | input |  | Main Controller I/O List | 76 |
| i_n_ppg_frame | input | [ppg_frame_bit_top-1:0] number of frame selected | Main Controller I/O List | 76 |
| i_const_value_ioff | input | [data_in_size_bit_top-1:0] constant value from regmap used for ppg ioff calibraton | Main Controller I/O List | 76 |
| i_rx_ch_frame | input | [n_max_frame-1:0] ppg rx channel frame from regamp | Main Controller I/O List | 76 |
| i_T_tx_led_set | input | [n_max_frame-1:0] tx led set time from regmap | Main Controller I/O List | 76 |
| i_T_tx_led_off | input | [n_max_frame-1:0] tx led off time from regmap | Main Controller I/O List | 76 |
| i_curr_sel_tx_frame_x | input | [n_max_frame-1:0] current injection | Main Controller I/O List | 76 |
| i_tx1_outlab_sel_frame_x | input | [n_max_frame-1:0] led output selected from regmap for each frame | Main Controller I/O List | 76 |
| i_tx2_outlab_sel_frame_x | input | [n_max_frame-1:0] led output selected from regmap for each frame | Main Controller I/O List | 76 |
| i_tx3_outlab_sel_frame_x | input | [n_max_frame-1:0] led output selected from regmap for each frame | Main Controller I/O List | 76 |
| i_tx4_outlab_sel_frame_x | input | [n_max_frame-1:0] led output selected from regmap for each frame | Main Controller I/O List | 76 |
| i_idac_dc_ppg_frame | input | [n_max_frame-1:0] idac value for each frame selected from regmap | Main Controller I/O List | 76 |
| i_average_ppg | input | [n_max_frame-1:0] average ppg for each frame selected from regmap | Main Controller I/O List | 76 |
| i_gain_alc_start | input | [gain_max_bit_top-1:0] btia gain for alc from regmap | Main Controller I/O List | 76 |
| i_gain_start | input | [n_max_frame-1:0] btia gain start for compensation from regmap | Main Controller I/O List | 76 |
| i_Tx_idac_Vref_debug | input | [Nmax_bit_top-1:0] Idac value for debug from regmap 76 | Main Controller I/O List | 76 |
| i_ppg_start_up_time | input | [ppg_start_up_decod_bit_top-1:0] start up time for ppg from regmap | Main Controller I/O List | 77 |
| i_en_txi | input | [n_max_frame-1:0] tx enabling for each frame from regmap | Main Controller I/O List | 77 |
| i_frame_repetition | input | [n_max_frame-1:0] i frame repetition for each frame from regmap | Main Controller I/O List | 77 |
| i_T_preset | input | [1:0] Preset time for digital ramp from regmap | Main Controller I/O List | 77 |
| i_m_ecg | input | [m_odr_max_bit_top-1:0] m parameter for ecg from regmap | Main Controller I/O List | 77 |
| i_m_bia | input | [m_odr_max_bit_top-1:0] m parameter for bia from regmap | Main Controller I/O List | 77 |
| i_m_gsr | input | [m_odr_max_bit_top-1:0] m parameter for gsr from regmap | Main Controller I/O List | 77 |
| i_m_ppg | input | [m_odr_max_bit_top-1:0] m parameter for ppg from regmap | Main Controller I/O List | 77 |
| i_debug_adc_error_cap8_0_bypass | input | error cap bypass for adc from regmap | Main Controller I/O List | 77 |
| i_base_address_ecg0 | input | [base_address_bit_top-1:0] base address for ecg0 in multiple fifo | Main Controller I/O List | 77 |
| i_base_address_bia | input | [base_address_bit_top-1:0] base address for bia/ecg1-2 in multiple fifo | Main Controller I/O List | 77 |
| i_base_address_gsr | input | [base_address_bit_top-1:0] base address for gsr in multiple fifo | Main Controller I/O List | 77 |
| i_base_address_ppg | input | [base_address_bit_top-1:0] base address for ppg in multiple fifo | Main Controller I/O List | 77 |
| i_frame_ppg_debug | input | [ppg_frame_bit_top-1:0] frame selection for ppg data debug | Main Controller I/O List | 77 |
| i_en_buf_gpio1 | input | enable buffer on gpio1 | Main Controller I/O List | 77 |
| i_en_buf_gpio2 | input | enable buffer on gpio2 | Main Controller I/O List | 77 |
| i_en_biobuf | input | enable biobuffer | Main Controller I/O List | 77 |
| i_do_calibration | input | enabling for adc calibration | Main Controller I/O List | 77 |
| i_mode_operation | input | [mode_operation_n_bit_top-1:0] mode operation selection | Main Controller I/O List | 77 |
| i_T_rx_set | input | [T1_max_bit_from_decoder_top- 1:0] rx channel time set | Main Controller I/O List | 77 |
| i_en_clkf | input | en 16 MHz clock | Main Controller I/O List | 77 |
| i_quokka_boot_end | input | from quokka | Main Controller I/O List | 77 |
| i_quokka_run | input | from quokka 77 | Main Controller I/O List | 77 |
| i_clk_16MHz_ready | input | (from analog circuit) | Main Controller I/O List | 78 |
| i_imp_curinj_en | input | enabling current injection for bia | Main Controller I/O List | 78 |
| i_en_ldo_1v8 | input | enabling ldo 1v8 | Main Controller I/O List | 78 |
| i_debug_comp_rx_ck | input | enabling debug for comp rx ck | Main Controller I/O List | 78 |
| i_debug_gsr_on | input | gsr on debug mode | Main Controller I/O List | 78 |
| i_debug_gsr_curr_on | input | gsr curr on debug mode | Main Controller I/O List | 78 |
| i_alc_disabled | input | [n_max_frame-1:0] disabling alc bit for each frame | Main Controller I/O List | 78 |
| i_en_cm_buf | input | enabling common buffer | Main Controller I/O List | 78 |
| i_en_rld | input | enabling rld | Main Controller I/O List | 78 |
| i_en_avg1 | input | enabling avg1 | Main Controller I/O List | 78 |
| i_en_avg2 | input | enabling avg1 | Main Controller I/O List | 78 |
| i_hc_en | input | enabling health channel | Main Controller I/O List | 78 |
| i_debug | input | enabling debug mode | Main Controller I/O List | 78 |
| i_imp_en | input | enabling bia channel | Main Controller I/O List | 78 |
| i_debug_en_tia | input | enabling debug tia | Main Controller I/O List | 78 |
| i_debug_en_buffer | input | enabling debug for buffer | Main Controller I/O List | 78 |
| i_debug_en_idac | input | enabling debug for IDAC | Main Controller I/O List | 78 |
| i_en_clk_chop10k | input | enabling chopper clock | Main Controller I/O List | 78 |
| i_debug_tx_preset | input | enabling tx preset | Main Controller I/O List | 78 |
| i_en_ldo_1v8_ext | input | enabling external ldo 1v8 | Main Controller I/O List | 78 |
| i_clk_imp_10k_en | input | enabling clock chopper for bia | Main Controller I/O List | 78 |
| i_b_cap_idac | input | [1:0] enabling cap for idac | Main Controller I/O List | 78 |
| i_adc_mux_bio_channel_debug | input | [2:0] enabling debug adc mux bio channel | Main Controller I/O List | 78 |
| i_adc_mux_sel_debug | input | enabling adc mux 78 | Main Controller I/O List | 78 |
| i_ispu_core_sw_rstn | input | ispu core enabling | Main Controller I/O List | 79 |
| i_T_TIAON | input | [T1_max_bit_from_decoder_top- 1:0] TIA Time | Main Controller I/O List | 79 |
| i_scan_mode | input | scan mode enabling | Main Controller I/O List | 79 |
| i_reset_debug_adc_data | input | reset adc data debug | Main Controller I/O List | 79 |
| i_start_adc_debug | input | pilot adc start om debug | Main Controller I/O List | 79 |
| i_en_ADC_debug | input | enabling adc debug | Main Controller I/O List | 79 |
| i_debug_adc_readout_bypass | input | enabling adc readout bypass | Main Controller I/O List | 79 |
| i_su_hlt_dly | input | enabling start up delay for ecg | Main Controller I/O List | 79 |
| i_multiple_fifo_sel | input | enabling multiple fifo | Main Controller I/O List | 79 |
| i_debug_calibration | input | enabling debug calibraiton | Main Controller I/O List | 79 |
| i_en_gsr_dc_cds | input | [1:0] enabling gsr cds mode | Main Controller I/O List | 79 |
| i_ADC_EOC | input | end of conversion from adc | Main Controller I/O List | 79 |
| i_ecg0_sel | input | select ecg0 channel | Main Controller I/O List | 79 |
| i_bia_sel | input | select bia channel | Main Controller I/O List | 79 |
| i_gsr_sel | input | select gsr channel | Main Controller I/O List | 79 |
| i_ppg_sel | input | select ppg channel | Main Controller I/O List | 79 |
| i_ppg_ioff_calibration | input | enabling ppg ioff calibration | Main Controller I/O List | 79 |
| i_ecg1_ecg2_sel | input | enabling ecg1 and ecg2 channel | Main Controller I/O List | 79 |
| i_rst_async_ecg | input | reset async for ecg | Main Controller I/O List | 79 |
| i_rst_async_bia | input | reset async for bia | Main Controller I/O List | 79 |
| i_ppg_quokka_elab_sel | input | enabling adsp elab for ppg | Main Controller I/O List | 79 |
| i_data_ADC_out | input | [data_in_size_bit_top-1:0] (from analog circuit) | Main Controller I/O List | 79 |
| i_time_slot_selection | input | [time_slot_sel_bit_top-1:0] odr selection from regmap 79 | Main Controller I/O List | 79 |
| i_Nmax_to_reg | input | [Nmax_bit_top-1:0] Max value for digital ramp | Main Controller I/O List | 80 |
| i_nstart_case | input | [Nmax_bit_top-1:0] n_start value for frist sterp | Main Controller I/O List | 80 |
| i_debug_rx_ch | input | [rx_ch_frame_n_bit_top-1:0] enabling debug for rx channel | Main Controller I/O List | 80 |
| i_T_delta1_to_reg | input | [delta_bit_top-1:0] delta 1 time for digital ramp | Main Controller I/O List | 80 |
| i_gain_max_set | input | [gain_max_bit_top-1:0] gain max for alc | Main Controller I/O List | 80 |
| i_BTIA_ALC_debug | input | [BTIA_ALC_register_bit_top-1:0] BTIA ALC Debug enable | Main Controller I/O List | 80 |
| i_comp_rx_out | input | input from analog comparator | Main Controller I/O List | 80 |
| i_adc_error_cap8_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap7_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap6_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap5_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap4_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap3_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap2_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap1_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_adc_error_cap0_debug | input | [6:0] adc cap error debug | Main Controller I/O List | 80 |
| i_BIDAC_debug_register | input | [IDAC_offset-1:0] | Main Controller I/O List | 80 |
| i_sleep_master | input |  | Main Controller I/O List | 80 |
| i_lpm | input | [1:0] low power mode for ldo | Main Controller I/O List | 80 |
| i_mpm | input | [1:0] medium power mode for ldo | Main Controller I/O List | 80 |
| i_hpm | input | [1:0] high power mode for ldo | Main Controller I/O List | 80 |
| i_dis_rc_viref | input | dis rc viref | Main Controller I/O List | 80 |
| i_T1 | input | [T1_max_bit_from_decoder_top- 1:0] 4 to 10 us=160nclk 80 | Main Controller I/O List | 80 |
| i_T2 | input | [T2_max_bit_from_decoder_top- 1:0] 0.5 to 2 us=~32 | Main Controller I/O List | 81 |
| i_N_clk_ppg | input | [N_clk_max_bit_top-1:0] Sample time for ppg | Main Controller I/O List | 81 |
| i_N_clk_ecg | input | [N_clk_max_bit_top-1:0] Sample time for ecg | Main Controller I/O List | 81 |
| i_N_clk_cal | input | [N_clk_max_bit_top-1:0] Sample time for adc calibration | Main Controller I/O List | 81 |
| scan_enable | input | scan enable for scan mode | Main Controller I/O List | 81 |
| i_timer_buffer_config | input | [1:0] timer buffer configuration | Main Controller I/O List | 81 |
| i_ppg_alc_frame_save | input | [ppg_frame_bit_top-1:0] alc data frame to save | Main Controller I/O List | 81 |
| i_reset_ppg_ioff_calib | input |  | Main Controller I/O List | 81 |
| HRDATA | input | [31:0] AHB Protocol signals | Main Controller I/O List | 81 |
| HREADY | input | AHB Protocol signals | Main Controller I/O List | 81 |
| HRESP | input | [1:0] AHB Protocol signals | Main Controller I/O List | 81 |
| HGRANT | input | AHB Protocol signals | Main Controller I/O List | 81 |
| SCANENABLE | input | Scan Test Mode Enbl | Main Controller I/O List | 81 |
| SCANINHCLK | input | Scan Chain Input | Main Controller I/O List | 81 |
| SCANOUTHCLK | output | Scan Chain Output | Main Controller I/O List | 81 |
| HSEL | output | 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HADDR | output | [31:0] 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HTRANS | output | [1:0] 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HWRITE | output | 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HSIZE | output | [2:0] 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HBURST | output | [2:0] 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HPROT | output | [3:0] 0 AHB Protocol signals | Main Controller I/O List | 81 |
| HWDATA | output | [31:0] 0 AHB Protocol signals 81 | Main Controller I/O List | 81 |
| HBUSREQ | output | 0 AHB Protocol signals | Main Controller I/O List | 82 |
| HLOCK | output | 0 AHB Protocol signals | Main Controller I/O List | 82 |
| o_bio_clock_div | output | 0 output for clock chopper | Main Controller I/O List | 82 |
| o_BIDAC | output | [IDAC_offset-1:0] 0 IDAC for top | Main Controller I/O List | 82 |
| o_rst_imp | output | 1 bia start up rst signal | Main Controller I/O List | 82 |
| o_rsti_imp | output | 1 bia start up rsti signal | Main Controller I/O List | 82 |
| o_sug_imp | output | 1 bia start up sug channel | Main Controller I/O List | 82 |
| o_pd_imp | output | 1 bia start up pd channel | Main Controller I/O List | 82 |
| o_start_operative_16MHz | output | 0 start operative 16MHz | Main Controller I/O List | 82 |
| o_su_hc2 | output | 1 ecg start up hc2 signal | Main Controller I/O List | 82 |
| o_rst_hc2 | output | 1 ecg start up rst signal | Main Controller I/O List | 82 |
| o_rsti_hc2 | output | 1 ecg start up rsti signal | Main Controller I/O List | 82 |
| o_pd_hc2 | output | 1 ecg start up pd signal | Main Controller I/O List | 82 |
| o_reset_reg_rst | output | 1 end of reset async phase | Main Controller I/O List | 82 |
| o_reset_reg_rst_imp_async | output | 1 end of reset async phase | Main Controller I/O List | 82 |
| o_imp_curinj_pd | output | 0 bia current injection output | Main Controller I/O List | 82 |
| o_Txi_IDAC_Vref | output | [Nmax_bit_top-1:0] 0 TX IDAC VREF TO analog domain | Main Controller I/O List | 82 |
| o_comp_rx_ck | output | 0 output for comparator debug | Main Controller I/O List | 82 |
| o_BTIA_gain | output | [gain_max_bit_top-1:0] 0 BTIA gain output to analog domain | Main Controller I/O List | 82 |
| o_data_out_debug_adc | output | [15:0] 0 o data output for adc debug | Main Controller I/O List | 82 |
| o_en_mask_ldo_pdclkf_reg | output | 1 mask for en_ldo and pdf | Main Controller I/O List | 82 |
| o_pd_clkf | output | 1 pd_clkf | Main Controller I/O List | 82 |
| o_trim_ldo_d | output | [1:0] 3 trim ldo value | Main Controller I/O List | 82 |
| o_BDC_PPG | output | [idac_dc_ppg_frame_bit_top-1:0] 0 idac dc ppg frame output 82 | Main Controller I/O List | 82 |
| o_adc_mux_bio_channel | output | [2:0] 0 adc mux bio channel | Main Controller I/O List | 83 |
| o_adc_mux_sel | output | 0 adc mux sel output | Main Controller I/O List | 83 |
| o_error_time_slot | output | 0 error time slot irq | Main Controller I/O List | 83 |
| o_curr_sel_tx_frame_x | output | [curr_sel_bit_top-1:0] 0 current selection for tx channel output | Main Controller I/O List | 83 |
| o_tx1_outlab_sel_frame_x | output | [bit_outab_sel_top-1:0] 0 tx outlab sel frame x | Main Controller I/O List | 83 |
| o_tx2_outlab_sel_frame_x | output | [bit_outab_sel_top-1:0] 0 tx outlab sel frame x | Main Controller I/O List | 83 |
| o_tx3_outlab_sel_frame_x | output | [bit_outab_sel_top-1:0] 0 tx outlab sel frame x | Main Controller I/O List | 83 |
| o_tx4_outlab_sel_frame_x | output | [bit_outab_sel_top-1:0] 0 tx outlab sel frame x | Main Controller I/O List | 83 |
| o_tx_preset | output | 0 tx prese to analog domain | Main Controller I/O List | 83 |
| o_en_tx | output | [n_tx_channel-1:0] 0 tx enable to analog domain | Main Controller I/O List | 83 |
| o_PD_TIA | output | 1 enabling tia to analog domain | Main Controller I/O List | 83 |
| o_PD_PGA | output | 1 enabling buffer to analog domain | Main Controller I/O List | 83 |
| o_PD_IDAC | output | 1 enabling idac to analog domain | Main Controller I/O List | 83 |
| o_gsr_curr_on | output | 0 gsr curr on pilot to analog domain | Main Controller I/O List | 83 |
| o_gsr_on | output | 0 grs on on pilot to analog domain | Main Controller I/O List | 83 |
| o_ADC_en | output | 0 ADC enabling | Main Controller I/O List | 83 |
| o_half_charge_ldo | output | 0 | Main Controller I/O List | 83 |
| o_ADC_start | output | 0 ADC Start sampling | Main Controller I/O List | 83 |
| o_N_step2_to_reg | output | [rx_ch_gain_limit-1:0] 0 N_Step2 calibration value | Main Controller I/O List | 83 |
| o_adc_test_cap | output | [9:0] 0 adc test cap | Main Controller I/O List | 83 |
| o_adc_error_cap9 | output | [7:0] 0 adc calibration result | Main Controller I/O List | 83 |
| o_adc_error_cap8 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 83 |
| o_adc_error_cap7 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 83 |
| o_adc_error_cap6 | output | [6:0] 0 adc calibration result 83 | Main Controller I/O List | 83 |
| o_adc_error_cap5 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 84 |
| o_adc_error_cap4 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 84 |
| o_adc_error_cap3 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 84 |
| o_adc_error_cap2 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 84 |
| o_adc_error_cap1 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 84 |
| o_adc_error_cap0 | output | [6:0] 0 adc calibration result | Main Controller I/O List | 84 |
| o_pd_cm_buf | output | 1 power down common buffer | Main Controller I/O List | 84 |
| o_pd_rld | output | 1 power down rld | Main Controller I/O List | 84 |
| o_pd_avg1 | output | 1 power down avg1 | Main Controller I/O List | 84 |
| o_pd_avg2 | output | 1 power down avg2 | Main Controller I/O List | 84 |
| o_mc_ahb_clk_en | output | 0 enable for master ahb clock | Main Controller I/O List | 84 |
| o_main_controller_device_status_register | output | [2:0] 0 device status register | Main Controller I/O List | 84 |
| o_main_controller_elab_status_register | output | [3:0] 0 device status register | Main Controller I/O List | 84 |
| o_en_ldo_1v8 | output | 0 enable ldo | Main Controller I/O List | 84 |
| o_en_bufxbio | output | 0 enable biobuffer to analog domain | Main Controller I/O List | 84 |
| o_rx_ch_frame | output | [ppg_rx_channel_bit_top-1:0] 0 selected rx ch frame to analog domain | Main Controller I/O List | 84 |
| o_ldo_ext | output | 0 enable external ldo | Main Controller I/O List | 84 |
| o_ppg_status_register | output | [n_state_bit-1:0] 0 ppg state status register | Main Controller I/O List | 84 |
| o_b_cap_idac | output | [1:0] 0 b cap idac to analog domain | Main Controller I/O List | 84 |
| o_ispu_irq_ctrl | output | [3:0] 0 ispu irq | Main Controller I/O List | 84 |
| o_irq_start_measurement | output | 0 irq start measurement to GPIO | Main Controller I/O List | 84 |
| o_end_calibration | output | 1 end calibration to analog domain | Main Controller I/O List | 84 |
| o_alc_data | output | [data_out_size_bit_top+2:0] 0 alc data to regmap | Main Controller I/O List | 84 |
| o_ppg_data_raw | output | [data_out_size_bit_top+2:0] 0 ppg raw data to regmap 84 | Main Controller I/O List | 84 |
| o_pd_buf_gpio1 | output | 1 power down for buffer gpio1 | Main Controller I/O List | 85 |
| o_pd_buf_gpio2 | output | 1 power down for buffer gpio2 | Main Controller I/O List | 85 |
| o_adc_data_debug_alc_1 | output | [frame_ppg_debug_alc_top-1:0] 0 alc 1 registers data debug | Main Controller I/O List | 85 |
| o_adc_data_debug_alc_2 | output | [frame_ppg_debug_alc_top-1:0] 0 alc 2 registers data debug | Main Controller I/O List | 85 |
| o_adc_data_debug_ppg_raw | output | [frame_ppg_debug_ppg_raw_top- 1:0] 0 ppg raw registers data debug | Main Controller I/O List | 85 |
| o_en_lead_off | output | 0 mask lead off | Main Controller I/O List | 85 |
| o_mc_busy | output | 0 main controller is working | Main Controller I/O List | 85 |
| o_en_ck_m_p_q | output | 0 clock m and q bia | Main Controller I/O List | 85 |
| o_en_ck_chop_imp | output | 0 clock chopper bia | Main Controller I/O List | 85 |
| o_saturation_flag | output | [n_max_frame-1:0] 0 ppg saturation flag | Main Controller I/O List | 85 |
| o_en_ck_hc2_10k | output | 0 clock chipper ecg | Main Controller I/O List | 85 |
| o_en_clk_16MHz_sleep | output | 1 sleep signal for pmu | Main Controller I/O List | 85 |
| o_gsr_clk_en_16M | output | 0 enable clock for gsr channel | Main Controller I/O List | 85 |

## **3. Block requirements** {#3-block-requirements}


#### **IPOS-MAIN-CONTROLLER-001** {#ipos-main-controller-001}
During the Configuration Phase (IDLE STATE of the Device_FSM), the user shall be able to: • Configure Bio-Channel or Optical Channel, the ADC Calibration and then Start a measurement cycle. • Put the device in Debug-Mode. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0117

[End]


#### **IPOS-MAIN-CONTROLLER-002** {#ipos-main-controller-002}
• The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2] [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0118

[End]


#### **IPOS-MAIN-CONTROLLER-003** {#ipos-main-controller-003}
• The user shall select active channel, in this case only ECG0_SEL and DS_SEL (Data Storage Mode) in DEVICE_CONFIG_CHANNEL register writing 0x21. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0119

[End]


#### **IPOS-MAIN-CONTROLLER-004** {#ipos-main-controller-004}
• The user shall select a division index for ECG, configuring M_ECG_l and M_ECG_h in SET_ECG_FREQ_l register and SET_ECG_FREQ_h register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0120

[End]


#### **IPOS-MAIN-CONTROLLER-005** {#ipos-main-controller-005}
• The user shall set the number of clocks for sampling ECG data from ADC in ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0121

[End]


#### **IPOS-MAIN-CONTROLLER-006** {#ipos-main-controller-006}
• The User shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0122

[End]


#### **IPOS-MAIN-CONTROLLER-007** {#ipos-main-controller-007}
• The user shall start measurement writing register DEVICE_CONFIG_OPERATION [0] at 1. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0123

[End]


#### **IPOS-MAIN-CONTROLLER-008** {#ipos-main-controller-008}
• To check data in unique FIFO (default config) the user shall check the first MSB which will have to be equal to the table in DATA TAG Table. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0124

[End]


#### **IPOS-MAIN-CONTROLLER-009** {#ipos-main-controller-009}
[DDS_STBIO1_0125] Requirement: • The user shall configure the time slot duration in DEVICE_CONFIG_OPERATION register [4:2].

Covers: DDS_STBIO1_0125

[End]


#### **IPOS-MAIN-CONTROLLER-010** {#ipos-main-controller-010}
• The user shall select active channel, in this case ECG0_SEL, BIA_SEL and DS_SEL (Data Storage Mode) in DEVICE_CONFIG_CHANNEL writing 0x23. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0126

[End]


#### **IPOS-MAIN-CONTROLLER-011** {#ipos-main-controller-011}
• The user shall select a division index for ECG, configuring M_ECG_l and M_ECG_h in SET_ECG_FREQ_l register and SET_ECG_FREQ_h register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0127

[End]


#### **IPOS-MAIN-CONTROLLER-012** {#ipos-main-controller-012}
• The user shall select a division index for ECG, configuring M_BIA_l and M_BIA_h in SET_BIA_FREQ_l register and SET_BIA_FREQ_h register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0128

[End]


#### **IPOS-MAIN-CONTROLLER-013** {#ipos-main-controller-013}
• The user shall set number of clocks for sampling ECG and BIA data from ADC in ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0129

[End]


#### **IPOS-MAIN-CONTROLLER-014** {#ipos-main-controller-014}
• The user shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0130

[End]


#### **IPOS-MAIN-CONTROLLER-015** {#ipos-main-controller-015}
• The user shall set at 1 IMP_EN in IMP_CTRL register. [TO: IPOS_MAIN_CTRL]

Covers: DDS_STBIO1_0140

[End]


#### **IPOS-MAIN-CONTROLLER-016** {#ipos-main-controller-016}
The only registers that the user shall change after setting the mode_operation to 1 are the ones described in requirement 7096. All the Other signals shall change only with mode_operation set

Covers: IPOS_STBIO1_MAIN_CONTROLLER_002

[End]


#### **IPOS-MAIN-CONTROLLER-017** {#ipos-main-controller-017}
[Covers: DDS_STBIO1_0116] When the Device_FSM FSM is in BOOT State, that is DEVICE_STATUS_REG register [2:0]) == 0x01 (main_controller_status_register), it shall wait that the ADSP ends the BOOT Phase, checking when the i_quokka_boot_end is set high. When the BOOT Phase is ended, the Device_FSM FSM shall go to IDLE State, check that DEVICE_STATUS_REG register [2:0]) == 0x02, (main_controller_status_register), check that the w_en_ldo1v8 signal is set low and that

Covers: IPOS_STBIO1_MAIN_CONTROLLER_004

[End]


#### **IPOS-MAIN-CONTROLLER-018** {#ipos-main-controller-018}
When in unique_fifo_mode (i_multiple_fifo set to 0), if during a time slot an operation is done, the Main_Controller_FSM shall write the time_slot_data inside the FIFO with a dedicated tag. The value of the time_slot_data shall be referred to the start of the entire measurement cycle (for

Covers: IPOS_STBIO1_MAIN_CONTROLLER_008

[End]


#### **IPOS-MAIN-CONTROLLER-019** {#ipos-main-controller-019}
[Covers: DDS_STBIO1_0123] [Covers: DDS_STBIO1_0141] When in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, or BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is set high, or ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set high, or GSR_SEL (DEVICE_CONFIG_CHANNEL register [3]) is set high, or ADC_DO_CALIBRATION ( ADC_CAL_CONFIG register [0]) is set high, or WAVE_VELOCITY_MODE (GENERAL_PPG_PARAMETERS_1 register [4]) is set high together wit h PPG_SEL (DEVICE_CONFIG_CHANNEL register [4]), when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_CLKF shall go

Covers: IPOS_STBIO1_MAIN_CONTROLLER_009

[End]


#### **IPOS-MAIN-CONTROLLER-020** {#ipos-main-controller-020}
[Covers: DDS_STBIO1_0119] When the FSM is in IDLE State, if ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is high, HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 0, ECG0 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall go low and the Device_FSM FSM shall go to the WAIT_SU State , so the main_controller_status_register (DEVICE_STATUS_REG register

Covers: IPOS_STBIO1_MAIN_CONTROLLER_010

[End]


#### **IPOS-MAIN-CONTROLLER-021** {#ipos-main-controller-021}
When the HC_EN (ECG_CTRL register [0]) is set to 0 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL register [1]) is set to 1, ECG1 and ECG2 shall be active so, when MODE_OPERATION (DEVICE_CONFIG_OPERATION register [1:0] ) is set different from 0, the O_PD_HC2 shall remain high, O_PD_IMP shall go low and the Device_FSM shall go to the WAIT_SU State, so main_controller_status_register

Covers: IPOS_STBIO1_MAIN_CONTROLLER_011

[End]


#### **IPOS-MAIN-CONTROLLER-022** {#ipos-main-controller-022}
If the calibration has been done, the ADC_error_caps values computed shall reset only if the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_0152

[End]


#### **IPOS-MAIN-CONTROLLER-023** {#ipos-main-controller-023}
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is equal to 1, O_PD_IMP shall go low within 5 clock cycle at

Covers: IPOS_STBIO1_MAIN_CONTROLLER_016

[End]


#### **IPOS-MAIN-CONTROLLER-024** {#ipos-main-controller-024}
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1 and the IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, the O_IMP_CURINJ_PD shall go low. On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, the O_IMP_CURINJ_PD shall remain

Covers: IPOS_STBIO1_MAIN_CONTROLLER_017

[End]


#### **IPOS-MAIN-CONTROLLER-025** {#ipos-main-controller-025}
When DEVICE is in WAIT_SU, if IMP_EN (IMP_CTRL register [0]) signal is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1, 5ms after the falling of imp_curinj_pd and O_PD_IMP, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 1, O_CK_M, O_CK_P and O_CK_Q shall be generated from Clock generator block so they run at FREQ_BIA_CLK_m_p_q (EN_CHOP_FREQ_MOD_DEMOD register [4:3] ) and its values shall be chosen from 20kHz, 50kHz, 100kHz, 200kHz . On the other hand, if IMP_CURRINJ_EN (CURR_INJ register [3]) is equal to 0, ck_m, ck_p and

Covers: IPOS_STBIO1_MAIN_CONTROLLER_018

[End]


#### **IPOS-MAIN-CONTROLLER-026** {#ipos-main-controller-026}
When IMP_CURRINJ_EN (CURR_INJ register [3]) is high, O_CK_Q shall be run with a phase

Covers: IPOS_STBIO1_MAIN_CONTROLLER_019

[End]


#### **IPOS-MAIN-CONTROLLER-027** {#ipos-main-controller-027}
When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; 20ms after the falling of O_RST_IMP, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set to 1, O_CK_CHOP_IMP shall be generated from Clock generator block, so O_CK_CHOP_IMP shall be run at 10kHz frequency. On the other hand, if EN_CHOP_CLK_IMP (EN_CHOP_FREQ_MOD_DEMOD register [1]) is set

Covers: IPOS_STBIO1_MAIN_CONTROLLER_021

[End]


#### **IPOS-MAIN-CONTROLLER-028** {#ipos-main-controller-028}
When DEVICE_FSM FSM is in WAIT_SU state, if IMP_EN signal (IMP_CTRL register [0]) is equal to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL register [2]) is equal to 1; If i_su_hlt_dly is set to 0, 205ms after the falling of O_RSTI_IMP, O_SUG_IMP shall go low. Instead, if SU_DLY (EN_CHOP_FREQ_MOD_DEMOD register [2]) is set to 1, 755ms after the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_023

[End]


#### **IPOS-MAIN-CONTROLLER-029** {#ipos-main-controller-029}
When DEVICE_FSM FSM is in WAIT_SU STATE ( main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x03) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL register [0]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, after WAIT_SU state the device shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal

Covers: IPOS_STBIO1_MAIN_CONTROLLER_024

[End]


#### **IPOS-MAIN-CONTROLLER-030** {#ipos-main-controller-030}
When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and ECG1_ECG2_SEL (DEVICE_CONFIG_CHANNEL [1]) is set to 1, after WAIT_SU the device_fsm shall go in

Covers: IPOS_STBIO1_MAIN_CONTROLLER_026

[End]


#### **IPOS-MAIN-CONTROLLER-031** {#ipos-main-controller-031}
When DEVICE_FSM FSM is in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) if HC_EN (ECG_CTRL register [0]) is set to 1 and ECG0_SEL (DEVICE_CONFIG_CHANNEL [0]) is set to 1 and IMP_EN (IMP_CTRL register [0]) is set to 1 and BIA_SEL (DEVICE_CONFIG_CHANNEL [2]) is set to 1, after WAIT_SU, the device FSM shall go in OPERATIVE (DEVICE_STATUS_REG register [2:0] is equal to 0x04).

Covers: IPOS_STBIO1_MAIN_CONTROLLER_028

[End]


#### **IPOS-MAIN-CONTROLLER-032** {#ipos-main-controller-032}
When DEVICE_FSM FSM is in IDLE if PPG_SEL (DEVICE_CONFIG_CHANNEL [4]) is set to 1 and MODE_OPERATION (bit [1:0] on DEVICE_CONFIG_OPERATION register) is different to 0, the device shall go in PPG state (main_controller_status_register in ELAB_STATUS_REG register

Covers: IPOS_STBIO1_MAIN_CONTROLLER_029

[End]


#### **IPOS-MAIN-CONTROLLER-033** {#ipos-main-controller-033}
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) the device shall be execute a number of frames equal to N_PPG_FRAME (GENERAL_PPG_PARAMETERS_1 register [3:0]) (Check the i_id_frame shall increase until it’s equal to N_PPG_FRAME-1). At the beginning of each frame o_ADC_EN shall go high and it shall go low when ALC_COMPENSATION is performed or

Covers: IPOS_STBIO1_MAIN_CONTROLLER_030

[End]


#### **IPOS-MAIN-CONTROLLER-034** {#ipos-main-controller-034}
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x 05) o_ADC_start shall go high a number of times equal “2 ^ value indicated in regmap of FRAME_{n}_SAMPLES (FRAME_n_PARAMETERS_1 register [5:3]) for ALC and PPG both (2*(2^regmap_value). Except when FRAME_{n}_SAMPLES is equal to 3’b000, in this case o_ADC_start shall go high 3 times.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_031

[End]


#### **IPOS-MAIN-CONTROLLER-035** {#ipos-main-controller-035}
When DEVICE_FSM FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) during each frame o_Txi_idac_VREF shall go from 0 to N_MAX (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]). At first, o_Txi_idac_VREF shall be increase its value of N_START for next step o_Txi_idac_VREF shall

Covers: IPOS_STBIO1_MAIN_CONTROLLER_032

[End]


#### **IPOS-MAIN-CONTROLLER-036** {#ipos-main-controller-036}
When not in IDLE STATE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02) , Device_FSM shall go back in IDLE only if the user turns off the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_033

[End]


#### **IPOS-MAIN-CONTROLLER-037** {#ipos-main-controller-037}
When in OPERATIVE (main_controller_status_register (DEVICE_STATUS_REG register [2:0]) is equal to 0x02), if the time slot counter reach its limit, the Device_FSM shall go into the error state (DEVICE_STATUS_REGISTER) and raise an interrupt (o_error_time_slot) to the Digital_Top.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_034

[End]


#### **IPOS-MAIN-CONTROLLER-038** {#ipos-main-controller-038}
When DEVICE_FSM FSM is in Operative State (DEVICE_STATUS_REG register [2:0]==0x04), the o_MC_busy shall go to 1 and shall go to 0 one clock cycle after entering the SLEEP state if

Covers: IPOS_STBIO1_MAIN_CONTROLLER_035

[End]


#### **IPOS-MAIN-CONTROLLER-039** {#ipos-main-controller-039}
When in Sleep Mode, the device shall go back to the Operative State if no error (o_error_irq stuck at 0) occurs and all the operations are ended . Furthermore, if no Bio -Channel operations are selected and more than 150us are left before the start of a new time slot, the o_pd_clkf (Digital

Covers: IPOS_STBIO1_MAIN_CONTROLLER_036

[End]


#### **IPOS-MAIN-CONTROLLER-040** {#ipos-main-controller-040}
In a Time Slot, when a BIO-Channel operation is selected, o_en_bufxbio signal (in Digital Top) shall go high at least a configurable time (Device Config Operation [6:5]) before selecting the first

Covers: IPOS_STBIO1_MAIN_CONTROLLER_037

[End]


#### **IPOS-MAIN-CONTROLLER-041** {#ipos-main-controller-041}
When the ELAB_FSM is in ECG State, the ADC_Mux (concatenation of {o_adc_mux_sel, o_adc_mux_bio_channel} on digital top) output shall be set equal to 001 and after 4 acquisitions (described in section 5.4 ADC PHASE) shall be set to 010. If ECG1 and ECG2 are selected, the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_038

[End]


#### **IPOS-MAIN-CONTROLLER-042** {#ipos-main-controller-042}
When ELAB FSM is in PPG state (main_controller_status_register in ELAB_STATUS_REG register [3:0] shall be equal to 0x05) or a WAIT_END_OPERATIVE State, o_en_biobuffer shall

Covers: IPOS_STBIO1_MAIN_CONTROLLER_039

[End]


#### **IPOS-MAIN-CONTROLLER-043** {#ipos-main-controller-043}
When i_rstn is asserted low, all the output shall be set to 0, except for count_cap that shall be set

Covers: IPOS_STBIO1_MAIN_CONTROLLER_044

[End]


#### **IPOS-MAIN-CONTROLLER-044** {#ipos-main-controller-044}
The o_adc_ready shall be set to 1 when the ADC is getting ready (o_adc_en is set to 1 but not

Covers: IPOS_STBIO1_MAIN_CONTROLLER_045

[End]


#### **IPOS-MAIN-CONTROLLER-045** {#ipos-main-controller-045}
When the calibration phase is ended, the o_end_cal_phase shall be set to 1 and shall stay high

Covers: IPOS_STBIO1_MAIN_CONTROLLER_047

[End]


#### **IPOS-MAIN-CONTROLLER-046** {#ipos-main-controller-046}
When ECG, BIA or GSR Is sampled, i_ADC_en is equal to 1, the o_ADC_clk_en shall be set to 1.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_049

[End]


#### **IPOS-MAIN-CONTROLLER-047** {#ipos-main-controller-047}
[Covers: DDS_STBIO1_0121] [Covers: DDS_STBIO1_0129] The Sampling Phase shall be configurable by the user with i_N_clk values from 0 up to 63. This

Covers: IPOS_STBIO1_MAIN_CONTROLLER_051

[End]


#### **IPOS-MAIN-CONTROLLER-048** {#ipos-main-controller-048}
When the i_ADC_en_mc and i_adc_en_mask is set to 0, all the output shall be set to 0, except for the o_end_cal_phases and o_ADC_clk_en. The o_end_cal_phases shall be set to 1 if i_do_calibration (bit 0 of ADC_CAL_CONFIG) is set to 0, otherwise shall be set to 0 until the end

Covers: IPOS_STBIO1_MAIN_CONTROLLER_052

[End]


#### **IPOS-MAIN-CONTROLLER-049** {#ipos-main-controller-049}
When the i_ADC_en_mc and i_adc_en_mask is set to 1, at least 160 clock cycles shall pass before

Covers: IPOS_STBIO1_MAIN_CONTROLLER_053

[End]


#### **IPOS-MAIN-CONTROLLER-050** {#ipos-main-controller-050}
When the ADC_phases fsm is ready and an acquisition is required, the o_ADC_start shall stay

Covers: IPOS_STBIO1_MAIN_CONTROLLER_054

[End]


#### **IPOS-MAIN-CONTROLLER-051** {#ipos-main-controller-051}
After an acquisition is started, the ADC_Phases shall wait for the i_ADC_EOC sampling the new

Covers: IPOS_STBIO1_MAIN_CONTROLLER_055

[End]


#### **IPOS-MAIN-CONTROLLER-052** {#ipos-main-controller-052}
The calibration phase shall set the adc_error_cap8…0 to the correct value, following the calibration

Covers: IPOS_STBIO1_MAIN_CONTROLLER_058

[End]


#### **IPOS-MAIN-CONTROLLER-053** {#ipos-main-controller-053}
If the i_noise signal is set to 1 when the DEVICE_FSM is into PPG State, the i_n_avarage shall

Covers: IPOS_STBIO1_MAIN_CONTROLLER_059

[End]


#### **IPOS-MAIN-CONTROLLER-054** {#ipos-main-controller-054}
When the last acquisition is performed, after the last i_ADC_EOC arrived, the ADC_phases shall

Covers: IPOS_STBIO1_MAIN_CONTROLLER_060

[End]


#### **IPOS-MAIN-CONTROLLER-055** {#ipos-main-controller-055}
When the i_data_out_adc is sampled, the 15 bit (MSB in little endian), shall be negated in order to

Covers: IPOS_STBIO1_MAIN_CONTROLLER_061

[End]


#### **IPOS-MAIN-CONTROLLER-056** {#ipos-main-controller-056}
When i_debug_calibration is set (second bitfield of ADC_CAL_CONFIG ), the number of samples used by the avarage block during the calibration shall be set to 2. (The purpose of this mode is to

Covers: IPOS_STBIO1_MAIN_CONTROLLER_062

[End]


#### **IPOS-MAIN-CONTROLLER-057** {#ipos-main-controller-057}
When i_debug_adc_error_cap8_0_bypass is set to 1 (set to 1 en_debug_adc_error_cap8_0_bypass of ADC_GENERAL_DEBUG_0 ), the calibration result shall be bypassed in favor of the value written inside the registers

Covers: IPOS_STBIO1_MAIN_CONTROLLER_063

[End]


#### **IPOS-MAIN-CONTROLLER-058** {#ipos-main-controller-058}
When the adc_readout_bypass mode is enabled by the 2 bitfield ADC_GENERAL_DEBUG_0 , the sampling phase of the ADC Phgen shall be bypassed in favor of regmap. In particular, the Sampling phase shall be controlled by the register EN_ADC_DEBUG and EN_ADC_START in ADC_GENERAL_DEBUG_0 and the sampled data shall be written in ADC_DATA_OUT_DEBUG_LOW and ADC_DATA_OUT_DEBUG_HIGH. and In this mode, before start a new sampling operation, the RESET_DEBUG_ADC DATA in

Covers: IPOS_STBIO1_MAIN_CONTROLLER_064

[End]


#### **IPOS-MAIN-CONTROLLER-059** {#ipos-main-controller-059}
When the i_hc_en is set to 0 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 2, ECG1 and ECG2 shall be active so the o_pd_hc2 shall remain high, o_pd_imp_from_bia shall go low

Covers: IPOS_STBIO1_MAIN_CONTROLLER_073

[End]


#### **IPOS-MAIN-CONTROLLER-060** {#ipos-main-controller-060}
When the i_hc_en is set to 1 and i_imp_en is set to 1 and i_n_ecg_channel is equal to 3, ECG0- ECG1 and ECG2 shall be active so the o_pd_hc2 shall go low, o_pd_imp shall go low and

Covers: IPOS_STBIO1_MAIN_CONTROLLER_074

[End]


#### **IPOS-MAIN-CONTROLLER-061** {#ipos-main-controller-061}
20ms after that the o_rst_hc2 is gone low, if i_clk_hlt_en is equal to 1, chopper_clock shall be generated and after another 10ms, o_rsti_hc2 shall go low. Instead, if i_clk_hlt_en is equal to 0,

Covers: IPOS_STBIO1_MAIN_CONTROLLER_077

[End]


#### **IPOS-MAIN-CONTROLLER-062** {#ipos-main-controller-062}
If i_su_hlt_dly is set to 0. At least after 205ms that the o_rsti_hc2 is gone low, o_su_hc2 shall go

Covers: IPOS_STBIO1_MAIN_CONTROLLER_078

[End]


#### **IPOS-MAIN-CONTROLLER-063** {#ipos-main-controller-063}
When the user selects an operative mode that includes the BIA channel, a start-up shall be done.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_080

[End]


#### **IPOS-MAIN-CONTROLLER-064** {#ipos-main-controller-064}
When i_imp_curinj signal is equal to 1, the o_imp_curinj_pd shall go low. On the other hand, if

Covers: IPOS_STBIO1_MAIN_CONTROLLER_082

[End]


#### **IPOS-MAIN-CONTROLLER-065** {#ipos-main-controller-065}
At least 5ms after the falling of o_imp_curinj_pd and o_pd_imp_from_bia, if i_imp_curinj is equal to 1, o_en_ck_m_p_q shall be high and ck_m, ck_p and ck_q shall be generated from Clock generator block. On the other hand, if i_imp_curinj is equal to 0, the ck_m_p_q shall stay low.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_083

[End]


#### **IPOS-MAIN-CONTROLLER-066** {#ipos-main-controller-066}
20ms after the falling of o_rst_imp, if i_clk_imp_en is set to 1, the o_en_ck_chop_imp shall be high and ck_chop_imp shall be generated from Clock generator block. On the hand, if i_clk_imp_en is

Covers: IPOS_STBIO1_MAIN_CONTROLLER_085

[End]


#### **IPOS-MAIN-CONTROLLER-067** {#ipos-main-controller-067}
If i_su_hlt_dly is set to 0,at least 205 ms after the falling of o_rsti_imp, o_sug_imp shall go low. Instead, if i_su_hlt_dly is set to 1, 755ms after the falling of o_rsti_imp, o_sug_imp shall go low.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_087

[End]


#### **IPOS-MAIN-CONTROLLER-068** {#ipos-main-controller-068}
The i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] shall define how many time slots pass between two GSR acquisitions following this formula: GSRdata = time_slot 2 ∗ m_gsr

Covers: IPOS_STBIO1_MAIN_CONTROLLER_088

[End]


#### **IPOS-MAIN-CONTROLLER-069** {#ipos-main-controller-069}
If the en_gsr_cds [bit 3 of GSR_CTRL] is set High, the i_m_gsr shall define also in which time slot after the GSR_Curr_on falls from 1 to 0, an acquisition without current injection (o_gsr_curr_on set

Covers: IPOS_STBIO1_MAIN_CONTROLLER_089

[End]


#### **IPOS-MAIN-CONTROLLER-070** {#ipos-main-controller-070}
If en_gsr_cds is set low [bit 3 of GSR_CTRL], the gsr_curr_on shall set high in every time slot

Covers: IPOS_STBIO1_MAIN_CONTROLLER_092

[End]


#### **IPOS-MAIN-CONTROLLER-071** {#ipos-main-controller-071}
If en_gsr_cds is set high [bit 3 of GSR_CTRL] the GSR_SNS (acquisition with o_gsr_curr_on set to 1) and GSR_CDS (acquisition with o_gsr_curr_on set to 0) shall be sampled 16 times, then mediated to get one single value for each of them, and then the final result shall be the subtraction between GSR_SNS and GSR_CDS. On the other hand, If en_gsr_cds is set low, no acquisition of GSR_CDS shall be done and the result shall be the average of 16 acquisitions of

Covers: IPOS_STBIO1_MAIN_CONTROLLER_093

[End]


#### **IPOS-MAIN-CONTROLLER-072** {#ipos-main-controller-072}
When only GSR is selected (NO ECG0 and PPG are selected), if i_m_gsr [SET_GSR_FREQ_h and SET_GSR_FREQ_l] is greater than 0, the Device FSM shall go in SLEEP after the IDLE State and shall go back in Operative State only when the measurement shall be run or, in case of

Covers: IPOS_STBIO1_MAIN_CONTROLLER_094

[End]


#### **IPOS-MAIN-CONTROLLER-073** {#ipos-main-controller-073}
The o_En_TIA, o_EN_Buff, o_EN_ADC and o_EN_IDAC shall be high when the PPG_FSM is

Covers: IPOS_STBIO1_MAIN_CONTROLLER_095

[End]


#### **IPOS-MAIN-CONTROLLER-074** {#ipos-main-controller-074}
When the i_m_ppg ( SET_PPG_FREQ_h and SET_PPG_FREQ_l) is different from 0 and PPG_SEL in DEVICE_CONFIG_CHANNEL register is set to 1, when the ELAB_FSM is in PPG STATE, PPG_IOFF_CALIB or PPG_ALC_STORAGE, the i_start_operation_for_ppg shall be set

Covers: IPOS_STBIO1_MAIN_CONTROLLER_096

[End]


#### **IPOS-MAIN-CONTROLLER-075** {#ipos-main-controller-075}
When in ALC Compensation, the PPG FSM shall raise the o_start_alc_comp signal to the ALC

Covers: IPOS_STBIO1_MAIN_CONTROLLER_098

[End]


#### **IPOS-MAIN-CONTROLLER-076** {#ipos-main-controller-076}
When in ALC Compensation, the PPG shall wait that the rise of i_end_compensation signal from the ALC Compensation block to go into the RX_Start_UP state. This shall happen in OPERATIVE.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_099

[End]


#### **IPOS-MAIN-CONTROLLER-077** {#ipos-main-controller-077}
When in Rx_Start_Up state, the o_tx_Preset shall be set 0, the en_tx_i shall be set to 1, the o_BIDAC shall maintain the value reached during the ALC Compensation summed up, if i_ppg_ioff_calibration is enabled, with the IOFF_OFFSET computed during the IOFF Calibration

Covers: IPOS_STBIO1_MAIN_CONTROLLER_100

[End]


#### **IPOS-MAIN-CONTROLLER-078** {#ipos-main-controller-078}
[Covers: DDS_STBIO1_0118] [Covers: DDS_STBIO1_0125] The user shall configure time slot duration in DEVICE_CONFIG_OPERATION register [4:2]

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1004

[End]


#### **IPOS-MAIN-CONTROLLER-079** {#ipos-main-controller-079}
The user shall configure which channel is selected and if work in Data Storage mode for the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1005

[End]


#### **IPOS-MAIN-CONTROLLER-080** {#ipos-main-controller-080}
[Covers: DDS_STBIO1_0120] [Covers: DDS_STBIO1_0122] [Covers: DDS_STBIO1_0127] [Covers: DDS_STBIO1_0130] In Order to enable an ECG0 Channel Operation, the user shall always select the ECG0 channel

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1007

[End]


#### **IPOS-MAIN-CONTROLLER-081** {#ipos-main-controller-081}
[Covers: DDS_STBIO1_0128] [Covers: DDS_STBIO1_0140] In Order to enable a BIA Channel Operation, the user shall always select the BIA channel

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1008

[End]


#### **IPOS-MAIN-CONTROLLER-082** {#ipos-main-controller-082}
In Order to enable a GSR Channel Operation, the user shall always select the GSR channel

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1009

[End]


#### **IPOS-MAIN-CONTROLLER-083** {#ipos-main-controller-083}
When in Rx_Start_Up state, the PPG_FSM shall stay in this state for the T_rx_set time (GENERAL_PPG_PARAMETERS_3 register [3:0])) and then go into the FIRST_ALC_SAMPLES

Covers: IPOS_STBIO1_MAIN_CONTROLLER_101

[End]


#### **IPOS-MAIN-CONTROLLER-084** {#ipos-main-controller-084}
In Order to enable a PPG Channel Operation, the user shall always select the PPG channel

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1010

[End]


#### **IPOS-MAIN-CONTROLLER-085** {#ipos-main-controller-085}
In Order to enable an ECG1_ECG2 Channel Operation, the user shall always select the ECG1_ECG2 channel (DEVICE_CONFIG_CHANNEL), set the i_M_ECG greater than zero and

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1011

[End]


#### **IPOS-MAIN-CONTROLLER-086** {#ipos-main-controller-086}
When in FIRST_ALC_SAMPLES state, the o_start_ADC signal shall be set high until

Covers: IPOS_STBIO1_MAIN_CONTROLLER_102

[End]


#### **IPOS-MAIN-CONTROLLER-087** {#ipos-main-controller-087}
When in FIRST_ALC_SAMPLES state, the PPG_FSM Shall stay in this state until 1 clock cycle after the rise of the i_end_average and the TX_start_up time has passed. After that, the PPG FSM

Covers: IPOS_STBIO1_MAIN_CONTROLLER_103

[End]


#### **IPOS-MAIN-CONTROLLER-088** {#ipos-main-controller-088}
Once in the ERROR state, the user shall wait 1ms before set to 0 the MODE_OPERATION to go

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1034

[End]


#### **IPOS-MAIN-CONTROLLER-089** {#ipos-main-controller-089}
When in FIRST_ALC_SAMPLES state, when i_end_average is set to 1, the o_start_digital_ramp signal shall be set high to start the rising of the digital ramp and go into the RISING_RAMP state.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_104

[End]


#### **IPOS-MAIN-CONTROLLER-090** {#ipos-main-controller-090}
When in Rising_Ramp state, at the half of Rising_time, the o_idac_dc_ppg_frame shall be set to the IDAC_DC_PPG_FRAME_{n} (FRAME_n_PARAMETERS_5 register [5:0]) value related to the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_105

[End]


#### **IPOS-MAIN-CONTROLLER-091** {#ipos-main-controller-091}
When in Rising_Ramp State, the PPG_FSM shall stay in this state until the end of the Rising Time

Covers: IPOS_STBIO1_MAIN_CONTROLLER_106

[End]


#### **IPOS-MAIN-CONTROLLER-092** {#ipos-main-controller-092}
When in Measurement state, the PPG_FSM shall stay in this state until the rising of the i_end_average signal from the ADC block. After that, the PPG_FSM shall bring itself into the Falling

Covers: IPOS_STBIO1_MAIN_CONTROLLER_108

[End]


#### **IPOS-MAIN-CONTROLLER-093** {#ipos-main-controller-093}
When in MEASUREMENT State, the o_falling_digital_ramp signal shall be set to 1 to go into the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_109

[End]


#### **IPOS-MAIN-CONTROLLER-094** {#ipos-main-controller-094}
The o_pd_tia, o_pd_idac and o_pd_pga shall be the negated version the o_en_tia, o_en_idac

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1095

[End]


#### **IPOS-MAIN-CONTROLLER-095** {#ipos-main-controller-095}
When in Falling_Ramp State, at the half of the Falling_Time the o_idac_dc_ppg_frame shall be

Covers: IPOS_STBIO1_MAIN_CONTROLLER_110

[End]


#### **IPOS-MAIN-CONTROLLER-096** {#ipos-main-controller-096}
Tx Preset shall be set to 1 a configurable TX_Preset_Step time before the start of the Digital

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1102

[End]


#### **IPOS-MAIN-CONTROLLER-097** {#ipos-main-controller-097}
Tx Preset shall be set to 0 before the rising phase(i_start_digtal_ramp) and after the falling phase

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1104

[End]


#### **IPOS-MAIN-CONTROLLER-098** {#ipos-main-controller-098}
When in Falling_Ramp state, the PPG_FSM shall stay in this state until the end of the Falling Time (depends on the user's configuration of Digital Ramp parameters) and bring itself into the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_111

[End]


#### **IPOS-MAIN-CONTROLLER-099** {#ipos-main-controller-099}
When the Ioff Calibration algorithm is enabled, it shall be performed every time a new

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1116

[End]


#### **IPOS-MAIN-CONTROLLER-100** {#ipos-main-controller-100}
When in SECOND_ALC_SAMPLES state, the o_en_Txi shall be set low after the end at least of the T_tx_ledoff time (TX_LEDOFF_FRAME_{n}) and the o_start_adc signal shall be set to 1.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_112

[End]


#### **IPOS-MAIN-CONTROLLER-101** {#ipos-main-controller-101}
When in SECOND_ALC_SAMPLES state, the PPG_FSM shall stay in this state until the rise of the end_of_conversion signal from the ADC block. After that, if there are no more frames to run, the PPG_FSM shall go into the Reset State, otherwise, if there are other frames to run and channel rx is not changed, the PPG_FSM shall go into the Rx_start_up phase. On the other hand, if there are other frame to run and rx_channel is changed, the PPG_FSM shall go into the RESET_PPG

Covers: IPOS_STBIO1_MAIN_CONTROLLER_113

[End]


#### **IPOS-MAIN-CONTROLLER-102** {#ipos-main-controller-102}
The PPG Noise Data shall be accumulated in two phases, the first when the PPG FSM state is in FIRST_ALC_SAMPLES States and the second when the PPG FSM state is in the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1139

[End]


#### **IPOS-MAIN-CONTROLLER-103** {#ipos-main-controller-103}
For GSR Operation, if i_en_cds is set 0, the behavior shall as described in Requirement 143, otherwise the o_write_enabled shall be asserted when i_end_of_coversion is set to 1 and i_n_average_ecg_bia_gsr is equal to their limit values when the measurement is done with

Covers: IPOS_STBIO1_MAIN_CONTROLLER_1143

[End]


#### **IPOS-MAIN-CONTROLLER-104** {#ipos-main-controller-104}
At the end of each Frame, the start_avarage signal shall be rise to the Average block computation. Once the Average is computed, if no averages_between_equal_frames option is selected, the data shall be written inside the FIFO Memory using the Main Control ler AHB Master interface. If there is avareges_between_equal_frames option selected from regmap, after the computations of this average, the obtained data shall be written inside the FIFO Memory using the Main Controller AHB

Covers: IPOS_STBIO1_MAIN_CONTROLLER_115

[End]


#### **IPOS-MAIN-CONTROLLER-105** {#ipos-main-controller-105}
When the input signal o_Tx_preset is set to 1, the o_Tx_Vref shall increment the first step at value i_N_start (DIGITAL_RAMP_CONFIG_PARAM_3 register [2:0]) at a time i_T_preset

Covers: IPOS_STBIO1_MAIN_CONTROLLER_118

[End]


#### **IPOS-MAIN-CONTROLLER-106** {#ipos-main-controller-106}
When the i_falling_digital_ramp is set to 1, the o_TX_Vref shall decrement from N_MAX value (DIGITAL_RAMP_CONFIG_PARAM_1 register [3:0]) to zero with a step equal to 1 every 2-clock

Covers: IPOS_STBIO1_MAIN_CONTROLLER_120

[End]


#### **IPOS-MAIN-CONTROLLER-107** {#ipos-main-controller-107}
When ALC_COMP starts, o_BTIA_gain (2:0) shall be set at i_gain_start (PPG_ALC_CONFIG_PARAM_2 register [4:2]) and o_w_BTIA_ALC (8:0) shall be set at

Covers: IPOS_STBIO1_MAIN_CONTROLLER_126

[End]


#### **IPOS-MAIN-CONTROLLER-108** {#ipos-main-controller-108}
When ECG0 and BIA are selected 21 acquisitions shall be required (acquisitions described in section 5.4 ADC PHASE) and then device shall go in SLEEP (DEVICE_STATUS_REG register

Covers: IPOS_STBIO1_MAIN_CONTROLLER_128

[End]


#### **IPOS-MAIN-CONTROLLER-109** {#ipos-main-controller-109}
According to time diagram, when in RESET_PPG and ELAB_FSM is in PPG state during the first frame (i_id_frame=0) , shall be wait a configurable time PPG_START_UP_TIME (PPG_START_UP_TIME starting from when i_start_operation_ppg is set to 1 and at least 1 clock

Covers: IPOS_STBIO1_MAIN_CONTROLLER_134

[End]


#### **IPOS-MAIN-CONTROLLER-110** {#ipos-main-controller-110}
The average block shall perform an average on 4 Samples for each of ECG_x_AC, BIA AC P, BIA AC Q, BIA DC P and BIA DC Q , 1 Sample ECG_x_DC (Check if the i_end_of_coversion rise the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_137

[End]


#### **IPOS-MAIN-CONTROLLER-111** {#ipos-main-controller-111}
The average block shall perform the average on 16 sample acquisition for GSR. When the CDS mode is enabled, the average block shall perform a n average on 16 sample acquisition on GSR ON and 16 sample acquisition on GSR OFF, then shall perform a subtraction operation between

Covers: IPOS_STBIO1_MAIN_CONTROLLER_138

[End]


#### **IPOS-MAIN-CONTROLLER-112** {#ipos-main-controller-112}
Once the PPG Raw Data and PPG Noise reach the i_n_average_ppg value , depending on the ALC Mask bit value, the two accumulated shall be subtracted and final results shall be computed as follow: I_N_Average_PPG Samples Result with ALC MASK=0 Result with ALC Mask=1 0 3= (N1+P+N2) (Acc_P-(Acc_N)/2) * 8 Acc_P*16 2 4= (N1+2P+N2) (Acc_P -(Acc_N)) * 4 Acc_P *8 4 8= (2N1+4P+2N2) (Acc_P -(Acc_N)) * 2 Acc_P *4 8 16= (4N1+8P+4N2) (Acc_P -(Acc_N)) Acc_P *2 16 32= (8N1+16P+8N2) (Acc_P -(Acc_N))/2 Acc_P 32 64= (16N1+32P+16N2) (Acc_P -(Acc_N))/4 Acc_P /2 64 128= (32N1+64P+32N2) (Acc_P -(Acc_N))/8 Acc_P /4 128 256= (64N1+128P+64N2) (Acc_P -(Acc_N))/16 Acc_P /8 Table 18: PPG Result Table Where PPG Raw Data is indicated as P and PPG Noise is indicated as N1 and N2, while Acc_P

Covers: IPOS_STBIO1_MAIN_CONTROLLER_140

[End]


#### **IPOS-MAIN-CONTROLLER-113** {#ipos-main-controller-113}
When i_frame_ppg_debug is set to a value greater than 0 and i_n_average_ppg is set to a value between 1 and 16, all the ADC output (i_data_in) for ALC (i_data_valid_noise_ppg_adc set to 1) and PPG data (i_data_valid_ppg_adc) shall be stored in o_adc_data_debug_alc_2,

Covers: IPOS_STBIO1_MAIN_CONTROLLER_2143

[End]


#### **IPOS-MAIN-CONTROLLER-114** {#ipos-main-controller-114}
[Covers: DDS_STBIO1_0124] [Covers: DDS_STBIO1_0142] The data written in FIFO shall have the following tag: DATA TYPE BIT: 23 - 20 BIT: 19 - 16 BIT: 15 - 0 PPG FRAME 0 0000 DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT DATA 20 BIT PPG FRAME 1 0001 PPG FRAME 2 0010 PPG FRAME 3 0011 PPG FRAME 4 0100 PPG FRAME 5 0101 PPG FRAME 6 0110 PPG FRAME 7 0111 PPG FRAME 8 1000 PPG FRAME 9 1001 PPG FRAME 10 1010 PPG FRAME 11 1011 TIME SLOT DATA 1111 0000 DATA 16 BIT ECG0_AC 1100 0000 DATA 16 BIT ECG0_DC 1101 0000 DATA 16 BIT ECG1_AC 1100 0001 DATA 16 BIT ECG1_DC 1101 0001 DATA 16 BIT ECG2_AC 1100 0010 DATA 16 BIT ECG2_DC 1101 0010 DATA 16 BIT

Covers: IPOS_STBIO1_MAIN_CONTROLLER_2144

[End]


#### **IPOS-MAIN-CONTROLLER-115** {#ipos-main-controller-115}
The Frame shall work as follows: 1. Select how many times a particular frame shall be repeated 2. The result of each repetition shall be obtained as explained in [IPOS_STBIO1_MAIN_CONTROLLER_1 40] REQUIREMENT 3. After the last repetition has been accumulated, the data output shall be obtained dividing by the number of repeated frames the accumulated data to obtain a 20 bit data. The final result shall be computed as follows: Number of times the Frame has been repeated Result 2 (Res_F_R1 + Res_F_R2)/2 4 (Res_F_R1 + Res_F_R2+Res_F_R3+Res_F_R4)/4 8 (Res_F_R1 + Res_F_R2+Res_F_R3+…..+Res_F_R8)/8 Table 20: Frame Repetitions Result Computation table Where Res_F_Rx stands for Result_frame_Repeated_times (Example: RES_F_R2 refers to the result of the second repetition of the frame.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_2145

[End]


#### **IPOS-MAIN-CONTROLLER-116** {#ipos-main-controller-116}
In case the ppg sample data are equal (once converted in two’s complement) at 0x8000 or 0x7FFF for at least half of the selected average (example, if 128 acquisitions are selected, the threshold shall be greater or equal to 64), o_saturation_flag shall be set to 1 and shall go to 0 at the start of the next frame or frame repetition.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_2146

[End]


#### **IPOS-MAIN-CONTROLLER-117** {#ipos-main-controller-117}
When the ELAB_FSM is in ECG State and only ECG0 is selected, the o_ADC_EN shall go high,

Covers: IPOS_STBIO1_MAIN_CONTROLLER_3124

[End]


#### **IPOS-MAIN-CONTROLLER-118** {#ipos-main-controller-118}
When ELAB_FSM is in ECG state and ECG1 and ECG2 are selected , o_ADC_EN shall go high and 10 acquisitions are required (acquisitions described in chapter in section 5.4 ADC PHASE).

Covers: IPOS_STBIO1_MAIN_CONTROLLER_3125

[End]


#### **IPOS-MAIN-CONTROLLER-119** {#ipos-main-controller-119}
When ELAB_FSM is in ECG state and EC0, ECG1 and ECG2 are selected , o_ADC_EN shall go high and15 acquisitions are required (acquisitions described in 5.4 ADC PHASE) and then device

Covers: IPOS_STBIO1_MAIN_CONTROLLER_3126

[End]


#### **IPOS-MAIN-CONTROLLER-120** {#ipos-main-controller-120}
When ELAB_FSM is in BIA state , o_ADC_EN shall go high and 16 acquisitions are required (acquisitions described in section 5.4 ADC PHASE ) and then device shall go in

Covers: IPOS_STBIO1_MAIN_CONTROLLER_3127

[End]


#### **IPOS-MAIN-CONTROLLER-121** {#ipos-main-controller-121}
When the wave velocity mode is selected and the device FSM is in WAIT_SU, the Elaboration FSM shall go into the TIMER BUFFER State and then into the PPG ALC STORAGE

Covers: IPOS_STBIO1_MAIN_CONTROLLER_3128

[End]


#### **IPOS-MAIN-CONTROLLER-122** {#ipos-main-controller-122}
When the ppg ioff calibration and the adc calibration are selected, the adc calibration shall be

Covers: IPOS_STBIO1_MAIN_CONTROLLER_3129

[End]


#### **IPOS-MAIN-CONTROLLER-123** {#ipos-main-controller-123}
If i_rst_async_ecg is set to 1, the start-up phase shall restart but no clock shall stop if enabled.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_4079

[End]


#### **IPOS-MAIN-CONTROLLER-124** {#ipos-main-controller-124}
If i_rst_async_ecg is set to 1, it shall go to zero at least 5ms after that o_su_hc2 is set to 0.

Covers: IPOS_STBIO1_MAIN_CONTROLLER_4080

[End]


#### **IPOS-MAIN-CONTROLLER-125** {#ipos-main-controller-125}
If i_rst_async_bia is set to 1, the start-up phase shall restart but no clock shall stop if

Covers: IPOS_STBIO1_MAIN_CONTROLLER_4090

[End]


#### **IPOS-MAIN-CONTROLLER-126** {#ipos-main-controller-126}
If i_rst_async_bia is set to 1, it shall go to zero at least 5ms after that the o_sug_imp is set to 0

Covers: IPOS_STBIO1_MAIN_CONTROLLER_4091

[End]


#### **IPOS-MAIN-CONTROLLER-127** {#ipos-main-controller-127}
When in Sleep Mode and no Bio-Channel are selected, if every elaboration is ended and there are at least 34 clock cycles at 32kHz before the start of a new time slot, the o_en_ldo_1v8 shall go

Covers: IPOS_STBIO1_MAIN_CONTROLLER_436

[End]


#### **IPOS-MAIN-CONTROLLER-128** {#ipos-main-controller-128}
The max value that the user shall use for every m_channel (m_ecg, m_bia, m_gsr and m_ppg) is

Covers: IPOS_STBIO1_MAIN_CONTROLLER_5004

[End]


#### **IPOS-MAIN-CONTROLLER-129** {#ipos-main-controller-129}
If the user set a value greater than 1024 into ones of the m_channel (see req 5004), the value shall clamp at 1024 (check the input i_m_ecg, i_m_bia, i_m_gsr or i_m_ppg into the main

Covers: IPOS_STBIO1_MAIN_CONTROLLER_5005

[End]


#### **IPOS-MAIN-CONTROLLER-130** {#ipos-main-controller-130}
[Covers: DDS_STBIO1_1114] The State WAIT_SU shall not be considered interruptible. If the user wants to interrupt the WAIT_SU state, it shall perform the Soft Reset procedure described in the DDS

Covers: IPOS_STBIO1_MAIN_CONTROLLER_5015

[End]


#### **IPOS-MAIN-CONTROLLER-131** {#ipos-main-controller-131}
When an ECG, BIA or GSR Operation is selected and DS_SEL is set to 0, The DATA Output for these two channels shall be written in the following regmap registers ECG0_AC ECG0_DC ECG1_BIA_P_AC ECG1_BIA_P_DC ECG2_BIA_Q_AC ECG2_BIA_Q_DC GSR_RESULT

Covers: IPOS_STBIO1_MAIN_CONTROLLER_5016

[End]


#### **IPOS-MAIN-CONTROLLER-132** {#ipos-main-controller-132}
i_rst_async_bia shall be used also to reset the START-UP phase for ECG channel 1 and

Covers: IPOS_STBIO1_MAIN_CONTROLLER_5092

[End]


#### **IPOS-MAIN-CONTROLLER-133** {#ipos-main-controller-133}
When i_wave_velocity mode is enabled together with the DISABLE_ALC, the PPG_ALC_STORAGE shall be performed but once the Device goes into OPERATIVE State, the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_6070

[End]


#### **IPOS-MAIN-CONTROLLER-134** {#ipos-main-controller-134}
When i_wave_velocity_mode is set to 1, the ALC Compensation shall be set only when the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_6098

[End]


#### **IPOS-MAIN-CONTROLLER-135** {#ipos-main-controller-135}
When i_ALC_comp_start is set to 1, the first rise of the o_comp_rx_ck shall happen at least after

Covers: IPOS_STBIO1_MAIN_CONTROLLER_6129

[End]


#### **IPOS-MAIN-CONTROLLER-136** {#ipos-main-controller-136}
All the PPG_FSM state shall be checked using the PPG_STATUS_REGISTER in Regmap (the

Covers: IPOS_STBIO1_MAIN_CONTROLLER_7095

[End]


#### **IPOS-MAIN-CONTROLLER-137** {#ipos-main-controller-137}
At the end of ALC compensation, if ALC is not masked, o_w_BTIA_ALC relative to the running frame, shall be set to output system (check when i_end_of_compensation rise in PPG FSM). If

Covers: IPOS_STBIO1_MAIN_CONTROLLER_728

[End]


#### **IPOS-MAIN-CONTROLLER-138** {#ipos-main-controller-138}
If multiple frame is selected (i_frame_repetition in ppg_fsm greater than 0), when Tx Preset falls from 1 to 0, the en_tx shall pass from 1 to 0 only during the last repetition (check that when

Covers: IPOS_STBIO1_MAIN_CONTROLLER_8106

[End]

