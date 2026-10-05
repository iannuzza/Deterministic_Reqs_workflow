# RAG Query Results
- Timestamp: 2026-09-14 10:11:02
- Query: wake up restore retention isolation power sequence
- Mode: hybrid-semantic
- Requested mode: hybrid-semantic
- Normalized Query: wake up restore retention isolation power sequence power_startup startup start boot initialization
- Normalized FTS Query: wake OR up OR restore OR retention OR isolation OR power OR sequence OR power_startup OR startup OR start OR boot OR initialization
- Top K: 10
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: available
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 59
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 6
- section: (unknown)
- source_type: figure
- chunk_index: 5
- rank_lexical: (not returned)
- rank_normalized: 1
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -25.848583
- semantic_score: (not returned)
- rrf_score: 0.016393
- normalized_terms: figure 12 boot routine 90 power_startup power up startup start initialization wake power_up

```text
Figure 12: Boot Routine ................................ ................................ ................................ ............. 90
```

## Result 2
- chunk_id: 138
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 38
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 21
- rank_semantic: 4
- lexical_score: (not returned)
- normalized_score: -14.452410
- semantic_score: 0.237772
- rrf_score: 0.016252
- normalized_terms: 37 en_ldo1v8_reg input wire enable ldo regmap bist_mode bist mode debug_mode debug scan_mode scan scan_enable start scan_clk clk scan_rstn rst clk_bistctlr controller collar clock rst_bistctlr_n resetn clk_ext_en external pad clk_ext_slow 32khz i_en_sh_clk sensor hub i_senshub_clk_sel 2 0 selector i_test_clk_fast test trimming trim 16mhz i_half_charge_ldo low power when only ppg selected select mask_en_ldo_pdclkf mask control pdf during dur boot clk_en_s0 gating gat logic inside stredl_afe_top clk_en_s1 if present hsel stmc ahb master clk_en_s2_i2c clk_en_s2_on i2c spi interface clk_en_s2_off off clk_en_s3 dropout regulator built self clock_reset reset rst_n por power_startup up startup initialization wake test_debug dft clock_gating power_up

```text
37 
 
EN_LDO1V8_REG input wire Enable LDO from regmap 
bist_mode input wire enable bist mode 
debug_mode input wire enable debug 
scan_mode input wire enable scan mode 
scan_enable input wire start scan mode 
scan_clk input wire scan clk 
scan_rstn input wire scan rst 
clk_bistctlr input wire bist controller and collar clock 
rst_bistctlr_n input wire bist controller and collar resetn 
clk_ext_en input wire enable external clock from pad 
clk_ext_slow input wire external clock 32kHz 
i_en_sh_clk input wire enable sensor hub clock 
i_senshub_clk_sel input wire 
[2:0] 
selector for sensor hub clock 
i_test_clk_fast input wire enable test and trimming for 16MHz clock 
i_half_charge_ldo input wire enable the low power mode for ldo when 
only ppg is selected 
mask_en_ldo_pdclkf input wire mask the control of pdf and ldo control 
during boot 
clk_en_s0 input wire clock gating logic inside stredl_afe_top 
clk_en_s1 input wire if present should be HSEL STMC AHB 
Master 
clk_en_s2_i2c input wire if present should be HSEL STMC AHB 
Master 
clk_en_s2_on input wire clk gating ON from AHB I2C/SPI Interface 
clk_en_s2_off input wire clk gating OFF from AHB I2C/SPI Interface 
clk_en_s3 input wire
```

## Result 3
- chunk_id: 67
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 6
- section: (unknown)
- source_type: figure
- chunk_index: 13
- rank_lexical: (not returned)
- rank_normalized: 2
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -25.693187
- semantic_score: (not returned)
- rrf_score: 0.016129
- normalized_terms: figure 20 boot phase flow 145 power_startup power up startup start initialization wake power_up

```text
Figure 20: Boot Phase Flow ................................ ................................ ................................ ..... 145
```

## Result 4
- chunk_id: 340
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 146
- section: (unknown)
- source_type: figure
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -25.693187
- semantic_score: (not returned)
- rrf_score: 0.015873
- normalized_terms: 145 figure 20 boot phase flow power_startup power up startup start initialization wake power_up

```text
145 
 
 
Figure 20: Boot Phase Flow
```

## Result 5
- chunk_id: 243
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 91
- section: (unknown)
- source_type: figure
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 4
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -22.858031
- semantic_score: (not returned)
- rrf_score: 0.015625
- normalized_terms: 90 figure 12 boot routine vpriority high end dds_stbio1_0017 requirement perform otp_boot bit written when quokka_run low dds_stbio1_0018 write start otp rises rise completes complete falls fall dds_stbio1_0019 power_startup power up startup initialization wake power_up

