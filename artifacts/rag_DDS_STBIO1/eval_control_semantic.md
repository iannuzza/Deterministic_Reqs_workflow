# RAG Query Results
- Timestamp: 2026-09-14 10:10:39
- Query: software controlled power management driver domain powered down
- Mode: hybrid-semantic
- Requested mode: hybrid-semantic
- Normalized Query: software controlled control power management driver domain powered down
- Normalized FTS Query: software OR controlled OR control OR power OR management OR driver OR domain OR powered OR down
- Top K: 10
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: available
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 127
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 33
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 1
- rank_semantic: 4
- lexical_score: (not returned)
- normalized_score: -23.782547
- semantic_score: 0.162592
- rrf_score: 0.020300
- normalized_terms: 32 10 4 power domain descriptions description 1 pd_top1v2 function ensures ensure continuity critical functions data storage mode sensor hub acquisition fifo read write elaboration adsp only characteristics characteristic never powered down control managed manag hardware 2 pd_stredl powers stredl core associated associat cache can when not use via software management driver see 12 3 pd_top3v3 supply otp memory block provides provide 7v during dur programming program operations operation pd_topio communication pad 11 interconnect first out storage_buffer store stor buffer queue sampling sample acquire acquir

```text
32 
 
10.4. Power Domain Descriptions 
10.4.1. PD_TOP1V2 
• Function: Ensures continuity of critical functions (Data Storage Mode, Sensor-Hub 
acquisition, FIFO read and write data, Elaboration Mode with ADSP only). 
• Characteristics: Never powered down. 
• Control: Managed by hardware. 
10.4.2. PD_STREDL  
• Function: Powers the STREDL core and associated cache. 
• Characteristics: Can be powered down when STREDL is not in use. 
• Control: Managed via software (power management driver)(see 12.3.1) 
10.4.3. PD_TOP3V3 
• Function: power supply to the OTP memory block. 
• Characteristics: Never powered down. It provides 4.7V of power supply to the 
OTP memory block during programming (write) operations 
• Control: Managed by hardware. 
10.4.4. PD_TOPIO 
• Function: Powers communication PAD 
• Characteristics: Never powered down. 
• Control: Managed by hardware. 
 
 
11. Interconnect
```

## Result 2
- chunk_id: 126
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 32
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: 1
- lexical_score: (not returned)
- normalized_score: -12.893824
- semantic_score: 0.313044
- rrf_score: 0.019971
- normalized_terms: 31 control modes mode interactions interaction between various variou functional blocks block 10 2 definitions definition power domain pd set logic sharing shar same supply which can powered off independently always alway aon even low retention retains retain register state when main down switchable completely save energy 3 architecture name included includ s type voltage v notes note pd_top1v2 adsp ca_fifo_bist_c ca_qk_bist_c ca_qk_rom_bist multi_channel_fifo i2c_spi_slave main_controller_top senshub_mst_i2c pad_mux pmu stbio1_regmap scan_out_mux ta_stbio1_bist_ctlr xbar_afe 1 hw active pd_stredl stredl sw idle pd_top3v3 h9a_mem_otp pump_85al05_2 3a 7 4 7v pd_topio level_shifter_sel 8v 6v management unit

```text
31 
 
control modes, and interactions between the various functional blocks.
 
10.2. Definitions 
 
• Power Domain (PD):  A set of logic blocks sharing the same power 
supply, which can be powered on/off independently. 
• Always-On Domain (AON): Domain that is always powered, even in 
low-power modes. 
• Retention Domain: Domain that retains register state even when the 
main logic is powered down. 
• Switchable Domain: Domain that can be completely powered off to 
save energy. 
10.3. Power Domain Architecture 
Domain 
Name 
Included Block(s) Domain 
Type 
Voltage [V] Control 
Mode 
Notes 
PD_TOP1V2  ADSP, ca_fifo_bist_c, 
ca_qk_bist_c, 
ca_qk_rom_bist, 
multi_channel_fifo, 
i2c_spi_slave, 
main_controller_top, 
senshub_mst_i2c, 
pad_mux, pmu, 
stbio1_regmap, 
scan_out_mux, 
ta_stbio1_bist_ctlr, 
xbar_afe            
Always-On 1.2 HW Always active 
PD_STREDL STREDL Switchable 1.2 SW Can be 
powered 
down in idle 
PD_TOP3V3 H9A_MEM_OTP_ 
PUMP_85AL05_2 3A 
Always-On 2.7÷4.7V HW Always active 
PD_TOPIO level_shifter_sel Always-On 1.8V÷3.6V HW Always active
```

