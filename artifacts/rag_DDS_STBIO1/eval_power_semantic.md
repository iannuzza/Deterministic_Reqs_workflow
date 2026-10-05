# RAG Query Results
- Timestamp: 2026-09-14 10:10:55
- Query: power domain architecture always on switchable retention
- Mode: hybrid-semantic
- Requested mode: hybrid-semantic
- Normalized Query: power domain architecture always alway switchable retention
- Normalized FTS Query: power OR domain OR architecture OR always OR alway OR switchable OR retention
- Top K: 10
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: available
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 126
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 32
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 1
- rank_normalized: 1
- rank_semantic: 1
- lexical_score: -32.714891
- normalized_score: -20.054447
- semantic_score: 0.401590
- rrf_score: 0.036885
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

## Result 2
- chunk_id: 125
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 31
- section: 10. Power Domains
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: 3
- lexical_score: (not returned)
- normalized_score: -9.566863
- semantic_score: 0.256776
- rrf_score: 0.019841
- normalized_terms: 10 power domains domain 1 introduction document paragraph describes describe architecture implemented implement stbio1 goal provide detailed detail overview partitioning partition their functionalities functionality

```text
10. Power Domains 
10.1. Introduction 
This document paragraph describes the Power Domain architecture implemented in the STBIO1. 
The goal is to provide a detailed overview of the power domain partitioning, their functionalities,
```

## Result 3
- chunk_id: 4
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 2
- section: (unknown)
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 4
- rank_semantic: 12
- lexical_score: (not returned)
- normalized_score: -8.953225
- semantic_score: 0.086569
- rrf_score: 0.019097
- normalized_terms: 17 9 1 top pinout list 18 10 power domains domain 30 introduction 2 definitions definition 31 3 architecture 4 descriptions description 32 pd_top1v2 pd_stredl pd_top3v3 pd_topio

```text
................  17 
9.1. TOP Pinout List ................................ ................................ ................................ .......... 18 
10. Power Domains ................................ ................................ ................................ .............. 30 
10.1. Introduction ................................ ................................ ................................ ................. 30 
10.2. Definitions ................................ ................................ ................................ ................... 31 
10.3. Power Domain Architecture ................................ ................................ ........................ 31 
10.4. Power Domain Descriptions ................................ ................................ ........................ 32 
10.4.1. PD_TOP1V2 .............................................................................................. 32 
10.4.2. PD_STREDL .............................................................................................. 32 
10.4.3. PD_TOP3V3 .............................................................................................. 32 
10.4.4. PD_TOPIO ....
```

## Result 4
- chunk_id: 362
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 157
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 6
- rank_semantic: 28
- lexical_score: (not returned)
- normalized_score: -4.848165
- semantic_score: 0.044204
- rrf_score: 0.017992
- normalized_terms: nages nage all bist status statu diagnosis diagnosi repair information debug data collar also provides provide support testing test multiple memories memory parallel sequential order 17 2 mbist controller acts interface between collars user control done through controls various variou reporting report activities activity allows allow mode selections selection programs program pre stored stor synthesized synthesiz algorithms algorithm instructions instruction attached attach main functionalities functionality management runbist retention etc configurable default march element initiate launching launch run compute global based bas individual tap includes include 7 bit register three registers bypass responds respond sequences sequence supplied suppli access port generates generate signals signal required requir operation built self storage_buffer store storage buffer fifo queue interrupt irq event flag test_debug scan dft power_on_reset power reset

```text
nages all the BIST status, 
diagnosis, repair information and debug data. The collar also provides support for testing multiple 
memories in parallel or in sequential order.  
17.2.2. MBIST Controller  
The controller acts as an interface between the collars and the user. All user BIST control is done 
through the controller. The controller controls various testing and reporting activities of the 
memory test. It allows various mode selections and programs the pre-stored synthesized 
algorithms instructions into collars attached to it.  
 
Main functionalities of controller are:  
• Mode management (RunBIST mode, Retention mode etc.)  
• Program the configurable collar with default algorithms, march element by march element 
and initiate the activities on memory through collars by launching the march run.  
• Compute the Global status based on the individual status from the collar.  
 
TAP  
• It includes a TAP controller, a 7-bit instruction register, three test data registers, and the 
bypass register.  
• This responds to the control sequences supplied through the test access port (TAP) and 
generates the control signals required for BIST operation
```

## Result 5
- chunk_id: 127
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 33
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 14
- rank_semantic: 30
- lexical_score: (not returned)
- normalized_score: -3.260706
- semantic_score: 0.038626
- rrf_score: 0.016291
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

## Result 6
- chunk_id: 281
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 111
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 2
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -10.458358
- semantic_score: (not returned)
- rrf_score: 0.016129
- normalized_terms: pos_senshub_mb_i2c end dds_stbio1_9500 requirement case also other sources source writes write fifo active then sensor hub work always alway multi mode fifo_mode input set 1 first out storage_buffer store stor storage buffer queue

```text
POS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9500] Requirement 
In case also other sources that writes into FIFO are active, then sensor hub shall work always in 
multi-fifo mode  fifo_mode input of sensor hub set to ‘1’ . 
[End]
```