```text
90 
 
 
Figure 12: Boot Routine 
[Vpriority High] [End] 
 
 
 
[DDS_STBIO1_0017] Requirement: 
To perform a BOOT routine, OTP_BOOT bit shall be written when quokka_run is low. 
[Vpriority High] [End] 
 
[DDS_STBIO1_0018] Requirement: 
The WRITE routine shall start when OTP Write Bit rises and completes when quokka_run falls. 
[Vpriority High] [End] 
 
[DDS_STBIO1_0019] Requirement:
```

## Result 6
- chunk_id: 222
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 82
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 19
- rank_semantic: 29
- lexical_score: (not returned)
- normalized_score: -15.034474
- semantic_score: 0.099706
- rrf_score: 0.015467
- normalized_terms: 81 port name direction type output reset value description hbusreq 0 ahb protocol signals signal hlock o_bio_clock_div clock chopper o_bidac idac_offset 1 idac top o_rst_imp bia start up rst o_rsti_imp rsti o_sug_imp sug channel o_pd_imp pd o_start_operative_16mhz operative 16mhz o_su_hc2 ecg hc2 o_rst_hc2 o_rsti_hc2 o_pd_hc2 o_reset_reg_rst end async phase o_reset_reg_rst_imp_async o_imp_curinj_pd current injection o_txi_idac_vref nmax_bit_top tx vref analog domain o_comp_rx_ck comparator debug o_btia_gain gain_max_bit_top btia gain o_data_out_debug_adc 15 o data adc o_en_mask_ldo_pdclkf_reg mask en_ldo pdf o_pd_clkf pd_clkf o_trim_l digital converter clock_reset clk rst_n resetn por power_startup power startup boot initialization wake test_debug test scan bist dft self power_on_reset power_up analog_to_digital digital_to_analog

```text
81 
 
Port name Direction Type Output 
Reset Value Description 
HBUSREQ output  0 AHB Protocol signals 
HLOCK output  0 AHB Protocol signals 
o_bio_clock_div output  0 output for clock chopper 
o_BIDAC output [IDAC_offset-1:0] 0 IDAC for top 
o_rst_imp output  1 bia start up rst signal 
o_rsti_imp output  1 bia start up rsti signal 
o_sug_imp output  1 bia start up sug channel 
o_pd_imp output  1 bia start up pd channel 
o_start_operative_16MHz output  0 start operative 16MHz 
o_su_hc2 output  1 ecg start up hc2 signal 
o_rst_hc2 output  1 ecg start up rst signal 
o_rsti_hc2 output  1 ecg start up rsti signal 
o_pd_hc2 output  1 ecg start up pd signal 
o_reset_reg_rst output  1 end of reset async phase 
o_reset_reg_rst_imp_async output  1 end of reset async phase 
o_imp_curinj_pd output  0 bia current injection output 
o_Txi_IDAC_Vref output [Nmax_bit_top-1:0] 0 TX IDAC VREF TO analog domain 
o_comp_rx_ck output  0 output for comparator debug 
o_BTIA_gain output [gain_max_bit_top-1:0] 0 BTIA gain output to analog domain 
o_data_out_debug_adc output [15:0] 0 o data output for adc debug 
o_en_mask_ldo_pdclkf_reg output  1 mask for en_ldo and pdf 
o_pd_clkf output  1 pd_clkf 
o_trim_l
```

## Result 7
- chunk_id: 233
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 87
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 27
- rank_semantic: 3
- lexical_score: (not returned)
- normalized_score: -6.090469
- semantic_score: 0.250313
- rrf_score: 0.015463
- normalized_terms: 86 hburstm output wire 2 0 hprotm 3 hwdatam 31 hbusreqm hlockm stmc_data_csn stmc_data_wen stmc_data_a 8 stmc_data_d 63 stmc_data_m stmc_data_q input stmc_rom_clk stmc_rom_csn stmc_rom_a 10 stmc_rom_q 22 quokka_run u_pmu adsp_run main_controller_top i_quokka_r un quokka_boot_end i_quokka_b oot_end ahb_master_clk_en clk_en_s1 scan_mode scan_en scan_clk scan_rst_n power_up power up