## Result 3
- chunk_id: 292
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 116
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 5
- rank_semantic: 20
- lexical_score: (not returned)
- normalized_score: -7.695395
- semantic_score: 0.043033
- rrf_score: 0.018510
- normalized_terms: 115 13 3 ispu integration por name directi comment top connection clk input 16mhz pmu u_pmu_clk_stredl_sig main_rst_n reset domain u_pmu_resetn_stredl_sig por_n ispu_xbar_sw_resetn software xbar u_regmap_otp_ispu_xbar_sw_reset n_sig ispu_core_sw_resetn core u_regmap_otp_ispu_core_sw_reset scan_mode scan mode u_pad_mux_scan_mode_sig scan_enable enable u_pad_mux_scan_enable_sig test_rst_n u_pad_mux_scan_rstn_sig bist_mode bist u_pad_mux_bist_mode_sig interrupt lines line u_ca_fifo_bist_c_oen_1 u_fifo_irq_fifo_u_m_irq_statu s_sig u_regmap_otp_irq_senshub_sts u_regmap_otp_irq_senshub_st sig u_regmap_otp_irq_ispu_mc_intr sts_sig u_regmap_otp_sw_interrupt_sig power management unit built self test clock_reset clock rst rst_n resetn connect connectivity link irq event flag statu test_debug debug dft power_on_reset

```text
115 
 
13.3. ISPU integration 
Por name Directi
on Comment TOP CONNECTION 
clk input clk 16MHz 
from pmu 
u_pmu_clk_stredl_sig 
 
main_rst_n input 
reset in 
16MHz 
domain 
u_pmu_resetn_stredl_sig 
 
POR_n input 
reset in 
16MHz 
domain 
u_pmu_resetn_stredl_sig 
 
ispu_xbar_sw_resetn input 
Software 
reset ISPU 
xbar 
u_regmap_otp_ispu_xbar_sw_reset
n_sig 
 
ispu_core_sw_resetn input 
Software 
reset ISPU 
core 
u_regmap_otp_ispu_core_sw_reset
n_sig 
 
scan_mode input Scan mode u_pad_mux_scan_mode_sig 
 
scan_enable input Scan enable u_pad_mux_scan_enable_sig 
 
test_rst_n input Scan reset u_pad_mux_scan_rstn_sig 
 
bist_mode input Bist mode 
enable 
u_pad_mux_bist_mode_sig 
 
interrupt input Interrupt 
lines 
 
u_ca_fifo_bist_c_oen_1, 
u_fifo_irq_FIFO_U_M_IRQ_STATU
S_sig, 
u_regmap_otp_irq_SENSHUB_STS
_sig, 
u_regmap_otp_irq_ISPU_MC_INTR
_STS_sig, 
u_regmap_otp_sw_interrupt_sig, 
u_ca_fifo_bist_c_oen_1, 
u_ca_fifo_bist_c_oen_1, 
u_ca_fifo_bist_c_oen_1, 
u_ca_fifo_bist_c_oen_1,
```

## Result 4
- chunk_id: 125
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 31
- section: 10. Power Domains
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 17
- rank_semantic: 2
- lexical_score: (not returned)
- normalized_score: -4.986515
- semantic_score: 0.200160
- rrf_score: 0.017019
- normalized_terms: 10 power domains domain 1 introduction document paragraph describes describe architecture implemented implement stbio1 goal provide detailed detail overview partitioning partition their functionalities functionality

```text
10. Power Domains 
10.1. Introduction 
This document paragraph describes the Power Domain architecture implemented in the STBIO1. 
The goal is to provide a detailed overview of the power domain partitioning, their functionalities,
```

