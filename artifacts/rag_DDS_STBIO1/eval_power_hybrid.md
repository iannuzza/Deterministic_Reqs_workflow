# RAG Query Results
- Timestamp: 2026-09-14 10:10:52
- Query: power domain architecture always on switchable retention
- Mode: hybrid
- Requested mode: hybrid
- Normalized Query: power domain architecture always alway switchable retention
- Normalized FTS Query: power OR domain OR architecture OR always OR alway OR switchable OR retention
- Top K: 10
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: not requested
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
- rank_semantic: (not returned)
- lexical_score: -32.714891
- normalized_score: -20.054447
- semantic_score: (not returned)
- rrf_score: 0.032787
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

## Result 3
- chunk_id: 125
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 31
- section: 10. Power Domains
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 3
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -9.566863
- semantic_score: (not returned)
- rrf_score: 0.015873
- normalized_terms: 10 power domains domain 1 introduction document paragraph describes describe architecture implemented implement stbio1 goal provide detailed detail overview partitioning partition their functionalities functionality

```text
10. Power Domains 
10.1. Introduction 
This document paragraph describes the Power Domain architecture implemented in the STBIO1. 
The goal is to provide a detailed overview of the power domain partitioning, their functionalities,
```

## Result 4
- chunk_id: 4
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 2
- section: (unknown)
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 4
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -8.953225
- semantic_score: (not returned)
- rrf_score: 0.015625
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

## Result 5
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

## Result 6
- chunk_id: 362
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 157
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 6
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -4.848165
- semantic_score: (not returned)
- rrf_score: 0.015152
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

## Result 7
- chunk_id: 230
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 85
- section: 13.1.3.3. Main Controller Peculiar Requirements
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 7
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -4.542754
- semantic_score: (not returned)
- rrf_score: 0.014925
- normalized_terms: 13 1 3 main controller peculiar requirements requirement manage all analog domain so its considered consider high priority check correctly s important cover different phase described describ partially chapter 12 ipos power_on_reset power reset

```text
13.1.3.3. Main Controller Peculiar Requirements 
Main Controller manage all the Analog domain, so all its requirements shall be considered as 
High Priority. To check correctly the requirements, it’s important to cover all the different phase 
described, partially, in chapter 12 and its IPOS.
```

## Result 8
- chunk_id: 3
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 2
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 8
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -4.379336
- semantic_score: (not returned)
- rrf_score: 0.014706
- normalized_terms: 9 5 stbio1 toplevel overview 11 6 symbol 15 7 i o list 8 functional modes mode 17 1 data storage 2 normal digital architecture top pinout storage_buffer store stor buffer fifo queue

```text
........................ ................................ ................................ ................ 9 
5. STBIO1 toplevel overview ................................ ................................ ................................ .. 11 
6. Symbol ................................ ................................ ................................ ...............................  15 
7. I/O List ................................ ................................ ................................ ................................  15 
8. STBIO1: Functional Modes ................................ ................................ ................................  17 
8.1. Data Storage Mode ................................ ................................ ................................ .... 17 
8.2. Normal Mode ................................ ................................ ................................ .............. 17 
9. Digital Architecture Overview................................ ................................ ..............................  17 
9.1. TOP Pinout List ................................ ................................ ................................ ........
```

## Result 9
- chunk_id: 9
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 3
- section: (unknown)
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 9
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -4.379336
- semantic_score: (not returned)
- rrf_score: 0.014493
- normalized_terms: 2 ecg bia 149 15 3 ppg only 151 16 scan 155 1 top level approach 17 bist 156 reference documents document memory architecture mbist collar controller built self test test_debug debug dft

```text
.2. ECG and BIA ........................................................................................... 149 
15.3.3. PPG Only ................................................................................................. 151 
16. SCAN ................................ ................................ ................................ ........................... 155 
16.1. Top Level Approach................................ ................................ ................................ .. 155 
17. BIST ................................ ................................ ................................ ............................. 156 
17.1. Reference documents ................................ ................................ ...............................  156 
17.2. Memory BIST Architecture ................................ ................................ ........................ 156 
17.2.1. MBIST Collar ........................................................................................... 156 
17.2.2. MBIST Controller ..................................................................................... 156 
17.2.3. Top Level Approach ..................................
```

## Result 10
- chunk_id: 361
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 157
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 10
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -4.000152
- semantic_score: (not returned)
- rrf_score: 0.014286
- normalized_terms: 156 17 bist 1 reference documents document current version author change description 0 00 prj ams_deliveries ams_delivery h9a_stbio1 memorycuts memorycut genericmbist_config bist_stbio1 doc ref_manual generic_mbist_um pdf stmicroelectronics stmicroelectronic trnd user manual release notes note kps genericmbist user_manual generic_mbist_rm 2 memory architecture solution consists consist wrapper collar common master controller ieee 1149 compliant test access port tap mbist which placed plac closest executes execute instructions instruction received receiv form march elements element runs speed spe under after testing reports report execution status statu manages manage all diagnosis diagnosi repair information debug data also provides provide support multiple memories parallel built self interrupt irq event flag test_debug scan dft power_on_reset power reset

```text
156 
 
17. BIST 
17.1. Reference documents 
Current 
Version 
Document Author Change 
Description 
1.0-
17.00 
/prj/ams_DELIVERIES/H9A_STBIO1/memorycuts/H9A_STBIO1-
-GenericMBIST_CONFIG--BIST_STBIO1/1.0-17.00/ 
/doc/ref_manual/generic_mbist_um.pdf 
STMicroelectronics 
TRnD 
 
User manual, 
release notes 
and KPS for 
the 
GenericMBIST 
 
1.0-
17.00 
/prj/ams_DELIVERIES/H9A_STBIO1/memorycuts/H9A_STBIO1-
-GenericMBIST_CONFIG--BIST_STBIO1/1.0-17.00/ 
/doc/user_manual/generic_mbist_rm.pdf 
STMicroelectronics 
TRnD 
 
Reference 
manual for the 
GenericMBIST 
 
 
17.2. Memory BIST Architecture  
The BIST solution consists of memory-wrapper “collar” and common master “controller” and an 
IEEE 1149.1 compliant Test Access Port (TAP).  
17.2.1. MBIST Collar  
The BIST collar is a wrapper which is placed closest to memory. It executes the instructions 
received from controller in the form of march elements to test the memory. It runs at the speed of 
the memory under test.  
After testing it reports the execution status to the controller and manages all the BIST status, 
diagnosis, repair information and debug data. The collar also provides support for testing multiple 
memories in parallel
```

