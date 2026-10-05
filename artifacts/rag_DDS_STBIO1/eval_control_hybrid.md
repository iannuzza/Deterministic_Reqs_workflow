# RAG Query Results
- Timestamp: 2026-09-14 10:10:36
- Query: software controlled power management driver domain powered down
- Mode: hybrid
- Requested mode: hybrid
- Normalized Query: software controlled control power management driver domain powered down
- Normalized FTS Query: software OR controlled OR control OR power OR management OR driver OR domain OR powered OR down
- Top K: 10
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: not requested
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
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -23.782547
- semantic_score: (not returned)
- rrf_score: 0.016393
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

## Result 3
- chunk_id: 126
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 32
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -12.893824
- semantic_score: (not returned)
- rrf_score: 0.015873
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

## Result 4
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

## Result 5
- chunk_id: 292
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 116
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 5
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -7.695395
- semantic_score: (not returned)
- rrf_score: 0.015385
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

## Result 6
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

## Result 7
- chunk_id: 134
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 36
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 7
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -6.452478
- semantic_score: (not returned)
- rrf_score: 0.014925
- normalized_terms: 35 12 stbio1 operating operat modes mode digital blocks block status statu different reported report table where indicates indicate clock running run off gated gat pmu adsp regmap fifo_ctrl sensor hub main ctrl ispu req_id power down dds_stbio1_10200 boot dds_stbio1_10201 configuration configure phase dds_stbio1_10202 operative data storage optionally dds_stbio1_10203 elaboration dds_stbio1_10204 sleep dds_stbio1_10205 management unit clock_reset clk reset rst rst_n resetn por config power_startup up startup start initialization wake storage_buffer store stor buffer fifo queue interrupt irq event flag power_on_reset power_up

```text
35 
 
12. STBIO1 Operating Modes 
 
Digital blocks status for different operating modes is reported in table, where ON indicates the 
clock is running and OFF that it is gated: 
 
 PMU ADSP Regmap FIFO_CTRL Sensor 
hub 
Main 
CTRL ISPU Req_ID 
Power Down On Off Off Off Off On Off DDS_STBIO1_10200 
Boot On On On Off Off On Off DDS_STBIO1_10201 
Configuration 
Phase On Off On Off Off On Off DDS_STBIO1_10202 
Operative 
data storage 
mode 
On Off Off On On On On 
(optionally) DDS_STBIO1_10203 
Operative 
elaboration 
mode 
On On Off On On On On 
(optionally) DDS_STBIO1_10204 
Sleep On Off Off On 
(Optionally) Off On On 
(optionally) DDS_STBIO1_10205
```

## Result 8
- chunk_id: 338
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 145
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 8
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -6.391276
- semantic_score: (not returned)
- rrf_score: 0.014706
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
- chunk_id: 136
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 37
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 9
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -6.274444
- semantic_score: (not returned)
- rrf_score: 0.014493
- normalized_terms: 36 13 modules module instantiations instantiation u_pmu pmu u_pad_mux pad_mux u_regmap_otp stbio1_regmap u_masterblaze_ahb senshub_mst_i2c u_xbar_afe xbar_afe interconnect u_adsp adsp u_fifo fifo controller u_ispu ispu u_i2c_spi_slave i2c_spi_slave u_ca_fifo_bist_c ram hard macro u_ca_qk_bist_c u_ca_qk_rom_bist rom u_psw_ctrl power island u_ta_afe_bist_crtl stbio1 bist u_otp otp u_main_controller_top main_controller_top 1 top description oversees oversee device start up phase clock generation digital analog domain reset sync different 2 i o list port name direction type clk_16m input wire 16 mhz ring oscillators oscillator clk_64k 64khz por1v2_1v2 por signal start_clk_16m ready 16mhz pdclockf down main i_bio_divider enable 32khz geneartion when bio channel activated activat management unit first out built self test clock_reset clk rst rst_n resetn storage_buffer store stor storage buffer queue test_debug debug scan dft power_on_reset