## Result 5
- chunk_id: 154
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 45
- section: 13.1.1.4. Clocks and Reset
- source_type: figure
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 2
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -13.757558
- semantic_score: (not returned)
- rrf_score: 0.016129
- normalized_terms: clocks clock scheme shown below figure 9 above req_id source target path delay gating gat analog control description f max requirements requirement definition dds_stbio1 1020 stbio1_top clk_16m dig_wrapper_lv u_pmu clk 16m no pwr_down controlled pmu 16 mhz 1021 clk_64k 64k 64 khz power management unit clock_reset reset rst rst_n resetn por clock_gating

```text
Clocks scheme is shown in the below figure 
 
Figure 9: Clocks Scheme 
Clocks scheme is shown in the above figure 
Req_ID Source Target Path Delay Clock Gating 
Analog Control 
and Description F Max 
Requirements 
Definition 
DDS_STBIO1_
1020 stbio1_top.clk_16m stbio1_top.dig_wrapper_LV.u_pmu.clk
_16m 
 No 
Pwr_down 
controlled by pmu 16 MHz 
DDS_STBIO1_
1021 stbio1_top.clk_64k stbio1_top.dig_wrapper_LV.u_pmu.clk
_64k  No 
No 
64 kHz
```

## Result 6
- chunk_id: 226
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 84
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 23
- rank_semantic: 6
- lexical_score: (not returned)
- normalized_score: -4.555466
- semantic_score: 0.131928
- rrf_score: 0.015836
- normalized_terms: 83 port name direction type output reset value description o_adc_error_cap5 6 0 adc calibration result o_adc_error_cap4 o_adc_error_cap3 o_adc_error_cap2 o_adc_error_cap1 o_adc_error_cap0 o_pd_cm_buf 1 power down common buffer o_pd_rld rld o_pd_avg1 avg1 o_pd_avg2 avg2 o_mc_ahb_clk_en enable master ahb clock o_main_controller_device_status_register 2 device status statu register o_main_controller_elab_status_register 3 o_en_ldo_1v8 ldo o_en_bufxbio biobuffer analog domain o_rx_ch_frame ppg_rx_channel_bit_top selected select rx ch frame o_ldo_ext external o_ppg_status_register n_state_bit ppg state o_b_cap_idac b cap idac o_ispu_irq_ctrl ispu irq o_irq_start_measurement digital converter low dropout regulator interrupt request clock_reset clk rst rst_n resetn por storage_buffer store stor storage fifo queue event flag power_on_reset analog_to_digital digital_to_analog

```text
83 
 
Port name Direction Type Output 
Reset Value Description 
o_adc_error_cap5 output [6:0] 0 adc calibration result 
o_adc_error_cap4 output [6:0] 0 adc calibration result 
o_adc_error_cap3 output [6:0] 0 adc calibration result 
o_adc_error_cap2 output [6:0] 0 adc calibration result 
o_adc_error_cap1 output [6:0] 0 adc calibration result 
o_adc_error_cap0 output [6:0] 0 adc calibration result 
o_pd_cm_buf output  1 power down common buffer 
o_pd_rld output  1 power down rld 
o_pd_avg1 output  1 power down avg1 
o_pd_avg2 output  1 power down avg2 
o_mc_ahb_clk_en output  0 enable for master ahb clock 
o_main_controller_device_status_register output [2:0] 0 device status register 
o_main_controller_elab_status_register output [3:0] 0 device status register 
o_en_ldo_1v8 output  0 enable ldo 
o_en_bufxbio output  0 enable biobuffer to analog domain 
o_rx_ch_frame output [ppg_rx_channel_bit_top-1:0] 0 selected rx ch frame to analog domain 
o_ldo_ext output  0 enable external ldo 
o_ppg_status_register output [n_state_bit-1:0] 0 ppg state status register 
o_b_cap_idac output [1:0] 0 b cap idac to analog domain 
o_ispu_irq_ctrl output [3:0] 0 ispu irq 
o_irq_start_measurement output
```

