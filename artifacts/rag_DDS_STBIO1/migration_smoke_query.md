# RAG Query Results
- Timestamp: 2026-09-10 15:24:47
- Query: shall
- Mode: hybrid
- Requested mode: hybrid
- Normalized Query: (empty)
- Normalized FTS Query: (empty)
- Top K: 8
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: not requested
- Automatic semantic fallback: not used
- Requirement-ID mapping check: not_applicable
## Result 1
- chunk_id: 178
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 59
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 1
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.341349
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.016393
- normalized_terms: 58 dds_stbio1_301 assumption will enabled enabl two consecutive writes write pag 3 address 0x40 set page 0x00 0x3e end dds_stbio1_302 requirement if mode_config register operative mode functional vpriority high dds_stbio1_303 0x01 scan dds_stbio1_304 0x04 bist dds_stbio1_305 0x08 debug dds_stbio1_306 0x10 ispu_debug dds_stbio1_307 0x20 memsafe dds_stbio1_308 bypass dds_stbio1_314 function gpio1 2 4_out general purpose sel irq gpi1 4 ext_cap_en 0 dds_stbio interrupt request built self test event flag statu test_debug dft

```text
58 
 
 
 
[DDS_STBIO1_301] Assumption 
It will be enabled by two consecutive writes, pag. 3 to address 0x40 to set the page and 0x00 to 
address 0x3E 
[End] 
 
[DDS_STBIO1_302] Requirement 
If MODE_CONFIG register is 0x00 the operative mode shall be functional. 
[Vpriority High] [End] 
 
[DDS_STBIO1_303] Requirement 
If MODE_CONFIG register is 0x01 the operative mode shall be SCAN.  
 [End] 
 
[DDS_STBIO1_304] Requirement 
If MODE_CONFIG register is 0x04 the operative mode shall be BIST.  
 [End] 
 
[DDS_STBIO1_305] Requirement 
If MODE_CONFIG register is 0x08 the operative mode shall be DEBUG.  
 [End] 
 
[DDS_STBIO1_306] Requirement 
If MODE_CONFIG register is 0x10 the operative mode shall be ISPU_DEBUG.  
[Vpriority High] [End] 
 
[DDS_STBIO1_307] Requirement 
If MODE_CONFIG register is 0x20 the operative mode shall be Bist MEMSAFE mode.  
 [Vpriority High] [End] 
 
[DDS_STBIO1_308] Requirement 
If MODE_CONFIG register is 0x40 the operative mode shall be Bist Bypass mode.  
[Vpriority High] [End] 
 
[DDS_STBIO1_314] Requirement 
In function mode, the GPIO1,2,3,4_out shall be General-Purpose if sel irq gpi1,2,3,4 is 0x00 and 
ext_cap_en is “0” 
[Vpriority High][End] 
 
[DDS_STBIO
```

## Result 2
- chunk_id: 241
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 90
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 2
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.326524
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.016129
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

## Result 3
- chunk_id: 278
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 110
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 3
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.319371
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.015873
- normalized_terms: 109 input sys_clk sensor hub connected connect 8mhz clock generate i2c communications communication compliant fm standard ipos_senshub_mb_i2c end dds_stbio1_9018 requirement trigger possible both ways hw via dvalid_masterblaze_ext signal sw using dvalid_register dds_stbio1_9024 only target addressed addres through slave0_dev_add register destination write operation dds_stbio1_9027 bit 0 slave1_dev_add slave2_dev_add slave3_dev_add registers ignored ignor read operations towards toward 1 2 3 performed perform dds_stbio1_9029 aux_sens_on values value all tested test since masterblaze supports support up 4 targets network dds_stbio1_9030 slavex_numop fields field slavex_config define how many bytes byte per slave effect x 12 ipos_senshub_mb_i clock_reset clk reset rst rst_n resetn por connection connectivity link power_on_reset power