```text
36 
 
13. Modules 
Instantiations 
• u_pmu: pmu 
• u_pad_mux: pad_mux 
• u_regmap_otp: stbio1_regmap 
• u_masterblaze_ahb: senshub_mst_i2c 
• u_xbar_afe: xbar_afe: interconnect 
• u_ADSP: ADSP 
• u_fifo: Fifo Controller 
• u_ispu: ispu 
• u_i2c_spi_slave: i2c_spi_slave 
• u_ca_fifo_bist_c: FIFO RAM (Hard Macro) 
• u_ca_qk_bist_c: ADSP RAM (Hard Macro) 
• u_ca_qk_rom_bist: ADSP ROM (Hard Macro) 
• u_psw_ctrl: ISPU Power Island 
• u_ta_afe_bist_crtl: STBIO1 Bist Controller (Hard Macro) 
• u_otp: otp (Hard Macro) 
• u_main_controller_top: main_controller_top 
 
13.1.1. PMU  
13.1.1.1. PMU TOP Description 
 
PMU oversees the Device Start-Up phase, the clock generation to the Digital and Analog Domain 
and Reset Sync to the different Clock Domain.  
13.1.1.2. PMU TOP I/O List 
Port name Direction Type Description 
clk_16m input wire Clock 16 MHz from analog ring oscillators 
clk_64k input wire Clock 64kHz from analog ring oscillators 
POR1V2_1V2 input wire POR Signal 
START_CLK_16M input wire Clock ready for 16MHz 
PDClockF input wire Power Down for 16MHz Ring Oscillator 
from main controller 
i_bio_divider input wire Enable 32kHz geneartion from 16MHz when 
a Bio-Channel is activated
```

## Result 10
- chunk_id: 207
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 74
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 10
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -6.081286
- semantic_score: (not returned)
- rrf_score: 0.014286
- normalized_terms: 73 13 1 3 main controller top description charge generating generat receiving receiv all control signals signal analog domain furthermore performs perform dsp elaboration adc output writes write different address ip divided divid sub blocks block same hierarchy level described describ next chapter together interfaced interfac fifo adsp pmu these last two will not document 2 i o list generic name type value ppg_frame_bit_top 4 n_max_frame 12 ppg_rx_channel_bit_top t_tx_led_set_bit_top 9 t_tx_led_off_max_bit_top 11 m_odr_max_bit_top mode_operation_n_bit_top idac_dc_ppg_frame_bit_top 6 time_slot_sel_bit_top t_tx_startup_bit_top 8 t_rx_set_bit_top nmax_bit_top base_address_bit_top delta_bit_top gain_max_bit_top t1_max_bit_top t2_max_bit_top 5 n_clk_max_bit_top n_average_ppg_max_bit_top rx_ch_gain_max_bit_to digital converter power management unit first out storage_buffer store stor storage buffer queue power_up up analog_to_digital digital_to_analog

```text
73 
 
13.1.3.1. Main Controller TOP Description 
The Main Controller is in charge of generating and receiving all the control signals for the Analog 
Domain, furthermore, performs DSP elaboration on ADC Output and writes it in different 
Address. 
The IP is divided into different sub-blocks, all at the same hierarchy level and described in the 
next chapter. Together with the Analog Domain, this IP is interfaced with the FIFO Controller, the 
ADSP and the PMU, these last two will not be described in this document. The IP is divided into 
different sub-blocks, all at the same hierarchy level and described in the next chapter. 
13.1.3.2. Main Controller TOP I/O List 
 
Generic name Type Value Description 
ppg_frame_bit_top  4  
n_max_frame  12  
ppg_rx_channel_bit_top  3  
T_tx_led_set_bit_top  9  
T_tx_led_off_max_bit_top  11  
m_odr_max_bit_top  12  
mode_operation_n_bit_top  2  
idac_dc_ppg_frame_bit_top  6  
time_slot_sel_bit_top  3  
T_tx_startup_bit_top  8  
T_rx_set_bit_top  9  
Nmax_bit_top  4  
base_address_bit_top  12  
delta_bit_top  4  
gain_max_bit_top  4  
T1_max_bit_top  9  
T2_max_bit_top  5  
N_clk_max_bit_top  6  
n_average_ppg_max_bit_top  3  
rx_ch_gain_max_bit_to
```