## Result 7
- chunk_id: 228
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 85
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 18
- rank_semantic: 24
- lexical_score: (not returned)
- normalized_score: -4.928382
- semantic_score: 0.034462
- rrf_score: 0.015797
- normalized_terms: 84 port name direction type output reset value description o_pd_buf_gpio1 1 power down buffer gpio1 o_pd_buf_gpio2 gpio2 o_adc_data_debug_alc_1 frame_ppg_debug_alc_top 0 alc registers register data debug o_adc_data_debug_alc_2 2 o_adc_data_debug_ppg_raw frame_ppg_debug_ppg_raw_top ppg raw o_en_lead_off mask lead off o_mc_busy main controller working work o_en_ck_m_p_q clock m q bia o_en_ck_chop_imp chopper o_saturation_flag n_max_frame saturation flag o_en_ck_hc2_10k chipper ecg o_en_clk_16mhz_sleep sleep signal pmu o_gsr_clk_en_16m enable gsr channel management unit clock_reset clk rst rst_n resetn por storage_buffer store stor storage fifo queue interrupt irq event statu test_debug test scan bist dft self power_on_reset analog_to_digital analog digital

```text
84 
 
Port name Direction Type Output 
Reset Value Description 
o_pd_buf_gpio1 output  1 power down for buffer gpio1 
o_pd_buf_gpio2 output  1 power down for buffer gpio2 
o_adc_data_debug_alc_1 output [frame_ppg_debug_alc_top-1:0] 0 alc 1 registers data debug 
o_adc_data_debug_alc_2 output [frame_ppg_debug_alc_top-1:0] 0 alc 2 registers data debug 
o_adc_data_debug_ppg_raw output [frame_ppg_debug_ppg_raw_top-
1:0] 
0 ppg raw registers data debug 
o_en_lead_off output  0 mask lead off 
o_mc_busy output  0 main controller is working 
o_en_ck_m_p_q output  0 clock m and q bia 
o_en_ck_chop_imp output  0 clock chopper bia 
o_saturation_flag output [n_max_frame-1:0] 0 ppg saturation flag 
o_en_ck_hc2_10k output  0 clock chipper ecg 
o_en_clk_16MHz_sleep output  1 sleep signal for pmu 
o_gsr_clk_en_16M output  0 enable clock for gsr channel
```

## Result 8
- chunk_id: 156
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 46
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 4
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -11.102885
- semantic_score: (not returned)
- rrf_score: 0.015625
- normalized_terms: rapper_lv u_pmuclk_xbar stbio1_top dig_wrapper_lv u fifo hcl k 1 u_pm clk_en_m2 all_test_mode clk_en_m2_reg u_p ad_mux scan_enable no 16 mhz dds_stbio1 2025 u_pmu clk_stredl u_ispu clk pwr_down controlled control pmu 2026 clk_xbar u_regmap otp hclk clk_en_m3 clk_en_m3_reg clk_en_s3 1025 u_stbio1_top u_device_startup tst_clk 32k tst_clk_32 32 khz 1026 tst_clk_16 m u_main_c ontroller_top i_clk_16mhz i_en_clk_16mhz_sleep scan_mode power management unit first out clock_reset clock reset rst rst_n resetn por storage_buffer store stor storage buffer queue power_up up