```text
109 
 
Input sys_clk of sensor hub shall be connected to 8MHz clock to generate I2C communications 
compliant with FM+ I2C standard. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9018] Requirement 
The trigger of sensor hub shall be possible in both ways, HW via dvalid_masterblaze_ext signal 
or SW using DVALID_REGISTER. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9024] Requirement 
Only I2C target addressed through SLAVE0_DEV_ADD register shall be the destination of an 
I2C Write Operation. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9027] Requirement 
The bit 0 of SLAVE1_DEV_ADD, SLAVE2_DEV_ADD, SLAVE3_DEV_ADD registers shall be 
ignored: ONLY read operations towards I2C target  1, 2 and 3 shall be performed. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9029] Requirement 
AUX_SENS_ON possible values shall be 0,1,2,3. All the values shall be tested since 
MasterBlaze supports up-to 4 I2C targets connected to I2C network. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9030] Requirement 
SLAVEx_NUMOP bit-fields of SLAVEx_CONFIG registers shall define how many bytes per slave 
are read as per effect of an I2C operation (x from 1 to 12). 
[TO: IPOS_Senshub_MB_i
```

## Result 4
- chunk_id: 285
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 113
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 4
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.288099
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.015625
- normalized_terms: 112 13 2 4 1 fifo_ctrl peculiar requirements requirement dds_stbio1_00000102 parameter mem_loc define first memory location fifo ram 0xc4000 ipos_fifo_ctrl_00000102 end dds_stbio1_00000202 register map defined defin 0x1000 0xc5000 ipos_fifo_ctrl_00000202 dds_stbio1_89456557 controller able address 5 kbyte divided divid 32 bit ipos_fifo_ctrl_89456557 dds_stbio1_89459082 work 16 mhz clock frequency ipos_fifo_ctrl_89459082 dds_stbio1_89455261 have ahb slave interface connected connect bus master physical ipos_fifo_ctrl_89455261 dds_stbio1_89455449 two working modes mode multiple unique these mutually exclusive ipos_fifo_ctrl_89455449 dds_stbio1_89455232 default t out clock_reset clk reset rst rst_n resetn por connection connectivity link storage_buffer store stor storage buffer queue

```text
112 
 
13.2.4.1. FIFO_CTRL Peculiar Requirements 
[DDS_STBIO1_00000102] Requirement 
The parameter MEM_LOC shall define the first Memory Location of the FIFO RAM: 
0xC4000. 
[TO: IPOS_FIFO_CTRL_00000102]   
[End] 
[DDS_STBIO1_00000202] Requirement 
The FIFO register map first memory location shall be defined as MEM_LOC + 0x1000: 
0xC5000. 
[TO: IPOS_FIFO_CTRL_00000202]   
[End] 
[DDS_STBIO1_89456557] Requirement:  
The FIFO Controller shall be able to address 1.5 kbyte divided into 32-bit address.  
[TO: IPOS_FIFO_CTRL_89456557]   
[End] 
[DDS_STBIO1_89459082] Requirement:  
The FIFO Controller shall work at 16 MHz clock frequency.  
[TO: IPOS_FIFO_CTRL_89459082]   
[End]  
[DDS_STBIO1_89455261] Requirement:  
The FIFO Controller shall have an AHB Slave Interface connected to the AHB BUS and 
a Memory Master Interface connected to the Physical Memory.   
[TO: IPOS_FIFO_CTRL_89455261]  
[End] 
[DDS_STBIO1_89455449] Requirement:  
The FIFO Controller shall have two working modes: Multiple FIFO and Unique FIFO. 
These two modes are mutually exclusive.   
[TO: IPOS_FIFO_CTRL_89455449] 
[End] 
[DDS_STBIO1_89455232] Requirement:  
As default, the FIFO shall work in Unique FIFO Mode.  
[T
```

## Result 5
- chunk_id: 280
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 111
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 5
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.233918
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.015385
- normalized_terms: 110 when quokka masterblaze p runs sleep_master signal 0 any dvalid triggered trigger hw sw ignored ignor ipos_senshub_mb_i2c end dds_stbio1_9034 requirement nack_register register reset every time new i2c operation starts start dds_stbio1_9260 each data stored stor fifo composed compos 4 words word 16bytes dds_stbio1_9261 3 12bytes contain slave dds_stbio1_9262 24 bits reserved reserv dds_stbio1_9263 last 8 tag field dds_stbio1_9300 ahb write registers has no effect if ip processor busy going value not updated updat dds_stbio1_9500 case also other sources source writes active then sensor hub work first out clock_reset clock clk rst rst_n resetn por storage_buffer store storage buffer queue

