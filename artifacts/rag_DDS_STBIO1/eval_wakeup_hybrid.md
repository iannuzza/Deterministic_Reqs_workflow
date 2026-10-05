# RAG Query Results
- Timestamp: 2026-09-14 10:10:58
- Query: wake up restore retention isolation power sequence
- Mode: hybrid
- Requested mode: hybrid
- Normalized Query: wake up restore retention isolation power sequence power_startup startup start boot initialization
- Normalized FTS Query: wake OR up OR restore OR retention OR isolation OR power OR sequence OR power_startup OR startup OR start OR boot OR initialization
- Top K: 10
- DB: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/artifacts/rag_DDS_STBIO1/rag_index.sqlite
- Semantic status: not requested
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

## Result 3
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

## Result 4
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

## Result 5
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

## Result 6
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

## Result 7
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

## Result 8
- chunk_id: 8
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 3
- section: (unknown)
- source_type: text
- chunk_index: 2
- rank_lexical: (not returned)
- rank_normalized: 8
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -20.467030
- semantic_score: (not returned)
- rrf_score: 0.014706
- normalized_terms: 132 13 4 2 stbio1 register map peculiar requirements requirement 134 14 soft reset procedures procedure 143 1 main controller 15 measurement cycle examples example boot phase 144 configuration configure 145 3 146 ecg only 147 bia 149 ppg clock_reset clock clk rst rst_n resetn por config power_startup power up startup start initialization wake power_up

```text
......................................... 132 
13.4.2. STBIO1 Register Map Peculiar Requirements ......................................... 134 
14. Soft Reset Procedures ................................ ................................ ................................ . 143 
14.1. Main Controller Soft Reset ................................ ................................ ........................ 143 
15. Measurement Cycle Examples ................................ ................................ ..................... 143 
15.1. BOOT Phase ................................ ................................ ................................ ............ 144 
15.2. Configuration Phase ................................ ................................ ................................ . 145 
15.3. Measurement Cycle ................................ ................................ ................................ .. 146 
15.3.1. ECG Only  ................................................................................................ 147 
15.3.2. ECG and BIA ........................................................................................... 149 
15.3.3. PPG Only ....................
```

## Result 9
- chunk_id: 309
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 131
- section: (unknown)
- source_type: text
- chunk_index: 1
- rank_lexical: (not returned)
- rank_normalized: 9
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -19.728934
- semantic_score: (not returned)
- rrf_score: 0.014493
- normalized_terms: 130 dds_stbio1_0507 requirement after initial boot phase turn ispu select page 3 regmap address 0x04 data 0x03 enable ldo 1v8 writing writ viref_ldo1v8_clk16m register 0x0f 0x02 clock 0x12 user mode 0x5e 0x01 power island configuration configure via ahb interface 0xca000 end low dropout regulator clock_reset clk reset rst rst_n resetn por config power_startup up startup start initialization wake power_up

```text
130 
 
 
[DDS_STBIO1_0507] Requirement: 
After the initial boot phase, to turn on the ISPU shall be: 
• Select page 3 of the regmap (ADDRESS=0x04, DATA=0x03) 
• Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register 
(ADDRESS=0x0F, DATA=0x02) 
• Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register 
(ADDRESS=0x0F, DATA=0x12) 
• Enable user mode by writing to regmap (ADDRESS=0x5E, DATA=0x01) 
• Enable the power island by writing to regmap POWER CONFIGURATION 
REGISTER via AHB interface (ADDRESS=0xCA000, DATA=0x01) 
[End]
```

## Result 10
- chunk_id: 368
- source_file: C:/Users/iannuzza/LOCAL_PROJ/Github_copilot_proj/STBIO_AI/specs/DDS_STBIO1.pdf
- page: 159
- section: 18.2. Debug mode
- source_type: text
- chunk_index: 3
- rank_lexical: (not returned)
- rank_normalized: 10
- rank_semantic: (not returned)
- lexical_score: (not returned)
- normalized_score: -19.466199
- semantic_score: (not returned)
- rrf_score: 0.014286
- normalized_terms: 18 2 debug mode dds_stbio1_0700 requirement after initial boot phase turn select page 3 regmap address 0x40 data 0x03 enable ldo 1v8 writing writ viref_ldo1v8_clk16m register 0x0f 0x02 clock 0x12 0x3e 0x08 end low dropout regulator clock_reset clk reset rst rst_n resetn por power_startup power up startup start initialization wake test_debug test scan bist dft self power_up

```text
18.2. Debug mode 
[DDS_STBIO1_0700] Requirement: 
After the initial boot phase, to turn on the Debug mode shall be: 
• Select page 3 of the regmap (ADDRESS=0x40, DATA=0x03) 
• Enable LDO 1V8 by writing to regmap VIREF_LDO1V8_CLK16M register 
(ADDRESS=0x0F, DATA=0x02) 
• Enable clock by writing to regmap VIREF_LDO1V8_CLK16M register 
(ADDRESS=0x0F, DATA=0x12) 
• Enable debug mode by writing to regmap (ADDRESS=0x3E, DATA=0x08) 
[End]
```