```text
rapper_LV.u_pmuclk_xbar 
 
stbio1_top.dig_wrapper_LV.u.fifo.HCL
K 
1 
stbio1_top.dig_wrapper_LV.u_pm
u.clk_en_m2 | 
stbio1_top.dig_wrapper_LV.u_pm
u.all_test_mode | 
stbio1_top.dig_wrapper_LV.u_pm
u.clk_en_m2_reg | 
~stbio1_top.dig_wrapper_LV.u_p
ad_mux.scan_enable 
No 
16 MHz 
DDS_STBIO1_
2025 
stbio1_top.dig_wrapper_LV.u_pmu.clk_stredl stbio1_top.dig_wrapper_LV.u_ispu.clk 
 No 
Pwr_down 
controlled by pmu 
16 MHz 
DDS_STBIO1_
2026 
stbio1_top.dig_wrapper_LV.u_pmu.clk_xbar 
stbio1_top.dig_wrapper_LV.u_regmap
_otp.hclk 
1 
stbio1_top.dig_wrapper_LV.u_pm
u.clk_en_m3 | 
stbio1_top.dig_wrapper_LV.u_pm
u.all_test_mode | 
stbio1_top.dig_wrapper_LV.u_pm
u.clk_en_m3_reg | 
stbio1_top.dig_wrapper_LV.u_pm
u.clk_en_s3 | 
~stbio1_top.dig_wrapper_LV.u_p
ad_mux.scan_enable  
No 
16 MHz 
DDS_STBIO1_
1025 
u_stbio1_top.u_pmu.u_device_startup.tst_clk_
32k 
stbio1_top.dig_wrapper_LV.tst_clk_32
k 
 No 
No 
32 kHz 
DDS_STBIO1_
1026 
stbio1_top.dig_wrapper_LV.u_pmu.tst_clk_16
m 
stbio1_top.dig_wrapper_LV.u_main_c
ontroller_top.i_clk_16MHz 1 
stbio1_top.dig_wrapper_LV.u_pm
u.i_en_clk_16MHz_sleep | 
stbio1_top.dig_wrapper_LV.u_pm
u.scan_mode | 
~stbio1_top.dig_wrapper_LV.u_p
ad_mux.scan_enable 
No 
16 M
```

## Result 9
- chunk_id: 99
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 16
- section: 6. Symbol
- source_type: figure
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 25
- rank_semantic: 11
- lexical_score: (not returned)
- normalized_score: -4.529376
- semantic_score: 0.082761
- rrf_score: 0.015286
- normalized_terms: dds_stbio1_0008 definition figure 4 stbio1 ball out top view side down 7 i o list dds_stbio1_0009 nr name function pin no type 1 av1v8 8 v analog power supply d5 2 av3v3 3 d4

```text
[DDS_STBIO1_0008] Definition 
 
 
Figure 4: STBIO1 - Ball out. TOP View (Ball side down) 
 
7. I/O List 
 
[DDS_STBIO1_0009] Definition 
 
Nr. Name Function Pin No. Type 
1 AV1V8 1.8 V Analog Power Supply D5 Power 
2 AV3V3 3.3 V Analog Power Supply D4 Power
```

## Result 10
- chunk_id: 88
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 12
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 6
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -6.741660
- semantic_score: (not returned)
- rrf_score: 0.015152
- normalized_terms: 11 5 stbio1 toplevel overview aim document explain main features feature asic electronic interface ecg bio impedance eda ppg photoplethysmography embedded embed single die analog front end device process capabilities capability collects collect processes processe different types type vital signals signal bia gsr optical channel designed design transceiver stimulating stimulat up eight leds measuring measur return six separate cent inputs input chain rejects reject offsets offset corruption asynchronous asynchronou modulated modulat interference typically ambient light eliminating eliminat need filters filter externally controlled control dc cancellation circuitry acquisition support low noise diagnostic level measurement presence variety interferers interferer has several complementary supporting such driven drive reference common mode rejection lead off detection identify fallen electrode body human breathing breath measurements configurabl sampling sample acquire acquir power_on_reset power reset

```text
11 
 
5. STBIO1 toplevel overview 
Aim of this document is to explain main features of the ASIC STBIO1, electronic interface of 
ECG, Bio-impedance, EDA and PPG (Photoplethysmography) embedded in a single die.  
 
STBIO1 is an Analog Front End Device with embedded process capabilities. 
STBIO1 collects and processes different types of Vital Signals: 
• ECG 
• PPG 
• BIA and GSR 
The optical channel (PPG) is designed as an optical transceiver, stimulating up to eight LEDs 
and measuring the return signal on up to six separate cent inputs. The signal chain rejects signal 
offsets and corruption from asynchronous modulated interference, typically from ambient light, 
eliminating the need for optical filters or externally controlled dc cancellation circuitry. 
The ECG signal acquisition is designed to support low noise, diagnostic level measurement in 
the presence of a variety of interferers. The ECG signal chain has several complementary 
features supporting ECG measurement, such as driven reference for common-mode rejection 
and lead off detection to identify a fallen electrode. 
The BIA signal chain is designed for body impedance and human breathing measurements with 
a configurabl
```