## Result 7
- chunk_id: 292
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 116
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 21
- rank_semantic: 10
- lexical_score: (not returned)
- normalized_score: -2.746616
- semantic_score: 0.092009
- rrf_score: 0.015917
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

## Result 8
- chunk_id: 226
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 84
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 22
- rank_semantic: 14
- lexical_score: (not returned)
- normalized_score: -2.721419
- semantic_score: 0.076929
- rrf_score: 0.015574
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

## Result 9
- chunk_id: 224
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 83
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 25
- rank_semantic: 9
- lexical_score: (not returned)
- normalized_score: -2.680447
- semantic_score: 0.115493
- rrf_score: 0.015388
- normalized_terms: 82 port name direction type output reset value description o_adc_mux_bio_channel 2 0 adc mux bio channel o_adc_mux_sel sel o_error_time_slot error time slot irq o_curr_sel_tx_frame_x curr_sel_bit_top 1 current selection tx o_tx1_outlab_sel_frame_x bit_outab_sel_top outlab frame x o_tx2_outlab_sel_frame_x o_tx3_outlab_sel_frame_x o_tx4_outlab_sel_frame_x o_tx_preset prese analog domain o_en_tx n_tx_channel enable o_pd_tia enabling enabl tia o_pd_pga buffer o_pd_idac idac o_gsr_curr_on gsr curr pilot o_gsr_on grs o_adc_en o_half_charge_ldo o_adc_start start sampling sample o_n_step2_to_reg rx_ch_gain_limit n_step2 calibration o_ad digital converter interrupt request clock_reset clock clk rst rst_n resetn por storage_buffer store stor storage fifo queue acquire acquir acquisition event flag statu power_on_reset power analog_to_digital digital_to_analog

```text
82 
 
Port name Direction Type Output 
Reset Value Description 
o_adc_mux_bio_channel output [2:0] 0 adc mux bio channel 
o_adc_mux_sel output  0 adc mux sel output 
o_error_time_slot output  0 error time slot irq 
o_curr_sel_tx_frame_x output [curr_sel_bit_top-1:0] 0 current selection for tx channel output 
o_tx1_outlab_sel_frame_x output [bit_outab_sel_top-1:0] 0 tx outlab sel frame x 
o_tx2_outlab_sel_frame_x output [bit_outab_sel_top-1:0] 0 tx outlab sel frame x 
o_tx3_outlab_sel_frame_x output [bit_outab_sel_top-1:0] 0 tx outlab sel frame x 
o_tx4_outlab_sel_frame_x output [bit_outab_sel_top-1:0] 0 tx outlab sel frame x 
o_tx_preset output  0 tx prese to analog domain 
o_en_tx output [n_tx_channel-1:0] 0 tx enable to analog domain 
o_PD_TIA output  1 enabling tia to analog domain 
o_PD_PGA output  1 enabling buffer to analog domain 
o_PD_IDAC output  1 enabling idac to analog domain 
o_gsr_curr_on output  0 gsr curr on pilot to analog domain 
o_gsr_on output  0 grs on on pilot to analog domain 
o_ADC_en output  0 ADC enabling 
o_half_charge_ldo output  0  
o_ADC_start output  0 ADC Start sampling 
o_N_step2_to_reg output [rx_ch_gain_limit-1:0] 0 N_Step2 calibration value 
o_ad
```

## Result 10
- chunk_id: 105
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 18
- section: 8. STBIO1: Functional Modes
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 5
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -7.287891
- semantic_score: (not returned)
- rrf_score: 0.015385
- normalized_terms: 8 stbio1 functional modes mode different measurement flow can distinguished distinguish according accord operative set user 1 data storage ds_sel bit device_config_channel register ppg_elab 0 general_parameters_ppg o will cut communication between main controller adsp analog control interface samples sample ecg bia signals signal adc average stores store sampled appropriate fifo gsr raw ppg s configuration configure always alway available after stored stor except when full occurs occur turned turn off but possible ispu before start cycle case read communicate 2 normal if also elaborated elaborat da digital converter first out config storage_buffer buffer queue sampling acquire acquir acquisition analog_to_digital

```text
8. STBIO1: Functional Modes 
Different measurement flow can be distinguished according to the operative mode set by the 
user: 
8.1. Data Storage Mode 
• Set DS_SEL bit in Device_Config_Channel register to 1 and PPG_ELAB to 0 in 
General_Parameters_PPG  
o This will cut the communication between Main Controller and ADSP 
• Analog control Interface samples ECG and BIA signals from ADC, average and stores 
data sampled in appropriate in FIFO.  
• Analog control Interface samples GSR signal from ADC and stores GSR data raw in 
FIFO.  
• Analog control Interface samples PPG signal from ADC, average (according to the user's 
configuration) and stores data in FIFO.  
• Raw data are always available in FIFO after stored. (Except when FIFO FULL occurs)  
 
In this mode, the ADSP is turned off, but it’s possible to turn on the ISPU before the start of a 
measurement Cycle. In this case, the ISPU shall read the data from FIFO and can 
communicate with the ADSP. 
 
8.2. Normal Mode 
• Set DS_SEL bit in Device_Config_Channel register to 0 
o Set PPG_ELAB to 1 if also PPG data shall be elaborated by the ADSP 
• Analog control Interface samples of ECG, BIA or GSR from ADC, average and stores 
da
```