```text
110 
 
When Quokka MasterBlaze µP runs (sleep_master signal = 0), any dvalid triggered (HW or SW) 
shall be ignored. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9034] Requirement 
The NACK_REGISTER register is reset every time a new I2C operation starts. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9260] Requirement 
Each data stored in FIFO shall be composed by 4 words (16bytes). 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9261] Requirement 
3 words (12bytes) of the data stored in FIFO shall contain the data from each I2C slave. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9262] Requirement 
24-bits of the data stored in FIFO shall be reserved at ‘0’. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9263] Requirement 
The last 8-bits of the data stored in FIFO shall contain the TAG field. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9300] Requirement 
The AHB Write to registers has no effect if the IP masterblaze processor is busy (I2C operation 
on-going); the registers value shall not be updated. 
[TO: IPOS_Senshub_MB_i2c]  
[End] 
 
[DDS_STBIO1_9500] Requirement 
In case also other sources that writes into FIFO are active, then sensor hub shall work
```

## Result 6
- chunk_id: 151
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 43
- section: (unknown)
- source_type: figure
- chunk_index: 2
- rank_lexical: 6
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.181494
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.015152
- normalized_terms: 42 figure 8 mask cell ldo fast ring oscillator w_en_ldo_sync32 w_pdclockf_sync32 relative 32khz synchronized synchroniz versions version ipos_pmu end dds_stbio1_0103 definition clk_64k_divided i_clk_64k 64khz divided divid two dds_stbio1_0104 requirement when device turned turn i_por1v2_1v2 high dds_stbio1_0105 low o en_ldo1v8 dds_stbio1_0106 o_pd_clkf dds_stbio1_0107 o_clk_16m_ready dds_stbio1_0108 o_dis_rc_viref dds_stbio1_0109 rises rise after least 10 cycles cycle considered consider stable dds_stbio1_0110 352 dropout regulator power_on_reset power reset

```text
42 
 
 
Figure 8: Mask Cell for LDO and Fast Ring Oscillator 
 
w_EN_LDO_sync32 and w_PDClockF_sync32 are the relative 32kHz synchronized versions. [TO: 
IPOS_PMU] [END] 
 
[DDS_STBIO1_0103] Definition: 
clk_64k_divided (32kHz) is i_clk_64k (64kHz) divided by two. [TO: IPOS_PMU] [END] 
 
 
[DDS_STBIO1_0104] Requirement:  
When the device is turned on, i_POR1V2_1V2 shall be high. [TO: IPOS_PMU] [END] 
 
 
[DDS_STBIO1_0105] Requirement: 
When i_POR1V2_1V2 is low, o_ EN_LDO1V8 shall be low. [TO: IPOS_PMU] [END] 
 
 
[DDS_STBIO1_0106] Requirement: 
When i_POR1V2_1V2 is low, o_PD_CLKF shall be high. [TO: IPOS_PMU] [END] 
 
[DDS_STBIO1_0107] Requirement: 
When i_POR1V2_1V2 is low, o_CLK_16M_READY shall be low. [TO: IPOS_PMU] [END] 
 
[DDS_STBIO1_0108] Requirement: 
When i_POR1V2_1V2 is low, o_DIS_RC_VIREF shall be high. [TO: IPOS_PMU] [END] 
 
[DDS_STBIO1_0109] Requirement: 
When i_POR1V2_1V2 rises, after at least 10 cycles of i_clk_64k (64kHz), o_ EN_LDO1V8 shall 
be high and the clk_64k_divided is considered stable. [TO: IPOS_PMU] [END] 
 
[DDS_STBIO1_0110] Requirement:  
When clk_64k_divided is stable, after at least 352 cycles of clk_64k_divided (32kHz), 
o_DIS_RC_VIREF shall be low. [TO: IPOS_PMU] [END]
```

## Result 7
- chunk_id: 351
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 150
- section: 15.3.2. ECG and BIA
- source_type: text
- chunk_index: 4
- rank_lexical: 7
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.120814
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.014925
- normalized_terms: ipos_main_ctrl end 4 configure adc sampling sample period dds_stbio1_0129 requirement user set number clocks clock ecg bia data adc_config_ecg register 5 general config dds_stbio1_0130 1 hc_en ecg_ctrl dds_stbio1_0140 imp_en imp_ctrl 6 select operative mode dds_stbio1_0141 start measurement writing writ device_config_operation 0 7 check dds_stbio1_0142 unique fifo default first msb which will have equal one described describ tag table analog digital converter out configuration storage_buffer store stor storage buffer queue acquire acquir acquisition analog_to_digital