```text
86 
 
HBURSTM output wire [ 2:0]  
HPROTM output wire [ 3:0]  
HWDATAM output wire [ 31:0]  
HBUSREQM output wire  
HLOCKM output wire  
stmc_data_CSN output wire  
stmc_data_WEN output wire  
stmc_data_A output wire [ 8:0]  
stmc_data_D output wire [ 63:0]  
stmc_data_M output wire [ 63:0]  
stmc_data_Q input wire [ 63:0]  
stmc_rom_CLK output wire  
stmc_rom_CSN output wire  
stmc_rom_A output wire [ 10:0]  
stmc_rom_Q input wire [ 22:0]  
quokka_run output wire 
u_pmu.adsp_run 
main_controller_top.i_quokka_r
un 
quokka_boot_end output wire main_controller_top.i_quokka_b
oot_end 
ahb_master_clk_en output wire U_pmu.clk_en_s1 
scan_mode input wire  
scan_en input wire  
scan_clk input wire  
scan_rst_n input wire
```

## Result 8
- chunk_id: 338
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 145
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 5
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -21.303469
- semantic_score: (not returned)
- rrf_score: 0.015385
- normalized_terms: 144 15 1 boot phase dds_stbio1_0114 requirement release por signal analog domain pmu manage turn ldo1v8 starts start clocks clock up sequence reported report ipos ipos_pmu end dds_stbio1_0115 after least 2 ms reset digital de asserted assert overlook part described describ device dds_stbio1_0116 check user read main_controller_status_register device_status_reg register 0 follow these steps step if value still process then ended idle ipos_main_ctrl power management unit clock_reset clk rst rst_n resetn power_startup startup initialization wake power_on_reset power_up

```text
144 
 
15.1. BOOT Phase 
 
[DDS_STBIO1_0114] Requirement: 
At the release of the POR signal from the analog domain, the PMU shall manage the turn-on of 
the LDO1V8 and starts clocks Start-Up Sequence (reported in PMU IPOS) [TO: IPOS_PMU] 
[END] 
[DDS_STBIO1_0115] Requirement: 
After At least 2 ms from the Release of the POR, the reset of the digital domain shall be de-
asserted (an overlook on this part is described in the PMU IPOS) and the device shall start the 
Boot Phase [TO: IPOS_PMU] [END] 
[DDS_STBIO1_0116] Requirement: 
To check the end of the BOOT phase, the user shall read the main_controller_status_register 
(DEVICE_STATUS_REG register [2:0]) and follow these steps: 
• Read the DEVICE_STATUS_REG [2:0] 
• Check if the Value is 1 (BOOT phase still in process) 
• If the value is 2, then the BOOT phase is ended and the device is in IDLE. [TO: 
IPOS_MAIN_CTRL] [END]
```

## Result 9
- chunk_id: 238
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 88
- section: 13.2.1.1.2. Requirements
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 6
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -20.958298
- semantic_score: (not returned)
- rrf_score: 0.015152
- normalized_terms: 13 2 1 requirements requirement dds_stbio1_0012 definition there three routine adsp use interact otp memory which write boot test registers register map 3 specific bits used trigger these routines power_startup power up startup start initialization wake test_debug debug scan bist dft self power_up

```text
13.2.1.1.2. Requirements 
 
[DDS_STBIO1_0012] Definition: 
There are three routine that the ADSP use to interact with the OTP memory, which are the Write, 
Boot and Test routine. In ADSP registers map there are 3 specific bits used to trigger these OTP 
routines:
```

## Result 10
- chunk_id: 241
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 90
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 7
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -20.548200
- semantic_score: (not returned)
- rrf_score: 0.014925
- normalized_terms: 89 dds_stbio1_0014 requirement boot routine starts start when otp_boot bit rises rise completes complete quokka_boot_end vpriority high end dds_stbio1_0015 during dur otp operation adsp copy content memory registers register following follow procedure access dds_stbio1_0016 first read last location address 0x7f if 0xff called cal lifecycle byte then proceeds proceed 0 0x2f otherwise not perform any further reads power_startup power up startup initialization wake power_up

```text
89 
 
 
[DDS_STBIO1_0014] Requirement: 
The BOOT routine shall starts when the OTP_BOOT bit rises and shall completes when 
quokka_boot_end rises. 
[Vpriority High] [End] 
 
 
 
 
[DDS_STBIO1_0015] Requirement: 
During OTP boot operation, the ADSP shall copy the content of the OTP memory into the OTP 
registers, following the procedure to access OTP memory 
[Vpriority High] [End]  
 
 
 
[DDS_STBIO1_0016] Requirement: 
During BOOT routine, ADSP shall first read the last location of the OTP memory, at address 
0x7F. If the content is 0xFF, called “lifecycle” byte, then the READ operation proceeds from 
address 0 to address 0x2F; otherwise, ADSP shall not perform any further reads.
```