```text
: IPOS_MAIN_CTRL] [END] 
4. CONFIGURE ADC SAMPLING PERIOD: 
[DDS_STBIO1_0129] Requirement: 
• The user shall set number of clocks for sampling ECG and BIA data from ADC in 
ADC_CONFIG_ECG register. [TO: IPOS_MAIN_CTRL] [END] 
5. GENERAL CONFIG: 
[DDS_STBIO1_0130] Requirement: 
• The user shall set at 1 HC_EN in ECG_CTRL register. [TO: IPOS_MAIN_CTRL] 
[END] 
      [DDS_STBIO1_0140] Requirement: 
• The user shall set at 1 IMP_EN in IMP_CTRL register. [TO: IPOS_MAIN_CTRL] 
[END] 
6. SELECT OPERATIVE MODE: 
[DDS_STBIO1_0141] Requirement: 
• The user shall start measurement writing register DEVICE_CONFIG_OPERATION [0] at 
1. [TO: IPOS_MAIN_CTRL] [END] 
7. CHECK DATA: 
[DDS_STBIO1_0142] Requirement: 
• To check data in unique FIFO (default config) the user shall check the first MSB which will 
have to be equal to the one described in the DATA TAG Table. [TO: IPOS_MAIN_CTRL] 
[END]
```

## Result 8
- chunk_id: 354
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 152
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: 8
- rank_normalized: (not returned)
- rank_semantic: (not returned)
- lexical_score: -3.113737
- normalized_score: (not returned)
- semantic_score: (not returned)
- rrf_score: 0.014706
- normalized_terms: 151 15 3 ppg only configuration configure generates generate each time slot number data according accord user 1 length dds_stbio1_0143 requirement duration device_config_operation register 4 2 select channel dds_stbio1_0144 active case ppg_sel ds_sel storage device_config_channel set 0x30 division index configured channels dds_stbio1_0145 writing writ m_ppg_l m_ppg_h set_ppg_freq_l set_ppg_freq_h adc sampling sample period dds_stbio1_0146 clocks clock adc_config_ppg 5 frames frame config dds_stbio1_0147 following follow these steps step alc parameters parameter t1 ppg_alc_config_param_1 t2 gain_start_set gain_max_set ppg_alc_config_param_2 digital ramp n_max t_delta digital_ramp_config_para analog converter storage_buffer store stor buffer fifo queue acquire acquir acquisition analog_to_digital

```text
151 
 
 
15.3.3. PPG Only 
 
This configuration generates each time slot, a number of PPG DATA according to user 
configuration.  
 
1. TIME SLOT LENGTH: 
[DDS_STBIO1_0143] Requirement: 
• The User shall configure time slot duration in DEVICE_CONFIG_OPERATION 
register [4:2]. 
2. SELECT CHANNEL: 
[DDS_STBIO1_0144] Requirement: 
• The user shall select active channel, in this case only PPG_SEL and DS_SEL 
(data Storage) in DEVICE_CONFIG_CHANNEL register shall be set to 0x30. 
3. SELECT DIVISION INDEX FOR CONFIGURED CHANNELS: 
[DDS_STBIO1_0145] Requirement: 
• The user shall configure a division index PPG, writing M_PPG_l and M_PPG_h in 
SET_PPG_FREQ_l register and SET_PPG_FREQ_h register. 
4. CONFIGURE ADC SAMPLING PERIOD: 
[DDS_STBIO1_0146] Requirement: 
• The user shall configure the number of clocks for sampling PPG data from ADC in 
ADC_CONFIG_PPG register. 
5. PPG FRAMES CONFIG:  
[DDS_STBIO1_0147] Requirement: 
The user shall configure each frame following these steps: 
5.1 ALC PARAMETERS: 
• T1 in PPG_ALC_CONFIG_PARAM_1 register. 
• T2, GAIN_START_SET, GAIN_MAX_SET in PPG_ALC_CONFIG_PARAM_2 
register. 
5.2 DIGITAL RAMP PARAMETERS: 
• N_MAX, T_DELTA in DIGITAL_RAMP_CONFIG_PARA
```

